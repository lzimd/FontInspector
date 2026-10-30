---
title: "The 'fmtx' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-fmtx-fmtx"></a>

# The `'fmtx'` table

<a id="anchor-fmtx-part-1"></a>

## Introduction

The *Font Metrics Table* (tag: `'fmtx'`) identifies a glyph whose points represent various font-wide metrics: ascent, descent, caret angle, caret offset. If this table is present, these points override their corresponding values in the `'hhea'` and `'vhea'` tables. Representing these metrics as points rather that values offers several advantages.

- In Quickdraw Text, glyphs are constrained to not exceed the font's ascent and descent. Because of this, many fonts artificially increase their ascent and descent values in the `'hhea'` table to accomodate exceptionally tall or low glyphs. The `'fmtx'` is only used in ATSUI, allowing the same font to specify "real" values for ascent and descent without changing the behavior in Quickdraw Text.
- Since `'fmtx'` metrics are represented as points, they can change for different variation settings, allowing the font to change its line spacing and/or caret angle as it changes weight, or optical point size.
- `'fmtx'` metric points can also be instructed, allowing the font to tune its line spacing at small sizes for improved readability.
- **NOTE**: The material in this chapter only applies to TrueType fonts.

<a id="anchor-fmtx-part-2"></a>

## Font Metrics Table Format

The Font Metrics table format is as follows:

| Type | Name | Meaning |
| --- | --- | --- |
| fixed32 | version | Version (set to 0x00020000). |
| uint32 | glyphIndex | The glyph whose points represent the metrics. |
| uint8 | horizontalBefore | Point number for the horizontal ascent. |
| uint8 | horizontalAfter | Point number for the horizontal descent. |
| uint8 | horizontalCaretHead | Point number for the horizontal caret head. |
| uint8 | horizontalCaretBase | Point number for the horizontal caret base. |
| uint8 | verticalBefore | Point number for the vertical ascent. |
| uint8 | verticalAfter | Point number for the vertical descent. |
| uint8 | verticalCaretHead | Point number for the vertical caret head. |
| uint8 | verticalCaretBase | Point number for the vertical caret base. |

Line spacing using the `'fmtx'` table is computed by measuring the distance from the font's "Before" metric point to the "After" metric point. "Before" is the point that specifies the distance from the baseline (or centerline for vertical) to the previous line's "After." In horizontal text, this corresponds to the font's ascent. "After" is the point that specifies the distance from the baseline (centerline) to the next line's "Before." In horizontal text, this corresponds to the font's descent.

Caret angle using the `'fmtx'` table is computed by using the angle between the font's "Caret Head" metric point and the "Caret Base" metric point. "Caret Head" is the point that specifies the angle for the caret relative to the "Caret Base" point. "Caret Base" is the point the specifies the location where the caret should intersect the baseline (centerline). For horizontal text, the y-coordinate of the "Caret Base" must be 0. For vertical text, the x-coordinate of the "Caret Base" must be 0.

If an `'fmtx'` table is present, it must specify point numbers for all eight metric points. Even if the font is intended for only horizontal writing, it must identify points for vertical metrics as well.

Typical coordinates for an italic font whose units-per-em is 2048 are shown in the following table:

| Name | Coordinates |
| --- | --- |
| Horizontal before | (0, 1600) |
| Horizontal after | (0, -448) |
| Horizontal caret head | (210, 1600) |
| Horizontal caret base | (-140, 0) |
| Vertical before | (1024, 0) |
| Vertical after | (-1024, 0) |
| Vertical caret head | (1024, 0) |
| Vertical caret base | (0, 0) |
