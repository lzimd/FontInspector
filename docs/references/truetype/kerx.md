---
title: "The 'kerx' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-kerx-kerx"></a>

# The `'kerx'` table

<a id="anchor-kerx-part-1"></a>

## General table information

The format for the kerning (`'kern'`) table was first designed in 1988. At that time, 680x0 processors were the design center, and memory was comparatively expensive. Because of these constraints, the table format was designed to take as little space as possible, and to use “tricks”which sped up processing.

In a world of multi-gigabyte machines running gigahertz processors, however, this design is anachronistic—and worse, an impediment. Developers wished to create fonts which required more than the original `'kern'` table could supply. To this end, an extended kerning table, the `'kerx'` table, has been introduced.

The `'kerx'` table contains the values that adjust the positioning of glyphs in a font. It can have multiple subtables in varied formats that can contain information for vertical or horizontal text.

Adjustments can be parallel to the flow of text or perpendicular to the flow of text, or both. For example, if perpendicular adjustments are specified and if text is normally written horizontally, adjustments will be up or down.

Four positioning formats are currently defined, formats 0, 1, 2, 4, and 6. The file format specification allows for additional formats to be defined for further use. Formats 3, 5, and 7 through 255 are reserved for future use.

Each subtable can be in one of the four formats specified below, and can contain information for vertical or horizontal text. A font can have multiple `'kerx'` subtables but since the adjustments made by these tables are additive, the order of the subtables containing adjustments is not important.

The positioning table has a header, which contains the format number, the number of subtables present, and the subtables themselves.

*The `'kerx'` Table*

| Type | Name | Description |
| --- | --- | --- |
| uint16 | version | The version number of the extended kerning table (currently 2, 3, or 4). |
| uint16 | padding | Unused; set to zero. |
| uint32 | nTables | The number of subtables included in the extended kerning table. |

If the `'kerx'` table version is 3 or greater, then the last subtable is followed by a `subtableGlyphCoverageArray`, as described below.

If the `'kerx'` table version is 4 or greater, then kerning values may be single values or vectors, as described below.

Positioning subtables also have a header that is used to identify the format of the subtable and the kind of information it contains.

*The `'kerx'` Subtable Header*

| Type | Name | Description |
| --- | --- | --- |
| uint32 | length | The length of this subtable in bytes, including this header. |
| uint32 | coverage | Circumstances under which this table is used. See below for description. |
| uint32 | tupleCount | The tuple count. This value is only used with variation fonts and should be 0 for all other fonts. The subtable's `tupleCount` will be ignored if the `'kerx'` table version is less than 4. |

If the subtable's `tupleCount` is greater than zero, then the subtable does not include single kern values, but `tupleCount`-dimensional vectors of kerning values associated with the global tuples in the font's [`'gvar'`](https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6gvar) table. The manner this is supported varies according to the subtable format.

The subtable `coverage` field is divided into the subfields given in below.

*The `coverage` Field*

| Mask value | Name | Description |
| --- | --- | --- |
| 0x80000000 | vertical | Set if table has vertical kerning values. |
| 0x40000000 | crossStream | Set if table has cross-stream kerning values. |
| 0x20000000 | variation | Set if table has variation kerning values. |
| 0x10000000 | processDirection | Process direction flag. If clear, process the glyphs forwards, that is, from first to last in the glyph stream. If we, process them from last to first. This flag only applies to state-table based `'kerx'` subtables (types 1 and 4). |
| 0x0FFFFF00 | unusedBits | Set to 0. |
| 0x000000FF | formatMask | These bytes contain the format of this subtable (0, 1, 2, 4, and 6 currently defined). |

A mask value of 0x40000000 indicates that cross-stream position adjustments are to be invoked. If text is normally written horizontally, adjustments will be vertical. If adjustment values are positive, the text will be moved up. If they are negative, the text will be moved down. If text is normally written vertically, adjustments will be horizontal. If adjustment values are positive, the text will be moved to the right. If they are negative, the text will be moved to the left.

