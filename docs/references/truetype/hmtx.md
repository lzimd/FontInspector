---
title: "The 'hmtx' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-hmtx-hmtx"></a>

# The `'hmtx'` table

<a id="anchor-hmtx-part-1"></a>

## General table information

The `'hmtx'` table contains metric information for the horizontal layout each of the glyphs in the font. It begins with the *hMetrics* array. Each element in this array has two parts: the advance width and left side bearing. The value *numOfLongHorMetrics* is taken from the [`'hhea'` (Horizontal Header) table](hhea.md). In a monospaced font, only one entry is required but that entry may not be omitted.

Optionally, an array of left side bearings follows. Generally, this array of left side bearings is used for a run of monospaced glyphs. For example, it might be used for a Kanji font or for Courier. Only one such run is allowed per font. It must be at the end of the table. The corresponding glyphs are assumed to have the same advance width as that found in the last entry in the *hMetrics* array. Since there must be a left side bearing and an advance width associated with each glyph in the font, the number of entries in this array is derived from the total number of glyphs in the font minus the value *numOfLongHorMetrics*.

A longHorMetric is defined by the C structure shown here:

```
struct {
	uint16 advanceWidth;
	int16 leftSideBearing;
}
```

**Table 24** : `'hmtx'` table

| Type | Name | Description |
| --- | --- | --- |
| longHorMetric | hMetrics\[numOfLongHorMetrics\] | The value numOfLongHorMetrics comes from the [`'hhea'`](hhea.md) table. If the font is monospaced, only one entry need be in the array but that entry is required. |
| FWord | leftSideBearing\[\] | Here the advanceWidth is assumed to be the same as the advanceWidth for the last entry above. The number of entries in this array is derived from the total number of glyphs minus numOfLongHorMetrics. This generally is used with a run of monospaced glyphs (e.g. Kanji fonts or Courier fonts). Only one run is allowed and it must be at the end. |

---

---

<a id="anchor-hmtx-part-2"></a>

## Dependencies

The value of the *numOfLongHorMetrics* field is found in the [`'hhea'` (Horizontal Header) table](hhea.md). Fonts that lack an [`'hhea'`](hhea.md) table must not have an `'hmtx'` table.

Other tables may have information duplicating data contained in the `'hmtx'` table. For example, glyph metrics can also be found in the [`'hdmx'` (Horizontal Device Metrics) table](hdmx.md) and [`'bloc'` (Bitmap Location) table](bloc.md). There is naturally no requirement that the ideal metrics of the 'hmtx' table be perfectly consistent with the device metrics found in other tables, but care should be taken that they are not significantly inconsistent.

<a id="anchor-hmtx-part-3"></a>

## Tools

ftxdumperfuser automatically updates the [`'hhea'`](hhea.md) table whenever the `'hmtx'` table is updated.

Care must be taken when using ftxdumperfuser to fuse in both the [`'hhea'`](hhea.md) table and the `'hmtx'` table of the same font. They should be fused in the order `'hhea'`-`'hmtx'` to make sure that the `numOfLongHorMetrics` field of the [`'hhea'`](hhea.md) table is valid. ftxdumperfuser allows the `numOfLongHorMetrics` field to be omitted from the XML source when fusing in an [`'hhea'`](hhea.md) table in order to prevent its accidental corruption.
