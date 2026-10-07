# Changelog

<!-- <START NEW CHANGELOG ENTRY> -->

<!-- <END NEW CHANGELOG ENTRY> -->

## [1.0.7] - 2026-10-07

### Fixed

- The gold line of the selected tab has one colour along its top, its sides and its top corners. In 1.0.5 one pixel at each top corner was brighter than the line beside it; it showed on the selected tab of a tab bar that is not the active one, in a split layout (`DEF-TABS-4`)

## [1.0.5] - 2026-10-07

### Fixed

- The selected tab joins the strip under the tab bar. The strip has the end colour of the tab's crimson gradient, and the tab's gold line no longer runs along its bottom (`DEF-TABS-1`)
- A tab coloured by `jupyterlab_colourful_tab_extension` no longer keeps a crimson block at its left edge and at its right edge (`DEF-TABS-2`)

### Changed

- Terminal default text is grey-green `#9eb59c`, the colour of an old terminal, where it was parchment. All other text keeps its colour (`DEF-TERM-3`)

## [1.0.3] - 2026-10-07

### Changed

- Scrollbars are thin. Every scrolling area in JupyterLab now draws the narrow scrollbar that the MOTD tab of `jupyterlab_galaxahub_motd_extension` uses: 10px wide in Chrome, where it was 15px. The thumb and track colours are unchanged

## [1.0.1] - 2026-10-03

### Added

- First public release of the theme, on the project structure of the steel dark theme: Mechanicum colours in `style/variables.css`, the ornament in `style/mechanicum.css` and its images in `style/images/`
