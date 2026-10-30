---
title: "MVAR — Metrics Variations Table"
description: "MVAR — Metrics Variations Table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2022-10-20T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/mvar.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-mvar-mvar-metrics-variations-table"></a>

# MVAR — Metrics Variations Table

The metrics variations table is used in variable fonts to provide variations for font-wide metric values found in the OS/2 table and other font tables. For a general overview of OpenType Font Variation and terminology related to variations, see the chapter, [OpenType Font Variations Overview](otvaroverview.md).

The metrics variations table contains an *item variation store* structure to represent variation data. The item variation store and constituent formats are described in the chapter, [OpenType Font Variations Common Table Formats](otvarcommonformats.md). The item variation store is also used in the [HVAR](hvar.md) and [GDEF](gdef.md) tables, but is different from the formats for variation data used in the ['cvar'](cvar.md) or ['gvar'](gvar.md) tables.

The item variation store format uses *delta-set indices* to reference variation delta data for particular target font-data items to which they are applied. Data external to the item variation store identifies the delta-set index to be used for each given target item. Within the MVAR table, an array of *value tag* records identifies a set of target items, and provides the delta-set index used for each. The target items are identified by four-byte tags, with a given tag representing some font-wide value found in another table. For example, the tag 'hasc' represents the OS/2.sTypoAscender value. More details on tags are provided below.

The item variation store format uses a two-level organization for variation data: a store can have multiple *item variation data* subtables, and each subtable has multiple delta-set rows. A delta-set index is a two-part index: an outer index that selects a particular item variation data subtable, and an inner index that selects a particular delta-set row within that subtable. A value record specifies both the outer and inner portions of the delta-set index.

> *Note:* Apple platforms allow for use of a font metrics ('fmtx') table to specify various font-wide metric values by reference to the X or Y coordinates of contour points for a specified “magic” glyph. OpenType Font Variations does not use the font metrics table.

