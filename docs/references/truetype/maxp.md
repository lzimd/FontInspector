---
title: "The 'maxp' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-maxp-maxp"></a>

# The `'maxp'` table

<a id="anchor-maxp-part-1"></a>

## General table information

The `'maxp'` table establishes the memory requirements for a font. It begins with a table version number. The next entry is the number of glyphs in the font. The remaining entries all establish maximum values for a number of parameters. Most of these are self explanatory. A few, however, need some clarification.

The `maxSizeOfInstructions` is the maximum size in bytes for all of the instructions associated with a particular glyph.

The `maxComponentElements` field refers to the maximum number of simple glyphs that will be used to create a compound glyph.

The `maxComponentDepth` refers to the number of levels of recursion used in constructing the most complex compound glyph. The maximum legal value for `maxComponentDepth` is 16. If there are no components within components, all compound glyphs can be deemed simple and this field can be set to the value one.

*The `'maxp'` Table*

| Type | Name | Description |
| --- | --- | --- |
| Fixed | version | 0x00010000 (1.0) |
| uint16 | numGlyphs | the number of glyphs in the font |
| uint16 | maxPoints | points in non-compound glyph |
| uint16 | maxContours | contours in non-compound glyph |
| uint16 | maxComponentPoints | points in compound glyph |
| uint16 | maxComponentContours | contours in compound glyph |
| uint16 | maxZones | set to 2 |
| uint16 | maxTwilightPoints | points used in Twilight Zone (Z0) |
| uint16 | maxStorage | number of Storage Area locations |
| uint16 | maxFunctionDefs | number of FDEFs |
| uint16 | maxInstructionDefs | number of IDEFs |
| uint16 | maxStackElements | maximum stack depth |
| uint16 | maxSizeOfInstructions | byte count for glyph instructions |
| uint16 | maxComponentElements | number of glyphs referenced at top level |
| uint16 | maxComponentDepth | levels of recursion, set to 0 if font has only simple glyphs |

Fonts with PostScript outlines (that is, OpenType fonts with `'CFF '` tables) use a six-byte version of the `'maxp'` table:

*The `'maxp'` Table for PostScript OpenType Fonts*

| Type | Name | Description |
| --- | --- | --- |
| Fixed | version | 0x00005000 (0.5) |
| uint16 | numGlyphs | the number of glyphs in the font |

<a id="anchor-maxp-part-2"></a>

## Dependencies

The `'maxp'` table contains a count for the number of glyphs in the font. Whenever this value changes, other tables which depend on it should also be updated. The tables affected includes:

- [glyph location table](loca.md) (`'loca'`)
- [glyph data table](glyf.md) (`'glyf'`)
- [`'Zapf'`](Zapf.md) table

In addition, some tables contain glyph indices which might need to be updated if a glyph is *removed* from the font. A partial list of such tables is:

- [character-glyph mapping table](cmap.md) (`'cmap'`)
- [justification table](just.md) (`'just'`)
- [kerning table](kern.md) (`'kern'`)
- [extended glyph metamorphosis table](morx.md) (`'morx'`)
