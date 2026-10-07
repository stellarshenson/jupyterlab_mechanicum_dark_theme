# Defects - jupyterlab_mechanicum_dark_theme

Observed wrong behaviour of the theme and the trail of what was tried against it.

## Authors

- `@kj` Konrad Jelen

## Main area tabs `TABS`

The tab bar of the main area, the selected tab and the strip under the tab bar

- [x] `DEF-TABS-1` **Selected tab does not join the strip under it** - MINOR; selected tab is a crimson gradient with a gold line at its bottom; the 8px strip under the tab bar (`.jp-Toolbar-micro`) is cloth; in Steel Dark tab and strip share one colour with no line between; `style/mechanicum.css`
  - evidence: build 1.0.4, Chrome 154: `.jp-Toolbar-micro` computes rgb(92, 26, 22), the gradient end colour; tab box-shadow has top, left and right segments only; screenshot shows tab and strip joined
  - repro: Mechanicum theme, open a terminal, look where the selected tab meets the strip under the tab bar
  - test-tags: MANUAL
  - root-cause: 2026-10-07T16:50:20Z @kj tab: `linear-gradient(#872a22, #5c1a16)` and `box-shadow: inset 0 0 0 1px`; strip: the cloth image of `.jp-Toolbar`
  - log: 2026-10-07T16:50:20Z @kj added
  - log: 2026-10-07T16:57:03Z @kj closed: fixed: strip under the tab bar takes the end colour of the tab gradient; the gold line of the tab has no bottom segment
- [x] `DEF-TABS-2` **Crimson stays at the edges of a coloured tab** - MINOR; selected tab coloured by `jupyterlab_colourful_tab_extension` keeps a crimson block at its left edge and at its right edge; `style/mechanicum.css`
  - evidence: build 1.0.4, Chrome 154: tab coloured Green computes background rgb(37, 59, 42), background-image none; screenshot shows no crimson at either edge
  - repro: Mechanicum theme, right-click a terminal tab, Tab Colour, Green, select that tab
  - test-tags: MANUAL
  - root-cause: 2026-10-07T16:50:20Z @kj extension sets `background-color` only; the theme's gradient is a `background-image` and shows in the tab's padding
  - log: 2026-10-07T16:50:20Z @kj added
  - log: 2026-10-07T16:57:03Z @kj closed: fixed: a selected tab with a `jp-colourful-tab-` class gets `background-image: none` and `box-shadow: none`

## Terminal `TERM`

Colours of the terminal

- [x] `DEF-TERM-3` **Terminal text is parchment, not grey-green** - MINOR; terminal default text is `#e6d9b8`; wanted: the grey-green of an old terminal; `style/mechanicum.css`
  - evidence: build 1.0.4, Chrome 154: default terminal text pixel is rgb(158, 181, 156), 8.4 on #181211; menu, file list and tab text colours unchanged
  - repro: Mechanicum theme, open a terminal, run `ls`
  - test-tags: MANUAL
  - root-cause: 2026-10-07T16:50:20Z @kj terminal reads `--jp-ui-font-color0` from `document.body`, the colour of all UI text
  - log: 2026-10-07T16:50:20Z @kj added
  - log: 2026-10-07T16:57:03Z @kj closed: fixed: `--jp-ui-font-color0` is #9eb59c on body and the theme's value on every child of body
