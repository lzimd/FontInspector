---
title: "head — Font Header Table"
description: "The font header table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-29T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/head.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-head-head-font-header-table"></a>

# head — Font Header Table

<a id="anchor-head-headHeader"></a>

This table gives global information about the font. The bounding box values should be computed using *only* glyphs that have contours. Glyphs with no contours should be ignored for the purposes of these calculations.

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-head-majorVersion"></a>uint16 | majorVersion | Major version number of the font header table — set to 1. |
| <a id="anchor-head-minorVersion"></a>uint16 | minorVersion | Minor version number of the font header table — set to 0. |
| <a id="anchor-head-fontRevision"></a>Fixed | fontRevision | Set by font manufacturer. |
| <a id="anchor-head-checkSumAdjustment"></a>uint32 | checksumAdjustment | To compute: set it to 0, sum the entire font as uint32, then store 0xB1B0AFBA - sum. If the font is used as a component in a font collection file, the value of this field will be invalidated by changes to the file structure and font [table directory](otff.md#anchor-otff-table-directory), and must be ignored. |
| <a id="anchor-head-magicNumber"></a>uint32 | magicNumber | Set to 0x5F0F3CF5. |
| <a id="anchor-head-flags"></a>uint16 | flags | **Bit 0:** Baseline for font at y=0.<br><br>**Bit 1:** Left sidebearing point at x=0 (relevant only for TrueType rasterizers) — see additional information below regarding variable fonts.<br><br>**Bit 2:** Instructions may depend on point size.<br><br>**Bit 3:** Force ppem to integer values for all internal scaler math; may use fractional ppem sizes if this bit is clear. It is strongly recommended that this be set in hinted fonts.<br><br>**Bit 4:** Instructions may alter advance width (the advance widths might not scale linearly).<br><br>**Bit 5:** This bit is not used in OpenType, and should not be set in order to ensure compatible behavior on all platforms. If set, it may result in different behavior for vertical layout in some platforms. (See [Apple’s specification](http://developer.apple.com/fonts//TrueType-Reference-Manual/RM06/Chap6head.html) for details regarding behavior in Apple platforms.)<br><br>**Bits 6 – 10:** These bits are not used in OpenType and should always be cleared. (See [Apple’s specification](http://developer.apple.com/fonts//TrueType-Reference-Manual/RM06/Chap6head.html) for details regarding legacy use in Apple platforms.)<br><br>**Bit 11:** Font data is “lossless” as a result of having been subjected to optimizing transformation and/or compression (such as compression mechanisms defined by ISO/IEC 14496-18, MicroType® Express, WOFF 2.0, or similar) where the original font functionality and features are retained but the binary compatibility between input and output font files is not guaranteed. As a result of the applied transform, the DSIG table may also be invalidated.<br><br>**Bit 12:** Font converted (produce compatible metrics).<br><br>**Bit 13:** Font optimized for ClearType®. Note, fonts that rely on embedded bitmaps (EBDT) for rendering should not be considered optimized for ClearType, and therefore should keep this bit cleared.<br><br>**Bit 14:** Last Resort font. If set, indicates that the glyphs encoded in the 'cmap' subtables are simply generic symbolic representations of code point ranges and do not truly represent support for those code points. If unset, indicates that the glyphs encoded in the 'cmap' subtables represent proper support for those code points.<br><br>**Bit 15:** Reserved, set to 0. |
| <a id="anchor-head-unitsPerEm"></a>uint16 | unitsPerEm | Set to a value from 16 to 16384. Any value in this range is valid. In fonts that have TrueType outlines, a power of 2 is recommended as this allows performance optimization in some rasterizers. |
| <a id="anchor-head-created"></a>LONGDATETIME | created | Number of seconds since 12:00 midnight that started January 1st, 1904, in GMT/UTC time zone. |
| <a id="anchor-head-modified"></a>LONGDATETIME | modified | Number of seconds since 12:00 midnight that started January 1st, 1904, in GMT/UTC time zone. |
| <a id="anchor-head-xMin"></a>int16 | xMin | Minimum x coordinate across all glyph bounding boxes. |
| <a id="anchor-head-yMin"></a>int16 | yMin | Minimum y coordinate across all glyph bounding boxes. |
| <a id="anchor-head-xMax"></a>int16 | xMax | Maximum x coordinate across all glyph bounding boxes. |
| <a id="anchor-head-yMax"></a>int16 | yMax | Maximum y coordinate across all glyph bounding boxes. |
| <a id="anchor-head-macstyle"></a>uint16 | macStyle | **Bit 0:** Bold (if set to 1);<br>**Bit 1:** Italic (if set to 1)<br>**Bit 2:** Underline (if set to 1)<br>**Bit 3:** Outline (if set to 1) <br>**Bit 4:** Shadow (if set to 1)<br>**Bit 5:** Condensed (if set to 1)<br>**Bit 6:** Extended (if set to 1)<br>**Bits 7 – 15:** Reserved (set to 0). |
| <a id="anchor-head-lowestRecPPEM"></a>uint16 | lowestRecPPEM | Smallest readable size in pixels. |
| <a id="anchor-head-fontDirectionHint"></a>int16 | fontDirectionHint <sup>a</sup> | Deprecated (Set to 2).<br>0: Fully mixed directional glyphs;<br>1: Only strongly left to right;<br>2: Like 1 but also contains neutrals;<br>-1: Only strongly right to left;<br>-2: Like -1 but also contains neutrals. |
| <a id="anchor-head-indexToLocFormat"></a>int16 | indexToLocFormat | 0 for short offsets (Offset16), 1 for long (Offset32). |
| <a id="anchor-head-glyphDataFormat"></a>int16 | glyphDataFormat | 0 for current format. |

<sup>a</sup> The fontDirectionHint field was intended for support of right-to-left scripts. Strong left to right, strong right to left, and neutral are properties of characters. A neutral character has no inherent directionality; it is not a character with zero (0) width. Spaces and punctuation are examples of neutral characters. Non-neutral characters are those with inherent directionality. For example, Roman letters (left-to-right) and Arabic letters (right-to-left) have strong directionality. In a “normal” Roman font where spaces and punctuation are present, the font direction hints should be set to two (2).

The unitsPerEm value determines the granularity of the font’s coordinate grid at which coordinates can be specified for visual elements such as outline control points or mark-attachment anchor positions. See the [TrueType Fundamentals](ttch01.md#anchor-ttch01-funits-and-the-grid) chapter for more information.

A glyph’s bounding box is the smallest rectangle that contains all of the glyph’s control points. (See the ['glyf'](glyf.md#anchor-glyf-glyph-headers) table chapter for more information.) The xMin, yMin, xMax and yMax values provide a bounding box that will contain all glyphs from the font. Glyphs without contours are ignored.

The macStyle bits must agree with the fsSelection bits in the [OS/2 table](os2.md). The fsSelection bits are used over the macStyle bits in Windows. The PANOSE values and 'post' table values are ignored for determining bold or italic fonts.

For historical reasons, the fontRevision value contained in this table is not used by Windows to determine the version of a font. Instead, Windows evaluates the version string (ID 5) in the 'name' table.

The left sidebearing point for each glyph corresponds to the first phantom point (“pp1” below—see [Phantom points](tt_instructing_glyphs.md#anchor-tt_instructing_glyphs-phantom-points)) and relates to the glyph left sidebearing (lsb) and xMin as follows:

> pp1 = xMin - lsb

If bit 1 of the flags field is set, then pp1 = 0 for all glyphs and the xMin and left sidebearing for each glyph must be equal.

In a variable font with TrueType outlines, the left side bearing for each glyph must equal xMin, and bit 1 in the flags field must be set. Also, bit 5 must be cleared in all variable fonts. For general information on OpenType Font Variations, see the chapter, [OpenType Font Variations Overview](otvaroverview.md).

Also, in a variable font, the minimum or maximum x or y values of control points can vary, and a tight bounding rectangle containing the outline or all points for an instance of any given glyph can be smaller or larger than for the default instance of that glyph. The xMin, yMin, xMax and yMax values in this table might or might not encompass the derived glyph outlines for an instance. In addition, variation deltas are not provided for these values. If an application requires a bounding rectangle that encompasses the glyphs for a non-default instance of the font, the derived glyph outlines for the instance should be processed to determine a bounding rectangle.