<a id="anchor-kerx-part-2"></a>

## Positioning subtable formats

The format-specific kerning subtables follow the kerning subtable header. The following sections give the details of Kerning Table Formats 0, 1, 2, 4, and 6. Formats 3, 5, and 7 through 255 are reserved for future use. The following kerning formats are currently defined:

- Format 0 is an ordered list of kerning pairs
- Format 1 is a state table for contextual kerning of up to eight glyphs
- Format 2 is a simple two-dimensional, byte offset-based array of kerning values with associated class subtables.
- Format 4 is a state table for control point/anchor point positioning
- Format 6 is a simple, index-based two-dimensional array of kerning values values with associated class subtables.

<a id="anchor-kerx-part-3"></a>

### Format 0 Kerning Subtable (Ordered List of Kerning Pairs)

Format 0 positioning subtables store positioning information as sorted lists of kerning pairs and values. Using information stored in the positioning subtable header, you can execute an efficient binary search of these lists.

A binary search is most efficiently coded if the search range is a power of two, so that the search range can be reduced by half by shifting instead of dividing. In general, the number of kerning pairs, `nPairs`, will not be a power of two. The value `searchRange` should be the largest power of two less than or equal to `nPairs`. The number of pairs not covered by `searchRange` (that is, `nPairs` - `searchRange`) is the value `rangeShift`.

Before the binary search loop is made, you need to determine whether the desired kerning pair is in the `searchRange` portion of the list. If it is, the binary search starts at the beginning of the list of kerning pairs. If it isn't, the search starts `rangeShift` bytes from the beginning of the list. This will be an entry boundary. The number of iterations made through the list of kerning pairs is determined by the value of `entrySelector`, which is calculated as the base 2 log of the largest power of two less than or equal to the value of `nPairs`.

Although this ordered list format is compact and easy to generate, the binary search loop requires `entrySelector` iterations in order to search.

This table gives the format of the Format 0 kerning subtable:

*The Type 0 `'kerx'` Subtable*

| Type | Name | Description |
| --- | --- | --- |
| uint32 | nPairs | The number of kerning pairs in this subtable. |
| uint32 | searchRange | The largest power of two less than or equal to the value of nPairs, multiplied by the size in bytes of an entry in the subtable. |
| uint32 | entrySelector | This is calculated as log2 of the largest power of two less than or equal to the value of nPairs. This value indicates how many iterations of the search loop have to be made. For example, in a list of eight items, there would be three iterations of the loop. |
| uint32 | rangeShift | The value of nPairs minus the largest power of two less than or equal to nPairs. This is multiplied by the size in bytes of an entry in the table. |

The format for the Format 0 kerning pairs and values is as follows:

*The Type 0 `'kerx'` Subtable Kerning Records*

| Type | Name | Description |
| --- | --- | --- |
| uint16 | left | The glyph index for the lefthand glyph in the kerning pair. |
| uint16 | right | The glyph index for the righthand glyph in the kerning pair. |
| sint16 | value | See below |

If the `tupleCount` for this subtable is 0, then the table contains single kerning values in FUnits for the left and right pair. If this value is greater than zero, the glyphs are moved apart. If this value is less than zero, the glyphs are moved together.

If the `tupleCount` is 1 or more, then the table contains offsets from the beginning of the subtable to a `tupleCount`-dimensional vector of FUnits controlling the kerning.

The left (high order word) and right (low order word) halves of the kerning pair make an unsigned 32-bit number, which is then used to order the kerning pairs numerically.

The table may end with a sentinel entry for a left-hand glyph of 0xFFFF, a right-hand glyph of 0xFFFF, and a kerning value of 0.

<a id="anchor-kerx-part-4"></a>

### Format 1 Kerning Subtable (State Table for Contextual Kerning)

