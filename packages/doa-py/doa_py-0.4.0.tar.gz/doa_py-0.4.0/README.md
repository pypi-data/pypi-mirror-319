<div align="left">
  <img src="pics/doa_py.svg" alt="DOA_Py logo" width="20%">
</div>

# DOA_Py

DOA Estimation algorithms implemented in Python. It can be used for ULA, UCA and broadband/wideband DOA estimation.

## Getting Started

### Installation

```bash
pip install doa_py
```

or install from source

```bash
git clone https://github.com/zhiim/doa_py.git
cd doa_py
pip install .
```

### Usage

A sample example of DOA estimation using MUSIC algorithm.

```python
import numpy as np

from doa_py import arrays, signals
from doa_py.algorithm import music
from doa_py.plot import plot_spatial_spectrum

# Create a 8-element ULA with 0.5m spacing
ula = arrays.UniformLinearArray(m=8, dd=0.5)
# Create a complex stochastic signal
source = signals.ComplexStochasticSignal(fc=3e8)

# Simulate the received data
received_data = ula.received_signal(
    signal=source, snr=0, nsamples=1000, angle_incidence=np.array([0, 30]), unit="deg"
)

# Calculate the MUSIC spectrum
angle_grids = np.arange(-90, 90, 1)
spectrum = music(
    received_data=received_data,
    num_signal=2,
    array=ula,
    signal_fre=3e8,
    angle_grids=angle_grids,
    unit="deg",
)

# Plot the spatial spectrum
plot_spatial_spectrum(
    spectrum=spectrum,
    ground_truth=np.array([0, 30]),
    angle_grids=angle_grids,
    num_signal=2,
)
```

You will a get a figure like this:
![music_spectrum](https://github.com/zhiim/doa_py/blob/master/pics/music_spectrum.svg)

Check [examples](https://github.com/zhiim/doa_py/tree/master/examples) for more examples.

## What's implemented

### Array Structures

- Uniform Linear Array (ULA)
- Uniform Rectangular Array (URA, to be implemented)
- Uniform Circular Array (UCA)

### Signal Models

- **Narrowband**
  - _ComplexStochasticSignal_: The amplitude of signals at each sampling point is a complex random variable.
  - _RandomFreqSignal_: Signals transmitted by different sources have different intermediate frequencies (IF).
- **Broadband**
  - _ChirpSignal_: Chirp signals with different chirp bandwidths within the sampling period.
  - _MultiFreqSignal_: Broadband signals formed by the superposition of multiple single-frequency signals within a certain frequency band.
  - _MixedSignal_: Narrorband and broadband mixed signal

### Algorithms

- DOA estimation for ULA
  - [x] MUSIC
  - [x] ESPRIT
  - [x] Root-MUSIC
  - [x] OMP
  - [x] l1-SVD
- DOA estimation for URA
  - [ ] URA-MUSIC
  - [ ] URA-ESPRIT
- DOA estimation for UCA
  - [x] UCA-RB-MUSIC
  - [x] UCA-ESPRIT
- Broadband/Wideband DOA estimation
  - [x] ISSM
  - [x] CSSM
  - [x] TOPS

## License

This project is licensed under the [MIT](LICENSE) License - see the LICENSE file for details.
