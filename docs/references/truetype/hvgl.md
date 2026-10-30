---
title: "The 'hvgl' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-hvgl-hvgl"></a>

# The `'hvgl'` table

The `'hvgl'` table defines glyphs and glyph components for *HVF*, or Hierarchical Variation Fonts. As the name implies, HVF glyphs comprise components called *composites* that in turn comprise other components. Leaf-level components are called *shapes*; shapes and composites are collectively referred to as *parts*. Glyphs are simply parts that can be referred to from outside the `'hvgl'` table.

The table contains both integer and floating point information. All values are stored in little-endian format with natural alignment. Floating point numbers are in IEEE 754 format. Composites use 32 bit floats; shapes use 64 bit floats. Trees are stored in depth-first order. The table itself must be aligned to a 64 bit float boundary when accessed in memory.

<a id="anchor-hvgl-part-1"></a>

### Table header

The table header contains version information, the offset to the index of parts by part number, the total number of parts, and the number of visible parts. Visible parts are always first by part number.

*`'hvgl'` Table Header*

| Field | Type | Comment |
| --- | --- | --- |
| Version (major) | `UInt16` | Currently 3 |
| Version (minor) | `UInt16` | Currently 1 |
| Format Flags | `UInt32` | Currently all zero |
| Number of parts | `UInt32` | All shapes and composites |
| Part index offset | `UInt32` | From beginning of hvgl table |
| Number of glyphs | `UInt32` | Count of externally visible parts |
| Unused | `UInt32` | Currently zero |

<a id="anchor-hvgl-part-2"></a>

### Part Index

The number of entries in this index is the number of parts, plus one for a sentinel entry. Each entry is a `UInt32`, the byte offset from the beginning of the part index to the location of the part data in the `hvgl` table. The final, sentinel entry points at the end of the last part’s data. All parts must be minimally aligned on a `UInt16` boundary (shapes and composites have their own, more stringent alignment requirements). The size of a part’s data is the difference between the offset of the part and the offset of the next part. Parts are padded at the end to maintain the alignment of the next part, and this padding will be included in the size of the part.

Having the part index be `Float64` aligned relative to the `hvgl` table makes alignment computations easier.

<a id="anchor-hvgl-part-3"></a>

### Part Header

Every part has one `UInt16` flag value at offset 0. The least significant bit is used to determine if the part is a shape (0) or a composite (1). All other flags are zero and ignored at this time.

<a id="anchor-hvgl-part-4"></a>

### Shape Part Data

Shape data must begin on a `Float64` boundary within the `hvgl` table, which itself must be aligned on a `Float64` boundary within the `sfnt` data.

Each shape has one or more paths; each path contains three or more segments (paths with less than three segments are not rendered). Each segment describes one quadratic Bezier curve.

There is also a delta matrix, which describes changes applied to the segment coordinates based on the values set for zero or more axes. Axis values are in the range `[-1.0, 1.0]`. The delta matrix contains two columns for each axis: the first is the change to apply if the axis value is in `[-1.0, 0.0)`; the second is applied if the axis value is in `[0.0, 1.0]`

| Field | Type | Comment |
| --- | --- | --- |
| Flags | `UInt16` | 0x0000 for shape |
| Number of axes | `UInt16` |  |
| Number of paths | `UInt16` | Typically 1 |
| Total segment count for shape | `UInt16` |  |
| Sizes of paths | `[UInt16]` | count of segments for each path |
| Blend types for all segments | `[UInt8]` | See below |
| Pad to Float64 alignment |  | if needed |
| Master coordinate vector *m* | `[Float64]` | 4 for each segment; see below for order |
| Delta coordinate matrix *M* | `[Float64]` | Column major order; 4×segments rows, 2×axes columns |

Note that for curve-type segments, the coordinates of the on-curve point are not stored. Instead, the position of the on-curve point as a fraction of the distance on the line between the previous off-curve point and the following off-curve point, or *parallel factor*, is stored, followed by a zero. The delta matrix stores the delta of the parallel factor for such segments.

*Order of coordinates in segment*

|  |
| --- |
| on-curve point x (parallel factor for curve-type segment) |
| on-curve point y (zero for curve-type segment) |
| off-curve point x |
| off-curve point y |

*Blend types*

