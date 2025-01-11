import numpy as np

from .music_based import music
from .utils import (
    divide_into_fre_bins,
    get_noise_space,
    get_signal_space,
)

C = 3e8


def imusic(
    received_data,
    num_signal,
    array,
    fs,
    angle_grids,
    num_groups,
    f_min=None,
    f_max=None,
    n_fft_min=128,
    unit="deg",
):
    """Incoherent MUSIC estimator for wideband DOA estimation.

    Args:
        received_data : Array received signals
        num_signal : Number of signals
        array : Instance of array class
        fs: sampling frequency
        angle_grids : Angle grids corresponding to spatial spectrum. It should
            be a numpy array.
        num_groups: Divide sampling points into serveral groups, and do FFT
            separately in each group
        f_min : Minimum frequency of interest. Defaults to None.
        f_max : Maximum frequency of interest. Defaults to None.
        n_fft_min: minimum number of FFT points
        unit : Unit of angle, 'rad' for radians, 'deg' for degrees. Defaults to
            'deg'.

    References:
        Wax, M., Tie-Jun Shan, and T. Kailath. “Spatio-Temporal Spectral
        Analysis by Eigenstructure Methods.” IEEE Transactions on Acoustics,
        Speech, and Signal Processing 32, no. 4 (August 1984): 817-27.
        https://doi.org/10.1109/TASSP.1984.1164400.
    """
    signal_fre_bins, fre_bins = divide_into_fre_bins(
        received_data, num_groups, fs, f_min, f_max, n_fft_min
    )

    # MUSIC algorithm in every frequency point
    spectrum_fre_bins = np.zeros((signal_fre_bins.shape[1], angle_grids.size))
    for i, fre in enumerate(fre_bins):
        spectrum_fre_bins[i, :] = music(
            received_data=signal_fre_bins[:, i, :],
            num_signal=num_signal,
            array=array,
            signal_fre=fre,
            angle_grids=angle_grids,
            unit=unit,
        )

    spectrum = np.mean(spectrum_fre_bins, axis=0)

    return np.squeeze(spectrum)


def norm_music(
    received_data,
    num_signal,
    array,
    fs,
    angle_grids,
    num_groups,
    f_min=None,
    f_max=None,
    n_fft_min=128,
    unit="deg",
):
    """Normalized incoherent MUSIC estimator for wideband DOA estimation.

    Args:
        received_data : Array received signals
        num_signal : Number of signals
        array : Instance of array class
        fs: sampling frequency
        angle_grids : Angle grids corresponding to spatial spectrum. It should
            be a numpy array.
        num_groups: Divide sampling points into serveral groups, and do FFT
            separately in each group
        f_min : Minimum frequency of interest. Defaults to None.
        f_max : Maximum frequency of interest. Defaults to None.
        n_fft_min: minimum number of FFT points
        unit : Unit of angle, 'rad' for radians, 'deg' for degrees. Defaults to
            'deg'.

    References:
        Salvati, Daniele, Carlo Drioli, and Gian Luca Foresti. “Incoherent
        Frequency Fusion for Broadband Steered Response Power Algorithms in
        Noisy Environments.” IEEE Signal Processing Letters 21, no. 5
        (May 2014): 581–85. https://doi.org/10.1109/LSP.2014.2311164.
    """
    signal_fre_bins, fre_bins = divide_into_fre_bins(
        received_data, num_groups, fs, f_min, f_max, n_fft_min
    )

    # MUSIC algorithm in every frequency point
    spectrum_fre_bins = np.zeros((signal_fre_bins.shape[1], angle_grids.size))
    for i, fre in enumerate(fre_bins):
        spectrum_fre_bins[i, :] = music(
            received_data=signal_fre_bins[:, i, :],
            num_signal=num_signal,
            array=array,
            signal_fre=fre,
            angle_grids=angle_grids,
            unit=unit,
        )

    spectrum = np.mean(
        spectrum_fre_bins
        / np.linalg.norm(spectrum_fre_bins, ord=np.inf, axis=1).reshape(-1, 1),
        axis=0,
    )

    return np.squeeze(spectrum)


