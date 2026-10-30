---
title: "hmtx — Horizontal Metrics Table"
description: "The horizontal metrix table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2023-01-10T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/hmtx.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-hmtx-hmtx-horizontal-metrics-table"></a>

# hmtx — Horizontal Metrics Table

Glyph metrics used for horizontal text layout include glyph advance widths, side bearings and X-direction min and max values (xMin, xMax). These are derived using a combination of the glyph outline data ('glyf', 'CFF ' or CFF2) and the horizontal metrics table. The horizontal metrics ('hmtx') table provides glyph advance widths and left side bearings.

In a font with TrueType outline data, the ['glyf'](glyf.md) table provides xMin and xMax values, but not advance widths or side bearings. The advance width is always obtained from the 'hmtx' table. In some fonts, depending on the state of flags in the ['head'](head.md) table, the left side bearings may be the same as the xMin values in the 'glyf' table, though this is not true for all fonts. (See the description of bit 1 of the flags field in the 'head' table.) For this reason, left side bearings are provided in the 'hmtx' table. The right side bearing is always derived using advance width and left side bearing values from the 'hmtx' table, plus bounding-box information in the glyph description — see below for more details.

In a variable font with TrueType outline data, the left side bearing value in the 'hmtx' table must always be equal to xMin (bit 1 of the 'head' flags field must be set). Hence, these values can also be derived directly from the 'glyf' table. Note that these values apply only to the default instance of the variable font: non-default instances may have different side bearing values. These can be derived from interpolated “phantom point” coordinates using the ['gvar'](gvar.md) table (see below for additional details), or by applying variation data in the [HVAR](hvar.md) table to default-instance values from the 'glyf' or 'hmtx' table.

In a font with CFF version 1 outline data, the 'CFF ' table does include advance widths. These values are used by PostScript processors, but are not used in OpenType layout. In an OpenType context, the 'hmtx' table is required and must be used for advance widths. Note that fonts in a Font Collection file that share a 'CFF ' table may specify different advance widths in font-specific 'hmtx' tables for a particular glyph index. Also note that the CFF2 table does not include advance widths. In addition, for either CFF or CFF2 data, there are no explicit xMin and xMax values; side bearings are implicitly contained within the CharString data, and can be obtained from the CFF / CFF2 rasterizer. Some layout engines may use left side bearing values in the 'hmtx' table, however; hence, font production tools should ensure that the left side bearing values in the 'hmtx' table match the implicit xMin values reflected in the CharString data. In a variable font with CFF2 outline data, left side bearing and advance width values for non-default instances should be obtained by combining information from the 'hmtx' and HVAR tables.

The table uses a LongHorMetric record to give the advance width and left side bearing of a glyph. Records are indexed by glyph ID. As an optimization, the number of records can be less than the number of glyphs, in which case the advance width value of the last record applies to all remaining glyph IDs. This can be useful in monospaced fonts, or in fonts that have a large number of glyphs with the same advance width (provided the glyphs are ordered appropriately). The number of LongHorMetric records is determined by the numberOfHMetrics field in the ['hhea'](hhea.md) table.

If numberOfHMetrics is less than the total number of glyphs, then the hMetrics array is followed by an array for the left side bearing values of the remaining glyphs. The number of elements in the leftSideBearings array will be derived from the numGlyphs field in the ['maxp'](maxp.md) table minus numberOfHMetrics.

*Horizontal Metrics Table:*

| Type | Name | Description |
| --- | --- | --- |
| LongHorMetric | hMetrics\[numberOfHMetrics\] | Paired advance width and left side bearing values for each glyph. Records are indexed by glyph ID. |
| FWORD | leftSideBearings\[numGlyphs - numberOfHMetrics\] | Left side bearings for glyph IDs greater than or equal to numberOfHMetrics. |

*LongHorMetric Record:*

| Type | Name | Description |
| --- | --- | --- |
| UFWORD | advanceWidth | Advance width, in font design units. |
| FWORD | lsb | Glyph left side bearing, in font design units. |

In a font with TrueType outlines, xMin and xMax values for each glyph are given in the 'glyf' table. The advance width (“aw”) and left side bearing (“lsb”) can be derived from the glyph “phantom points”, which are computed by the TrueType rasterizer; or they can be obtained from the 'hmtx' table. In a font with CFF or CFF2 outlines, xMin (= left side bearing) and xMax values can be obtained from the CFF / CFF2 rasterizer. From those values, the right side bearing (“rsb”) is calculated as follows:

```
    rsb = aw - (lsb + xMax - xMin)
```

If pp1 and pp2 are TrueType phantom points used to control lsb and rsb, their initial position in the X-direction is calculated as follows:

```
    pp1 = xMin - lsb
    pp2 = pp1 + aw
```

If a glyph has no contours, xMax/xMin are not defined. The left side bearing indicated in the 'hmtx' table for such glyphs should be zero.