| Value | Type |
| --- | --- |
| 0 | Curve |
| 1 | Corner, or tangent surrounded by identical types |
| 2 | Tangent not part of two in a row |
| 3 | First tangent of exactly two in a row |
| 4 | Second tangent of exactly two in a row |

The order of axis extrema columns determines the indices that composites use to specify axis values, with the negative extremum first, then the positive. Column 0 is axis 0 negative, column 1 is axis 0 positive, and so on.

<a id="anchor-hvgl-part-5"></a>

### Composite Part Data

Composites are made up of subparts, as well as parameters describing how to render those subparts based on the settings of the composite’s own axes. For each subpart, the composite specifies its axis values and an optional transformation. There are master values describing the composite’s appearance when its axes are all set to 0.0, and delta matrices that operate in an analogous way to the delta matrix for a shape.

The parameters can be applied not only to the direct subparts of the composite, but also to *any* subpart in the tree of parts that make up the composite (called the *structure tree*). All references to subparts and to subpart axes are in depth-first order in that tree (excluding the root, the composite itself).

Because of this, the row indices for the axis values range from the first axis of the first (immediate) subpart in depth-first order to the last axis of the last (leaf) subpart in depth-first order. The row indices for rotations and translations range from the offset of the first (immediate) subpart in depth-first order to the offset of the last (leaf) subpart in depth-first order. All matrices have the same number of columns, twice the number of axes of the composite (used in the same way as the delta matrix in shapes). Since these deltas are meant to be applied to the composite’s subparts (immediate and nested), all data starts with the first immediate subpart.

Since the vectors and matrices for all subparts are combined in this way, the axis blend algorithm can be run all at once rather than subpart by subpart. For example, the extremum axis values for all subparts can be computed in one (sparse) matrix-vector multiplication plus addition.

Composite parts must be aligned to a `Float32` boundary. Their layout is considerably more complex than shapes, both because there is more data and because that data is stored in sparse formats. Transforms are decomposed into pure rotations around the origin and pure translations, which are always applied in the order rotation, then translation.

The order of the axis extrema columns in these matrices define the axis indices other composites use to specify axis values, the same as for shapes. Column 0 is axis 0 negative, column 1 is axis 0 positive, and so on.

*Composite header*

| Field | Type | Comment |
| --- | --- | --- |
| Flags | `UInt16` | 0x0001 for composite |
| Number of axes | `UInt16` |  |
| Number of subparts | `UInt16` | Count of direct subparts = size of subpart array |
| Total parts in structure tree | `UInt16` | Number of subparts including root |
| Total axes in structure tree | `UInt16` | Sum of axis count for all nodes including root |
| Maximum number of extremes | `UInt16` | The maximum value of 2×axes across all parts in structure tree |
| Count of master axis values | `UInt16` | Count of non-zero axis value deltas for master |
| Count of extremum axis values | `UInt16` | Count of non-zero axis value deltas for extrema |
| Count of master translations | `UInt16` | Count of non-zero master translations |
| Count of master rotations | `UInt16` | Count of non-zero master rotations |
| Count of extremum translations | `UInt16` | Count of non-zero extremum translations |
| Count of extremum rotations | `UInt16` | Count of non-zero extremum rotations |
| Offset to subpart array/4 | `UInt16` | Byte offset from start of composite, divided by 4 |
| Offset to extremum column starts/4 | `UInt16` | Byte offset from start of composite, divided by 4 |
| Offset to master axis deltas/4 | `UInt16` | Byte offset from start of composite, divided by 4 |
| Offset to extremum axis deltas/4 | `UInt16` | Byte offset from start of composite, divided by 4 |
| Offset to all translations/4 | `UInt16` | Byte offset from start of composite, divided by 4 |
| Offset to all rotations/4 | `UInt16` | Byte offset from start of composite, divided by 4 |

Note that the size of the header is an even number of 16-bit integers, so that the data after the header naturally starts on a 4-byte boundary.

The subpart array stores information for the composite’s *immediate* subparts. Each entry is laid out as follows:

*Subpart array entry*

| Field | Type | Comment |
| --- | --- | --- |
| Part table index | `UInt32` | Index of part that this subpart renders |
| Tree part offset | `UInt16` | Row offset of data in transform vector or matrix |
| Tree axis offset | `UInt16` | Row offset of data in axis value vector or matrix |

