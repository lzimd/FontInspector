---
title: "sbix — Standard Bitmap Graphics Table"
description: "sbix - Standard Bitmap Graphics Table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-30T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/sbix.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-sbix-sbix-standard-bitmap-graphics-table"></a>

# sbix — Standard Bitmap Graphics Table

This table provides access to bitmap data in a standard graphics format, such as PNG, JPEG or TIFF.

The 'sbix' table has functionality somewhat similar to the EBDT table in that both provide bitmap data for glyph presentation. They are different in three important respects, however. First, whereas the EBDT table supports only black/white or grayscale bitmaps, the 'sbix' table supports color bitmaps. Secondly, whereas the EBDT table uses formats specific to the OpenType specification, the 'sbix' table uses standard bitmap graphics formats that are in common use. Thirdly, whereas the EBDT table must be used in conjunction with other tables (EBLC and EBSC) for processing the bitmap data, the 'sbix' table contains complete data required for processing bitmaps.

A font that includes an 'sbix' table may also include outline glyph data in a 'glyf' or 'CFF ' table. An 'sbix' table can provide bitmap data for all glyph IDs, or for only a subset of glyph IDs. A font can also include different bitmap data for different sizes (“strikes”), and the glyph coverage for one size can be different from that for another size.

<a id="anchor-sbix-header"></a>

## Header

The 'sbix' table begins with a header:

*sbixHeader*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-sbix-version"></a>uint16 | version | Table version number — set to 1 |
| <a id="anchor-sbix-flags"></a>uint16 | flags | Bit 0: Set to 1.<br> Bit 1: Draw outlines.<br> Bits 2 to 15: reserved (set to 0). |
| <a id="anchor-sbix-numStrikes"></a>uint32 | numStrikes | Number of bitmap strikes. |
| <a id="anchor-sbix-strikeOffsets"></a>Offset32 | strikeOffsets\[numStrikes\] | Offsets from the beginning of the 'sbix' table to data for each individual bitmap strike. |

For historical reasons, bit 0 of the flags field should always be set to 1.

If bit 1 of the flags field is clear, then the application is instructed to draw only the bitmaps for each glyph supported in the 'sbix' table. If bit 1 is set, then the application is instructed to draw the bitmap and the outline, in that order (that is, with the outline overlaid on top of the bitmap). If the 'sbix' table does not contain bitmap data for a glyph, then the outline is always drawn, regardless of the state of bit 1.

> *Note:* Application support for bit 1 of the flags field is optional. To ensure the best compatibility, set this bit to 0.

<a id="anchor-sbix-strikes"></a>

## Strikes

Each strike includes a header and the glyph bitmap data. The header has the following format:

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-sbix-ppem"></a>uint16 | ppem | The PPEM size for which this strike was designed. |
| <a id="anchor-sbix-ppi"></a>uint16 | ppi | The device pixel density (in PPI) for which this strike was designed. (E.g., 96 PPI, 192 PPI.) |
| <a id="anchor-sbix-glyphDataOffsets"></a>Offset32 | glyphDataOffsets\[numGlyphs+1\] | Offset from the beginning of the strike data header to bitmap data for an individual glyph ID. |

The glyphDataOffset array includes offsets for every glyph ID, plus one extra. The number of glyphs is determined from the 'maxp' table. The length of the bitmap data for each glyph is variable, and can be determined from the difference between two consecutive offsets. Hence, the length of data for glyph N is glyphDataOffset\[N+1\] - glyphDataOffset\[N\]. If this is zero, there is no bitmap data for that glyph in this strike. There is one extra offset in the array in order to provide the length of data for the last glyph.

> *Note:* The length of data for non-printing glyphs, such as space, should always be zero.

A strike does not need to include data for every glyph, and does not need to include data for the same set of glyphs as other strikes. If the application is using bitmap data to draw text and there is bitmap data for a glyph in *any* strike, then the glyph must be drawn using a bitmap from *some* strike. If the exact size is not available, implementations may choose a bitmap based on the closest available larger size, or the closest available integer-multiple larger size, or on some other basis. The only cases in which a glyph is not drawn using a bitmap are if the application has not requested that text be drawn using bitmap data or if there is no bitmap data for the glyph in any strike.

Each strike targets a specific PPEM size and device pixel density (PPI). Thus, a font can contain two strikes for the same PPEM but different pixel densities, or two strikes for the same pixel density but different PPEMs. Note that some platforms might not support selection of strikes for particular pixel densities.

<a id="anchor-sbix-glyph-data"></a>

## Glyph data

The data for each glyph includes a header and the actual, embedded graphic data, with the following format:

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-sbix-originOffsetX"></a>int16 | originOffsetX | The horizontal (x-axis) position of the left edge of the bitmap graphic in relation to the glyph design space origin. |
| <a id="anchor-sbix-originOffsetY"></a>int16 | originOffsetY | The vertical (y-axis) position of the bottom edge of the bitmap graphic in relation to the glyph design space origin. |
| <a id="anchor-sbix-graphicType"></a>Tag | graphicType | Indicates the format of the embedded graphic data: one of 'jpg ', 'png ' or 'tiff', or the special format 'dupe'. |
| <a id="anchor-sbix-data"></a>uint8 | data\[\] | The actual embedded graphic data. The total length is inferred from sequential entries in the glyphDataOffsets array and the fixed size (8 bytes) of the preceding fields. |

The originOffsetX and originOffsetY values give the placement of the bitmap graphic in relation to the standard coordinate system of the glyph design space. For example, if originOffsetX equals 20, the left edge of the bitmap is placed 20 units to the right of the origin; if originOffsetY equals -30, then the bottom edge of the graphic is 30 units below the origin.

When placing the graphic within the line of text, the placement depends upon whether there are contours in the ['glyf'](glyf.md) table for the current glyph ID:

- If there is no glyph contour, the glyph design space origin for the graphic is placed at the starting drawing position for this glyph. The lsb value for the current glyph ID from the 'hmtx' table has no effect.
- If there is a glyph contour, the glyph design space origin for the graphic is placed at the lower left corner of the glyph bounding box (xMin, yMin).

The graphicType field indicates the format of the embedded graphic data. Three standard formats are supported: JPEG, PNG and TIFF; these are indicated using tag values 'jpg ', 'png ' and 'tiff', respectively.

The special graphicType of 'dupe' indicates that the data field contains a uint16, big-endian glyph ID. The bitmap data for the indicated glyph must be used for the current glyph.

> *Note:* Apple’s specification for TrueType fonts allows for a graphicType tag value of 'pdf ' or 'mask'. These values are not supported in the OpenType specification, however.

<a id="anchor-sbix-table-dependencies"></a>

## Table dependencies

The glyph count is derived from the ['maxp' table](maxp.md). Advance and side-bearing glyph metrics are stored in the ['hmtx' table](hmtx.md) for horizontal layout, and the ['vmtx' table](vmtx.md) for vertical layout.