Format 1 positioning tables contain a format specific header and a state table to allow kerning of up to eight glyphs at once. The format specific header for a Format 1 positioning table is as follows:

*The Type 1 `'kerx'` Header*

| Type | Name | Description |
| --- | --- | --- |
| STXHeader | stHeader | The contextual kerning state table header. |
| uint32 | valueTable | Offset in bytes from the beginning of the state table to the beginning of the kerning value array. |

The actions in a contextual kerning subtable are three words in length. The first word is the index of the new state in the state table. The second word is a table-specific flag field. The flags and their descriptions follow:

*The Type 1 `'kerx'` Subtable Actions*

| Mask value | Interpretation |
| --- | --- |
| 0x8000 | Push: if set, push this glyph on the kerning stack. |
| 0x4000 | If set, don't advance to the next glyph before going to the new state. |
| 0x2000 | If set, reset the kerning data (clear the stack) |
| 0x1FFF | Not used; set to 0. |

If the push flag is set, the position of the current glyph in the glyph array will be pushed onto a stack of up to eight glyphs, called the kerning stack.

The final word in the action is an index into the kerning value array. If this index is 0xFFFF, then no kerning is to be performed.

If the `tupleCount` for this subtable is 0, then the kerning value table is a list of FUnit kerning values. Each pops one glyph from the kerning stack and applies the kerning value to it. The end of the list is marked by the value 0xFFFF.

If the `tupleCount` for this subtable 1 or more, then the kerning value table is a list of `tupleCount`-dimensional vectors of FUnit kerning values. Each pops one glyph from the kerning stack and applies the kerning vector to it. The end of the list is marked by the single value 0xFFFF.

<a id="anchor-kerx-part-5"></a>

### Format 2 Kerning Subtable (Simple Offset-based `n` × `m` Array of Kerning Values)

Format 2 positioning subtables store kerning information in a two-dimensional array of kerning values. The glyphs are mapped to classes, using a different mapping for left-hand and right-hand glyphs. This allows glyphs that have similar left-hand or right-hand shapes to be handled together (e.g., accented forms of a letter).

Each row in the array represents one left-hand glyph class, each column represents one right-hand glyph class, and each cell contains a kerning value. Row and column 0 should indicate glyphs that do not kern and contain all zeros.

The right-hand class values are stored pre-multiplied by the number of bytes in a single kerning value (i.e., two). The left-hand class values are stored pre-multiplied by the number of bytes in one row and offset by the offset of the array from the start of the kerning array. This eliminates the need to multiply the row and column values together to determine the location of the kerning value. The array can be indexed by completing the left-hand and right-hand class mappings, adding the class values to the address of the kerning array, and fetching the kerning value to which the new address points.

The header of the format 2 simple array header subtable is as follows:

*Simple Offset-based Array Header*

| Type | Name | Description |
| --- | --- | --- |
| uint32 | rowWidth | The number of bytes in each row of the kerning value array |
| uint32 | leftOffsetTable | Offset from beginning of this subtable to the left-hand offset table. |
| uint32 | rightOffsetTable | Offset from beginning of this subtable to right-hand offset table. |
| uint32 | array | Offset from beginning of this subtable to the start of the kerning array. |

The left- and right-hand offset tables are lookup tables. Values are 16-bit unsigned offsets and default to zero for glyphs not covered by the lookup table.

To find a kerning value, first calculate the row of the left-hand (or top) glyph and column of the right-hand (or bottom) glyph. Use them to calculate the index of the kerning value for the pair.

Note that all the values in the kerning array for row and column zero should be 0.

If the `tupleCount` for this subtable is 0, then the kerning array contains single kerning values in FUnits for the left and right classes. If this value is greater than zero, the glyphs are moved apart. If this value is less than zero, the glyphs are moved together.

