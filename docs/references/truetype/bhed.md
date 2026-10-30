---
title: "The 'bhed' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-bhed-bhed"></a>

# The `'bhed'` table

<a id="anchor-bhed-part-1"></a>

## General table information

The `'bhed'` table contains global information about a bitmap font. It records such facts as the font version number, the creation and modification dates, revision number and basic typographic data that applies to the font as a whole. This includes a specification of the font bounding box, the direction in which the font's glyphs are most likely to be written and other information about the placement of glyphs in the em square. The checksum is used to verify the integrity of the data in the font. It can also be used to distinguish between two similar fonts.

The `'bhed'` table is byte-for-byte identical with the [`'head'`](head.md "'head' table documentation") (font header) table. OS X uses the presence of a `'bhed'` table as a flag that a font doesn't have any glyph outlines but only embedded bitmaps. For more information on the fields in a `'bhed'` table and their values, see [the documentation for the `'head'` (font header) table](head.md "'head' (font header) table").

<a id="anchor-bhed-part-2"></a>

## Platform-specific Information

This table is used in OS X to signal the presence of a bitmap-only font. It is *required* if a font has no outlines. If a font does have outlines, then there should be no `'bhed'` table.

<a id="anchor-bhed-part-3"></a>

## Dependencies

If a `'bhed'` table is present in a font, the font must also have [`'bdat'`](bdat.md "'bdat' table documentation") and [`'bloc'`](bloc.md "'bloc' table documentation") tables. The font must have no [`'head'`](head.md "'head' table documentation") or [`'glyf'`](glyf.md "'glyf' table documentation") tables.

Field dependencies between the `'bhed'` table's fields and other tables are described in [the documentation for the `'head'` (font header) table](head.md "'head' (font header) table").
