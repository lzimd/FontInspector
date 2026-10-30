---
title: "The 'head' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-head-head"></a>

# The `'head'` table

<a id="anchor-head-part-1"></a>

## General table information

The `'head'` table contains global information about the font. It records such facts as the font version number, the creation and modification dates, revision number and basic typographic data that applies to the font as a whole. This includes a specification of the font bounding box, the direction in which the font's glyphs are most likely to be written and other information about the placement of glyphs in the em square. The checksum is used to verify the integrity of the data in the font. It can also be used to distinguish between two similar fonts.

The flags give global information about the font. If bit 0 is set to one, the baselines for the font is at y= 0 (that is, the x-axis). If bit 1 is set to one, the x-position of the leftmost black bit is assumed to be the left side bearing. If bit 2 is set to one, instructions may use point size explicitly in place of pixels per em. This means that scaling a 12 point screen font to obtain the equivalent printer font may not produce the identical result as requesting a 12 point printer font. Setting bit 3 causes the use of integer scaling instead of fractional scaling. Setting bit 4 allows fonts to alter device dependent widths.

The values xMin, yMin, xMax and yMax must be computed by looking at the outline data for the glyphs in the font. Together they specify a rectangle that constitute a bounding box for all of the (ungridfitted) glyphs in the font.

The number of units per em for the font is set in this table. This value should be a power of 2. Its range is from 64 through 16384.

This value lowestRecPPEM is the smallest readable size in pixels per em for this font.

The fontDirectionHint provides information about the way in which the glyphs in this font are likely to be set. A value of 0 indicates a mixed directional font; a value of one indicates only left to right glyphs, -1 only right to left glyphs. The values 2 and -2 refer to fonts which contain some neutral glyphs, that is glyphs without a strong directionality.

A neutral character has no inherent directionality. (It is not a character with zero width). Spaces and punctuation are examples of neutral characters. Non-neutral characters are those with inherent directionality. For example Roman letters (left-to-right) and Arabic letters (right-to-left) have directionality. In a Roman font where spaces and punctuation are present, the font direction hint should be set to 2.

The indexToLocFormat value indicates the type of offset format used in the index to loc (`'loca'`) table.

**Table 22** : `'head'` table

| Type | Name | Description |
| --- | --- | --- |
| Fixed | version | 0x00010000 if (version 1.0) |
| Fixed | fontRevision | set by font manufacturer |
| uint32 | checkSumAdjustment | To compute: set it to 0, calculate the checksum for the `'head'` table and put it in the table directory, sum the entire font as a uint32\_t, then store `0xB1B0AFBA - sum`. (The checksum for the `'head'` table will be wrong as a result. That is OK; do not reset it.) |
| uint32 | magicNumber | set to 0x5F0F3CF5 |
| uint16 | flags | bit 0 - y value of 0 specifies baseline<br> bit 1 - x position of left most black bit is LSB<br> bit 2 - scaled point size and actual point size will differ (i.e. 24 point glyph differs from 12 point glyph scaled by factor of 2)<br> bit 3 - use integer scaling instead of fractional<br> bit 4 - (used by the Microsoft implementation of the TrueType scaler)<br> bit 5 - This bit should be set in fonts that are intended to be laid out vertically, and in which the glyphs have been drawn such that an x-coordinate of 0 corresponds to the desired vertical baseline.<br> bit 6 - This bit must be set to zero.<br> bit 7 - This bit should be set if the font requires layout for correct linguistic rendering (e.g. Arabic fonts).<br> bit 8 - This bit should be set for an AAT font which has one or more metamorphosis effects designated as happening by default.<br> bit 9 - This bit should be set if the font contains any strong right-to-left glyphs.<br> bit 10 - This bit should be set if the font contains Indic-style rearrangement effects.<br> bits 11-13 - Defined by [Adobe](http://partners.adobe.com/asn/developer/opentype/head.htm).<br> bit 14 - This bit should be set if the glyphs in the font are simply generic symbols for code point ranges, such as for a last resort font. |
| uint16 | unitsPerEm | range from 64 to 16384 |
| longDateTime | created | international date |
| longDateTime | modified | international date |
| FWord | xMin | for all glyph bounding boxes |
| FWord | yMin | for all glyph bounding boxes |
| FWord | xMax | for all glyph bounding boxes |
| FWord | yMax | for all glyph bounding boxes |
| uint16 | macStyle | bit 0 bold<br> bit 1 italic<br> bit 2 underline<br> bit 3 outline<br> bit 4 shadow<br> bit 5 condensed (narrow)<br> bit 6 extended |
| uint16 | lowestRecPPEM | smallest readable size in pixels |
| int16 | fontDirectionHint | 0 Mixed directional glyphs<br> 1 Only strongly left to right glyphs<br> 2 Like 1 but also contains neutrals<br> -1 Only strongly right to left glyphs<br> -2 Like -1 but also contains neutrals |
| int16 | indexToLocFormat | 0 for short offsets, 1 for long |
| int16 | glyphDataFormat | 0 for current format |

---

<a id="anchor-head-part-2"></a>

## Platform-specific Information

Although it is officially listed as a "required" TrueType table, it is not in fact required for all sfnt-housed fonts on OS X. Indeed, it isn't even required by all TrueType fonts.

TrueType fonts which have no outline data but consist of bitmaps only should not have a `'head'` table. They should use the byte-by-byte identical [`'bhed'` table](bhed.md) instead. The OS X uses the presence of a `'bhed'` to signal the fact that a font has no outlines.

<a id="anchor-head-part-3"></a>

## Dependencies

Many of the fields in the `'head'` table are closely related to the values in other tables. For example, the *unitsPerEm* field is fundamental to all tables which deal with curves or metrics. This table is used throughout the TrueType rendering engine as a short-cut to determine various key aspects of the font.

Inasmuch as any change to any other table will have an impact on the *checkSumAdjustment* and *modified* fields of the `'head'` table, it is always wisest to update the 'head' table after any font editing operation.
