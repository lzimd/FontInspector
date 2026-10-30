---
title: "VVAR — Vertical Metrics Variations Table"
description: "VVAR — Vertical Metrics Variations Table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-30T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/vvar.md"
last-modified: "2026-09-17T18:19:03Z"
---

<a id="anchor-vvar-vvar-vertical-metrics-variations-table"></a>

# VVAR — Vertical Metrics Variations Table

The VVAR table is used in variable fonts to provide variations for vertical glyph metric values. This can be used to provide variation data for advance heights in the ['vmtx'](vmtx.md) table. In fonts with TrueType outlines, it can also be used to provide variation data for top and bottom side bearings obtained from the 'vmtx' table and glyph bounding boxes. In addition, it can also be used in fonts that have CFF2 outlines to provide vertical-origin variation data.

For a general overview of OpenType Font Variations and terminology related to variations, see the chapter, [OpenType Font Variations Overview](otvaroverview.md).

In a font with TrueType outlines, the rasterizer will generate “phantom” points that represent left, right, top and bottom side bearings. (See the chapter [Instructing TrueType Glyphs](tt_instructing_glyphs.md#anchor-tt_instructing_glyphs-phantom-points) for more background on phantom points.) In a TrueType variable font, the [glyph variations ('gvar')](gvar.md) table will include variation data for the phantom points of each glyph, allowing glyph metrics to be interpolated for different variation instances as part of deriving the interpolated glyph outlines. For this reason, the VVAR table is not required in variable fonts that have TrueType outlines. For text-layout operations that require glyph metrics but not actual glyph outlines, however, there can be significant performance benefits by being able to obtain adjusted glyph metrics for an instance without needing to interpolate glyph outlines. For this reason, it is recommended that a VVAR table be included in variable fonts that have TrueType outlines and that support vertical layout.

The CFF2 rasterizer does not generate phantom points as in the TrueType rasterizer. For this reason, a VVAR table is required to handle any variation in vertical glyph metrics in a variable font with CFF 2 outlines.

The format and processing of the VVAR table is analogous to the [horizontal metrics variations (HVAR)](hvar.md) table.

<a id="anchor-vvar-related-and-co-requisite-tables"></a>

## Related and Co-Requisite Tables

The VVAR table is used only in variable fonts that support vertical layout. It must be used in combination with a [vertical metrics ('vmtx')](vmtx.md) table, and also in combination with a [font variations ('fvar')](fvar.md) table, and other required or optional tables used in variable fonts. See [Variation Data Tables and Miscellaneous Requirements](otvaroverview.md#anchor-otvaroverview-variation-data-tables-and-miscellaneous-requirements) in the OpenType Font Variations Overview chapter for general information.

For variable fonts that have TrueType outlines and that support vertical layout, the VVAR table is optional but recommended. For variable fonts that have CFF2 outlines and that support vertical layout, the VVAR table is required if there is any variation in glyph advance heights across the variation space.

> *Note:* The VDMX table is not used in variable fonts.

<a id="anchor-vvar-table-formats"></a>

## Table Formats

The vertical metrics variations table has the following format.

*Vertical metrics variations table:*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-vvar-majorVersion"></a>uint16 | majorVersion | Major version number of the vertical metrics variations table — set to 1. |
| <a id="anchor-vvar-minorVersion"></a>uint16 | minorVersion | Minor version number of the vertical metrics variations table — set to 0. |
| <a id="anchor-vvar-itemVariationStoreOffset"></a>Offset32 | itemVariationStoreOffset | Offset in bytes from the start of this table to the item variation store table. |
| <a id="anchor-vvar-advanceHeightMappingOffset"></a>Offset32 | advanceHeightMappingOffset | Offset in bytes from the start of this table to the delta-set index mapping for advance heights (may be NULL). |
| <a id="anchor-vvar-tsbMappingOffset"></a>Offset32 | tsbMappingOffset | Offset in bytes from the start of this table to the delta-set index mapping for top side bearings (may be NULL). |
| <a id="anchor-vvar-bsbMappingOffset"></a>Offset32 | bsbMappingOffset | Offset in bytes from the start of this table to the delta-set index mapping for bottom side bearings (may be NULL). |
| <a id="anchor-vvar-vOrgMappingOffset"></a>Offset32 | vOrgMappingOffset | Offset in bytes from the start of this table to the delta-set index mapping for Y coordinates of vertical origins (may be NULL). |

The item variation store table is documented in the chapter, [OpenType Font Variations Common Table Formats](otvarcommonformats.md).

Mapping subtables are represented using a DeltaSetIndexMap table; see [Associating Target Items to Variation Data](otvarcommonformats.md#anchor-otvarcommonformats-associating-target-items-to-variation-data) in the Common Table Formats chapter for the definition of this table. In the VVAR table, only format 0 of the DeltaSetIndexMap is used. Mapping subtables are optional. If a given mapping subtable is not provided, the offset is set to NULL.

Variation data for advance heights is required. A delta-set index mapping subtable for advance heights can be provided, but is optional. If a mapping table is not provided, glyph indices are used as implicit delta-set indices, as in the HVAR table.

Variation data for side bearings are optional. If included, mapping subtables are required to provide the delta-set index for each glyph.

Mappings and variation data for vertical origins are not used in fonts with TrueType outlines, but can be included in variable fonts with CFF 2 outlines if there is variability in the Y coordinates of glyph vertical origins, the default values of which are recorded in the VORG table. A mapping subtable is required for vertical-origin variation data.