The metrics variations table must be used in combination with a [font variations ('fvar')](fvar.md) table and other required or optional tables used in variable fonts. See [Variation Data Tables and Miscellaneous Requirements](otvaroverview.md#anchor-otvaroverview-variation-data-tables-and-miscellaneous-requirements) in the OpenType Font Variations Overview chapter for additional details.

<a id="anchor-mvar-table-formats"></a>

## Table Formats

The metrics variations table has the following format.

<a id="anchor-mvar-mvarTable"></a>

*Metrics variations table:*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-mvar-majorVersion"></a>uint16 | majorVersion | Major version number of the metrics variations table — set to 1. |
| <a id="anchor-mvar-minorVersion"></a>uint16 | minorVersion | Minor version number of the metrics variations table — set to 0. |
| <a id="anchor-mvar-reserved"></a>uint16 | (reserved) | Not used; set to 0. |
| <a id="anchor-mvar-valueRecordSize"></a>uint16 | valueRecordSize | The size in bytes of each value record — must be greater than zero. |
| <a id="anchor-mvar-valueRecordCount"></a>uint16 | valueRecordCount | The number of value records — may be zero. |
| <a id="anchor-mvar-itemVarStoreOffset"></a>Offset16 | itemVariationStoreOffset | Offset in bytes from the start of this table to the item variation store table. If valueRecordCount is zero, set to zero; if valueRecordCount is greater than zero, must be greater than zero. |
| <a id="anchor-mvar-valueRecords"></a>ValueRecord | valueRecords\[valueRecordCount\] | Array of value records that identify target items and the associated delta-set index for each. The valueTag records must be in binary order of their valueTag field. |

The valueRecordSize field indicates the size of each value record. Future, minor version updates of the MVAR table may define compatible extensions to the value record format with additional fields. Implementations must use the valueRecordSize field to determine the start of each record.

The valueRecords array is an array of value records that identify the target, font-wide measures for which variation adjustment data is provided (target items), and outer and inner delta-set indices for each item into the item variation store data.

<a id="anchor-mvar-valueRec"></a>

*ValueRecord:*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-mvar-valueTag"></a>Tag | valueTag | Four-byte tag identifying a font-wide measure. |
| <a id="anchor-mvar-deltaSetOuterIndex"></a>uint16 | deltaSetOuterIndex | A delta-set outer index — used to select an item variation data subtable within the item variation store. |
| <a id="anchor-mvar-deltaSetInnerIndex"></a>uint16 | deltaSetInnerIndex | A delta-set inner index — used to select a delta-set row within an item variation data subtable. |

The value records must be given in binary order of the valueTag values. Each tag identifies a font-wide measure found in some other font table. For example, if a value record has a value tag of 'hasc', this corresponds to the OS/2.sTypoAscender field. Details on the tags used within the MVAR table are provided below.

<a id="anchor-mvar-processing"></a>

## Processing

When reading a value within a variable font, such as the OS/2.sCapHeight value (the target item), the value tags array in the metrics variations table is scanned to find the tag that corresponds to that target item. Records in the array are stored in binary order of values in the valueTag fields. If the tag does not occur in the tag array, then the item is constant across the font’s variation space. If the tag does occur, however, then the delta-set index is used to reference a set of deltas within the item variation store. The two-level organization of data within the item variation store is described in the chapter [OpenType Font Variations Common Table Formats](otvarcommonformats.md). Each delta set includes different deltas that apply to variation instances falling within different regions of the variation space. The process by which the deltas are processed to derive an interpolated value for a given target item is described in the chapter, [OpenType Font Variations Overview](otvaroverview.md).

<a id="anchor-mvar-value-tags"></a>

## Value Tags

Four-byte tags are used to represent particular metric or other values. For example, the tag 'hasc' (horizontal ascent) is used to represent the OS/2.sTypoAscender value. Tags are defined for various values found in the [OS/2 and Windows metrics (OS/2)](os2.md) table, the [horizontal header ('hhea')](hhea.md) table, the [grid-fitting and scan-conversion ('gasp')](gasp.md) table, the [PostScript ('post')](post.md) table, and the [vertical metrics header ('vhea')](vhea.md) table.

> *Note:* The OS/2.usWeightClass, OS/2.usWidthClass and post.italicAngle values are not supported by variation data in the MVAR table. This is because values for these three fields correspond directly to input axis values for the 'wght', 'wdth' and 'slnt' variation axes. See the discussion of these axes in the [OpenType Design-Variation Axis Tag Registry](dvaraxisreg.md) for details on the relationship between these fields and the corresponding design axes.

Tags in the metrics variations table are case sensitive. Tags defined in this table use only lowercase letters or digits.

Tags that are used in a font’s metrics variations table should be those that are documented in this table specification. A font may also use privately-defined tags, which have semantics known only by private agreement. Private-use tags must begin with an uppercase letter and use only uppercase letters or digits. If a private-use tag is used in a given font, any application that does not recognize that tag should ignore it.

The following tags are defined:

<a id="anchor-mvar-valueTags_logicalGrouping"></a>

*Value tags, ordered by logical groupings:*

| Tag | Mnemonic | Value represented |
| --- | --- | --- |
| 'hasc' | horizontal ascender | OS/2.sTypoAscender |
| 'hdsc' | horizontal descender | OS/2.sTypoDescender |
| 'hlgp' | horizontal line gap | OS/2.sTypoLineGap |
| 'hcla' | horizontal clipping ascent | OS/2.usWinAscent |
| 'hcld' | horizontal clipping descent | OS/2.usWinDescent |
| 'vasc' | vertical ascender | vhea.ascent |
| 'vdsc' | vertical descender | vhea.descent |
| 'vlgp' | vertical line gap | vhea.lineGap |
| 'hcrs' | horizontal caret rise | hhea.caretSlopeRise |
| 'hcrn' | horizontal caret run | hhea.caretSlopeRun |
| 'hcof' | horizontal caret offset | hhea.caretOffset |
| 'vcrs' | vertical caret rise | vhea.caretSlopeRise |
| 'vcrn' | vertical caret run | vhea.caretSlopeRun |
| 'vcof' | vertical caret offset | vhea.caretOffset |
| 'xhgt' | x height | OS/2.sxHeight |
| 'cpht' | cap height | OS/2.sCapHeight |
| 'sbxs' | subscript em x size | OS/2.ySubscriptXSize |
| 'sbys' | subscript em y size | OS/2.ySubscriptYSize |
| 'sbxo' | subscript em x offset | OS/2.ySubscriptXOffset |
| 'sbyo' | subscript em y offset | OS/2.ySubscriptYOffset |
| 'spxs' | superscript em x size | OS/2.ySuperscriptXSize |
| 'spys' | superscript em y size | OS/2.ySuperscriptYSize |
| 'spxo' | superscript em x offset | OS/2.ySuperscriptXOffset |
| 'spyo' | superscript em y offset | OS/2.ySuperscriptYOffset |
| 'strs' | strikeout size | OS/2.yStrikeoutSize |
| 'stro' | strikeout offset | OS/2.yStrikeoutPosition |
| 'unds' | underline size | post.underlineThickness |
| 'undo' | underline offset | post.underlinePosition |
| 'gsp0' | gaspRange\[0\] | gasp.gaspRange\[0\].rangeMaxPPEM |
| 'gsp1' | gaspRange\[1\] | gasp.gaspRange\[1\].rangeMaxPPEM |
| 'gsp2' | gaspRange\[2\] | gasp.gaspRange\[2\].rangeMaxPPEM |
| 'gsp3' | gaspRange\[3\] | gasp.gaspRange\[3\].rangeMaxPPEM |
| 'gsp4' | gaspRange\[4\] | gasp.gaspRange\[4\].rangeMaxPPEM |
| 'gsp5' | gaspRange\[5\] | gasp.gaspRange\[5\].rangeMaxPPEM |
| 'gsp6' | gaspRange\[6\] | gasp.gaspRange\[6\].rangeMaxPPEM |
| 'gsp7' | gaspRange\[7\] | gasp.gaspRange\[7\].rangeMaxPPEM |
| 'gsp8' | gaspRange\[8\] | gasp.gaspRange\[8\].rangeMaxPPEM |
| 'gsp9' | gaspRange\[9\] | gasp.gaspRange\[9\].rangeMaxPPEM |

<a id="anchor-mvar-valueTags_alphabetical"></a>

*Value tags, in alphabetical order of tags:*

| Tag | Mnemonic | Value represented |
| --- | --- | --- |
| <a id="anchor-mvar-cpht"></a>'cpht' | cap height | OS/2.sCapHeight |
| <a id="anchor-mvar-gsp0"></a>'gsp0' | gaspRange\[0\] | gasp.gaspRange\[0\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp1"></a>'gsp1' | gaspRange\[1\] | gasp.gaspRange\[1\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp2"></a>'gsp2' | gaspRange\[2\] | gasp.gaspRange\[2\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp3"></a>'gsp3' | gaspRange\[3\] | gasp.gaspRange\[3\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp4"></a>'gsp4' | gaspRange\[4\] | gasp.gaspRange\[4\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp5"></a>'gsp5' | gaspRange\[5\] | gasp.gaspRange\[5\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp6"></a>'gsp6' | gaspRange\[6\] | gasp.gaspRange\[6\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp7"></a>'gsp7' | gaspRange\[7\] | gasp.gaspRange\[7\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp8"></a>'gsp8' | gaspRange\[8\] | gasp.gaspRange\[8\].rangeMaxPPEM |
| <a id="anchor-mvar-gsp9"></a>'gsp9' | gaspRange\[9\] | gasp.gaspRange\[9\].rangeMaxPPEM |
| <a id="anchor-mvar-hasc"></a>'hasc' | horizontal ascender | OS/2.sTypoAscender |
| <a id="anchor-mvar-hcla"></a>'hcla' | horizontal clipping ascent | OS/2.usWinAscent |
| <a id="anchor-mvar-hcld"></a>'hcld' | horizontal clipping descent | OS/2.usWinDescent |
| <a id="anchor-mvar-hcof"></a>'hcof' | horizontal caret offset | hhea.caretOffset |
| <a id="anchor-mvar-hcrn"></a>'hcrn' | horizontal caret run | hhea.caretSlopeRun |
| <a id="anchor-mvar-hcrs"></a>'hcrs' | horizontal caret rise | hhea.caretSlopeRise |
| <a id="anchor-mvar-hdsc"></a>'hdsc' | horizontal descender | OS/2.sTypoDescender |
| <a id="anchor-mvar-hlgp"></a>'hlgp' | horizontal line gap | OS/2.sTypoLineGap |
| <a id="anchor-mvar-sbxo"></a>'sbxo' | subscript em x offset | OS/2.ySubscriptXOffset |
| <a id="anchor-mvar-sbxs"></a>'sbxs' | subscript em x size | OS/2.ySubscriptXSize |
| <a id="anchor-mvar-sbyo"></a>'sbyo' | subscript em y offset | OS/2.ySubscriptYOffset |
| <a id="anchor-mvar-sbys"></a>'sbys' | subscript em y size | OS/2.ySubscriptYSize |
| <a id="anchor-mvar-spxo"></a>'spxo' | superscript em x offset | OS/2.ySuperscriptXOffset |
| <a id="anchor-mvar-spxs"></a>'spxs' | superscript em x size | OS/2.ySuperscriptXSize |
| <a id="anchor-mvar-spyo"></a>'spyo' | superscript em y offset | OS/2.ySuperscriptYOffset |
| <a id="anchor-mvar-spys"></a>'spys' | superscript em y size | OS/2.ySuperscriptYSize |
| <a id="anchor-mvar-stro"></a>'stro' | strikeout offset | OS/2.yStrikeoutPosition |
| <a id="anchor-mvar-strs"></a>'strs' | strikeout size | OS/2.yStrikeoutSize |
| <a id="anchor-mvar-undo"></a>'undo' | underline offset | post.underlinePosition |
| <a id="anchor-mvar-unds"></a>'unds' | underline size | post.underlineThickness |
| <a id="anchor-mvar-vasc"></a>'vasc' | vertical ascender | vhea.ascent |
| <a id="anchor-mvar-vcof"></a>'vcof' | vertical caret offset | vhea.caretOffset |
| <a id="anchor-mvar-vcrn"></a>'vcrn' | vertical caret run | vhea.caretSlopeRun |
| <a id="anchor-mvar-vcrs"></a>'vcrs' | vertical caret rise | vhea.caretSlopeRise |
| <a id="anchor-mvar-vdsc"></a>'vdsc' | vertical descender | vhea.descent |
| <a id="anchor-mvar-vlgp"></a>'vlgp' | vertical line gap | vhea.lineGap |
| <a id="anchor-mvar-xght"></a>'xhgt' | x height | OS/2.sxHeight |

Note that the tags 'gsp0' to 'gsp9' are used to provide variation data for the rangeMaxPPEM member of records in a [grid-fitting and scan-conversion procedure ('gasp')](gasp.md) table. The last 'gasp' table entry always uses a rangeMaxPPEM value of 0xFFFF. The maximum number of value records for 'gasp' entries must never be more than one less the number of entries in the 'gasp' table.