If the `tupleCount` is 1 or more, then the kerning array contains offsets from the beginning of the subtable to a `tupleCount`-dimensional vector of FUnits controlling the kerning.

<a id="anchor-kerx-part-6"></a>

### Format 4 Kerning Subtable (State Table for Control Point/Anchor Point Positioning)

Format 4 positioning tables contain a format specific header and a state table to allow positioning a glyph by aligning a control/anchor point on the glyph with a control/anchor point on another glyph. The format specific header for a Format 4 positioning table is as follows:

*The Type 4 `'kerx'` Subtable Header*

| Type | Name | Description |
| --- | --- | --- |
| STXHeader | stHeader | The control point positioning state table header. |
| uint32 | flags | Flags |

The flags field has the following format:

*Format 4 Flags*

| Value | Interpretation |
| --- | --- |
| 0xC0000000 | Action type mask. A two-bit field containing the action type. |
| 0x3F000000 | Unused - must be zero. |
| 0x00FFFFFF | Masks the offset in bytes from the beginning of the state table to the beginning of the control point table. |

The values in the entry table within a control point positioning subtable are very like the actions for a state table subtable (type 1). The first word is the index of the next state, the second word contains flags, and the third word is either 0xFFFF (for no action) or the index of the action to perform.

The flags and their descriptions follow:

*Format 4 Actions*

| Mask value | Interpretation |
| --- | --- |
| 0x8000 | Mark: if set, remember this glyph as the marked glyph. |
| 0x4000 | If set, don't advance to the next glyph before going to the new state |

If the mark flag is set, the position of the current glyph in the glyph array will be saved. This glyph is called the marked glyph.

If the action type field is 0 the action contains control point numbers:

*Control Point Actions*

| Type | Name | Description |
| --- | --- | --- |
| uint16 | markControlPoint | Control point in marked glyph. |
| uint16 | currControlPoint | Control point in current glyph. |

If the action type field is 1 the action contains anchor point numbers:

*Anchor Point Actions*

| Type | Name | Description |
| --- | --- | --- |
| uint16 | markAnchorPoint | Anchor point in marked glyph. |
| uint16 | currAnchorPoint | Anchor point in current glyph. |

If the action type field is 2 the action contains coordinates:

*Control Point Coordinate Actions*

| Type | Name | Description |
| --- | --- | --- |
| FWord | markX | X-coordinate of mark control point |
| FWord | markY | Y-coordinate of mark control point |
| FWord | currX | X-coordinate of current control point |
| FWord | currY | Y-coordinate of current control point |

The current glyph is positioned so that the two control/anchor points overlap.

The value of the `tupleCount` field does not affect the interpretation of a type 4 `'kerx'` subtable. For variation-sensitive kerning with type 4 subtables, the action type field should be 0 (indicating the use of control point numbers), and the `'gvar'` contain appropriate information to reposition the control points used in kerning.

<a id="anchor-kerx-part-7"></a>

### Format 6 Kerning Subtable (Simple Index-based `n` × `m` Array of Kerning Values)

Format 6 positioning subtables store kerning information in a two-dimensional array of kerning values. The glyphs are mapped to classes, using a different mapping for left-hand and right-hand glyphs. This allows glyphs that have similar left-hand or right-hand shapes to be handled together (e.g., accented forms of a letter).

Each row in the array represents one left-hand glyph class, each column represents one right-hand glyph class, and each cell contains a kerning value. Row and column 0 should indicate glyphs that do not kern and contain all zeros.

The header of the format 6 simple array header subtable is as follows:

*Simple Index-based Array Header*

| Type | Name | Description |
| --- | --- | --- |
| uint32 | flags | Flags for this subtable. See below. |
| uint16 | rowCount | The number of rows in the kerning value array |
| uint16 | columnCount | The number of columns in the kerning value array |
| uint32 | rowIndexTableOffset | Offset from beginning of this subtable to the row index lookup table. |
| uint32 | columnIndexTableOffset | Offset from beginning of this subtable to column index offset table. |
| uint32 | kerningArrayOffset | Offset from beginning of this subtable to the start of the kerning array. |
| uint32 | kerningVectorOffset | Offset from beginning of this subtable to the start of the kerning vectors. This value is only present if the `tupleCount` for this subtable is 1 or more. |

