# Change Log
All notable changes to this project will be documented in this file.

<details>
<summary>Unreleased changes</summary>

### Added
  - Support for Rigol waveform captures

### Changed
  - Open file dialog in directory of current waveform capture

### Fixed
  - Minimum number of subsampling points
</details>


## [v2.0](https://github.com/sam210723/wavebin/releases/tag/v2.0) - 2021-02-07
Complete re-write of the project with various new features.

<details>
<summary>Details</summary>

### Added
  - Export waveforms to PulseView srzip file
  - Export waveforms to WAV files
  - Waveform clipping option for digital signals
  - Adjustable subsampling for large waveform captures
  - Hardware graphics acceleration with OpenGL
  - Colours for channels 3 and 4
  - GUI controls to repace CLI arguments
  - Hotkey support

### Changed
  - Show filter name when enabled
  - Waveform data type retrieved from header
  - Left axis label always from channel 0

### Fixed
  - Unit abbreviations in axis labels
  - Savitzky-Golay filter window calculation
  - Slow waveform rendering (see [pyqtgraph#533](https://github.com/pyqtgraph/pyqtgraph/issues/533))
  - Cleaner verbose console output formatting
</details>


## [v1.2](https://github.com/sam210723/wavebin/releases/tag/v1.2) - 2019-11-27
Added support for capture files containing multiple waveforms and a low-pass filter (``-f`` option) to smooth waveforms.

<details>
<summary>Details</summary>

### Added
  - Multi-waveform support
  - Waveform low-pass filter ([Savitzky-Golay](https://web.archive.org/web/20150710002613/http://wiki.scipy.org:80/Cookbook/SavitzkyGolay))
  - Waveform colours
  - Multi-waveform sample
  - Data waveform sample
  - Application icon

### Changed
  - Refactor detail sidebar
  - Remove ``magnitude`` dependency

### Fixed
  - np.linspace float deprecation warning
</details>


## [v1.1](https://github.com/sam210723/wavebin/releases/tag/v1.1) - 2019-11-20
Rewrote Qt code and added a sidebar containing the waveform properties.

<details>
<summary>Details</summary>

### Added
  - Waveform detail sidebar

### Changed
  - Disable Y axis zooming
  - Enum capitalisation

### Fixed
  - Qt code layout
</details>


## [v1.0](https://github.com/sam210723/wavebin/releases/tag/v1.0) - 2019-11-19
Initial release of **wavebin**.
