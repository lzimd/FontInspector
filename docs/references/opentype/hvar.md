---
title: "HVAR — Horizontal Metrics Variations Table"
description: "HVAR — Horizontal Metrics Variations Table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2022-10-20T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/hvar.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-hvar-hvar-horizontal-metrics-variations-table"></a>

# HVAR — Horizontal Metrics Variations Table

The HVAR table is used in variable fonts to provide variations for horizontal glyph metrics values. This can be used to provide variation data for advance widths in the ['hmtx'](hmtx.md) table. In fonts with TrueType outlines, it can also be used to provide variation data for left and right side bearings obtained from the 'hmtx' table and glyph bounding boxes.

For a general overview of OpenType Font Variations and terminology related to variations, see the chapter, [OpenType Font Variations Overview](otvaroverview.md).

In a font with TrueType outlines, the rasterizer will generate “phantom” points that represent left, right, top and bottom side bearings. (See the chapter [Instructing TrueType Glyphs](tt_instructing_glyphs.md#anchor-tt_instructing_glyphs-phantom-points) for more background on phantom points.) In a TrueType variable font, the [glyph variations ('gvar')](gvar.md) table will include variation data for the phantom points of each glyph, allowing glyph metrics to be interpolated for different variation instances as part of deriving the interpolated glyph outlines. For this reason, the HVAR table is not required in variable fonts that have TrueType outlines. For text-layout operations that require glyph metrics but not actual glyph outlines, however, there can be significant performance benefits by being able to obtain adjusted glyph metrics for an instance without needing to interpolate glyph outlines. For this reason, it is recommended that an HVAR table be included in variable fonts that have TrueType outlines.

The CFF2 rasterizer does not generate phantom points as in the TrueType rasterizer. For this reason, an HVAR table is required to handle any variation in horizontal glyph metrics in a variable font with CFF2 outlines.

Take note that, in a variable font with TrueType outlines, the left side bearing for each glyph must equal xMin, and bit 1 in the flags field of the 'head' table must be set.

The HVAR table contains an *item variation store* table to represent variation data. The item variation store and constituent formats are described in the chapter, [OpenType Font Variations Common Table Formats](otvarcommonformats.md). The item variation store is also used in the [VVAR](vvar.md), [GDEF](gdef.md) and certain other tables, but is different from the formats for variation data used in the ['cvar'](cvar.md) or ['gvar'](gvar.md) tables.

The item variation store format uses *delta-set indices* to reference variation delta data for particular target, font-data items to which they are applied, such as the advance width of a particular glyph. Data external to the item variation store identifies the delta-set index to be used for each given target item. Within the HVAR table, glyph IDs can be used as implicit indices for advance width variations, or an optional delta-set index mapping table can be used that explicitly provides delta-set indices for advance widths to be associated with each glyph ID.

An advance width mapping subtable adds additional data within the HVAR table, but it also makes it possible to use a more compact representation of the data in the item variation store. For example, if multiple glyphs have the same advance widths, the mapping subtable allows all of them to reference a single delta set within the store. Additional optimizations within the item variation store are possible. See the Common Table Formats chapter for more discussion about size optimization. In general, inclusion of an advance width mapping subtable is recommended.

Optional mapping subtables can also be used to provide delta-set indices for glyph side bearings. In variable fonts with TrueType outlines, variation data for side bearings is recommended. If variation data for side bearings is provided, it should include data for both left and right side bearings, and mapping subtables for left and right side bearings must also be included.

<a id="anchor-hvar-related-and-co-requisite-tables"></a>

## Related and Co-Requisite Tables

The HVAR table is used only in variable fonts. It must be used in combination with a [horizontal metrics ('hmtx')](hmtx.md) table, and also in combination with a [font variations ('fvar')](fvar.md) table, and other required or optional tables used in variable fonts. See [Variation data tables and miscellaneous requirements](otvaroverview.md#anchor-otvaroverview-variation-data-tables-and-miscellaneous-requirements) in the OpenType Font Variations Overview chapter for general information.

For variable fonts that have TrueType outlines, the HVAR table is optional but recommended. For variable fonts that have CFF 2 outlines, the HVAR table is required if there is any variation in glyph advance widths across the variation space.

> *Note:* The 'hdmx' table is not used in variable fonts.

<a id="anchor-hvar-table-formats"></a>

## Table Formats

The horizontal metrics variations table has the following format.

*Horizontal metrics variations table:*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-hvar-majorVersion"></a>uint16 | majorVersion | Major version number of the horizontal metrics variations table — set to 1. |
| <a id="anchor-hvar-minorVersion"></a>uint16 | minorVersion | Minor version number of the horizontal metrics variations table — set to 0. |
| <a id="anchor-hvar-itemVariationStoreOffset"></a>Offset32 | itemVariationStoreOffset | Offset in bytes from the start of this table to the item variation store table. |
| <a id="anchor-hvar-advanceWidthMappingOffset"></a>Offset32 | advanceWidthMappingOffset | Offset in bytes from the start of this table to the delta-set index mapping for advance widths (may be NULL). |
| <a id="anchor-hvar-lsbMappingOffset"></a>Offset32 | lsbMappingOffset | Offset in bytes from the start of this table to the delta-set index mapping for left side bearings (may be NULL). |
| <a id="anchor-hvar-rsbMappingOffset"></a>Offset32 | rsbMappingOffset | Offset in bytes from the start of this table to the delta-set index mapping for right side bearings (may be NULL). |

The item variation store table is documented in the chapter, [OpenType Font Variations Common Table Formats](otvarcommonformats.md#anchor-otvarcommonformats-item-variation-store).

Mapping subtables are represented using a DeltaSetIndexMap table; see [Associating Target Items to Variation Data](otvarcommonformats.md#anchor-otvarcommonformats-associating-target-items-to-variation-data) in the Common Table Formats chapter for the definition of this table. In the HVAR table, only format 0 of the DeltaSetIndexMap is used. Mapping subtables are optional. If a given mapping subtable is not provided, the offset is set to NULL.

Variation data for advance widths is required. A delta-set index mapping subtable for advance widths can be provided, but is optional. If a mapping subtable is not provided, glyph indices are used as implicit delta-set indices. To access the delta set for the advance of given glyph, the delta-set outer-level index is zero, and the glyph ID is used as the inner-level index.

Variation data for side bearings are optional. If included, mapping tables are required to provide the delta-set index for each glyph.

<a id="anchor-hvar-processing"></a>

## Processing

When performing text layout using a particular variation instance of a variable font, the application will need to obtain adjusted glyph metrics for that instance. The application obtains default values from the 'hmtx' and 'glyf' tables, and uses the HVAR table to obtain interpolated adjustment values that are applied to the defaults.

Delta-set indices are obtained based on the glyph ID. If there is no delta-set index mapping subtable for advance widths (advanceWidthMappingOffset is NULL), then glyph IDs implicitly provide the indices: for a given glyph ID, the delta-set outer-level index is zero, and the glyph ID is the delta-set inner-level index. If a delta-set index mapping table is provided, glyph IDs are used to lookup a mapping entry, which provides the outer- and inner-level delta-set indices in a packed format. See [Associating Target Items to Variation Data](otvarcommonformats.md#anchor-otvarcommonformats-associating-target-items-to-variation-data) for details.

The delta-set indices are used to reference a delta set for the target advance width or side bearing within the item variation store. The two-level organization of data within the item variation store is described in the chapter [OpenType Font Variations Common Table Formats](otvarcommonformats.md). Each delta set includes different deltas that apply to variation instances falling within different regions of the variation space. The process by which the deltas are processed to derive an interpolated value for a given target item is described in the chapter, [OpenType Font Variations Overview](otvaroverview.md).