The only flag defined for a type 6 `'kerx'` subtable is `valuesAreLong` (bit 0). If set, then values in the two class tables and the kerning array are four bytes in size. If clear, then they are two bytes in size.

As a rule, the `valuesAreLong` flag *must* be set if `rowCount` × `columnCount` is greater than 65535. If `rowCount` × `columnCount` is 65535 or less, the `valuesAreLong` flag *may* be set, but the use of long values under such circumstances is discouraged—it makes the table unnecessarily large.

The two index tables are lookup tables. Each contains indices into the kerning array. Values in the row index lookup table are pre-multiplied by `columnCount` to avoid having to do the multiplication at runtime. The lookup table values default to 0 for glyphs not covered.

To find a kerning value, first calculate the row index of the first glyph and column index of the second glyph. Add them to calculate the index of the kerning value for the pair.

Note that all the values in the kerning array for row and column zero should be 0.

If the `tupleCount` for this subtable is 0, then the kerning array contains single kerning values in FUnits. If this value is greater than zero, the glyphs are moved apart. If this value is less than zero, the glyphs are moved together.

If the `tupleCount` is 1 or more, then the kerning array contains offsets from the beginning of the `kerningVectors` table to a `tupleCount`-dimensional vector of FUnits controlling the kerning. If the `valuesAreLong` flag is set, then these offsets are four bytes in size; otherwise, they are two bytes in size.

<a id="anchor-kerx-part-8"></a>

## Subtable Glyph Coverage Tables

A subtable glyph coverage table is used to determine whether or not a particular glyph in the font is relevant to a given subtable. Its format is as follows:

| Type | Name | Description |
| --- | --- | --- |
| uint32 | subtableOffsets\[\] | Array of offsets from the beginning of the subtable glyph coverage table to the glyph coverage bitfield for a given subtable; there is one offset for each subtable in the `'kerx'` table. Use `0xFFFFFFFF` to indicate that there is no coverage bitfield for the given subtable. Coverage bitfields are only used for type 1 and 4 `'kerx'` subtables. |
| uint8 | coverageBitfields\[\] | The individual coverage bitfields |

Each coverage bitfield is `(numGlyphs + CHAR_BIT - 1) / CHAR_BIT` bytes in size (rounded up to a four-byte boundary).

To determine if a particular glyph is covered by the subtable, calculate `coverageBitfield[glyph/CHAR_BIT] & (1 << (glyph & (CHAR_BIT-1)))`. If this is non-zero, the glyph is covered.

In practice, for a given run of text, a coverage bitfield is generated for the glyphs in that run. That bitfield is then ANDed with the coverage bitfield for each subtable. If the result is zero, then none of the glyphs in the run is used by the subtable and the subtable may be skipped.

As a rule, the most benefit accrues when the coverage bitfield only includes the glyphs that trigger a kerning action. This will maximize the number of subtables which can be skipped.

<a id="anchor-kerx-part-9"></a>

## Variation Font Support

If the `'kerx'` table version is 4 or greater, then it can be used to provide variable kerning in variation fonts.

Normally in a `'kerx'` table, each glyph pair is associated with a single two-byte `FUnit` value. If this value is negative, the glyphs are moved closer together; if it is positive, they are moved further apart.

In a variation font, if the `tupleCount` value is 1 or more, then the glyph pair is associated with a `tupleCount`-dimensional vector of two-byte `FUnit` values. These are used in connection with the global tuple coordinates defined in the font's `'gvar'` table. The first value in the vector is the default kerning value for the glyph pair. The remaining values are deltas associated with one of the global coordinates.

