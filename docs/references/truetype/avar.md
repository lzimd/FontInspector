---
title: "The 'avar' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-avar-avar"></a>

# The `'avar'` table

<a id="anchor-avar-part-1"></a>

## Introduction

In drawing a glyph with variations, the coordinates specified by the user must be mapped from the space defined by the axes' minimum, default, and maximum values into a normalized space of -1.0, 0 and 1.0. The *Axis Variation table* (tag: `'avar'`) allows the font to modify the mapping between axis values and these normalized values, which are represented as `shortFrac` values. The default mapping to normalized coordinates can be represented by the following pseudo-code fragment:

```
if (userValue < axisDefault)
	normalizedValue = (userValue - axisDefault) / (axisDefault - axisMin)
else
	normalizedValue = (userValue - axisDefault) / (axisMax - axisDefault)
```

If there is an Axis Variation table, then the normalized value may then be remapped, allowing the font to specify non-linear changes in how the variations are applied.

- **NOTE**: The material in this chapter only applies to TrueType fonts.

<a id="anchor-avar-part-2"></a>

## Axis Variation Table Formats

The Axis Variation Header is shown in the following table:

| Type | Name | Meaning |
| --- | --- | --- |
| fixed32 | version | Table version; set to 0x00010000. |
| int32 | axisCount | The number of variation axes. |
| shortFracSegment | segment\[axisCount\] | The segment maps for each axis. |

The `shortFracSegment` format is as follows:

| Type | Name | Meaning |
| --- | --- | --- |
| uint16 | pairCount | The number of pairs for this axis. |
| shortFracCorrespondence | correspondence\[pairCount\] | The array of correspondence values. |

The `shortFracCorrespondence` structure is shown in the following table:

| Type | Name | Meaning |
| --- | --- | --- |
| shortFrac | fromCoord | Value in normalized user space. |
| shortFrac | toCoord | Value in normalized axis space. |

The `shortFracSegment` defines a mapping between the user's coordinate (`fromCoord`), and the coordinate along the variation axis (`toCoord`). The mapping is expressed as a series of correspondence points, each pair of which specifies a range in the user's space and a corresponding range in the axis' space. Using this, each value of the user's coordinate is mapped to a corresponding value in the axis' space.

<a id="anchor-avar-part-3"></a>

## Segment Example

Let's look at an example of how this mapping works. The following table shows a set of mapping data that might be present in the `'avar'` table of a font.

| From (user) | To (axis) |
| --- | --- |
| -1.0 | -1.0 |
| -0.75 | -0.5 |
| 0 | 0 |
| 0.4 | 0.4 |
| 0.6 | 0.9 |
| 1.0 | 1.0 |

The following table shows how specified user values would be mapped into axis values, using this `'avar'` data.

| User value | Axis value |
| --- | --- |
| -1.0 | -1.0 |
| -0.75 | -0.5 |
| -0.5 | -0.3333 |
| -0.25 | -0.1667 |
| 0 | 0 |
| 0.25 | 0.25 |
| 0.5 | 0.65 |
| 0.75 | 0.9375 |
| 1.0 | 1.0 |

A segment must always have at least three correspondence pairs: minus one mapping to minus one, zero mapping to zero, and one mapping to one. This implies that a segment may not change the sign of a coordinate value. The segment's pairs must be sorted on `fromCoord`, beginning with -1.0 and ending with 1.0.

**NOTE**: A `shortFrac` is an `int16` with a bias of 14. This means it can represent numbers between 1.999 `(0x7fff)` and -2.0 `(0x8000)`. 1.0 is stored as 16384 `(0x4000)` and -1.0 is stored as -16384 `(0xc000)`.
