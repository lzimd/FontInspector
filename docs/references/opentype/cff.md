---
title: "CFF — Compact Font Format (Version 1)"
description: "The compact font format table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-01-19T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/cff.md"
last-modified: "2026-09-17T18:19:03Z"
---

<a id="anchor-cff-cff-compact-font-format-version-1"></a>

# CFF — Compact Font Format (Version 1)

This table contains a Compact Font Format (CFF) font representation and is structured according to [Adobe Technical Note #5176: “The Compact Font Format Specification,”](http://partners.adobe.com/public/developer/en/font/5176.CFF.pdf) and [Adobe Technical Note #5177: “Type 2 Charstring Format.”](http://partners.adobe.com/public/developer/en/font/5177.Type2.pdf)

> *Note:* See Adobe Technical Note #5176 for details regarding the CFF INDEX, DICT and FontSet structures mentioned below.

The CFF font format existed as an independent font format prior to the development of OpenType. When incorporated into the OpenType format, certain essential font information continued to be represented using mechanisms defined in the CFF format, duplicating other data representations available within OpenType for use in fonts with TrueType outlines. For example, CFF incorporates glyph widths into glyph outline descriptions, though these could otherwise be provided in the ['hmtx' table](hmtx.md). OpenType fonts with TrueType outlines use a glyph index in conjunction with offsets in the ['loca' table](loca.md) to access glyph data within the 'glyf' table. This concept is retained in OpenType CFF fonts, except that glyph data is accessed through a *CharStrings INDEX* structure within the 'CFF ' table.

See [Comparison of 'glyf', 'CFF ' and CFF2 tables](glyphformatcomparison.md) for a summary of significant differences between the 'glyf', 'CFF ' and CFF2 tables.

The Name INDEX in the 'CFF ' table must contain only one entry; that is, there must be only one font in the CFF FontSet. It is not a requirement that this name be the same as name ID 6 entries in the ['name' table](name.md). Note that, in an OpenType font collection file, a single 'CFF ' table can be shared across multiple fonts; names used by applications must be those provided in the 'name' table, not the Name INDEX entry.

The CFF Top DICT must specify a CharstringType value of 2.

The numGlyphs field in the ['maxp' table](maxp.md) must be the same as the number of entries in the CFF’s CharStrings INDEX. The OpenType font glyph index is the same as the CFF glyph index for all glyphs in the font.