For example, Skia defines eight global coordinates in its `'gvar'` table. Its `'kerx'` table subtables could therefore have `tupleCount` values of 0 (for non-variable kerning) or 2 through 9 (one default value and one to eight deltas). Any delta not explicitly present is set equal to 0.

The variation settings for the font determine a point in the `n`-dimensional space defined by the font's `n` variation axes. This point is used to calculate a scalar for each global coordinate in the font's `'gvar'` table. The calculation of the scalar is exactly analogous to the calculations done for the `'gvar'` table itself. The delta defined in the `'kerx'` subtable is multiplied by this scalar and added to the default kerning value. The end result is the kerning value actually applied to the glyph pair.

To illustrate, let us assume a font with the following:

- Two variation axes, `'wght'` and `'wdth'`
- Eight global coordinates in the `'gvar'` table: (1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, -1), (1, 1), and (-1, 1). (These first two conditions are true for Skia.)
- A pair of glyphs associated with the kerning vector \[100, 5, -10, -15, 20, 0, 0, -25, 30\]. This defines a default kerning value of 100 and eight deltas for the eight global coordinates.

Let is further assume that the normalized value of the `'wght'` axis is 0.4 and the normalized value of the `'wdth'` axis is -0.25.

The first global coordinate has a value of 1 for the `'wght'` axis and 0 for the `'wdth'` axis. A 0 value means the axis' setting is ignored, so the only value we consider is that of the `'wght'` axis. Our setting for this axis is between 0 and the global coordinate's value for the axis, so we will apply this global coordinate's delta. Specifically, our setting is 0.4 of the way between 0 and global coordinate's setting, so we will apply 0.4 of the delta, or 2 (0.4 × 5). Our kerning value so far is therefore 100 + 2 = 102.

The second global coordinate has a value of -1 for the `'wght'` axis and 0 for the `'wdth'` axis. Again, we ignore the `'wdth'`. Our setting for this axis is *not* between 0 and the global coordinate's value for the axis, so we will *not* apply this global coordinate's delta. Our kerning value so far is still 102.

The third delta is similarly skipped (the `'wght'` coordinate is 0 and our `'wdth'` axis setting is not between 0 and the global coordinate's `'wdth'` axis value).

The fourth delta is applied (the `'wght'` coordinate is 0 but our `'wdth'` axis setting is between 0 and the global coordinate's `'wdth'` axis value). We add (-0.25 / -1.0) × -15 = -3.75 to our kerning value hitherto to get 98.25.

The only other delta we will apply is the sixth, because it's the only one where our settings are in the correct range for the axes which are not being ignored—but since the delta itself is 0, we make no further changes.

Our final kerning value is therefore 98.25.

<a id="anchor-kerx-part-10"></a>

## Platform-specific Information

The `'kerx'` table is supported on OS X 10.7 and iOS 7 onward. Type 2 `'kerx'` subtables do not work prior to iOS 7 and OS X 10.9.

Support for the `processDirection` flag and version 3 `'kerx'` tables is available in iOS 9 or later and OS X 10.11 or later.

Support for `tupleCount` values of 1 or more and type 6 `'kerx'` subtables is planned for future releases of iOS and OS X.

<a id="anchor-kerx-part-11"></a>

## Dependencies

The `'kerx'` table refers to glyphs by their glyph index. These values should not exceed the number of glyphs for the font as contained in [the maximum profile (`'maxp'`) table.](maxp.md)

If the font has an [`'ankr'` (anchor point)](ankr.md) table, it is used to define the anchor points. Otherwise, the "anchor points" are the points defined by the [`'glyf'` (glyph data)](glyf.md) table.

<a id="anchor-kerx-part-12"></a>

## Tools

Dumping and fusing of `'kerx'` tables is supported in ftxdumperfuser. `'kerx'` tables can also be generated using ftxenhancer.
