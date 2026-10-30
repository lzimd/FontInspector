---
title: "CBDT — Color Bitmap Data Table"
description: "CBDT - Color Bitmap Data Table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-31T00:00:00Z"
updated_at: "2024-05-31T20:48:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/a22b82065976c7f3aa7d96800eac1c0fbe12d7c6/typographydocs/opentype/spec/cbdt.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-cbdt-cbdt-color-bitmap-data-table"></a>

# CBDT — Color Bitmap Data Table

<a id="anchor-cbdt-tableStructure"></a>

The CBDT table is used to embed color bitmap glyph data. It is used together with the [CBLC](cblc.md) table, which provides embedded bitmap locators. The formats of these two tables are downward compatible extensions of the [EBDT](ebdt.md) and [EBLC](eblc.md) tables used for embedded monochrome and grayscale bitmaps.

<a id="anchor-cbdt-table-structure"></a>

## Table structure

The CBDT table begins with a header containing simply the table version number.

*CbdtHeader*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cbdt-majorVersion"></a>uint16 | majorVersion | Major version of the CBDT table, = 3. |
| <a id="anchor-cbdt-minorVersion"></a>uint16 | minorVersion | Minor version of the CBDT table, = 0. |

Note that the first version of the CBDT table is 3.0.

The rest of the CBDT table is a collection of bitmap data. The data can be presented in three possible formats, indicated by information in the CBLC table. Some of the formats contain metric information plus image data, and other formats contain only the image data. Long word alignment is not required for these subtables; byte alignment is sufficient.

<a id="anchor-cbdt-uncompressed-color-bitmaps"></a>

## Uncompressed color bitmaps

The value 32 may be used in the bitDepth field of [BitmapSize](cblc.md#anchor-cblc-bitmapsize-record) records within the CBLC table to identify color bitmaps with 8-bit blue/green/red/alpha (“BGRA”) channels per pixel, encoded in that order for each pixel. The color channels represent pre-multiplied color and must be encoded colors in the sRGB colorspace, as specified in [IEC 61966-2-1:1999/Amd 1:2003](https://webstore.iec.ch/publication/6168). For example, the color “full-green with half translucency” is encoded as \\x00\\x80\\x00\\x80 (BGR values are pre-multiplied), and not \\x00\\xFF\\x00\\x80.

All bitmap image data formats defined in the EBDT / EBLC tables are valid for use with the CBDT / CBLC tables.

<a id="anchor-cbdt-compressed-color-bitmaps"></a>

## Compressed color bitmaps

Images for each individual glyph may be stored as straight PNG data, as specified in ISO/IEC 15948. Only the following chunks are allowed in such PNG data: IHDR, PLTE, tRNS, sRGB, IDAT, and IEND. If other chunks are present, the behavior is undefined. The image data must be in the sRGB colorspace, regardless of color information that could be present in other chunks in the PNG data. The individual images must have the same size as expected by the table in the bitmap metrics.

<a id="anchor-cbdt-glyph-metrics"></a>

## Glyph metrics

There are also two different formats for glyph metrics: big glyph metrics and small glyph metrics. Big glyph metrics define metrics information for both horizontal and vertical layouts. This is important in fonts (such as Kanji) where both types of layout may be used. Small glyph metrics define metrics information for one layout direction only. Which direction applies, horizontal or vertical, is determined by the flags field of BitmapSize records within the CBLC table.

<a id="anchor-cbdt-bigGlyphMetrics"></a>

*BigGlyphMetrics record*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cbdt-height_bgm"></a>uint8 | height | Number of rows in the bitmap. |
| <a id="anchor-cbdt-width_bgm"></a>uint8 | width | Number of columns in the bitmap. |
| <a id="anchor-cbdt-horiBearingX_bgm"></a>int8 | horiBearingX | Distance in pixels from the horizontal origin to the left edge of the bitmap. |
| <a id="anchor-cbdt-horiBearingY_bgm"></a>int8 | horiBearingY | Distance in pixels from the horizontal origin to the top edge of the bitmap. |
| <a id="anchor-cbdt-horiAdvance_bgm"></a>uint8 | horiAdvance | Horizontal advance width in pixels. |
| <a id="anchor-cbdt-vertBearingX_bgm"></a>int8 | vertBearingX | Distance in pixels from the vertical origin to the left edge of the bitmap. |
| <a id="anchor-cbdt-vertBearingY_bgm"></a>int8 | vertBearingY | Distance in pixels from the vertical origin to the top edge of the bitmap. |
| <a id="anchor-cbdt-vertAdvance_bgm"></a>uint8 | vertAdvance | Vertical advance width in pixels. |

<a id="anchor-cbdt-smallGlyphMetrics"></a>

*SmallGlyphMetrics record*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cbdt-height_sgm"></a>uint8 | height | Number of rows in the bitmap. |
| <a id="anchor-cbdt-width_sgm"></a>uint8 | width | Number of columns in the bitmap. |
| <a id="anchor-cbdt-bearingX_sgm"></a>int8 | bearingX | Distance in pixels from the horizontal origin to the left edge of the bitmap (for horizontal text); or distance in pixels from the vertical origin to the top edge of the bitmap (for vertical text). |
| <a id="anchor-cbdt-bearingY_sgm"></a>int8 | bearingY | Distance in pixels from the horizontal origin to the top edge of the bitmap (for horizontal text); or distance in pixels from the vertical origin to the left edge of the bitmap (for vertical text). |
| <a id="anchor-cbdt-advance_sgm"></a>uint8 | advance | Horizontal or vertical advance width in pixels. |

<a id="anchor-cbdt-glyph-bitmap-data-formats"></a>

## Glyph bitmap data formats

In addition to nine different formats already defined for glyph bitmap data in the EBDT table, there are three additional formats for use in the CBDT table, described below.

<a id="anchor-cbdt-format-17-small-metrics-png-image-data"></a>

### Format 17: small metrics, PNG image data

*GlyphBitmapFormat17 table*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cbdt-glyphMetrics_17"></a>smallGlyphMetrics | glyphMetrics | Metrics information for the glyph |
| <a id="anchor-cbdt-dataLen_17"></a>uint32 | dataLen | Length of data in bytes |
| <a id="anchor-cbdt-data_17"></a>uint8 | data\[dataLen\] | Raw PNG data |

<a id="anchor-cbdt-format-18-big-metrics-png-image-data"></a>

### Format 18: big metrics, PNG image data

*GlyphBitmapFormat18 table*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cbdt-glyphMetrics_18"></a>bigGlyphMetrics | glyphMetrics | Metrics information for the glyph |
| <a id="anchor-cbdt-dataLen_18"></a>uint32 | dataLen | Length of data in bytes |
| <a id="anchor-cbdt-data_18"></a>uint8 | data\[dataLen\] | Raw PNG data |

<a id="anchor-cbdt-format-19-metrics-in-cblc-table-png-image-data"></a>

### Format 19: metrics in CBLC table, PNG image data

*GlyphBitmapFormat19 table*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cbdt-dataLen_19"></a>uint32 | dataLen | Length of data in bytes |
| <a id="anchor-cbdt-data_19"></a>uint8 | data\[dataLen\] | Raw PNG data |

<a id="anchor-cbdt-scaling-behavior"></a>

## Scaling behavior

Applications using these glyphs may need to scale them to fit the raster size available for display. How this scaling takes place is application dependent. It is recommended that where possible the application downscale using the closest sized bitmap that is larger than the desired end raster size.
