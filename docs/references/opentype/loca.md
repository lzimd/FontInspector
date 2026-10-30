---
title: "loca — Index to Location"
description: "The index-to-location table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-03-15T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/loca.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-loca-loca-index-to-location"></a>

# loca — Index to Location

The index to location ('loca') table stores an array of offsets to the locations of glyph descriptions in the ['glyf'](glyf.md) table, relative to the beginning of that table. Offsets in the array are referenced by corresponding glyph IDs.

Offsets must be in ascending order, with loca\[*n*\] \<= loca\[*n+1*\]. The length of each glyph description is determined by the difference between two consecutive entries: loca\[*n+1*\] - loca\[*n*\]. To compute the length of the last glyph description, there is an extra entry in the offsets array after the entry for the last valid glyph ID. Thus, the number of elements in the offsets array is numGlyphs + 1.

By definition, glyph index zero points to the “missing character” glyph, which is the glyph that is displayed if a character is not found in the font’s ['cmap'](cmap.md) table. A missing character is commonly represented by a blank box or a space. If the font does not contain an outline for this glyph, then the first and second offsets should have the same value. This also applies to any other glyphs without an outline, such as the glyph for the space character: if a glyph has no outline or instructions, then loca\[*n*\] = loca\[*n+1*\].

There are two formats of this table: a short format, and a long format. The format is specified by the indexToLocFormat entry in the ['head'](head.md) table.

*Short format*

| Type | Name | Description |
| --- | --- | --- |
| Offset16 | offsets\[numGlyphs + 1\] | The local offset divided by 2 is stored. |

*Long format*

| Type | Name | Description |
| --- | --- | --- |
| Offset32 | offsets\[numGlyphs + 1\] | The actual local offset is stored. |