Note that the first subpart of the composite always has 0 for both offsets. This array must be on a `UInt32` boundary, and the number of entries is the “number of subparts” from the header.

*Extremum column starts, master row indices, extremum row indices*

| Field | Type | Comment |
| --- | --- | --- |
| Extremum column starts | `[UInt16]` | 2×axes, plus 1 for sentinel |
| Master row indices | `[UInt16]` | Same count as non-zero master axis value deltas |
| Extremum row indices | `[UInt16]` | Same count as non-zero extremum axis value deltas |

The extremum column starts (referenced by the offset in the header) is followed by the master row indices, which is followed by the extremum row indices. This section must be on a `UInt32` boundary.

The master row index list has the same length as the count of non-zero master axis value deltas, and gives the row for each value. It must be in ascending order by row.

The extremum row index list length is the count of non-zero extremum axis value deltas. It must be in ascending order of column index, and for each column with non-zero axis value deltas, the row indices of those non-zero values must be in ascending order.

The extremum column starts gives the offset within the extremum row index list where each column’s data begins. It also has one sentinel value at the end which is the length of the extremum row index list. The length of the extremum column starts list is the number of extrema for the composite (number of columns), plus one for the sentinel. The column starts must be non-decreasing.

Together, the extremum row index list and the extremum column starts list follow the standard CSC (compressed sparse column) sparse matrix format. For example, if there are two axes (four extrema), and there are non-zero values in (row 7, column 0) and (row 2, column 3), then the extremum row index list is \[7, 2\], and the extremum column start list is \[0, 1, 1, 1, 2\]. Columns 1 and 2 have no non-zero entries and so their sections of the extremum row index list are of zero length.

*Master axis value deltas*

| Field | Type | Comment |
| --- | --- | --- |
| Master axis value deltas | `[Float32]` | Same length as master row indices |

This array is at the offset given by “master axis deltas” in the header and must be on a `Float32` boundary. Each value corresponds to the master row index at the same offset.

*Extremum axis value deltas*

| Field | Type | Comment |
| --- | --- | --- |
| Extremum axis value deltas | `[Float32]` | Same length as extremum row indices |

This array is at the offset given by “extremum axis deltas” in the header and must be on a `Float32` boundary. Each value corresponds to the entry at the same offset in the extremum row index list, with the column determined by the column starts.

*Master translation deltas, extremum translation deltas, extremum translation indices, master translation indices (“Translations”)*

| Field | Type | Comment |
| --- | --- | --- |
| Master translation deltas | `[(x: Float32, y: Float32)] ` | length: master translation count |
| Extremum translation deltas | `[(x: Float32, y: Float32)]` | length: extremum translation count |
| Extremum translation indices | `[(row: UInt16, column: UInt16)]` | length: extremum translation count |
| Master translation indices | `[UInt16]` | length: master translation count |

These four arrays begin at the offset given by “all translations” in the header. This section must begin on a `Float32` boundary.

The master translation indices correspond with the master translation deltas, and the extremum translation indices correspond with the extremum translation deltas. The indices must be in ascending order by row, and within row by column.

*Master rotation deltas, extremum rotation deltas, extremum rotation indices, master rotation indices (“Rotations”)*

| Field | Type | Comment |
| --- | --- | --- |
| Master rotation deltas | `[Float32]` | length: master rotation count |
| Extremum rotation deltas | `[Float32]` | length: extremum rotation count |
| Extremum rotation indices | `[(row: UInt16, column: UInt16)]` | length: extremum rotation count |
| Master rotation indices | `[UInt16]` | length: master rotation count |

These four arrays begin at the offset given by “all rotations” in the header. This section must begin on a `Float32` boundary.

The master rotation indices correspond with the master rotation deltas, and the extremum rotation indices correspond with the extremum rotation deltas. As with translations, indices must be in ascending order by row, and within row by column.

Rotations are in radians, measured counterclockwise.

<a id="anchor-hvgl-part-6"></a>

## Platform-specific Information

The `'hvgl'` table is supported on macOS 15.6 and iOS 18.6 onward.

<a id="anchor-hvgl-part-7"></a>

## Dependencies

The `'hvgl'` table refers to glyphs by their part index, which is 32 bits. Currently other tables in sfnt fonts do not support glyph numbers beyond 16 bits.
