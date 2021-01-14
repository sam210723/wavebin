# Change Log
All notable changes to this project will be documented in this file.

<details>
<summary>Unreleased changes</summary>

### Added
  - Colours for channels 3 and 4
  - Adjustable subsampling for large waveform captures

### Changed
  - 

### Fixed
  - Unit abbreviations in axis labels
  - Savitzky-Golay filter window calculation
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
