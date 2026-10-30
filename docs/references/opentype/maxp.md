---
title: "maxp — Maximum Profile"
description: "The maxp - Maximum Profile table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2021-10-26T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7a06e1def6e2f40e43dc8897e5372614bcc413f6/typographydocs/opentype/spec/maxp.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-maxp-maxp-maximum-profile"></a>

# maxp — Maximum Profile

This table establishes the memory requirements for this font. Fonts with CFF or CFF2 outlines must use Version 0.5 of this table, specifying only the numGlyphs field. Fonts with TrueType outlines must use Version 1.0 of this table, where all data is required.

<a id="anchor-maxp-maxpHeader_05"></a>

*Version 0.5*

| Type | Name | Description |
| --- | --- | --- |
| Version16Dot16 | version | 0x00005000 for version 0.5 |
| uint16 | numGlyphs | The number of glyphs in the font. |

<a id="anchor-maxp-maxpHeader_10"></a>

*Version 1.0*

| Type | Name | Description |
| --- | --- | --- |
| Version16Dot16 | version | 0x00010000 for version 1.0. |
| uint16 | numGlyphs | The number of glyphs in the font. |
| uint16 | maxPoints | Maximum points in a non-composite glyph. |
| uint16 | maxContours | Maximum contours in a non-composite glyph. |
| uint16 | maxCompositePoints | Maximum points in a composite glyph. |
| uint16 | maxCompositeContours | Maximum contours in a composite glyph. |
| uint16 | maxZones | 1 if instructions do not use the twilight zone (Z0), or 2 if instructions do use Z0; should be set to 2 in most cases. |
| uint16 | maxTwilightPoints | Maximum points used in Z0. |
| uint16 | maxStorage | Number of Storage Area locations. |
| uint16 | maxFunctionDefs | Number of FDEFs, equal to the highest function number + 1. |
| uint16 | maxInstructionDefs | Number of IDEFs. |
| uint16 | maxStackElements | Maximum stack depth across Font Program (['fpgm' table](fpgm.md)), CVT Program (['prep' table](prep.md)) and all glyph instructions (in the ['glyf' table](glyf.md)). |
| uint16 | maxSizeOfInstructions | Maximum byte count for glyph instructions. |
| uint16 | maxComponentElements | Maximum number of components referenced at “top level” for any composite glyph. |
| uint16 | maxComponentDepth | Maximum levels of recursion; 1 for simple components. |
