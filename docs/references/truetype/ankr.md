---
title: "The 'ankr' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-ankr-acnt"></a>

# The `'ankr'` table

<a id="anchor-ankr-part-1"></a>

## Introduction

The *anchor point table* (tag name: `'ankr'`) provides a way to define *anchor points*—points within the coordinate space of a given glyph independent of the control points used to render the glyph. Anchor points are used in conjunction with the [`'kerx'`](kerx.md).

The `'ankr'` table starts with a header:

*The `'ankr'` table header*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | version | Version number (set to zero) |
| UInt16 | flags | Flags (currently unused; set to zero) |
| UInt32 | lookupTableOffset | Offset to the table's lookup table; currently this is always `0x0000000C` |
| UInt32 | glyphDataTableOffset | Offset to the glyph data table |

The lookup table is a standard AAT lookup table. Values are two-byte offsets from the beginning of the glyph data table to the data for the given glyph. Because 0 is a valid value for such an offset, glyphs without anchor points *must not* be included in the lookup table.

The glyph data table is a series of glyph data entry, one for each glyph with anchor points. Glyph data entries are structured as follows:

*The `'ankr'` table header*

| Type | Name | Description |
| --- | --- | --- |
| UInt32 | numPoints | Number of anchor points for this glyph |
| UInt32\[\] | anchorPoints | Individual anchor points. Each anchor point is a two-byte signed x-coordinate followed by a two-byte signed y-coordinate |

<a id="anchor-ankr-part-2"></a>

## Availability

The `'ankr'` table is supported on OS X 10.9 (Mavericks) and later, and on iOS version 7.0 and later.
