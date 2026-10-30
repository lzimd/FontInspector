---
title: "The 'EBSC' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-EBSC-bhed"></a>

# The `'EBSC'` table

<a id="anchor-EBSC-part-1"></a>

## General table information

The `'EBSC'` table provides a mechanism for forcing the TrueType scaler to use a particular size of embedded bitmap when generating glyphs for a different point size.

The `'EBSC'` table is used only for bitmap-only TrueType fonts. Fonts which have outline data will always use the outlines to generate glyphs for a point size if there is no embedded bitmap available.

If the font has no glyph outlines, then embedded bitmaps are the only mechanism the TrueType scaler can use to provide a glyph for a charater. If there is an embeded bitmap for the requested size, that will be used; otherwise, the scaler will have to create one from the bitmap for another point size. The TrueType scaler has an algorithm it uses to determine which point size is appropriate to use in such a case; the `'EBSC'` table allows the font designer to override this default algorithm.

The `'EBSC'` table begins with a header describing the point size overrides it contains:

| Type | Name | Description |
| --- | --- | --- |
| Fixed | version | Version number of the table (0x00020000 for the initial version). |
| UInt32 | numSizes | The number of EBSCScaleTable in this table. |
| variable | scaleTables\[numSizes\] | Subtables indicating how to override the TrueType scaler's default algorithm for finding a point size to use when generating a glyph for a point size not in the font. |

The header is followed immediately by the scaleTables array. The numSizes in the header indicates the number of EBSCScaleTable in the array. Each override is defined by one EBSCScaleTable.

| Type | Name | Description |
| --- | --- | --- |
| BLOCLineMetrics | hori | Horizontal line metrics for this point size (not used on the Mac OS). |
| BLOCLineMetrics | vert | Vertical line metrics (not used on OS X). |
| UInt8 | ppemX | The horizontal point size for this EBSCScaleTable |
| UInt8 | ppemY | The vertical point size for this EBSCScaleTable |
| UInt8 | substitutePpemX | The horizontal point size to use when generating glyphs for the point size in the ppemX field. |
| UInt8 | substitutePpemY | The vertical point size to use when generating glyphs for the point size in the ppemY field. |

For example, suppose a font has 9-point and 24-point embedded bitmaps. Ordinarly, the TrueType scaler would use the 9-point bitmaps as a source of data if trying to generate an 18-point bitmap. The `'EBSC'` table can be used to override this, however, by including an EBSCScaleTable with the ppemX equal to 18 and the substitutePpemX equal to 24.

<a id="anchor-EBSC-part-2"></a>

## Platform-specific Information

OS X does not use the horizontal and vertical line metrics fields. See documentation on the [bitmap location table](bloc.md) to see how these fields are structured.

<a id="anchor-EBSC-part-3"></a>

## Dependencies

If an `'EBSC'` table is present in a font, the font must be a bitmap-only font. That is, it should also have [`'bdat'`](bdat.md "'bdat' table documentation") and [`'bloc'`](bloc.md "'bloc' table documentation") tables. The font must have no [`'head'`](head.md "'head' table documentation") or [`'glyf'`](glyf.md "'glyf' table documentation") tables. Bitmap only fonts use the [`'bhed'`](bhed.md) table to store information ordinarily found in the [`'head'`](head.md) table.
