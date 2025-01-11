from abc import ABC
from typing import Literal

import numpy as np

from .signals import BroadSignal, NarrowSignal, Signal

C = 3e8  # wave speed


class Array(ABC):
    def __init__(
        self,
        element_position_x,
        element_position_y,
        element_position_z,
        rng=None,
    ):
        """element position should be defined in 3D (x, y, z) coordinate
        system"""
        self._element_position = np.vstack(
            (element_position_x, element_position_y, element_position_z)
        ).T

        if rng is None:
            self._rng = np.random.default_rng()
        else:
            self._rng = rng

    @property
    def num_antennas(self):
        return self._element_position.shape[0]

    @property
    def array_position(self):
        return self._element_position

    def set_rng(self, rng):
        """Setting random number generator

        Args:
            rng (np.random.Generator): random generator used to generator random
        """
        self._rng = rng

    def _unify_unit(self, variable, unit):
        if unit == "deg":
            variable = variable / 180 * np.pi

        return variable

    def steering_vector(self, fre, angle_incidence, unit="deg"):
        """Calculate steering vector corresponding to the angle of incidence

        Args:
            fre (float): Frequency of carrier wave
            angle_incidence (float | np.ndarray): Incidence angle. If only
                azimuth is considered, `angle_incidence` is a 1xN dimensional
                matrix; if two dimensions are considered, `angle_incidence` is
                a 2xN dimensional matrix, where the first row is the azimuth and
                the second row is the elevation angle.
            unit: The unit of the angle, `rad` represents radian,
                `deg` represents degree. Defaults to 'deg'.

        Returns:
            If `angle_incidence` corresponds to single signal, return a steering
            vector of dimension `Mx1`. If `angle_incidence` is doa of k signals,
            return a steering maxtrix of dimension `Mxk`
        """
        if np.squeeze(angle_incidence).ndim == 1 or angle_incidence.size == 1:
            angle_incidence = np.vstack(
                (angle_incidence.reshape(1, -1), np.zeros(angle_incidence.size))
            )

        angle_incidence = self._unify_unit(
            np.reshape(angle_incidence, (2, -1)), unit
        )

        cos_cos = np.cos(angle_incidence[0]) * np.cos(angle_incidence[1])
        sin_cos = np.sin(angle_incidence[0]) * np.cos(angle_incidence[1])
        sin_ = np.sin(angle_incidence[1])

        time_delay = (
            1 / C * self.array_position @ np.vstack((cos_cos, sin_cos, sin_))
        )
        steering_vector = np.exp(-1j * 2 * np.pi * fre * time_delay)

        return steering_vector

    def received_signal(
        self,
        signal: Signal,
        angle_incidence,
        snr=None,
        nsamples=100,
        amp=None,
        unit="deg",
        use_cache=False,
        calc_method: Literal["delay", "fft"] = "delay",
        **kwargs,
    ):
        """Generate array received signal based on array signal model

        If `broadband` is set to True, generate array received signal based on
        broadband signal's model.

        Args:
            signal: An instance of the `Signal` class
            angle_incidence: Incidence angle. If only azimuth is considered,
                `angle_incidence` is a 1xN dimensional matrix; if two dimensions
                are considered, `angle_incidence` is a 2xN dimensional matrix,
                where the first row is the azimuth and the second row is the
                elevation angle.
            snr: Signal-to-noise ratio. If set to None, no noise will be added
            nsamples (int): Number of snapshots, defaults to 100
            amp: The amplitude of each signal, 1d numpy array
            unit: The unit of the angle, `rad` represents radian,
                `deg` represents degree. Defaults to 'deg'.
            use_cache (bool): If True, use cache to generate identical signals
                (noise is random). Default to `False`.
            calc_method (str): Only used when generate broadband signal.
                Generate broadband signal in frequency domain, or time domain
                using delay. Defaults to `delay`.
        """
        # Convert the angle from degree to radians
        angle_incidence = self._unify_unit(angle_incidence, unit)

        if isinstance(signal, BroadSignal):
            received = self._gen_broadband(
                signal=signal,
                snr=snr,
                nsamples=nsamples,
                angle_incidence=angle_incidence,
                amp=amp,
                use_cache=use_cache,
                calc_method=calc_method,
                **kwargs,
            )
        if isinstance(signal, NarrowSignal):
            received = self._gen_narrowband(
                signal=signal,
                snr=snr,
                nsamples=nsamples,
                angle_incidence=angle_incidence,
                amp=amp,
                use_cache=use_cache,
            )

        return received

    def _gen_narrowband(
        self,
        signal: NarrowSignal,
        snr,
        nsamples,
        angle_incidence,
        amp,
        use_cache=False,
    ):
        """Generate narrowband received signal

        `azimuth` and `elevation` are already in radians
        """
        if angle_incidence.ndim == 1:
            num_signal = angle_incidence.size
        else:
            num_signal = angle_incidence.shape[1]

        manifold_matrix = self.steering_vector(
            signal.frequency, angle_incidence, unit="rad"
        )

        incidence_signal = signal.gen(
            n=num_signal, nsamples=nsamples, amp=amp, use_cache=use_cache
        )

        received = manifold_matrix @ incidence_signal

        if snr is not None:
            received = self._add_awgn(received, snr)

        return received

    def _gen_broadband(
        self,
        signal: BroadSignal,
        snr,
        nsamples,
        angle_incidence,
        amp,
        use_cache=False,
        calc_method: Literal["delay", "fft"] = "delay",
        **kwargs,
    ):
        assert calc_method in ["fft", "delay"], "Invalid calculation method"

        if calc_method == "fft":
            return self._gen_broadband_fft(
                signal=signal,
                snr=snr,
                nsamples=nsamples,
                angle_incidence=angle_incidence,
                amp=amp,
                use_cache=use_cache,
                **kwargs,
            )
        else:
            return self._gen_broadband_delay(
                signal=signal,
                snr=snr,
                nsamples=nsamples,
                angle_incidence=angle_incidence,
                amp=amp,
                use_cache=use_cache,
                **kwargs,
            )

    def _gen_broadband_fft(
        self,
        signal: BroadSignal,
        snr,
        nsamples,
        angle_incidence,
        amp,
        use_cache=False,
        **kwargs,
    ):
        """Generate broadband received signal using FFT model

        `azimuth` and `elevation` are already in radians
        """
        if angle_incidence.ndim == 1:
            num_signal = angle_incidence.size
        else:
            num_signal = angle_incidence.shape[1]

        num_antennas = self._element_position.shape[0]

        incidence_signal = signal.gen(
            n=num_signal,
            nsamples=nsamples,
            amp=amp,
            use_cache=use_cache,
            delay=None,
            **kwargs,
        )

        # generate array signal in frequency domain
        signal_fre_domain = np.fft.fft(incidence_signal, axis=1)

        received_fre_domain = np.zeros(
            (num_antennas, nsamples), dtype=np.complex128
        )
        fre_points = np.fft.fftfreq(nsamples, 1 / signal.fs)
        for i, fre in enumerate(fre_points):
            manifold_fre = self.steering_vector(
                fre, angle_incidence, unit="rad"
            )

            # calculate array received signal at every frequency point
            received_fre_domain[:, i] = manifold_fre @ signal_fre_domain[:, i]

        received = np.fft.ifft(received_fre_domain, axis=1)

        if snr is not None:
            received = self._add_awgn(received, snr)

        return received

    def _gen_broadband_delay(
        self,
        signal: BroadSignal,
        snr,
        nsamples,
        angle_incidence,
        amp,
        use_cache=False,
        **kwargs,
    ):
        """Generate broadband received signal by applying delay

        `azimuth` and `elevation` are already in radians
        """
        if angle_incidence.ndim == 1:
            num_signal = angle_incidence.size
        else:
            num_signal = angle_incidence.shape[1]

        if np.squeeze(angle_incidence).ndim == 1 or angle_incidence.size == 1:
            angle_incidence = np.vstack(
                (angle_incidence.reshape(1, -1), np.zeros(angle_incidence.size))
            )

        angle_incidence = np.reshape(angle_incidence, (2, -1))

        # calculate time delay
        cos_cos = np.cos(angle_incidence[0]) * np.cos(angle_incidence[1])
        sin_cos = np.sin(angle_incidence[0]) * np.cos(angle_incidence[1])
        sin_ = np.sin(angle_incidence[1])
        time_delay = -(
            1 / C * self.array_position @ np.vstack((cos_cos, sin_cos, sin_))
        )

        received = np.zeros((self.num_antennas, nsamples), dtype=np.complex128)

        # clear cache if not use cache
        if not use_cache:
            signal.clear_cache()

        # must use cache as the same signal is received by different antennas
        for i in range(self.num_antennas):
            received[i, :] = np.sum(
                signal.gen(
                    n=num_signal,
                    nsamples=nsamples,
                    amp=amp,
                    use_cache=True,
                    delay=time_delay[i, :],
                    **kwargs,
                ),
                axis=0,
            )

        if snr is not None:
            received = self._add_awgn(received, snr)

        return received

    def _add_awgn(self, signal, snr_db):
        sig_pow = np.mean(np.abs(signal) ** 2, axis=1)
        noise_pow = sig_pow / 10 ** (snr_db / 10)
        noise = (np.sqrt(noise_pow / 2)).reshape(-1, 1) * (
            self._rng.standard_normal(size=signal.shape)
            + 1j * self._rng.standard_normal(size=signal.shape)
        )
        return signal + noise


class UniformLinearArray(Array):
    def __init__(self, m: int, dd: float, rng=None):
        """Uniform linear array.

        The array is uniformly arranged along the y-axis.

        Args:
            m (int): number of antenna elements
            dd (float): distance between adjacent antennas
            rng (np.random.Generator): random generator used to generator random
        """
        # antenna position in (x, y, z) coordinate system
        element_position_x = np.zeros(m)
        element_position_y = np.arange(m) * dd
        element_position_z = np.zeros(m)

        super().__init__(
            element_position_x, element_position_y, element_position_z, rng
        )


class UniformCircularArray(Array):
    def __init__(self, m, r, rng=None):
        """Uniform circular array.

        The origin is taken as the center of the circle, and the
        counterclockwise direction is considered as the positive direction.

        Args:
            m (int): Number of antennas.
            r (float): Radius of the circular array.
            rng (optional): Random number generator. Defaults to None.
        """
        self._radius = r

        element_position_x = r * np.cos(2 * np.pi * np.arange(m) / m)
        element_position_y = r * np.sin(2 * np.pi * np.arange(m) / m)
        element_position_z = np.zeros(m)

        super().__init__(
            element_position_x, element_position_y, element_position_z, rng
        )

    @property
    def radius(self):
        return self._radius
