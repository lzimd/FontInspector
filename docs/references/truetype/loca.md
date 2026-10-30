---
title: "The 'loca' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-loca-loca"></a>

# The `'loca'` table

<a id="anchor-loca-part-1"></a>

## General table information

The `'loca'` table stores the offsets to the locations of the glyphs in the font relative to the beginning of the `'glyf'` table. Its purpose is to provide quick access to the data for a particular character. For example, in the standard Macintosh glyph ordering, the character A is the 76th glyph in a font. The `'loca'` table stores the offset from the start of the `'glyf'` table to the position at which the data for each glyph can be found.

Table 32 shows a sample `'loca'` table for a font with *`n`* glyphs. The table stores the offset from the start of the glyph data to the start of the indexed glyph. Note that the glyph length column is not actually stored in the table but can be computed with the data the table provides. Glyph 0, being the first glyph in the font, has an offset of 0 words from the start of the glyph data. Its length can be calculated by subtracting its offset from the offset of the next glyph in the table. To make it possible to compute the length of the last glyph element, there is an extra entry after the offset that points to the last valid index. This index points to the end of the glyph data.

The size of the offset depends upon the format used. This is specified in the [Font Header (`'head'`) table](head.md). In the short format, it is words that are being counted. An offset of 100 would represent 200 bytes. In the long format, it is bytes that are counted. An offset of 100 would represent 100 bytes.

**Table 32**: `'loca'` example

| Glyph Index | Offset | Glyph length |
| --- | --- | --- |
| 0 | 0 | 100 |
| 1 | 100 | 150 |
| 2 | 250 |  |
| ... | ... | ... |
| n-1 | 1170 | 120 |
| extra | 1290 |  |

By definition, the first glyph in any TrueType font must be the MISSING CHARACTER GLYPH. As a result, index zero always points to the glyph that is displayed when a requested character is not found in the font. On the Macintosh, the MISSING CHARACTER GLYPH is commonly represented by a blank box. If the font does not contain an outline for the missing character, then the first and second offsets should have the same value. This also applies to any other character without an outline, such as the space character. If a glyph has no outline, its length should be zero.

There are two versions of this table, the short and the long. The version used is specified in the [Font Header (`'head'`) table](head.md) in the `indexToLocFormat` field. The choice of long or short offsets is dependent on the maximum possible offset distance.

This table is an array of *n* offsets where *n* is the number of glyphs in the font plus one (for the extra entry mentioned above). The actual offset for any particular glyph is divided by 2. The number of glyphs in a font must be stored in the [Maximum Profile `'maxp'` table](maxp.md).

The glyph data is always word aligned.

**Table 33** : `'loca'` short version

| Type | Name | Description |
| --- | --- | --- |
| uint16 | offsets\[n\] | The actual local offset divided by 2 is stored. The value of n is the number of glyphs in the font + 1. The number of glyphs in the font is found in the maximum profile table. |

**Table 34**: `'loca'` long version

| Type | Name | Description |
| --- | --- | --- |
| uint32 | offsets\[n\] | The actual local offset is stored. The value of n is the number of glyphs in the font + 1. The number of glyphs in the font is found in the maximum profile table. |

---

<a id="anchor-loca-part-2"></a>

## Platform-specific Information

The `'loca'` table only used with fonts that have TrueType outlines (that is, a [`'glyf'` table](glyf.md)). Fonts that have no TrueType outlines do not require a `'loca'` table.

<a id="anchor-loca-part-3"></a>

## Dependencies

The `'loca'` table is most intimately dependent upon the contents of the [`'glyf'` table](glyf.md) and vice versa. Changes to the `'loca'` table *must not be made* unless appropriate changes to the [`'glyf'` table](glyf.md) are simultaneously made.

The size of entries in the `'loca'` table must be appropriate for the value of the `indexToLocFormat` field of the [`'head'` table](head.md). The number of entries must be the same as the `numGlyphs` field of the [`'maxp'` table](maxp.md).

<a id="anchor-loca-part-4"></a>

## Tools

The `'loca'` table can be dumped and fused with ftxdumperfuser. However, it's probably a bad idea to edit the `'loca'` table by itself. ftxdumperfuser automatically updates the `'loca'` and [`'head'`](head.md) tables whenever the [`'glyf'`](glyf.md) table is modified.
