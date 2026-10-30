---
title: "EBSC — Embedded Bitmap Scaling Table"
description: "EBSC - Embedded Bitmap Scaling Table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-01-21T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/ebsc.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-ebsc-ebsc-embedded-bitmap-scaling-table"></a>

# EBSC — Embedded Bitmap Scaling Table

The EBSC table provides a mechanism for describing embedded bitmaps which are created by scaling other embedded bitmaps. While this is the sort of thing that outline font technologies were invented to avoid, there are cases (small sizes of Kanji, for example) where scaling a bitmap produces more legible glyphs than scan-converting an outline. For this reason, the EBSC table allows a font to define a bitmap strike as a scaled version of another strike.

The EBSC table is used together with the [EBDT](ebdt.md) table, which provides embedded monochrome or grayscale bitmap data, and the [EBLC](eblc.md) table, which provides embedded bitmap locators.

<a id="anchor-ebsc-formats"></a>

## Formats

The EBSC table has the following format:

*EBSC table*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-ebsc-majorVersion"></a>uint16 | majorVersion | Major version of the EBSC table, = 2. |
| <a id="anchor-ebsc-minorVersion"></a>uint16 | minorVersion | Minor version of the EBSC table, = 0. |
| <a id="anchor-ebsc-numSizes"></a>uint32 | numSizes |  |
| BitmapScale | strikes\[numSizes\] | Array of BitmapScale records, one for each strike. |

> *Note:* The first version of the EBSC table is 2.0.

The numSizes field indicates the number of BitmapScale records in the array. Each strike is defined by one BitmapScale record.

<a id="anchor-ebsc-bitmapScaleTable"></a>

*BitmapScale record*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-ebsc-hori"></a>SbitLineMetrics | hori | line metrics |
| <a id="anchor-ebsc-vert"></a>SbitLineMetrics | vert | line metrics |
| <a id="anchor-ebsc-ppemX"></a>uint8 | ppemX | target horizontal pixels per Em |
| <a id="anchor-ebsc-ppemY"></a>uint8 | ppemY | target vertical pixels per Em |
| <a id="anchor-ebsc-substitutePpemX"></a>uint8 | substitutePpemX | use bitmaps of this size |
| <a id="anchor-ebsc-substitutePpemY"></a>uint8 | substitutePpemY | use bitmaps of this size |

The line metrics have the same format and meaning as those in the [BitmapSize record](eblc.md#anchor-eblc-bitmapsize-record) in the EBLC table, and refer to font wide metrics after scaling. The ppemX and ppemY values describe the size of the font after scaling. The substitutePpemX and substitutePpemY values describe the size of a strike that exists as an sbit in the EBLC and EBDT, and that will be scaled up or down to generate the new strike.

Scaling in the x direction is independent of scaling in the y direction, and their scaling values may differ. A square aspect-ratio strike could be scaled to a non-square aspect ratio. Glyph metrics are scaled by the same factor as the pixels per Em (in the appropriate direction), and are rounded to the nearest integer pixel.
