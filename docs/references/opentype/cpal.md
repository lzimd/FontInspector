---
title: "CPAL — Color Palette Table"
description: "CPAL - Color Palette Table (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-29T00:00:00Z"
updated_at: "2025-03-19T23:08:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7741ba55884073c5993bb4c2c45859886172ae54/typographydocs/opentype/spec/cpal.md"
last-modified: "2026-09-17T18:19:03Z"
---

<a id="anchor-cpal-cpal-color-palette-table"></a>

# CPAL — Color Palette Table

The palette table is a set of one or more palettes, each containing a predefined number of color records. It may also contain 'name' table IDs describing the palettes and their entries.

Palettes are defined by a set of color records. Each color record specifies a color in the sRGB color space using 8-bit BGRA (blue, green, red, alpha) representation. The sRGB color space is specified in [IEC 61966-2-1:1999 *Multimedia systems and equipment - Colour measurement and management - Part 2-1: Colour management - Default RGB colour space - sRGB*](https://webstore.iec.ch/publication/6169). Details on the specification for the sRGB color space, including the color primaries and “gamma” transfer function, are also provided in [CSS Color Module Level 4, section 10.2](https://www.w3.org/TR/css-color-4/#predefined).

All palettes have the same number of color records, specified by numColorRecords. All color records for all palettes are arranged in a single array, and the color records for any given palette are a contiguous sequence of color records within that array. The first color record of each palette is provided in the colorRecordIndices array.

Multiple colorRecordIndices may refer to the same color record, in which case multiple palettes would use the same color records; hence the number of functionally distinct palettes may be fewer than the numPalettes entry. Also, the sequence of color records for different palettes may overlap, with certain color records shared between multiple palettes. Thus, the total number of color records in the CPAL table may be less than the number of palette entries multiplied by the number of palettes.

The first palette, palette index 0, is the default palette. A minimum of one palette must be provided in the CPAL table if the table is present. Palettes must have a minimum of one color record. An empty CPAL table, with no palettes and no color records is not permitted.

Colors within a palette are referenced by base-zero index. The number of colors in each palette is given by numPaletteEntries. The number of color records in the color records array (numColorRecords) must be greater than or equal to max(colorRecordIndices) + numPaletteEntries.

<a id="anchor-cpal-palette-table-header"></a>

## Palette table header

The CPAL table begins with a header that starts with a version number. Currently, only versions 0 and 1 are defined.

<a id="anchor-cpal-cpal-version-0"></a>

### CPAL version 0

The CPAL header version 0 is organized as follows:

*CPAL version 0*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cpal-version_0"></a>uint16 | version | Table version number (=0). |
| <a id="anchor-cpal-numPaletteEntries_0"></a>uint16 | numPaletteEntries | Number of palette entries in each palette. |
| <a id="anchor-cpal-numPalettes_0"></a>uint16 | numPalettes | Number of palettes in the table. |
| <a id="anchor-cpal-numColorRecords_0"></a>uint16 | numColorRecords | Total number of color records, combined for all palettes. |
| <a id="anchor-cpal-offsetFirstColorRecord_0"></a>Offset32 | colorRecordsArrayOffset | Offset from the beginning of CPAL table to the first ColorRecord. |
| <a id="anchor-cpal-colorRecordIndices_0"></a>uint16 | colorRecordIndices\[numPalettes\] | Index of each palette’s first color record in the combined color record array. |

<a id="anchor-cpal-cpal-version-1"></a>

### CPAL version 1

The CPAL header version 1 adds three additional fields to the end of the table header and is organized as follows:

*CPAL version1*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cpal-version_1"></a>uint16 | version | Table version number (=1). |
| <a id="anchor-cpal-numPalettesEntries_1"></a>uint16 | numPaletteEntries | Number of palette entries in each palette. |
| <a id="anchor-cpal-numPalette_1"></a>uint16 | numPalettes | Number of palettes in the table. |
| <a id="anchor-cpal-numColorRecords_1"></a>uint16 | numColorRecords | Total number of color records, combined for all palettes. |
| <a id="anchor-cpal-offsetFirstColorRecord_1"></a>Offset32 | colorRecordsArrayOffset | Offset from the beginning of CPAL table to the first ColorRecord. |
| <a id="anchor-cpal-colorRecordIndices_1"></a>uint16 | colorRecordIndices\[numPalettes\] | Index of each palette’s first color record in the combined color record array. |
| <a id="anchor-cpal-offsetPaletteTypeArray_1"></a>Offset32 | paletteTypesArrayOffset | Offset from the beginning of CPAL table to the Palette Types Array. Set to 0 if no array is provided. |
| <a id="anchor-cpal-offsetPaletteLabelArray_1"></a>Offset32 | paletteLabelsArrayOffset | Offset from the beginning of CPAL table to the Palette Labels Array. Set to 0 if no array is provided. |
| <a id="anchor-cpal-offsetPaletteEntryLabelArray_1"></a>Offset32 | paletteEntryLabelsArrayOffset | Offset from the beginning of CPAL table to the Palette Entry Labels Array. Set to 0 if no array is provided. |

<a id="anchor-cpal-palette-entries-and-color-records"></a>

## Palette entries and color records

Colors defined in the CPAL table are referenced by a palette index plus a palette-entry index. Indices are base zero. For a given palette index and palette-entry index, an entry within the color records array is derived: *colorRecordIndex = colorRecordIndices\[paletteIndex\] + paletteEntryIndex*.

<a id="anchor-cpal-colorRecArray"></a>

The color records array is comprised of color records:

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cpal-colorRecs"></a>ColorRecord | colorRecords\[numColorRecords\] | Color records for all palettes. |

<a id="anchor-cpal-colorRec"></a>

Each color record has BGRA values. The color space for these values is sRGB.

*ColorRecord*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cpal-blue"></a>uint8 | blue | Blue value (B0). |
| <a id="anchor-cpal-green"></a>uint8 | green | Green value (B1). |
| <a id="anchor-cpal-red"></a>uint8 | red | Red value (B2). |
| <a id="anchor-cpal-alpha"></a>uint8 | alpha | Alpha value (B3). |

The colors in the color record should not be pre-multiplied, and the alpha value should be explicitly set for each palette entry.

An alpha value of zero means no opacity (fully transparent); 255 means opaque (no transparency). The alpha value in the color record may be combined with and does not supersede alpha or opacity attributes set in higher-level contexts.

When placing and registering overlapping elements, there is the possibility of “seaming”, where the edge rendering of one element interferes with another element. This could be more or less visible depending on the contrast of the colors used.

<a id="anchor-cpal-palette-types-array"></a>

## Palette types array

The palette types array is an array of integer values specifying flags for each palette.

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cpal-palTypesArray"></a>uint32 | paletteTypes\[numPalettes\] | Array of 32-bit flag fields that describe properties of each palette. See below for details. |

The following flags are defined:

| Mask | Name | Description |
| --- | --- | --- |
| 0x0001 | USABLE\_WITH\_LIGHT\_BACKGROUND | Bit 0: palette is appropriate to use when displaying the font on a light background such as white. |
| 0x0002 | USABLE\_WITH\_DARK\_BACKGROUND | Bit 1: palette is appropriate to use when displaying the font on a dark background such as black. |
| 0xFFFC | Reserved | Reserved for future use — set to 0. |

The USABLE\_WITH\_LIGHT\_BACKGROUND and USABLE\_WITH\_DARK\_BACKGROUND flags are not mutually exclusive: they may both be set.

<a id="anchor-cpal-palette-labels-array"></a>

## Palette labels array

The palette labels array is an array of integer values specifying ['name'](name.md) table IDs that provide user interface strings associated with each palette. Typically, these will be IDs in the font-specific name ID range.

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cpal-palLabelsArray"></a>uint16 | paletteLabels\[numPalettes\] | Array of 'name' table IDs. Use 0xFFFF for a particular palette if no string is provided. |

<a id="anchor-cpal-palette-entry-label-array"></a>

## Palette entry label array

The palette entry label array is an array of integer values specifying ['name'](name.md) table IDs that provide user interface strings associated with each palette entry. (For example, “Outline”, “Fill”.) This set of palette entry labels applies to all palettes in the font. Typically, the IDs will be in the font-specific name ID range.

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-cpal-palEntryLabelsArray"></a>uint16 | paletteEntryLabels\[numPaletteEntries\] | Array of 'name' table IDs. Use 0xFFFF for a particular entry if no string is provided. |

<a id="anchor-cpal-relationship-to-colr-and-svg-tables"></a>

## Relationship to COLR and SVG tables

Both the [COLR](colr.md) and [SVG](svg.md) tables can use CPAL to define their palettes.

<a id="anchor-cpal-colr-and-cpal"></a>

### COLR and CPAL

In fonts that have a [COLR](colr.md) table, the CPAL table is required, and contains all the font-specified colors used by multicolored glyphs.

As noted in the [COLR](colr.md) table description, the palette entry index of 0xFFFF if specified in the [COLR](colr.md) table represents the foreground color used in the system. This special value does not change across multiple palettes. The maximum palette entry index is 65535 - 1, as the 65536th position is used in the COLR table to indicate the foreground font color.

<a id="anchor-cpal-svg-and-cpal"></a>

### SVG and CPAL

In fonts that have an [SVG](svg.md) table, the CPAL table can be used to contain the values of any color variables used by SVG glyph descriptions in the SVG table. SVG glyph descriptions can also include color specifications directly, however. Thus, the CPAL table is optional for fonts with an SVG table.

Foreground color is expressed by the “currentColor” keyword in the SVG glyph descriptions.

When used with an [SVG](svg.md) table, the default palette’s colors must be set to the same values as the default values for the color variables in the SVG glyph descriptions; this is for text engines that support the SVG table but not color palettes. The SVG glyph descriptions can express their own explicit or “hard-coded” colors as well. These are not related to color variables and thus do not vary by palette selection. See the SVG table specification for more details.

<a id="anchor-cpal-interpolation-of-colors"></a>

### Interpolation of colors

The [SVG](svg.md) table and version 1 of the [COLR](colr.md) table both support color gradient fills. The gradients are defined using color stops to specify color values at specific positions along a color line, with color values for other positions on the color line derived by interpolation.

When interpolating color values, linear interpolation between color stop positions is used. For example, suppose adjacent color stops are specified for positions 0.5 and 0.9 on a color line, and a color value is being calculated for position 0.8. The color value of the first color stop will contribute 75% of the value ((0.8 - 0.5) / (0.9 - 0.5)), and the color value of the second color stop will contribute 25% of the value. Interpolated values at each position of the color line are computed in this way for each of the R, G and B color components.

When interpolating color values, specific aspects of the representation of colors as well as handling of alpha need to be considered.

Representations of sRGB color values are expressed as levels of red, green and blue color “primaries” with specific, absolute chromaticity values, which are defined in the sRGB specification. Color-primary levels can potentially be expressed using a linear-light scale that correlates directly to light energy. (On a linear-light scale, for example, a doubling of a color value would correspond to a doubling of display luminance.) For sRGB, however, standard practice is to represent levels using a scale defined by a non-linear transfer function, sometimes referred to as “gamma”. This transfer function is also defined in the sRGB specification. (See [CSS Color Module Level 4, section 10.2](https://www.w3.org/TR/css-color-4/#predefined) for details.) In the CPAL table, sRGB color values are always specified in terms of the non-linear, sRGB transfer function.

> *Note:* An advantage of representing colors using a non-linear scale is that it allows more effective use of limited bit depth when color-primary levels are represented as integers: smaller differences in light energy can be represented for lower levels than for higher levels. This is beneficial since the human visual system is more sensitive to differences at low luminance levels than to differences at high luminance levels.

When interpolating colors, different results will be obtained if the interpolation is computed using the non-linear scale for color levels than if using the linear-light scale. For interoperable results, whether the non-linear or linear-light scale is to be used needs to be specified.

For gradient color values in the SVG table, the required interpolation behavior is defined in the [Scalable Vector Graphics 1.1 (Second Edition)](http://www.w3.org/TR/SVG11) specification: the [‘color-interpolation’ property](https://www.w3.org/TR/SVG11/painting.html#ColorInterpolationProperty) can be used in an SVG document to declare whether interpolation is done using the non-linear sRGB scale (the default), or using a linear-light scale by applying the inverse sRGB transfer function.

For gradient color values in the COLR table, interpolation must be computed using linear-light values (i.e., after applying the inverse sRGB transfer function).

After an interpolated color value is computed, whether or not the non-linear sRGB transfer function needs to be re-applied is determined by the requirements of the implementation context.

For both the COLR and SVG tables, interpolation must be done with alpha pre-multiplied into each linearized R, G and B component. For alpha specified in a CPAL ColorRecord, the value is converted to a floating value in the range \[0, 1.0\] by dividing by 255, then multiplied into each R, G and B component. In the COLR table, color references in formats used for version 1 include a separate alpha value; that alpha value (with variation, in a variable font) is multiplied into the R, G and B components as well. Interpolated values are then calculated by linear interpolation using these pre-multiplied, linear-light R, G and B values.

> *Note:* Alpha components use a linear scale and can be directly interpolated apart from the R, G and B components without any linearization step.

Once interpolation of the pre-multiplied red, green and blue values and of the alpha value is complete, the red, green and blue results are then un-pre-multiplied by dividing each interpolated value by the corresponding interpolated alpha.

While color values are specified as 8-bit integers, the interpolation computations will require greater precision in each of the linearization, pre-multiply, and interpolation steps. Also, when rendered results are to be presented on an imaging device with known characteristics, visual banding artifacts in a gradient can be minimized by taking full advantage of the color bit depth supported by the device. For instance, if a display supports 10- or 12-bit quantization per color channel, then ideally the ramp of color values in a gradient would use that level of quantization. Other factors from the presentation context may, however, also affect the available capabilities. Therefore, no minimum level of precision is specified as a requirement.
