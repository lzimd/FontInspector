---
title: "hhea — Horizontal Header Table"
description: "The horizontal header table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2023-01-10T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/hhea.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-hhea-hhea-horizontal-header-table"></a>

# hhea — Horizontal Header Table

<a id="anchor-hhea-hheaHeader"></a>

This table contains information for horizontal layout. The values in the minRightSidebearing, minLeftSideBearing and xMaxExtent should be computed using *only* glyphs that have contours. Glyphs with no contours should be ignored for the purposes of these calculations. All reserved areas must be set to 0.

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-hhea-majorVersion"></a>uint16 | majorVersion | Major version number of the horizontal header table — set to 1. |
| <a id="anchor-hhea-minorVersion"></a>uint16 | minorVersion | Minor version number of the horizontal header table — set to 0. |
| <a id="anchor-hhea-ascender"></a>FWORD | ascender | Typographic ascent—see remarks below. |
| <a id="anchor-hhea-descender"></a>FWORD | descender | Typographic descent—see remarks below. |
| <a id="anchor-hhea-lineGap"></a>FWORD | lineGap | Typographic line gap.<br>Negative lineGap values are treated as zero in some legacy platform implementations. |
| <a id="anchor-hhea-advanceWidthMax"></a>UFWORD | advanceWidthMax | Maximum advance width value in 'hmtx' table. |
| <a id="anchor-hhea-minLeftSideBearing"></a>FWORD | minLeftSideBearing | Minimum left sidebearing value in 'hmtx' table for glyphs with contours (empty glyphs should be ignored). |
| <a id="anchor-hhea-minRightSideBearing"></a>FWORD | minRightSideBearing | Minimum right sidebearing value; calculated as min(aw - (lsb + xMax - xMin)) for glyphs with contours (empty glyphs should be ignored). |
| <a id="anchor-hhea-xMaxExtent"></a>FWORD | xMaxExtent | Max(lsb + (xMax - xMin)). |
| <a id="anchor-hhea-caretSlopeRise"></a>int16 | caretSlopeRise | Used to calculate the slope of the cursor (rise/run); 1 for vertical. |
| <a id="anchor-hhea-caretSlopeRun"></a>int16 | caretSlopeRun | 0 for vertical. |
| <a id="anchor-hhea-caretOffset"></a>int16 | caretOffset | The amount by which a slanted highlight on a glyph needs to be shifted to produce the best appearance. Set to 0 for non-slanted fonts |
| int16 | (reserved) | set to 0 |
| int16 | (reserved) | set to 0 |
| int16 | (reserved) | set to 0 |
| int16 | (reserved) | set to 0 |
| <a id="anchor-hhea-metricDataFormat"></a>int16 | metricDataFormat | 0 for current format. |
| <a id="anchor-hhea-numberOfHMetrics"></a>uint16 | numberOfHMetrics | Number of hMetric entries in 'hmtx' table |

The ascender, descender and linegap values in this table are Apple specific; see [Apple's specification](http://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6hhea.html) for details regarding Apple platforms. The [sTypoAscender](os2.md#anchor-os2-stypoascender), [sTypoDescender](os2.md#anchor-os2-stypodescender) and [sTypoLineGap](os2.md#anchor-os2-stypolinegap) fields in the OS/2 table are used on the Windows platform, and are recommended for new text-layout implementations. Font developers should evaluate behavior in target applications that may use fields in this table or in the OS/2 table to ensure consistent layout. See the descriptions of the OS/2 fields for additional details.

<a id="anchor-hhea-hhea-table-and-opentype-font-variations"></a>

## 'hhea' Table and OpenType Font Variations

In a variable font, various font-metric values within the horizontal header table may need to be adjusted for different variation instances. Variation data for 'hhea' entries can be provided in the [metrics variations (MVAR)](mvar.md) table. Different 'hhea' entries are associated with particular variation data in the MVAR table using value tags, as follows:

| 'hhea' entry | Tag |
| --- | --- |
| <a id="anchor-hhea-hcof"></a>caretOffset | 'hcof' |
| <a id="anchor-hhea-hcrs"></a>caretSlopeRise | 'hcrs' |
| <a id="anchor-hhea-hcrn"></a>caretSlopeRun | 'hcrn' |

For general information on OpenType Font Variations, see the chapter, [OpenType Font Variations Overview](otvaroverview.md).
