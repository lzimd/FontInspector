---
title: "The 'sbix' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-sbix-chapterContent"></a>

# The `'sbix'` table

<a id="anchor-sbix-part-1"></a>

## General table information

This table provides access to bitmap data in a standard graphics format (such as PNG, JPEG, TIFF).

The table begins with a header:

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | version | Version number (set to 1) |
| UInt16 | flags | See below |
| UInt32 | numStrikes | Number of bitmap strikes to follow |
| UInt32 | strikeOffset\[numStrikes\] | Offset from begining of table to data for the individual strike |

The only two bits used in the `flags` field are bits 0 and 1. For historical reasons, bit 0 must always be 1. Bit 1 is a `sbixDrawOutlines` flag and is interpreted as follows:

| Binary Value | Description |
| --- | --- |
| 0 | Draw only `'sbix'` bitmaps |
| 1 | Draw both `'sbix'` bitmaps and outlines, in that order |

These bits only have an effect on the rendering of glyphs with at least one bitmap in the `'sbix'` table. Glyphs with no bitmaps at all are always drawn with their outlines (if any).

The other bits in the `flags` field should be set to zero.

<a id="anchor-sbix-part-2"></a>

## Strikes

Each strike data record looks like this:

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | ppem | The PPEM for which this strike was designed (e.g., 9, 12, 24) |
| UInt16 | resolution | The screen resolution (in dpi) for which this strike was designed (e.g., 72) |
| UInt32 | glyphDataOffset\[numGlyphs+1\] | Offset from the beginning of the strike data record to data for the individual glyph |

The length of the data for a given glyph is found by `glyphDataOffset[glyphID+1] - glyphDataOffset[glyphID]`. If this is zero, there is no bitmap data for that glyph in this strike. (This should always be true for non-printing glyphs such as space.)

The data record for the glyph looks like this:

| Type | Name | Description |
| --- | --- | --- |
| SInt16 | originOffsetX | The x-value of the point in the glyph relative to its lower-left corner which corresponds to the origin of the glyph on the screen, that is the point on the baseline at the left edge of the glyph. |
| SInt16 | originOffsetY | The y-value of the point in the glyph relative to its lower-left corner which corresponds to the origin of the glyph on the screen, that is the point on the baseline at the left edge of the glyph. |
| FourCharCode | graphicType | Indicates the type of graphic and relieves clients of the need to parse the graphic data in order to determine the data type. Currently, only `'jpg '`, `'pdf '`, `'png '`, and `'tiff'` are defined. |
| UInt8 | data\[\] | The actual embedded graphic data. The total length is inferred from sequential `glyphDataOffset`s. |

Not every glyph needs to have an entry in every strike in an `'sbix'` table. If a glyph has *no* entry in any strike of an `'sbix'` table, then its outline is drawn.

For example, the Apple Color Emoji font has no bitmap for `U+1F1E6 REGIONAL INDICATOR SYMBOL LETTER A` through `U+1F1FF REGIONAL INDICATOR SYMBOL LETTER Z`. These are therefore drawn with outlines. It does, however, have bitmaps for `U+1F638 GRINNING CAT FACE WITH SMILING EYES`, and that character is therefore drawn with bitmaps.

Note that if *any* strike has a bitmap for a particular glyph, the bitmap for that glyph will *always* be drawn. Whether or not the outline is also drawn (if present) depends on the value of the `flags` field in the header. To use an embedded PDF in an `'sbix'` table, it need therefore be included in only one strike.

<a id="anchor-sbix-part-3"></a>

### Special graphics types

In addition to `graphicType` values indicating a simple graphics image (`'jpg '`, `'pdf '`, `'png '`, and `'tiff'`), there are two special `graphicType` codes.

The special `graphicType` of `'dupe'` indicates that the `data` field contains a two-byte, big-endian glyph ID. The bitmap data for the indicated glyph should be used for the current glyph.

The special `graphicType` of `'mask'` indicates that image is to be rendered with a mask. The data structure that follows looks like this:

| Type | Name | Description |
| --- | --- | --- |
| UInt32 | maskOffset | Offset (from the beginning of the `'sbix'` table) to the mask data |
| FourCharCode | graphicType | Type of the masked graphic data (*not* of the mask). Currently, only `'jpg '`, `'pdf '`, `'png '`, and `'tiff'` are defined. |
| UInt8 | data\[\] | The actual masked graphic data. The total length is inferred from sequential `glyphDataOffset`s. |