def cssm(
    received_data,
    num_signal,
    array,
    fs,
    angle_grids,
    pre_estimate,
    fre_ref=None,
    f_min=None,
    f_max=None,
    unit="deg",
):
    """Coherent Signal Subspace Method (CSSM) for wideband DOA estimation.

    Args:
        received_data : Array received signals
        num_signal : Number of signals
        array : Instance of array class
        fs: sampling frequency
        angle_grids : Angle grids corresponding to spatial spectrum. It should
            be a numpy array.
        pre_estimate: pre-estimated angles
        fre_ref: reference frequency. If it's not provided the frequency point
            with the maximum power will be used.
        f_min : Minimum frequency of interest. Defaults to None.
        f_max : Maximum frequency of interest. Defaults to None.
        unit : Unit of angle, 'rad' for radians, 'deg' for degrees. Defaults to
            'deg'.

    References:
        Wang, H., and M. Kaveh. “Coherent Signal-Subspace Processing for the
        Detection and Estimation of Angles of Arrival of Multiple Wide-Band
        Sources.” IEEE Transactions on Acoustics, Speech, and Signal Processing
        33, no. 4 (August 1985): 823-31.
        https://doi.org/10.1109/TASSP.1985.1164667.
    """
    num_snapshots = received_data.shape[1]
    pre_estimate = pre_estimate.reshape(1, -1)

    # Divide the received signal into multiple frequency points
    delta_f = fs / num_snapshots
    # there is a little trick to use as wider frequency range as possible
    idx_f_min = max(int(f_min / delta_f) - 1, 0) if f_min is not None else 0
    idx_f_max = (
        min(int(f_max / delta_f) + 1, num_snapshots // 2)
        if f_max is not None
        else num_snapshots // 2
    )
    signal_fre_bins = np.fft.fft(received_data, axis=1)[
        :, idx_f_min : idx_f_max + 1
    ]
    fre_bins = np.fft.fftfreq(num_snapshots, 1 / fs)[idx_f_min : idx_f_max + 1]

    if fre_ref is None:
        # Find the frequency point with the maximum power
        fre_ref = fre_bins[np.argmax(np.abs(signal_fre_bins).sum(axis=0))]

    # Calculate the manifold matrix corresponding to the pre-estimated angles at
    # the reference frequency point
    matrix_a_ref = array.steering_vector(fre_ref, pre_estimate, unit=unit)

    for i, fre in enumerate(fre_bins):
        # Manifold matrix corresponding to the pre-estimated angles at
        # each frequency point
        matrix_a_f = array.steering_vector(fre, pre_estimate, unit=unit)
        matrix_q = matrix_a_f @ matrix_a_ref.transpose().conj()
        # Perform singular value decomposition on matrix_q
        matrix_u, _, matrix_vh = np.linalg.svd(matrix_q)
        # Construct the optimal focusing matrix using the RSS method
        matrix_t_f = matrix_vh.transpose().conj() @ matrix_u.transpose().conj()
        # Focus the received signals at each frequency point to the reference
        # frequency point
        signal_fre_bins[:, i] = matrix_t_f @ signal_fre_bins[:, i]

    spectrum = music(
        received_data=signal_fre_bins,
        num_signal=num_signal,
        array=array,
        signal_fre=fre_ref,
        angle_grids=angle_grids,
        unit=unit,
    )

    return np.squeeze(spectrum)


def tops(
    received_data,
    num_signal,
    array,
    fs,
    angle_grids,
    num_groups,
    fre_ref=None,
    f_min=None,
    f_max=None,
    n_fft_min=128,
    unit="deg",
):
    """Test of orthogonality of projected subspaces (TOPS) method for wideband
    DOA estimation.

    Args:
        received_data: received signals from the array.
        num_signal: Number of signals.
        array : Instance of array class
        fs: Sampling frequency.
        angle_grids: Grid points of spatial spectrum, should be a numpy array.
        num_groups: Number of groups for FFT, each group performs an
            independent FFT.
        fre_ref: reference frequency. If it's not provided the frequency point
            with the maximum power will be used.
        f_min : Minimum frequency of interest. Defaults to None.
        f_max : Maximum frequency of interest. Defaults to None.
        n_fft_min: minimum number of FFT points
        unit: Unit of angle measurement, 'rad' for radians, 'deg' for degrees.
            Defaults to 'deg'.

    References:
        Yoon, Yeo-Sun, L.M. Kaplan, and J.H. McClellan. “TOPS: New DOA Estimator
        for Wideband Signals.” IEEE Transactions on Signal Processing 54, no. 6
        (June 2006): 1977-89. https://doi.org/10.1109/TSP.2006.872581.
    """
    num_antennas = received_data.shape[0]

    signal_fre_bins, fre_bins = divide_into_fre_bins(
        received_data, num_groups, fs, f_min, f_max, n_fft_min
    )

    if fre_ref is None:
        fre_ref = fre_bins[np.argmax(np.abs(signal_fre_bins).sum(axis=(0, 2)))]

    # index of reference frequency in FFT output
    ref_index = int(fre_ref / (fs / fre_bins.size))
    # get signal space of reference frequency
    signal_space_ref = get_signal_space(
        np.cov(signal_fre_bins[:, ref_index, :]), num_signal=num_signal
    )

    spectrum = np.zeros(angle_grids.size)
    for i, grid in enumerate(angle_grids):
        matrix_d = np.empty((num_signal, 0), dtype=np.complex128)

        for j, fre in enumerate(fre_bins):
            # calculate noise subspace for the current frequency point
            noise_space_f = get_noise_space(
                np.cov(signal_fre_bins[:, j, :]), num_signal
            )

            # construct transformation matrix
            matrix_phi = array.steering_vector(fre - fre_ref, grid, unit=unit)
            matrix_phi = np.diag(np.squeeze(matrix_phi))

            # transform the signal subspace of the reference frequency to the
            # current frequency using the transformation matrix
            matrix_u = matrix_phi @ signal_space_ref

            # construct projection matrix to reduce errors in matrix U
            matrix_a_f = array.steering_vector(fre, grid, unit=unit)
            matrix_p = (
                np.eye(num_antennas)
                - 1
                / (matrix_a_f.transpose().conj() @ matrix_a_f)
                * matrix_a_f
                @ matrix_a_f.transpose().conj()
            )

            # project matrix U using the projection matrix
            matrix_u = matrix_p @ matrix_u

            matrix_d = np.concatenate(
                (matrix_d, matrix_u.T.conj() @ noise_space_f), axis=1
            )

        # construct spatial spectrum using the minimum eigenvalue of matrix D
        _, s, _ = np.linalg.svd(matrix_d)
        spectrum[i] = 1 / min(s)

    return spectrum
