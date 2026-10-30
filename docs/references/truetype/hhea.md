---
title: "The 'hhea' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-hhea-hhea"></a>

# The `'hhea'` table

<a id="anchor-hhea-part-1"></a>

## General table information

The `'hhea'` table contains information needed to layout fonts whose characters are written horizontally, that is, either left to right or right to left. This table contains information that is general to the font as a whole. Information which pertains to specific glyphs is given in the `'hmtx'` table defined below.

The table begins with a version number. It includes values which represent the design intentions of the font's designer (ascent, descent and linegap) as well as values that are computed and which must be consistent with the data appearing in the `'hmtx'` table (advanceWidthMax, minLeftSideBearing, minRightSideBearing).

The `'hhea'` table uses the concept of extent. The extent is the distance from the left side bearing to the right most positions in the glyph outline.

The `caretSlopeRise` and `caretSlopeRun` are used to specify the mathematical slope of the proper angle for the caret when displayed with this font. The slope is equal to `caretSlopeRise` divided by `caretSlopeRun`. Thus, a rise of 1 and run of 0 will specify a vertical caret (infinite slope). A rise of 0 and run of 1 will specify a horizontal caret (zero slope). Something in-between will be desirable for fonts whose glyphs are obliqued or italic. For example, one could use a rise of 2048 and a run of 270 for a slope of 7.6, which corresponds to an angle of 82.5°. (`tan(82.5°) = 7.6`)

Note that since the slope is a *ratio*, values may be used which simplify or speed up calculations. A `caretSlopeRise` of 8 and `caretSlopeRun` of 6 means the same thing as `caretSlopeRise` of 4 and `caretSlopeRun` of 3. As such, a run of 0 is sufficient to specify a vertical caret; the rise is superfluous. Similarly, a rise of 0 is sufficient to specify a horizontal caret.

`caretSlopeRise` and `caretSlopeRun` may not both be zero.

The `caretOffset` value is the amount by which a slanted highlight on a glyph needs to be shifted to produce the best appearance. Since `caretOffset` is a signed FUnit value, it will scale.

A number of fields in this table are reserved and should be set to a value of zero.

The values for `ascent`, `descent` and `lineGap` represent the design intentions of the font's creator rather than any computed value, and individual glyphs may well exceed the the limits they represent. The values for the `advanceWidthMax`, `minLeftSideBearing` and `minRightSideBearing` are computed values and must be consistent with whatever values appear in the `'hmtx'` table. These values are as their names imply, the actual maximum advance width for any glyph in the font, the minimum left side bearing for any glyph and the minimum right side bearing for any glyph. Similarly, the `xMin`, `yMin`, `xMax`, and `yMax`, fields in the [`'head'`](https://developer.apple.com/fonts/TrueType-Reference-Manual/Chap6head.html) represent the actual extrema for the glyphs in the font.

The value `numOfLongHorMetrics` is used by the [`'hmtx'`](https://developer.apple.com/fonts/TrueType-Reference-Manual/Chap6htmx.xml) table.

*The `'hhea'` Table*

| Type | Name | Description |
| --- | --- | --- |
| Fixed | version | 0x00010000 (1.0) |
| FWord | ascent | Distance from baseline of highest ascender |
| FWord | descent | Distance from baseline of lowest descender |
| FWord | lineGap | typographic line gap |
| uFWord | advanceWidthMax | must be consistent with horizontal metrics |
| FWord | minLeftSideBearing | must be consistent with horizontal metrics |
| FWord | minRightSideBearing | must be consistent with horizontal metrics |
| FWord | xMaxExtent | max(lsb + (xMax-xMin)) |
| int16 | caretSlopeRise | used to calculate the slope of the caret (rise/run) set to 1 for vertical caret |
| int16 | caretSlopeRun | 0 for vertical |
| FWord | caretOffset | set value to 0 for non-slanted fonts |
| int16 | reserved | set value to 0 |
| int16 | reserved | set value to 0 |
| int16 | reserved | set value to 0 |
| int16 | reserved | set value to 0 |
| int16 | metricDataFormat | 0 for current format |
| uint16 | numOfLongHorMetrics | number of advance widths in metrics table |

---

<a id="anchor-hhea-part-2"></a>

## Dependencies

Other tables may have information duplicating data contained in the `'hhea'` table, most notably the *ascent* and *descent* fields. Such information may be found in tables such as the [`'OS/2'` table](OS2.md) or the [`'bloc'` table](bloc.md). Care should always be taken that metric information within a font is consistent, as different applications and systems get the metric information from different places.

This is particularly true for fonts intended for cross-platform use. E.g., Windows uses the [`'OS/2'` table](OS2.md) as the basic source for ascent and descent for the font.

The caret slope calculated as the ratio between `caretSlopeRise` and `caretSlopeRun` should be equal to `tan(90° + p)`, where `p` is the value of the `italicAngle` field in the `'post'` table.

The value of the *numOfLongHorMetrics* field is used by the [`'hmtx'` (Horizontal Metrics) table](hmtx.md). Fonts that lack an `'hhea'` table must not have an `'hmtx'` table.

<a id="anchor-hhea-part-3"></a>

## Tools

ftxdumperfuser automatically updates the `'hhea'` table whenever the [`'hmtx'`](hmtx.md) table is updated.

Care must be taken when using ftxdumperfuser to fuse in both the `'hhea'` table and the [`'hmtx'`](hmtx.md) table of the same font. They should be fused in the order `'hhea'`-`'hmtx'` to make sure that the `numOfLongHorMetrics` field of the `'hhea'` table is valid. ftxdumperfuser allows the `numOfLongHorMetrics` field to be omitted from the XML source when fusing in an `'hhea'` table in order to prevent its accidental corruption.

Other fields may also be omitted in the XML source. In such cases, values will be carried over from an existing `'hhea'` table or supplied by examining the font.
