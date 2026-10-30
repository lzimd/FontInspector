---
title: "The 'hvpm' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-hvpm-hvpm"></a>

# The `'hvpm'` table

The `'hvpm'` table allows for part remapping within *HVF*, or Hierarchical Variation Fonts. As the name implies, HVF glyphs comprise components called *composites* that in turn comprise other components. Leaf-level components are called *shapes*; shapes and composites are collectively referred to as *parts*.

The `'hvpm'` table is used in conjunction with an `'hvgl'` table to replace parts by other parts during rendering. Fonts within a `.ttc` collection can share the same `'hvgl'` table but each have a different `'hvpm'` table (or none).

All quantities are little-endian with natural alignment.

<a id="anchor-hvpm-part-1"></a>

### Table header

The table header contains version information, the offset to the index of parts by part number, the total number of parts, and the number of visible parts. Visible parts are always first by part number.

*`'hvpm'` Table Header*

| Field | Type | Comment |
| --- | --- | --- |
| Version | `UInt16` | Currently 1 |
| Flags | `UInt16` | Currently all zero |
| Map subtable offset | `UInt32` | From beginning of hvpm table |

<a id="anchor-hvpm-part-2"></a>

### Mapping subtable

*Subtable header*

| Field | Type | Comment |
| --- | --- | --- |
| Count | `UInt32` | Number of ranges |

The ranges follow immediately in the following format:

| Field | Type | Comment |
| --- | --- | --- |
| Start | `UInt32` | First part ID of range to map |
| End | `UInt32` | Last part ID of range to map |
| Destination | `UInt32` | First part ID to map to |

Any part ID falling within a range will be mapped to `id-Start+Destination`. Any part ID that that does not fall within a range in the map is used unmodified. The ranges must be in ascending order by start and must not overlap.

Any substitute part S mapped from an original part O must be able to use the exact same rendering parameters as O. O and S must be of the same type (shape or composite), and have the same number of axes with the same semantic functions, in the same order. If both S and O are composites, they must have the same number of subparts, and all the above constraints apply recursively down the structure trees of O and S (as described in the `'hvgl'` documentation).

<a id="anchor-hvpm-part-3"></a>

## Platform-specific Information

The `'hvpm'` table is supported on macOS 15.6 and iOS 18.6 onward.

<a id="anchor-hvpm-part-4"></a>

## Dependencies

The `'hvpm'` table works in conjunction with the `'hvgl'` table.