The data for the mask is as follows:

| Type | Name | Description |
| --- | --- | --- |
| UInt32 | maskLength | Length of the mask data (including this header) |
| UInt16 | reserved | Currently unused; set to 0. |
| UInt16 | blendingMode | Indicates how the mask is to be applied. |
| SInt16 | originOffsetX | The horizontal (*x*-axis) position of the left edge of the bitmap graphic in relation to the glyph design space origin. |
| SInt16 | originOffsetY | The vertical (*y*-axis) position of the left edge of the bitmap graphic in relation to the glyph design space origin. |
| FourCharCode | graphicType | Indicates the graphic type of the mask and relieves clients of the need to parse the graphic data in order to determine the data type. Currently, only `'jpg '`, `'png '`, and `'tiff'` are defined. |
| UInt8 | data\[\] | The actual embedded mask data. |

The `originOffsetX` and `originOffsetY` values give the placement of the bitmap graphic in relation to the standard coordinate system of the glyph design space. For example, if `originOffsetX` equals 20, the left edge of the bitmap is place 20 units to the right of the origin; if `originOffsetY` equals -30, then the bottom edge of the graphic is 30 FUnits below the origin.

When placing the graphic within the line of text, the placement depends upon whether there are contours in the `'glyf'` table for the current glyph ID:

- If there *is no* glyph contour, the glyph design space origin for the graphic is placed at the starting drawing position for this glyph. The `lsb` value for the current glyph ID from the `'hmtx` table has no effect.
- If there *is* a glyph contour, the glyph design space origin for the graphic is placed at the lower left corner of the glyph bounding box `(xMin, yMin)`.

There are five values defined for the `blendingMode`:

| Name | Value | Description |
| --- | --- | --- |
| sbixBlendModeMultiply | 0 | Multiplies the source image samples with the background image samples. This results in colors that are at least as dark as either of the two contributing sample colors. |
| sbixBlendModeDarken | 1 | Creates the composite image samples by choosing the darker samples (either from the source image or the background). The result is that the background image samples are replaced by any source image samples that are darker. Otherwise, the background image samples are left unchanged. |
| sbixBlendModeHardLight | 2 | Either multiplies or screens colors, depending on the source image sample color. If the source image sample color is lighter than 50% gray, the background is lightened, similar to screening. If the source image sample color is darker than 50% gray, the background is darkened, similar to multiplying. If the source image sample color is equal to 50% gray, the source image is not changed. Image samples that are equal to pure black or pure white result in pure black or white. The overall effect is similar to what you’d achieve by shining a harsh spotlight on the source image. Use this to add highlights to a glyph. |
| sbixBlendModeSourceAtop | 3 | `R = S*Da + D*(1 - Sa)` |
| sbixBlendModeXOR | 4 | `R = S*(1 - Da) + D*(1 - Sa)`. This XOR mode is only nominally related to the classical bitmap XOR operation. |

The `sbixBlendModeSourceAtop` and `sbixBlendModeXOR` blend mode constants represent Porter-Duff blend modes. The symbols in the equations for these blend modes are:

- R is the premultiplied result
- S is the source color, and includes alpha
- D is the destination color, and includes alpha
- Ra, Sa, and Da are the alpha components of R, S, and D

You can find more information on blend modes, including examples of images produced using them, and many mathematical descriptions of the modes, in *PDF Reference, Fourth Edition*, Version 1.5, Adobe Systems, Inc. If you are a former QuickDraw developer, it may be helpful for you to think of blend modes as an alternative to transfer modes.

<a id="anchor-sbix-part-4"></a>

## Platform-specific Information

The `'sbix'` table is supported in macOS 10.7 (Lion) and later.

The `'dupe'` data type is available in macOS 10.9 (Mavericks) or iOS 7 and later.

Both are supported on all versions of ipadOS, watchOS, and tvOS.

Support for the `'pdf '` and `'mask'` data types and `sbixDrawOutlines` flag are planned for future releases of iOS and macOS.

<a id="anchor-sbix-part-5"></a>

## Dependencies

The glyph count is derived from the [`'maxp'` (Maximum Profile) table](bhed.md).

Overall glyph metrics (left side bearing, advance) are stored in the [`'hmtx'` (Horizontal Metrics) table.](bhed.md)
