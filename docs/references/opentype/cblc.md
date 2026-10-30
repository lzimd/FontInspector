---
title: "CBLC — Color Bitmap Location Table"
description: "CBLC - Color Bitmap Location Table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-30T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/cblc.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-cblc-cblc-color-bitmap-location-table"></a>

# CBLC — Color Bitmap Location Table

The CBLC table provides embedded bitmap locators. It is used together with the [CBDT](cbdt.md) table, which provides embedded, color bitmap glyph data. The formats of these two tables are downward compatible extensions of the [EBDT](ebdt.md) and [EBLC](eblc.md) tables used for embedded monochrome and grayscale bitmaps.

The CBLC table begins with a header containing the table version and number of strikes. An OpenType font may have one or more strikes embedded in the 'CBDT' table.

*CblcHeader*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cblc-majorVersion"></a>uint16 | majorVersion | Major version of the CBLC table, = 3. |
| <a id="anchor-cblc-minorVersion"></a>uint16 | minorVersion | Minor version of the CBLC table, = 0. |
| <a id="anchor-cblc-numSizes"></a>uint32 | numSizes | Number of BitmapSize records. |
| BitmapSize | bitmapSizes\[numSizes\] | BitmapSize records array. |

Note that the first version of the CBLC table is 3.0.

<a id="anchor-cblc-bitmapsize-record"></a>

Each strike is defined by a BitmapSize record.

*BitmapSize record*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cblc-indexSubTableArrayOffset"></a>Offset32 | indexSubtableListOffset | Offset to index subtable from beginning of CBLC. |
| <a id="anchor-cblc-indexTablesSize"></a>uint32 | indexSubtableListSize | Number of bytes in corresponding index subtables and array. |
| <a id="anchor-cblc-numberofIndexSubTables"></a>uint32 | numberOfIndexSubtables | There is an index subtable for each range or format change. |
| <a id="anchor-cblc-colorRef"></a>uint32 | colorRef | Not used; set to 0. |
| <a id="anchor-cblc-Hori"></a>SbitLineMetrics | hori | Line metrics for text rendered horizontally. |
| <a id="anchor-cblc-Vert"></a>SbitLineMetrics | vert | Line metrics for text rendered vertically. |
| <a id="anchor-cblc-startGlyphIndex"></a>uint16 | startGlyphIndex | Lowest glyph index for this size. |
| <a id="anchor-cblc-endGlyphIndex"></a>uint16 | endGlyphIndex | Highest glyph index for this size. |
| <a id="anchor-cblc-ppemX"></a>uint8 | ppemX | Horizontal pixels per em. |
| <a id="anchor-cblc-ppemY"></a>uint8 | ppemY | Vertical pixels per em. |
| <a id="anchor-cblc-bitDepth"></a>uint8 | bitDepth | In addition to already defined bitDepth values 1, 2, 4, and 8 used for monochrome and grayscale bitmaps, the value of 32 is used to identify color bitmaps with 8 bit per channel BGRA pixel data. |
| <a id="anchor-cblc-flags"></a>int8 | flags | Vertical or horizontal (see the [Bitmap flags](eblc.md#anchor-eblc-bitmapFlags) section of the EBLC table chapter). |

The indexSubtableListOffset is the offset from the beginning of the CBLC table to an [IndexSubtableList](eblc.md#anchor-eblc-indexsubtablelist). The indexSubtableListSize is the total size in bytes of the IndexSubtableList data, including the array of IndexSubtables. Each strike has an IndexSubtableList to support various formats and discontiguous ranges of bitmaps. Each IndexSubtable provides the locations of the bitmap data for one or more glyphs within the CBDT table, and may optionally provide glyph metrics to use for that set of glyphs.

Remaining details regarding the structure of the CBDT table are identical to those defined for the [EBLC](eblc.md) table.
