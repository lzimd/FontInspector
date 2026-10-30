---
title: "OS/2 — OS/2 and Windows Metrics Table"
description: "The OS/2 and Windows metrics table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-29T00:00:00Z"
updated_at: "2025-03-20T21:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7d4f69a958353ed113017d0e707cbd183de5a949/typographydocs/opentype/spec/os2.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-os2-os2-os2-and-windows-metrics-table"></a>

# OS/2 — OS/2 and Windows Metrics Table

The OS/2 table consists of a set of metrics and other data that are required in OpenType fonts.

<a id="anchor-os2-os2-table-formats"></a>

## OS/2 Table Formats

Six versions of the OS/2 table have been defined: versions 0 to 5. All versions are supported, but use of version 4 or later is strongly recommended.

<a id="anchor-os2-version-5"></a>

### Version 5

The format of version 5 is as follows:

| Type | Name | Comments |
| --- | --- | --- |
| uint16 | [version](#anchor-os2-version) | 0x0005 |
| FWORD | [xAvgCharWidth](#anchor-os2-xavgcharwidth) |  |
| uint16 | [usWeightClass](#anchor-os2-usweightclass) |  |
| uint16 | [usWidthClass](#anchor-os2-uswidthclass) |  |
| uint16 | [fsType](#anchor-os2-fstype) |  |
| FWORD | [ySubscriptXSize](#anchor-os2-ysubscriptxsize) |  |
| FWORD | [ySubscriptYSize](#anchor-os2-ysubscriptysize) |  |
| FWORD | [ySubscriptXOffset](#anchor-os2-ysubscriptxoffset) |  |
| FWORD | [ySubscriptYOffset](#anchor-os2-ysubscriptyoffset) |  |
| FWORD | [ySuperscriptXSize](#anchor-os2-ysuperscriptxsize) |  |
| FWORD | [ySuperscriptYSize](#anchor-os2-ysuperscriptysize) |  |
| FWORD | [ySuperscriptXOffset](#anchor-os2-ysuperscriptxoffset) |  |
| FWORD | [ySuperscriptYOffset](#anchor-os2-ysuperscriptyoffset) |  |
| FWORD | [yStrikeoutSize](#anchor-os2-ystrikeoutsize) |  |
| FWORD | [yStrikeoutPosition](#anchor-os2-ystrikeoutposition) |  |
| int16 | [sFamilyClass](#anchor-os2-sfamilyclass) |  |
| uint8 | [panose\[10\]](#anchor-os2-panose) |  |
| uint32 | [ulUnicodeRange1](#anchor-os2-ulunicoderange) | Bits 0 – 31 |
| uint32 | [ulUnicodeRange2](#anchor-os2-ulunicoderange) | Bits 32 – 63 |
| uint32 | [ulUnicodeRange3](#anchor-os2-ulunicoderange) | Bits 64 – 95 |
| uint32 | [ulUnicodeRange4](#anchor-os2-ulunicoderange) | Bits 96 – 127 |
| Tag | [achVendID](#anchor-os2-achvendid) |  |
| uint16 | [fsSelection](#anchor-os2-fsselection) |  |
| uint16 | [usFirstCharIndex](#anchor-os2-usfirstcharindex) |  |
| uint16 | [usLastCharIndex](#anchor-os2-uslastcharindex) |  |
| FWORD | [sTypoAscender](#anchor-os2-stypoascender) |  |
| FWORD | [sTypoDescender](#anchor-os2-stypodescender) |  |
| FWORD | [sTypoLineGap](#anchor-os2-stypolinegap) |  |
| UFWORD | [usWinAscent](#anchor-os2-uswinascent) |  |
| UFWORD | [usWinDescent](#anchor-os2-uswindescent) |  |
| uint32 | [ulCodePageRange1](#anchor-os2-ulcodepagerange) | Bits 0 – 31 |
| uint32 | [ulCodePageRange2](#anchor-os2-ulcodepagerange) | Bits 32 – 63 |
| FWORD | [sxHeight](#anchor-os2-sxheight) |  |
| FWORD | [sCapHeight](#anchor-os2-scapheight) |  |
| uint16 | [usDefaultChar](#anchor-os2-usdefaultchar) |  |
| uint16 | [usBreakChar](#anchor-os2-usbreakchar) |  |
| uint16 | [usMaxContext](#anchor-os2-usmaxcontext) |  |
| uint16 | [usLowerOpticalPointSize](#anchor-os2-usloweropticalpointsize) |  |
| uint16 | [usUpperOpticalPointSize](#anchor-os2-usupperopticalpointsize) |  |

<a id="anchor-os2-version-4"></a>

### Version 4

Version 4 was defined in OpenType 1.5. Version 4 has two fewer fields than version 5, and the same fields as in version 3. Although new fields were not added beyond those in version 3, the specification of certain fields was revised. The format of version 4 is as follows:

| Type | Name |
| --- | --- |
| uint16 | [version](#anchor-os2-version) |
| FWORD | [xAvgCharWidth](#anchor-os2-xavgcharwidth) |
| uint16 | [usWeightClass](#anchor-os2-usweightclass) |
| uint16 | [usWidthClass](#anchor-os2-uswidthclass) |
| uint16 | [fsType](#anchor-os2-fstype) |
| FWORD | [ySubscriptXSize](#anchor-os2-ysubscriptxsize) |
| FWORD | [ySubscriptYSize](#anchor-os2-ysubscriptysize) |
| FWORD | [ySubscriptXOffset](#anchor-os2-ysubscriptxoffset) |
| FWORD | [ySubscriptYOffset](#anchor-os2-ysubscriptyoffset) |
| FWORD | [ySuperscriptXSize](#anchor-os2-ysuperscriptxsize) |
| FWORD | [ySuperscriptYSize](#anchor-os2-ysuperscriptysize) |
| FWORD | [ySuperscriptXOffset](#anchor-os2-ysuperscriptxoffset) |
| FWORD | [ySuperscriptYOffset](#anchor-os2-ysuperscriptyoffset) |
| FWORD | [yStrikeoutSize](#anchor-os2-ystrikeoutsize) |
| FWORD | [yStrikeoutPosition](#anchor-os2-ystrikeoutposition) |
| int16 | [sFamilyClass](#anchor-os2-sfamilyclass) |
| uint8 | [panose\[10\]](#anchor-os2-panose) |
| uint32 | [ulUnicodeRange1](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange2](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange3](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange4](#anchor-os2-ulunicoderange) |
| Tag | [achVendID](#anchor-os2-achvendid) |
| uint16 | [fsSelection](#anchor-os2-fsselection) |
| uint16 | [usFirstCharIndex](#anchor-os2-usfirstcharindex) |
| uint16 | [usLastCharIndex](#anchor-os2-uslastcharindex) |
| FWORD | [sTypoAscender](#anchor-os2-stypoascender) |
| FWORD | [sTypoDescender](#anchor-os2-stypodescender) |
| FWORD | [sTypoLineGap](#anchor-os2-stypolinegap) |
| UFWORD | [usWinAscent](#anchor-os2-uswinascent) |
| UFWORD | [usWinDescent](#anchor-os2-uswindescent) |
| uint32 | [ulCodePageRange1](#anchor-os2-ulcodepagerange) |
| uint32 | [ulCodePageRange2](#anchor-os2-ulcodepagerange) |
| FWORD | [sxHeight](#anchor-os2-sxheight) |
| FWORD | [sCapHeight](#anchor-os2-scapheight) |
| uint16 | [usDefaultChar](#anchor-os2-usdefaultchar) |
| uint16 | [usBreakChar](#anchor-os2-usbreakchar) |
| uint16 | [usMaxContext](#anchor-os2-usmaxcontext) |

<a id="anchor-os2-version-3"></a>

### Version 3

Version 3 was defined in OpenType 1.4. Version 3 has the same fields as in version 4, and as in version 2. Although new fields were not added beyond those in version 2, the specification of certain fields was revised to reflect changes in Unicode 3.2. The format of version 3 is identical to the format for version 4, given above.

<a id="anchor-os2-version-2"></a>

### Version 2

Version 2 was defined in OpenType 1.1. Version 2 has the same fields as in version 3, and five additional fields beyond those in version 1. The format of version 2 is identical to the format for version 4, given above.

<a id="anchor-os2-version-1"></a>

### Version 1

Version 1 was defined in TrueType revision 1.66. Version 1 has five fewer fields than version 2, and two additional fields beyond those in version 0. The format of version 1 is as follows:

| Type | Name |
| --- | --- |
| uint16 | [version](#anchor-os2-version) |
| FWORD | [xAvgCharWidth](#anchor-os2-xavgcharwidth) |
| uint16 | [usWeightClass](#anchor-os2-usweightclass) |
| uint16 | [usWidthClass](#anchor-os2-uswidthclass) |
| uint16 | [fsType](#anchor-os2-fstype) |
| FWORD | [ySubscriptXSize](#anchor-os2-ysubscriptxsize) |
| FWORD | [ySubscriptYSize](#anchor-os2-ysubscriptysize) |
| FWORD | [ySubscriptXOffset](#anchor-os2-ysubscriptxoffset) |
| FWORD | [ySubscriptYOffset](#anchor-os2-ysubscriptyoffset) |
| FWORD | [ySuperscriptXSize](#anchor-os2-ysuperscriptxsize) |
| FWORD | [ySuperscriptYSize](#anchor-os2-ysuperscriptysize) |
| FWORD | [ySuperscriptXOffset](#anchor-os2-ysuperscriptxoffset) |
| FWORD | [ySuperscriptYOffset](#anchor-os2-ysuperscriptyoffset) |
| FWORD | [yStrikeoutSize](#anchor-os2-ystrikeoutsize) |
| FWORD | [yStrikeoutPosition](#anchor-os2-ystrikeoutposition) |
| int16 | [sFamilyClass](#anchor-os2-sfamilyclass) |
| uint8 | [panose\[10\]](#anchor-os2-panose) |
| uint32 | [ulUnicodeRange1](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange2](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange3](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange4](#anchor-os2-ulunicoderange) |
| Tag | [achVendID](#anchor-os2-achvendid) |
| uint16 | [fsSelection](#anchor-os2-fsselection) |
| uint16 | [usFirstCharIndex](#anchor-os2-usfirstcharindex) |
| uint16 | [usLastCharIndex](#anchor-os2-uslastcharindex) |
| FWORD | [sTypoAscender](#anchor-os2-stypoascender) |
| FWORD | [sTypoDescender](#anchor-os2-stypodescender) |
| FWORD | [sTypoLineGap](#anchor-os2-stypolinegap) |
| UFWORD | [usWinAscent](#anchor-os2-uswinascent) |
| UFWORD | [usWinDescent](#anchor-os2-uswindescent) |
| uint32 | [ulCodePageRange1](#anchor-os2-ulcodepagerange) |
| uint32 | [ulCodePageRange2](#anchor-os2-ulcodepagerange) |

<a id="anchor-os2-version-0"></a>

### Version 0

Version 0 was defined in TrueType revision 1.5. The format of version 0 is as follows:

| Type | Name |
| --- | --- |
| uint16 | [version](#anchor-os2-version) |
| FWORD | [xAvgCharWidth](#anchor-os2-xavgcharwidth) |
| uint16 | [usWeightClass](#anchor-os2-usweightclass) |
| uint16 | [usWidthClass](#anchor-os2-uswidthclass) |
| uint16 | [fsType](#anchor-os2-fstype) |
| FWORD | [ySubscriptXSize](#anchor-os2-ysubscriptxsize) |
| FWORD | [ySubscriptYSize](#anchor-os2-ysubscriptysize) |
| FWORD | [ySubscriptXOffset](#anchor-os2-ysubscriptxoffset) |
| FWORD | [ySubscriptYOffset](#anchor-os2-ysubscriptyoffset) |
| FWORD | [ySuperscriptXSize](#anchor-os2-ysuperscriptxsize) |
| FWORD | [ySuperscriptYSize](#anchor-os2-ysuperscriptysize) |
| FWORD | [ySuperscriptXOffset](#anchor-os2-ysuperscriptxoffset) |
| FWORD | [ySuperscriptYOffset](#anchor-os2-ysuperscriptyoffset) |
| FWORD | [yStrikeoutSize](#anchor-os2-ystrikeoutsize) |
| FWORD | [yStrikeoutPosition](#anchor-os2-ystrikeoutposition) |
| int16 | [sFamilyClass](#anchor-os2-sfamilyclass) |
| uint8 | [panose\[10\]](#anchor-os2-panose) |
| uint32 | [ulUnicodeRange1](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange2](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange3](#anchor-os2-ulunicoderange) |
| uint32 | [ulUnicodeRange4](#anchor-os2-ulunicoderange) |
| Tag | [achVendID](#anchor-os2-achvendid) |
| uint16 | [fsSelection](#anchor-os2-fsselection) |
| uint16 | [usFirstCharIndex](#anchor-os2-usfirstcharindex) |
| uint16 | [usLastCharIndex](#anchor-os2-uslastcharindex) |
| FWORD | [sTypoAscender](#anchor-os2-stypoascender) |
| FWORD | [sTypoDescender](#anchor-os2-stypodescender) |
| FWORD | [sTypoLineGap](#anchor-os2-stypolinegap) |
| UFWORD | [usWinAscent](#anchor-os2-uswinascent) |
| UFWORD | [usWinDescent](#anchor-os2-uswindescent) |

> *Note:* Documentation for OS/2 version 0 in [Apple’s TrueType Reference Manual](https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6OS2.html) stops at the usLastCharIndex field and does not include the last five fields of the table as it was defined by Microsoft. Some legacy TrueType fonts could have been built with a shortened version 0 OS/2 table. Applications should check the table length for a version 0 OS/2 table before reading these fields.

<a id="anchor-os2-os2-field-details"></a>

## OS/2 Field Details

This section provides details covering all versions of the OS/2 table.

<a id="anchor-os2-version"></a>

### version

|  |  |
| --- | --- |
| Format: | uint16 |
| Units: | n/a |
| Title: | OS/2 table version number. |
| Description: | The version number for the OS/2 table: 0x0000 to 0x0005. |
| Comments: | The version number allows for identification of the precise contents and layout for the OS/2 table. |

<a id="anchor-os2-xavgcharwidth"></a>

### xAvgCharWidth

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Average weighted escapement. |
| Description: | The Average Character Width field specifies the arithmetic average of the escapement (width) of all non-zero width glyphs in the font. |
| Comments: | The value for xAvgCharWidth is calculated by obtaining the arithmetic average of the width of all non-zero width glyphs in the font. It is strongly recommended that implementers do not rely on this value for computing layout for lines of text, especially for cases where complex scripts are used.<br><br> *Note:* Some fonts have xAvgCharWidth values that do not conform to this calculation. Fonts could have been originally created with a version 0 to version 2 OS/2 table using the legacy calculation described below, then later updated with a newer OS/2 table version but without changing the xAvgCharWidth value. In some CJK fonts, the xAvgCharWidth can be almost half the value that would be expected by the above calculation. Applications should not use xAvgCharWidth for determining actual glyph advance widths. |
| Version differences: | Versions 0 to 2: When first defined, the specification was biased toward Basic Latin characters, and it was thought that the xAvgCharWidth value could be used to estimate the average length of lines of text. The following formula for calculating xAvgCharWidth was provided: For characters given in the table below, sum the width of each character times the weight factor indicated, then divide the total by 1000. This method of calculating the value of this field was superseded with the introduction of version 3 of the OS/2 table and is deprecated.<br>[See table](#nested-os2-1) |

<a id="nested-os2-1"></a>

The following table was originally nested in row 6, cell 2 of the table above.

| Letter | Weight factor | Letter | Weight factor |
| --- | --- | --- | --- |
| a | 64 | o | 56 |
| b | 14 | p | 17 |
| c | 27 | q | 4 |
| d | 35 | r | 49 |
| e | 100 | s | 56 |
| f | 20 | t | 71 |
| g | 14 | u | 31 |
| h | 42 | v | 10 |
| i | 63 | w | 18 |
| j | 3 | x | 3 |
| k | 6 | y | 18 |
| l | 35 | z | 2 |
| m | 20 | space | 166 |
| n | 56 |  |  |

<a id="anchor-os2-usweightclass"></a>

### usWeightClass

|  |  |
| --- | --- |
| Format: | uint16 |
| Title: | Weight class. |
| Description: | Indicates the visual weight (degree of blackness or thickness of strokes) of the characters in the font. Values from 1 to 1000 are valid. |
| Comments: | usWeightClass values use the same scale as the 'wght' axis that is used in the ['fvar'](fvar.md) table of variable fonts and in the [STAT](stat.md) table. While integer values from 1 to 1000 are supported, some legacy platforms could have limitations on supported values. The following are commonly used values:<br>[See table](#nested-os2-2) |

<a id="nested-os2-2"></a>

The following table was originally nested in row 4, cell 2 of the table above.

| Value | Description | C Definition (from windows.h) |
| --- | --- | --- |
| 100 | Thin | FW\_THIN |
| 200 | Extra-light (Ultra-light) | FW\_EXTRALIGHT |
| 300 | Light | FW\_LIGHT |
| 400 | Normal (Regular) | FW\_NORMAL |
| 500 | Medium | FW\_MEDIUM |
| 600 | Semi-bold (Demi-bold) | FW\_SEMIBOLD |
| 700 | Bold | FW\_BOLD |
| 800 | Extra-bold (Ultra-bold) | FW\_EXTRABOLD |
| 900 | Black (Heavy) | FW\_BLACK |

<a id="anchor-os2-uswidthclass"></a>

### usWidthClass

|  |  |
| --- | --- |
| Format: | uint16 |
| Title: | Width class. |
| Description: | Indicates a relative change from the normal aspect ratio (width to height ratio) as specified by a font designer for the glyphs in a font. |
| Comments: | Although every glyph in a font can have a different numeric aspect ratio, each glyph in a font of normal width is considered to have a relative aspect ratio of one. When a new type style is created of a different width class (either by a font designer or by some automated means) the relative aspect ratio of the glyphs in the new font is some percentage greater or less than the corresponding glyphs in the normal font — it is this difference that this field specifies. <br><br> The valid usWidthClass values are shown in the following table. Note that the usWidthClass values are related to but distinct from the scale for the 'wdth' axis that is used in the ['fvar'](fvar.md) table of variable fonts and in the [STAT](stat.md) table. The “% of normal” column in the following table provides a mapping from usWidthClass values 1 – 9 to 'wdth' values.<br>[See table](#nested-os2-3) |

<a id="nested-os2-3"></a>

The following table was originally nested in row 4, cell 2 of the table above.

| Value | Description | C Definition | % of normal |
| --- | --- | --- | --- |
| 1 | Ultra-condensed | FWIDTH\_ULTRA\_CONDENSED | 50 |
| 2 | Extra-condensed | FWIDTH\_EXTRA\_CONDENSED | 62.5 |
| 3 | Condensed | FWIDTH\_CONDENSED | 75 |
| 4 | Semi-condensed | FWIDTH\_SEMI\_CONDENSED | 87.5 |
| 5 | Medium (normal) | FWIDTH\_NORMAL | 100 |
| 6 | Semi-expanded | FWIDTH\_SEMI\_EXPANDED | 112.5 |
| 7 | Expanded | FWIDTH\_EXPANDED | 125 |
| 8 | Extra-expanded | FWIDTH\_EXTRA\_EXPANDED | 150 |
| 9 | Ultra-expanded | FWIDTH\_ULTRA\_EXPANDED | 200 |

<a id="anchor-os2-fstype"></a>

### fsType

|  |  |
| --- | --- |
| Format: | uint16 |
| Title: | Type flags. |
| Description: | Indicates font embedding licensing rights for the font. The interpretation of flags is as follows:<a id="anchor-os2-fst_0"></a><br>[See table](#nested-os2-4) |
| Comments: | Embeddable fonts may be stored in a document. When a document with embedded fonts is opened on a system that does not have the font installed (the remote system), the embedded font may be loaded for temporary (and in some cases, permanent) use on that system by an embedding-aware application. Embedding licensing rights are granted by the vendor of the font. <br><br> *Applications that implement support for font embedding must not embed fonts which are not licensed to permit embedding. Also, when embedding a font into a document, applications must not modify the embedding permissions and restrictions indicated in this field. In addition, applications loading embedded fonts for temporary use (Preview & Print or Editable embedding) **must** delete the fonts when the document containing the embedded font is closed.* <br><br> Bits 0 to 3 (the embedding permissions sub-field) are mutually exclusive: fonts should never have more than one of these bits set. Note that, if two or more bits are set, some applications could assume the *least-restrictive permission indicated*. (See version differences for more discussion.) *Caution:* Font vendors are responsible to set these bits correctly to obtain the desired application behaviors. For Restricted License embedding to take effect, the Embedding permissions sub-field must have the value 2 (that is, only bit 1 is set). <br><br> *Note:* [Apple’s TrueType Reference Manual](https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6OS2.html) specifies bit 1 of the fsType field, and only bit 1, as having an assigned semantic. This originated from a pre-release draft specification for the OS/2 table. However, the final specification for version 0 of the OS/2 table defined bits 0 to 3. Also, some early font implementations mistakenly used *the value 1* (bit 0 set), leading to problems of non-interoperability. For this reason, bit 0 was specified as reserved in the final specification for version 0. Bit 0 is permanently reserved, and its use is deprecated. |
| Version differences: | **Versions 0 to 1:** only bits 0 to 3 were assigned. Applications must ignore bits 4 to 15 when reading a version 0 or version 1 table. <br><br> **Versions 0 to 2:** The specification for versions 0 to 2 did not specify that bits 0 to 3 must be mutually exclusive. Rather, those specifications stated that, in the event that more than one of bits 0 to 3 are set in a given font, then the *least-restrictive permission indicated take precedence*. In particular, some fonts using a version 0 to version 2 OS/2 table have both bit 2 and bit 3 set with the intent to indicate both preview/print and edit permissions. Applications are permitted to use this behavior for fonts with a version 0 to version 2 OS/2 table. <br><br> **Versions 3 and later:** The specification for version 3, added in OpenType 1.4, introduced the explicit requirement that bits 0 to 3 must be mutually exclusive. |

<a id="nested-os2-4"></a>

The following table was originally nested in row 3, cell 2 of the table above.

| Bits | Mask | Description |
| --- | --- | --- |
| 0 – 3 | 0x000F | Usage permissions. Valid fonts must set at most one of bits 1, 2 or 3; bit 0 is permanently reserved and must be zero. Valid values for this sub-field are 0, 2, 4 or 8. The meaning of these values is as follows: <br><br> **0:** Installable embedding: the font may be embedded, and may be permanently installed for use on a remote systems, or for use by other users. The user of the remote system acquires the identical rights, obligations and licenses for that font as the original purchaser of the font, and is subject to the same end-user license agreement, copyright, design patent, and/or trademark as was the original purchaser. <br><br> **2:** Restricted License embedding: the font must not be modified, embedded or exchanged in any manner without first obtaining explicit permission of the legal owner. <br><br> **4:** Preview & Print embedding: the font may be embedded, and may be temporarily loaded on other systems for purposes of viewing or printing the document. Documents containing Preview & Print fonts must be opened “read-only”; no edits may be applied to the document. <br><br> **8:** Editable embedding: the font may be embedded, and may be temporarily loaded on other systems. As with Preview & Print embedding, documents containing Editable fonts may be opened for reading. In addition, editing is permitted, including ability to format new text using the embedded font, and changes may be saved. |
| 4 – 7 | 0x00F0 | Reserved, must be zero. |
| <a id="anchor-os2-fst_bit8"></a>8 | 0x0100 | No subsetting: When this bit is set, the font must not be subsetted prior to embedding. Other embedding restrictions specified in bits 0 – 3 and bit 9 also apply. |
| <a id="anchor-os2-fst_bit9"></a>9 | 0x0200 | Bitmap embedding only: When this bit is set, only bitmaps contained in the font may be embedded. No outline data may be embedded. If there are no bitmaps available in the font, then the font is considered unembeddable and the embedding services will fail. Other embedding restrictions specified in bits 0-3 and 8 also apply. |
| 10 – 15 | 0xFC00 | Reserved, must be zero. |

<a id="anchor-os2-ysubscriptxsize"></a>

### ySubscriptXSize

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Subscript horizontal font size. |
| Description: | The recommended horizontal size in font design units for subscripts for this font. Should be \> 0. |
| Comments: | If a font has two recommended sizes for subscripts, e.g., numerics and other, the numeric sizes should be stressed. This size field maps to the em size of the font being used for a subscript. The horizontal font size specifies a font designer’s recommended horizontal size of subscript glyphs associated with this font. If a font does not include all required subscript glyphs for an application, and the application can substitute glyphs by scaling the glyphs of a font or by substituting glyphs from another font, this field specifies the recommended nominal width for those subscript glyphs. <br><br> For example, if the em for a font is 2048 units and ySubScriptXSize is set to 205, then the horizontal size for a simulated subscript glyph would be 1/10th the size of the normal glyph. <br><br>*Note:* This was implemented in the OS/2 platform as a signed value, even though only values \> 0 would be expected. |

<a id="anchor-os2-ysubscriptysize"></a>

### ySubscriptYSize

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Subscript vertical font size. |
| Description: | The recommended vertical size in font design units for subscripts for this font. Should be \> 0. |
| Comments: | If a font has two recommended sizes for subscripts, e.g. numerics and other, the numeric sizes should be stressed. This size field maps to the em size of the font being used for a subscript. The vertical font size specifies a font designer’s recommendation for vertical size of subscript glyphs associated with this font. If a font does not include all required subscript glyphs for an application, and the application can substitute glyphs by scaling the glyphs in a font or by substituting glyphs from another font, this field specifies the recommended nominal height for those subscript glyphs. <br><br> For example, if the em for a font is 2048 units and ySubScriptYSize is set to 205, then the vertical size for a simulated subscript glyph would be 1/10th the size of the normal glyph. <br><br>*Note:* This was implemented in the OS/2 platform as a signed value, even though only values \> 0 would be expected. |

<a id="anchor-os2-ysubscriptxoffset"></a>

### ySubscriptXOffset

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Subscript x offset. |
| Description: | The recommended horizontal offset in font design units for subscripts for this font. |
| Comments: | The ySubscriptXOffset field specifies a font designer’s recommended horizontal offset — from the glyph origin to the glyph origin of the subscript’s glyph — for subscript glyphs associated with this font. If a font does not include all required subscript glyphs for an application, and the application can substitute glyphs, this field specifies the recommended horizontal position from the glyph escapement point of the last glyph before the first subscript glyph. For upright glyphs, this value is usually zero; however, if the glyphs of a font have an incline (italic or slant), the reference point for subscript glyphs is usually adjusted to compensate for the angle of incline. |

<a id="anchor-os2-ysubscriptyoffset"></a>

### ySubscriptYOffset

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Subscript y offset. |
| Description: | The recommended vertical offset in font design units from the baseline for subscripts for this font. |
| Comments: | The ySubscriptYOffset field specifies a font designer’s recommended vertical offset from the glyph baseline to the glyph baseline for subscript glyphs associated with this font. Values are expressed as a positive offset below the glyph baseline. If a font does not include all required subscript glyphs for an application, this field specifies the recommended vertical distance below the glyph baseline for alternate subscript glyphs supplied by the application. |

<a id="anchor-os2-ysuperscriptxsize"></a>

### ySuperscriptXSize

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Superscript horizontal font size. |
| Description: | The recommended horizontal size in font design units for superscripts for this font. Should be \> 0. |
| Comments: | If a font has two recommended sizes for superscripts, e.g., numerics and other, the numeric sizes should be stressed. This size field maps to the em size of the font being used for a superscript. The horizontal font size specifies a font designer’s recommended horizontal size for superscript glyphs associated with this font. If a font does not include all required superscript glyphs for an application, and the application can substitute glyphs by scaling the glyphs of a font or by substituting glyphs from another font, this field specifies the recommended nominal width for those superscript glyphs. <br><br> For example, if the em for a font is 2048 units and ySuperScriptXSize is set to 205, then the horizontal size for a simulated superscript glyph would be 1/10th the size of the normal glyph.<br><br>*Note:* This was implemented in the OS/2 platform as a signed value, even though only values \> 0 would be expected. |

<a id="anchor-os2-ysuperscriptysize"></a>

### ySuperscriptYSize

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Superscript vertical font size. |
| Description: | The recommended vertical size in font design units for superscripts for this font. Should be \> 0. |
| Comments: | If a font has two recommended sizes for superscripts, e.g., numerics and other, the numeric sizes should be stressed. This size field maps to the em size of the font being used for a superscript. The vertical font size specifies a font designer’s recommended vertical size for superscript glyphs associated with this font. If a font does not include all required superscript glyphs for an application, and the application can substitute glyphs by scaling the glyphs of a font or by substituting glyphs from another font, this field specifies the recommended nominal height for those superscript glyphs. <br><br> For example, if the em for a font is 2048 units and ySuperScriptYSize is set to 205, then the vertical size for a simulated superscript glyph would be 1/10th the size of the normal glyph.<br><br>*Note:* This was implemented in the OS/2 platform as a signed value, even though only values \> 0 would be expected. |

<a id="anchor-os2-ysuperscriptxoffset"></a>

### ySuperscriptXOffset

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Superscript x offset. |
| Description: | The recommended horizontal offset in font design units for superscripts for this font. |
| Comments: | The ySuperscriptXOffset field specifies a font designer’s recommended horizontal offset — from the glyph’s origin to the superscript glyph’s origin for the superscript glyphs associated with this font. If a font does not include all required superscript glyphs for an application, this field specifies the recommended horizontal position from the escapement point of the glyph before the first superscript glyph. For upright glyphs, this value is usually zero; however, if the glyphs of a font have an incline (italic or slant), the reference point for superscript glyphs is usually adjusted to compensate for the angle of incline. |

<a id="anchor-os2-ysuperscriptyoffset"></a>

### ySuperscriptYOffset

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Superscript y offset. |
| Description: | The recommended vertical offset in font design units from the baseline for superscripts for this font. |
| Comments: | The ySuperscriptYOffset field specifies a font designer’s recommended vertical offset — from the glyph’s baseline to the superscript glyph’s baseline associated with this font. Values for this field are expressed as a positive offset above the glyph baseline. If a font does not include all required superscript glyphs for an application, this field specifies the recommended vertical distance above the glyph baseline for alternate superscript glyphs supplied by the application. |

<a id="anchor-os2-ystrikeoutsize"></a>

### yStrikeoutSize

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Strikeout size. |
| Description: | Thickness of the strikeout stroke in font design units. Should be \> 0. |
| Comments: | This field should normally be the thickness of the em dash for the current font, and should also match the underline thickness, which is specified in the ['post'](post.md#anchor-post-underlineThickness) table.<br><br>*Note:* This was implemented in the OS/2 platform as a signed value, even though only values \> 0 would be expected. |

<a id="anchor-os2-ystrikeoutposition"></a>

### yStrikeoutPosition

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Title: | Strikeout position. |
| Description: | The position of the top of the strikeout stroke relative to the baseline in font design units. |
| Comments: | Positive values represent distances above the baseline; negative values represent distances below the baseline. Aligning the strikeout position with the em dash is suggested. Note, however, that the strikeout position should not interfere with the recognition of standard characters, and therefore should not line up with crossbars in the font. |

<a id="anchor-os2-sfamilyclass"></a>

### sFamilyClass

|  |  |
| --- | --- |
| Format: | int16 |
| Title: | Font-family class and subclass. |
| Description: | This field provides a classification of font-family design. |
| Comments: | The family class and subclass are assigned to a font based on the family design. This field is intended for use in selecting an alternate font family when the requested font is not available.<br><br> The class and subclass provide a two-level classification. The high byte of this field contains the family class, while the low byte contains the family subclass. The interpretation of subclass values depends on the class value.<br><br> Registered class and subclass values were originally defined by IBM. For details on registered values, see [IBM Font Family Classifications](ibmfc.md). |

<a id="anchor-os2-panose"></a>

### panose

|  |  |
| --- | --- |
| Format: | uint8\[10\] |
| Title: | PANOSE classification number |
| International: | Additional specifications are required for PANOSE to classify non-Latin character sets. |
| Description: | This 10-byte array of numbers is used to describe the visual characteristics of a given typeface. These characteristics are then used to associate the font with other fonts of similar appearance having different names. The variables for each digit are listed below. |
| Comments: | The PANOSE definition contains ten bytes, each of which can have multiple possible values. The PANOSE values are fully described in the [PANOSE Classification Metrics Guide](http://www.panose.com/). Note that the first byte is used for a high-level classification, “Family Kind”, and that the interpretation of the remaining bytes is contingent on the value of the first byte. For example, if the Family Kind value is 2 (Latin Text), then the next byte specifies “Serif Style”; but if the Family Kind value is 3 (Latin Hand Written), then the next byte specifies “Tool Kind”. Some applications might support only certain Family Kind values. The following table gives the interpretation for the panose array when the Family Kind is Latin Text:<br>[See table](#nested-os2-5)<br>Some applications can use the PANOSE values for font selection, to select a font matching certain parameters. For example, Proportion (for Family Kind = Latin Text) might be used to determine if a font is monospaced; or Serif Style might be used to determine if a font falls into generic *serif* or *sans serif* classes. Some applications will use Family Kind = 5 (Latin Symbol) to identify symbol fonts, which might affect font selection or fallback behaviors. There are no requirements for how applications should use the PANOSE values.<br>In a variable font that uses OpenType Font Variation mechanisms, there is no way to represent different PANOSE values for different instances supported by the font. The PANOSE values can be set based on the default instance. |
| Version differences: | Early versions of this specification provided more details regarding PANOSE values. However, the external specification cited above is the normative source and should be referred to for such details. |

<a id="nested-os2-5"></a>

The following table was originally nested in row 5, cell 2 of the table above.

| Type | Name |
| --- | --- |
| uint8 | bFamilyType |
| uint8 | bSerifStyle |
| uint8 | bWeight |
| uint8 | bProportion |
| uint8 | bContrast |
| uint8 | bStrokeVariation |
| uint8 | bArmStyle |
| uint8 | bLetterform |
| uint8 | bMidline |
| uint8 | bXHeight |

<a id="anchor-os2-ulunicoderange"></a>

### ulUnicodeRange\*

ulUnicodeRange1 (bits 0 – 31)<br> ulUnicodeRange2 (bits 32 – 63)<br> ulUnicodeRange3 (bits 64 – 95)<br> ulUnicodeRange4 (bits 96 – 127)

<br>

|  |  |
| --- | --- |
| Format: | uint32\[4\] (128 bits total) |
| Title: | Unicode Character Range |
| Description: | This field is used to specify the Unicode blocks or ranges encompassed by the font file in 'cmap' subtables for platform 3, encoding ID 1 (Microsoft platform, Unicode BMP) and platform 3, encoding ID 10 (Microsoft platform, Unicode full repertoire). If a bit is set (1), then the Unicode ranges assigned to that bit are considered functional. If the bit is clear (0), then the range is not considered functional. Each of the bits is treated as an independent flag and the bits can be set in any combination. The determination of “functional” is left up to the font designer, although character set selection should attempt to be functional by ranges if at all possible. <br><br> **All reserved fields must be zero.** Each uint32 is in Big-Endian form.<br>[See table](#nested-os2-6) |
| Comments: | All available bits were exhausted as of Unicode 5.1. The bit assignments were last updated for OS/2 version 4 in OpenType 1.5. There are many additional ranges supported in the current version of Unicode that are not supported by these fields in the OS/2 table. See the 'dlng' and 'slng' tags in the ['meta' table](meta.md) for an alternate mechanism to declare what scripts or languages a font can support or is designed for. |
| Version differences: | Different versions of the OS/2 table were created when different Unicode versions were current, and the initial specification for a given version defined fewer bit assignments than for later versions. Some applications might not support all assignments for fonts that have earlier OS/2 versions. <br><br> All of the bit assignments listed above are valid for any version of the OS/2 table, though OS/2 versions 1 and 2 were specified with some assignments that did not correspond to well-defined Unicode ranges and that conflict with later assignments — see the details below. If a font has a version 1 or version 2 OS/2 table with one of these bits set, the obsolete assignment could be the intended interpretation. Because these assignments do not correspond to well-defined ranges, however, the implied character coverage is unclear. <br><br> **Version 0:** When version 0 was first specified, no bit assignments were defined. Some applications could ignore these fields in a version 0 OS/2 table. <br><br> **Version 1:** <br> Version 1 was first specified concurrent with Unicode 1.1, and bit assignments were defined for bits 0 to 69 only. With fonts that have a version 1 table, some applications might recognize only bits 0 to 69. <br><br> Also, version 1 was specified with some bit assignments that did not correspond to a well-defined Unicode range:<br>Bit 8: “Greek Symbols and Coptic” (bit 7 was specified as “Basic Greek”)<br>Bit 12: “Hebrew Extended” (bit 11 was specified as “Basic Hebrew”)<br>Bit 14: “Arabic Extended” (bit 13 was specified as “Basic Arabic”)<br>Bit 27: “Georgian Extended” (bit 26 was specified as “Basic Georgian”)<br>These assignments were discontinued as of version 2. <br><br> In addition, versions 1 and 2 were defined with bit 53 specified as “CJK Miscellaneous”, which also does not correspond to any well-defined Unicode range. This assignment was discontinued as of version 3. <br><br> **Version 2:** <br> Version 2 was defined in OpenType 1.1, which was concurrent with Unicode 2.1. At that time, bit assignments were defined for bits 0 to 69 only. Bit assignments for version 2 were updated in OpenType 1.3, adding assignments for bits 70 to 83 corresponding to new blocks assigned in Unicode 2.0 and Unicode 3.0. With fonts that have a version 2 table, some applications might recognize only those bits assigned in OpenType 1.2 or OpenType 1.3. <br><br> Also, the specification for version 2 continued to use a problematic assignment for bit 53 — see details for version 1. This assignment was discontinued as of version 3. <br><br> **Version 3:** Version 3 was defined in OpenType 1.4 with assignments for bits 84 to 92 corresponding to additional ranges in Unicode 3.2. In addition, some already-assigned bits were extended to cover additional Unicode ranges for related characters; see details in the table above. <br><br> **Version 4:** Version 4 was defined in OpenType 1.5 with assignments for bit 58 and bits 93 to 122 corresponding to additional ranges in Unicode 5.1. Also, bits 8, 12, 14, 27 and 53 were re-assigned (see version 1 for previous assignments). In addition, some already-assigned bits were extended to cover additional Unicode ranges for related characters; see details in the table above. |

<a id="nested-os2-6"></a>

The following table was originally nested in row 3, cell 2 of the table above.

| Bit | Unicode Range | Block range | Notes |
| --- | --- | --- | --- |
| 0 | Basic Latin | 0000-007F |  |
| 1 | Latin-1 Supplement | 0080-00FF |  |
| 2 | Latin Extended-A | 0100-017F |  |
| 3 | Latin Extended-B | 0180-024F |  |
| 4 | IPA Extensions | 0250-02AF |  |
|  | Phonetic Extensions | 1D00-1D7F | Added in OpenType 1.5 for OS/2 version 4. |
|  | Phonetic Extensions Supplement | 1D80-1DBF | Added in OpenType 1.5 for OS/2 version 4. |
| 5 | Spacing Modifier Letters | 02B0-02FF |  |
|  | Modifier Tone Letters | A700-A71F | Added in OpenType 1.5 for OS/2 version 4. |
| 6 | Combining Diacritical Marks | 0300-036F |  |
|  | Combining Diacritical Marks Supplement | 1DC0-1DFF | Added in OpenType 1.5 for OS/2 version 4. |
| 7 | Greek and Coptic | 0370-03FF |  |
| 8 | Coptic | 2C80-2CFF | Added in OpenType 1.5 for OS/2 version 4. See below for other version differences. |
| 9 | Cyrillic | 0400-04FF |  |
|  | Cyrillic Supplement | 0500-052F | Added in OpenType 1.4 for OS/2 version 3. |
|  | Cyrillic Extended-A | 2DE0-2DFF | Added in OpenType 1.5 for OS/2 version 4. |
|  | Cyrillic Extended-B | A640-A69F | Added in OpenType 1.5 for OS/2 version 4. |
| 10 | Armenian | 0530-058F |  |
| 11 | Hebrew | 0590-05FF |  |
| 12 | Vai | A500-A63F | Added in OpenType 1.5 for OS/2 version 4. See below for other version differences. |
| 13 | Arabic | 0600-06FF |  |
|  | Arabic Supplement | 0750-077F | Added in OpenType 1.5 for OS/2 version 4. |
| 14 | NKo | 07C0-07FF | Added in OpenType 1.5 for OS/2 version 4. See below for other version differences. |
| 15 | Devanagari | 0900-097F |  |
| 16 | Bangla | 0980-09FF |  |
| 17 | Gurmukhi | 0A00-0A7F |  |
| 18 | Gujarati | 0A80-0AFF |  |
| 19 | Odia | 0B00-0B7F |  |
| 20 | Tamil | 0B80-0BFF |  |
| 21 | Telugu | 0C00-0C7F |  |
| 22 | Kannada | 0C80-0CFF |  |
| 23 | Malayalam | 0D00-0D7F |  |
| 24 | Thai | 0E00-0E7F |  |
| 25 | Lao | 0E80-0EFF |  |
| 26 | Georgian | 10A0-10FF |  |
|  | Georgian Supplement | 2D00-2D2F | Added in OpenType 1.5 for OS/2 version 4. |
| 27 | Balinese | 1B00-1B7F | Added in OpenType 1.5 for OS/2 version 4. See below for other version differences. |
| 28 | Hangul Jamo | 1100-11FF |  |
| 29 | Latin Extended Additional | 1E00-1EFF |  |
|  | Latin Extended-C | 2C60-2C7F | Added in OpenType 1.5 for OS/2 version 4. |
|  | Latin Extended-D | A720-A7FF | Added in OpenType 1.5 for OS/2 version 4. |
| 30 | Greek Extended | 1F00-1FFF |  |
| 31 | General Punctuation | 2000-206F |  |
|  | Supplemental Punctuation | 2E00-2E7F | Added in OpenType 1.5 for OS/2 version 4. |
| 32 | Superscripts And Subscripts | 2070-209F |  |
| 33 | Currency Symbols | 20A0-20CF |  |
| 34 | Combining Diacritical Marks For Symbols | 20D0-20FF |  |
| 35 | Letterlike Symbols | 2100-214F |  |
| 36 | Number Forms | 2150-218F |  |
| 37 | Arrows | 2190-21FF |  |
|  | Supplemental Arrows-A | 27F0-27FF | Added in OpenType 1.4 for OS/2 version 3. |
|  | Supplemental Arrows-B | 2900-297F | Added in OpenType 1.4 for OS/2 version 3. |
|  | Miscellaneous Symbols and Arrows | 2B00-2BFF | Added in OpenType 1.5 for OS/2 version 4. |
| 38 | Mathematical Operators | 2200-22FF |  |
|  | Supplemental Mathematical Operators | 2A00-2AFF | Added in OpenType 1.4 for OS/2 version 3. |
|  | Miscellaneous Mathematical Symbols-A | 27C0-27EF | Added in OpenType 1.4 for OS/2 version 3. |
|  | Miscellaneous Mathematical Symbols-B | 2980-29FF | Added in OpenType 1.4 for OS/2 version 3. |
| 39 | Miscellaneous Technical | 2300-23FF |  |
| 40 | Control Pictures | 2400-243F |  |
| 41 | Optical Character Recognition | 2440-245F |  |
| 42 | Enclosed Alphanumerics | 2460-24FF |  |
| 43 | Box Drawing | 2500-257F |  |
| 44 | Block Elements | 2580-259F |  |
| 45 | Geometric Shapes | 25A0-25FF |  |
| 46 | Miscellaneous Symbols | 2600-26FF |  |
| 47 | Dingbats | 2700-27BF |  |
| 48 | CJK Symbols And Punctuation | 3000-303F |  |
| 49 | Hiragana | 3040-309F |  |
| 50 | Katakana | 30A0-30FF |  |
|  | Katakana Phonetic Extensions | 31F0-31FF | Added in OpenType 1.4 for OS/2 version 3. |
| 51 | Bopomofo | 3100-312F |  |
|  | Bopomofo Extended | 31A0-31BF | Added in OpenType 1.3, extending OS/2 version 2. |
| 52 | Hangul Compatibility Jamo | 3130-318F |  |
| 53 | Phags-pa | A840-A87F | Added in OpenType 1.5 for OS/2 version 4. See below for other version differences. |
| 54 | Enclosed CJK Letters And Months | 3200-32FF |  |
| 55 | CJK Compatibility | 3300-33FF |  |
| 56 | Hangul Syllables | AC00-D7AF |  |
| 57 | Non-Plane 0 | 10000-10FFFF | Setting this bit implies there is at least one character beyond the Basic Multilingual Plane supported by this font. First assigned in OpenType 1.3 for OS/2 version 2. |
| 58 | Phoenician | 10900-1091F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 59 | CJK Unified Ideographs | 4E00-9FFF |  |
|  | CJK Radicals Supplement | 2E80-2EFF | Added in OpenType 1.3 for OS/2 version 2. |
|  | Kangxi Radicals | 2F00-2FDF | Added in OpenType 1.3 for OS/2 version 2. |
|  | Ideographic Description Characters | 2FF0-2FFF | Added in OpenType 1.3 for OS/2 version 2. |
|  | CJK Unified Ideographs Extension A | 3400-4DBF | Added in OpenType 1.3 for OS/2 version 2. |
|  | CJK Unified Ideographs Extension B | 20000-2A6DF | Added in OpenType 1.4 for OS/2 version 3. |
|  | Kanbun | 3190-319F | Added in OpenType 1.4 for OS/2 version 3. |
| 60 | Private Use Area (plane 0) | E000-F8FF |  |
| 61 | CJK Strokes | 31C0-31EF | Added in OpenType 1.5 for OS/2 version 4. |
|  | CJK Compatibility Ideographs | F900-FAFF |  |
|  | CJK Compatibility Ideographs Supplement | 2F800-2FA1F | Added in OpenType 1.4 for OS/2 version 3. |
| 62 | Alphabetic Presentation Forms | FB00-FB4F |  |
| 63 | Arabic Presentation Forms-A | FB50-FDFF |  |
| 64 | Combining Half Marks | FE20-FE2F |  |
| 65 | Vertical Forms | FE10-FE1F | Added in OpenType 1.5 for OS/2 version 4. |
|  | CJK Compatibility Forms | FE30-FE4F |  |
| 66 | Small Form Variants | FE50-FE6F |  |
| 67 | Arabic Presentation Forms-B | FE70-FEFF |  |
| 68 | Halfwidth And Fullwidth Forms | FF00-FFEF |  |
| 69 | Specials | FFF0-FFFF |  |
| 70 | Tibetan | 0F00-0FFF | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 71 | Syriac | 0700-074F | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 72 | Thaana | 0780-07BF | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 73 | Sinhala | 0D80-0DFF | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 74 | Myanmar | 1000-109F | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 75 | Ethiopic | 1200-137F | First assigned in OpenType 1.3, extending OS/2 version 2. |
|  | Ethiopic Supplement | 1380-139F | Added in OpenType 1.5 for OS/2 version 4. |
|  | Ethiopic Extended | 2D80-2DDF | Added in OpenType 1.5 for OS/2 version 4. |
| 76 | Cherokee | 13A0-13FF | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 77 | Unified Canadian Aboriginal Syllabics | 1400-167F | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 78 | Ogham | 1680-169F | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 79 | Runic | 16A0-16FF | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 80 | Khmer | 1780-17FF | First assigned in OpenType 1.3, extending OS/2 version 2. |
|  | Khmer Symbols | 19E0-19FF | Added in OpenType 1.5 for OS/2 version 4. |
| 81 | Mongolian | 1800-18AF | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 82 | Braille Patterns | 2800-28FF | First assigned in OpenType 1.3, extending OS/2 version 2. |
| 83 | Yi Syllables | A000-A48F | First assigned in OpenType 1.3, extending OS/2 version 2. |
|  | Yi Radicals | A490-A4CF | Added in OpenType 1.3, extending OS/2 version 2. |
| 84 | Tagalog | 1700-171F | First assigned in OpenType 1.4 for OS/2 version 3. |
|  | Hanunoo | 1720-173F | Added in OpenType 1.4 for OS/2 version 3. |
|  | Buhid | 1740-175F | Added in OpenType 1.4 for OS/2 version 3. |
|  | Tagbanwa | 1760-177F | Added in OpenType 1.4 for OS/2 version 3. |
| 85 | Old Italic | 10300-1032F | First assigned in OpenType 1.4 for OS/2 version 3. |
| 86 | Gothic | 10330-1034F | First assigned in OpenType 1.4 for OS/2 version 3. |
| 87 | Deseret | 10400-1044F | First assigned in OpenType 1.4 for OS/2 version 3. |
| 88 | Byzantine Musical Symbols | 1D000-1D0FF | First assigned in OpenType 1.4 for OS/2 version 3. |
|  | Musical Symbols | 1D100-1D1FF | Added in OpenType 1.4 for OS/2 version 3. |
|  | Ancient Greek Musical Notation | 1D200-1D24F | Added in OpenType 1.5 for OS/2 version 4. |
| 89 | Mathematical Alphanumeric Symbols | 1D400-1D7FF | First assigned in OpenType 1.4 for OS/2 version 3. |
| 90 | Private Use (plane 15) | F0000-FFFFD | First assigned in OpenType 1.4 for OS/2 version 3. |
|  | Private Use (plane 16) | 100000-10FFFD | Added in OpenType 1.4 for OS/2 version 3. |
| 91 | Variation Selectors | FE00-FE0F | First assigned in OpenType 1.4 for OS/2 version 3. |
|  | Variation Selectors Supplement | E0100-E01EF | Added in OpenType 1.4 for OS/2 version 3. |
| 92 | Tags | E0000-E007F | First assigned in OpenType 1.4 for OS/2 version 3. |
| 93 | Limbu | 1900-194F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 94 | Tai Le | 1950-197F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 95 | New Tai Lue | 1980-19DF | First assigned in OpenType 1.5 for OS/2 version 4. |
| 96 | Buginese | 1A00-1A1F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 97 | Glagolitic | 2C00-2C5F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 98 | Tifinagh | 2D30-2D7F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 99 | Yijing Hexagram Symbols | 4DC0-4DFF | First assigned in OpenType 1.5 for OS/2 version 4. |
| 100 | Syloti Nagri | A800-A82F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 101 | Linear B Syllabary | 10000-1007F | First assigned in OpenType 1.5 for OS/2 version 4. |
|  | Linear B Ideograms | 10080-100FF | Added in OpenType 1.5 for OS/2 version 4. |
|  | Aegean Numbers | 10100-1013F | Added in OpenType 1.5 for OS/2 version 4. |
| 102 | Ancient Greek Numbers | 10140-1018F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 103 | Ugaritic | 10380-1039F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 104 | Old Persian | 103A0-103DF | First assigned in OpenType 1.5 for OS/2 version 4. |
| 105 | Shavian | 10450-1047F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 106 | Osmanya | 10480-104AF | First assigned in OpenType 1.5 for OS/2 version 4. |
| 107 | Cypriot Syllabary | 10800-1083F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 108 | Kharoshthi | 10A00-10A5F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 109 | Tai Xuan Jing Symbols | 1D300-1D35F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 110 | Cuneiform | 12000-123FF | First assigned in OpenType 1.5 for OS/2 version 4. |
|  | Cuneiform Numbers and Punctuation | 12400-1247F | Added in OpenType 1.5 for OS/2 version 4. |
| 111 | Counting Rod Numerals | 1D360-1D37F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 112 | Sundanese | 1B80-1BBF | First assigned in OpenType 1.5 for OS/2 version 4. |
| 113 | Lepcha | 1C00-1C4F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 114 | Ol Chiki | 1C50-1C7F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 115 | Saurashtra | A880-A8DF | First assigned in OpenType 1.5 for OS/2 version 4. |
| 116 | Kayah Li | A900-A92F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 117 | Rejang | A930-A95F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 118 | Cham | AA00-AA5F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 119 | Ancient Symbols | 10190-101CF | First assigned in OpenType 1.5 for OS/2 version 4. |
| 120 | Phaistos Disc | 101D0-101FF | First assigned in OpenType 1.5 for OS/2 version 4. |
| 121 | Carian | 102A0-102DF | First assigned in OpenType 1.5 for OS/2 version 4. |
|  | Lycian | 10280-1029F | Added in OpenType 1.5 for OS/2 version 4. |
|  | Lydian | 10920-1093F | Added in OpenType 1.5 for OS/2 version 4. |
| 122 | Domino Tiles | 1F030-1F09F | First assigned in OpenType 1.5 for OS/2 version 4. |
|  | Mahjong Tiles | 1F000-1F02F | First assigned in OpenType 1.5 for OS/2 version 4. |
| 123-127 | Reserved |  |  |

<a id="anchor-os2-achvendid"></a>

### achVendID

|  |  |
| --- | --- |
| Format: | Tag |
| Title: | Font Vendor Identification |
| Description: | The four character identifier for the vendor of the given typeface. |
| Comments: | This is not the royalty owner of the original artwork. This is the company responsible for the marketing and distribution of the typeface that is being classified. For example, there can be multiple vendors of ITC Zapf Dingbats, with some vendors providing differentiating benefits in their fonts (more kern pairs, unregularized data, hand hinted, etc.). This identifier will allow for the correct vendor’s type to be used over another, possibly inferior, font file. <br><br> A registry of vendor IDs is maintained by Microsoft. Registered IDs must be unique to a single vendor. Non-registered IDs may also be used, but are discouraged: vendors are strongly encouraged to register an ID to ensure that there are no conflicts between different vendors in use of a given ID, and that customers are able to find vendor contact information for a given font. This field can also be left blank (set to null, or a tag comprised of four space characters). <br><br> All vendor IDs use the Tag data type, which is equivalent to a four-character string composed of a limited set of ASCII characters. For details regarding the Tag data type, see [Data Types](otff.md#anchor-otff-data-types). By convention, only registered tags should be comprised of only uppercase letters (or space). <br><br> For a list of registered Vendor IDs, or for details on registering a vendor ID or updating vendor information, see [Registered typography vendors](https://www.microsoft.com/typography/links/vendorlist.aspx). |

<a id="anchor-os2-fsselection"></a>

### fsSelection

|  |  |
| --- | --- |
| Format: | uint16 |
| Title: | Font selection flags. |
| Description: | Contains information concerning the nature of the font patterns, as follows:<br>[See table](#nested-os2-7) |
| Comments: | All undefined bits must be zero. <br><br> The fsSelection field was originally created for compatibility with the OS/2 platform. Some style description bits, such as bit 0, are used by modern applications, while other style description bits are not. <br><br> **Bit 0:** The setting of bits 0 must match the setting of bit 1 in the [macStyle](head.md#anchor-head-macstyle) field of the 'head' table. <br><br> **Bits 1 – 4:** Bits 1 – 4 are rarely used bits that indicate the font is primarily a decorative or special purpose font. <br><br> **Bit 5:** The setting of bit 5 must match the settings of bit 0 in the [macStyle](head.md#anchor-head-macstyle) field of the 'head' table. <br><br> **Bit 6:** Bit 6 is not used in widely used in modern applications. If bit 6 is set, then bits 0 and 5 must be clear, else the behavior is undefined. Note that, if both bit 0 and bit 5 are clear, that does not give any indication as to whether or not bit 6 will be clear. For example, Arial Light is not the regular style of Arial and would have all bits cleared. In extended font families, bit 6 does not need to be set for fonts other than the regular style that, nonetheless, use "Regular" for name ID 2. (See [Name IDs](name.md#anchor-name-name-ids) for more information.) <br><br> **Bit 7:** <br> Bit 7 was defined in version 4 and is used in many modern applications. For new fonts, vendors are encouraged to use a version 4 or later OS/2 table and to have bit 7 set. <br><br> If a font was created with an earlier version of the OS/2 table and is updated to the current version of the OS/2 table, then setting bit 7 could create potential for reflow of existing documents which use the fonts. To minimize such risk, the bit would be set only if using the OS/2.usWin\* metrics for line height would yield significantly inferior results than using the OS/2.sTypo\* values. <br><br> **Bit 8:** <br> If bit 8 is set, then ['name' table](name.md) strings for family and subfamily are provided that are consistent with a weight/width/slope (WWS) family model without requiring the use of name IDs 21 or 22. <br><br> Bit 8 and name IDs 21 and 22 were introduced for use by applications that assume a WWS family model, given that there exist fonts with style variants that do not fit into one of the three attributes, weight, width or slope. <br><br> Many typographic families include faces that differ only in one or more of these three attributes. In such cases, name IDs 1 and 2 or IDs 16 and 17 will not present challenges for software that assumes a WWS model. But some typographic families include faces that differ in some *other* attributes. For example, a family might include variations for “handwriting”, “caption”, “display”, “optical size”, etc. In such cases, a font could incorporate that attribute into a typographic subfamily name (ID 17 string), whereas applications that assume a WWS model would require that attribute to be incorporated into a family name (ID 1 or ID 16). <br><br> IF a face differs within its family only in terms of weight, width or slope attributes, then bit 8 should be set. This applies even if the face is part of a large family that includes *other* faces distinguished by other attributes. Setting bit 8 serves as an indicator to apps that assume the WWS model that name IDs 1 and 2 or IDs 16 and 17 are consistent with the WWS model and no further treatment is required, including checking to see whether name IDs 21 and 22 are present. Hence, when bit 8 is set, name IDs 21 and 22 are never required and should not be included. <br><br> If a face differs within its family from Regular by attributes other than weight, width or slope, then bit 8 should \*not\* be set, and name IDs 21 and 22 should be included. By having bit 8 not set, that serves as an indicator to apps that assume a WWS model that they should look for name IDs 21 and 22, or that some other treatment of names could be required. <br><br> The [STAT](stat.md) table was introduced in a later version of OpenType, after bit 8 and name IDs 21 and 22 were defined. The STAT table was introduced, in part, to solve the same kind of requirement but in a more general way that could be useful for applications assuming other family models. If a face has attributes other than weight, width or slope and does not have name IDs 21 and 22, some applications that assume a WWS model could be able to support that font using information in the STAT table. However, even if a STAT table is present (as is required for variable fonts), the recommendations above regarding bit 8 and name IDs 21 and 22 should still be followed. <br><br> In this context, “typographic family” is the Microsoft Unicode string for name ID 16, if present, else the Microsoft Unicode string for name ID 1; “weight” is OS/2.usWeightClass; “width” is OS/2.usWidthClass; “slope” is OS/2.fsSelection bit 0 (ITALIC) and bit 9 (OBLIQUE). <br><br> **Bit 9:** <br> If bit 9 is set, then this font is to be considered an “oblique” style by processes which make a distinction between oblique and italic styles, such as Cascading Style Sheets font matching. For example, a font created by algorithmically slanting an upright face will set this bit. <br><br> If a font has a version 4 or later OS/2 table and this bit is not set, then this font is not to be considered an “oblique” style. For example, a font that has a classic italic design will not set this bit. <br><br> This bit, unlike the ITALIC bit (bit 0), is not related to style-linking in applications that assume a four-member font-family model comprised of regular, italic, bold and bold italic. It may be set or unset independently of the ITALIC bit. In most cases, if OBLIQUE is set, then ITALIC will also be set, though this is not required. <br><br> **Bit 15:** Bit 15 is permanently reserved. It has been used in some legacy implementations and could result in special behavior in some implementations. Use of this bit is deprecated. |
| Version differences: | **Versions 0 to 3:** Only bit 0 (italic) to bit 6 (regular) are assigned. Bits 7 to 15 are reserved and must be set to 0. Applications should ignore bits 7 to 15 in a font that has a version 0 to version 3 OS/2 table. <br><br> **Version 4 to 5:** Bits 7 to 9 were defined in version 4 (OpenType 1.5). Bits 10 to 15 are reserved and must be set to 0. Applications should ignore bits 10 to 15 in a font that has a version 4 or version 5 OS/2 table. |

<a id="nested-os2-7"></a>

The following table was originally nested in row 3, cell 2 of the table above.

| Bit # | macStyle bit | C definition | Description |
| --- | --- | --- | --- |
| <a id="anchor-os2-fss_bit0"></a>0 | bit 1 | ITALIC | Font contains italic or oblique glyphs, otherwise they are upright. |
| <a id="anchor-os2-fss_bit1"></a>1 |  | UNDERSCORE | Glyphs are underscored. |
| <a id="anchor-os2-fss_bit2"></a>2 |  | NEGATIVE | Glyphs have their foreground and background reversed. |
| <a id="anchor-os2-fss_bit3"></a>3 |  | OUTLINED | Outline (hollow) glyphs, otherwise they are solid. |
| <a id="anchor-os2-fss_bit4"></a>4 |  | STRIKEOUT | Glyphs are overstruck. |
| <a id="anchor-os2-fss_bit5"></a>5 | bit 0 | BOLD | Glyphs are emboldened. |
| <a id="anchor-os2-fss_bit6"></a>6 |  | REGULAR | Glyphs are in the standard weight/style for the font. |
| <a id="anchor-os2-fss_bit7"></a>7 |  | USE\_TYPO\_METRICS | If set, it is strongly recommended that applications use OS/2.sTypoAscender - OS/2.sTypoDescender + OS/2.sTypoLineGap as the default line spacing for this font. |
| <a id="anchor-os2-fss_bit8"></a>8 |  | WWS | The font has 'name' table strings consistent with a weight/width/slope family without requiring use of name IDs 21 and 22. (See a more detailed description below.) |
| <a id="anchor-os2-fss_bit9"></a>9 |  | OBLIQUE | Font contains oblique glyphs. |
| 10–15 |  | Reserved | Reserved; set to 0. |

<a id="anchor-os2-usfirstcharindex"></a>

### usFirstCharIndex

|  |  |
| --- | --- |
| Format: | uint16 |
| Description: | The minimum Unicode index (character code) in this font, according to the 'cmap' subtable for platform ID 3 and platform- specific encoding ID 0 or 1. For most fonts supporting Win-ANSI or other character sets, this value would be 0x0020. This field cannot represent supplementary character values (codepoints greater than 0xFFFF). Fonts that support supplementary characters should set the value in this field to 0xFFFF if the minimum index value is a supplementary character. |

<a id="anchor-os2-uslastcharindex"></a>

### usLastCharIndex

|  |  |
| --- | --- |
| Format: | uint16 |
| Description: | The maximum Unicode index (character code) in this font, according to the 'cmap' subtable for platform ID 3 and encoding ID 0 or 1. This value depends on which character sets the font supports. This field cannot represent supplementary character values (codepoints greater than 0xFFFF). Fonts that support supplementary characters should set the value in this field to 0xFFFF. |

<a id="anchor-os2-stypoascender"></a>

### sTypoAscender

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Description: | The typographic ascender for this font. This field should be combined with the sTypoDescender and sTypoLineGap values to determine default line spacing. <br><br><br>This field is similar to the [ascender](hhea.md#anchor-hhea-ascender) field in the 'hhea' table as well as to the [usWinAscent](#anchor-os2-uswinascent) field in this table. However, legacy platform implementations used those fields with platform-specific behaviors. As a result, those fields are constrained by backward-compatibility requirements, and they do not ensure consistent layout across implementations. The sTypoAscender, sTypoDescender and sTypoLineGap fields are intended to allow applications to lay out documents in a typographically correct and portable fashion. <br><br> The USE\_TYPO\_METRICS flag (bit 7) of the fsSelection field is used to choose between using sTypo\* values or usWin\* values for default line metrics. See [fsSelection](#anchor-os2-fsselection) for additional details. <br><br> It is not a general requirement that sTypoAscender - sTypoDescender be equal to unitsPerEm. These values should be set to provide default line spacing appropriate for the primary languages the font is designed to support. <br><br> For CJK (Chinese, Japanese, and Korean) fonts that are intended to be used for vertical (as well as horizontal) layout, the required value for sTypoAscender is that which describes the top of the [ideographic em-box](baselinetags.md#anchor-baselinetags-ideographic-em-box). For example, if the ideographic em-box of the font extends from coordinates 0,-120 to 1000,880 (that is, a 1000 × 1000 box set 120 design units below the Latin baseline), then the value of sTypoAscender must be set to 880. Failing to adhere to these requirements will result in incorrect vertical layout. <br><br> Also see the [Recommendations Section](recom.md#anchor-recom-stypoascender-stypodescender-and-stypolinegap) for more on this field. |

<a id="anchor-os2-stypodescender"></a>

### sTypoDescender

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Description: | The typographic descender for this font. This field should be combined with the sTypoAscender and sTypoLineGap values to determine default line spacing. <br><br> This field is similar to the [descender](hhea.md#anchor-hhea-descender) field in the 'hhea' table as well as to the [usWinDescent](#anchor-os2-uswindescent) field in this table. However, legacy platform implementations used those fields with platform-specific behaviors. As a result, those fields are constrained by backward-compatibility requirements, and they do not ensure consistent layout across implementations. The sTypoAscender, sTypoDescender and sTypoLineGap fields are intended to allow applications to lay out documents in a typographically correct and portable fashion. <br><br> The USE\_TYPO\_METRICS flag (bit 7) of the fsSelection field is used to choose between using sTypo\* values or usWin\* values for default line metrics. See [fsSelection](#anchor-os2-fsselection) for additional details. <br><br> It is not a general requirement that sTypoAscender - sTypoDescender be equal to unitsPerEm. These values should be set to provide default line spacing appropriate for the primary languages the font is designed to support. <br><br> For CJK (Chinese, Japanese, and Korean) fonts that are intended to be used for vertical (as well as horizontal) layout, the required value for sTypoDescender is that which describes the bottom of the [ideographic em-box](baselinetags.md#anchor-baselinetags-ideographic-em-box). For example, if the ideographic em-box of the font extends from coordinates 0,-120 to 1000,880 (that is, a 1000 × 1000 box set 120 design units below the Latin baseline), then the value of sTypoDescender must be set to -120. Failing to adhere to these requirements will result in incorrect vertical layout. <br><br> Also see the [Recommendations Section](recom.md#anchor-recom-stypoascender-stypodescender-and-stypolinegap) for more on this field. |

<a id="anchor-os2-stypolinegap"></a>

### sTypoLineGap

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Description: | The typographic line gap for this font. This field should be combined with the sTypoAscender and sTypoDescender values to determine default line spacing. <br><br> This field is similar to the [lineGap](hhea.md#anchor-hhea-lineGap) field in the 'hhea' table. However, legacy platform implementations treat that field with platform-specific behaviors. As a result, that field is constrained by backward-compatibility requirements, and does not ensure consistent layout across implementations. The sTypoAscender, sTypoDescender and sTypoLineGap fields are intended to allow applications to lay out documents in a typographically correct and portable fashion. <br><br> The USE\_TYPO\_METRICS flag (bit 7) of the fsSelection field is used to choose between using sTypo\* values or usWin\* values for default line metrics. See [fsSelection](#anchor-os2-fsselection) for additional details. |

<a id="anchor-os2-uswinascent"></a>

### usWinAscent

|  |  |
| --- | --- |
| Format: | UFWORD |
| Units: | Font design units |
| Description: | The “Windows ascender” metric. This should be used to specify the height above the baseline for a clipping region. <br><br> This is similar to the [sTypoAscender](#anchor-os2-stypoascender) field, and also to the [ascender](hhea.md#anchor-hhea-ascender) field in the 'hhea' table. There are important differences between these, however. <br><br> In the Windows GDI implementation, the usWinAscent and usWinDescent values have been used to determine the size of the bitmap surface in the TrueType rasterizer. Windows GDI will clip any portion of a TrueType glyph outline that appears above the usWinAscent value. If any clipping is unacceptable, then the value should be set greater than or equal to yMax. <br><br> *Note:* This pertains to the default position of glyphs, not their final position in layout after data from the GPOS or 'kern' table has been applied. Also, this clipping behavior interacts with the [VDMX table](vdmx.md): if a VDMX table is present and there is data for the current device aspect ratio and rasterization size, then the VDMX data will supersede the usWinAscent and usWinDescent values. <br><br> Some legacy applications use the usWinAscent and usWinDescent values to determine default line spacing. This is strongly discouraged. The sTypo\* fields should be used for this purpose. <br><br> Note that some applications use either the usWin\* values or the sTypo\* values to determine default line spacing, depending on whether the USE\_TYPO\_METRICS flag (bit 7) of the fsSelection field is set. This could be useful to provide compatibility with legacy documents using older fonts, while also providing better and more-portable layout using newer fonts. See [fsSelection](#anchor-os2-fsselection) for additional details. <br><br> Applications that use the sTypo\* fields for default line spacing can use the usWin\* values to determine the size of a clipping region. Some applications use a clipping region for editing scenarios to determine what portion of the display surface to re-draw when text is edited, or how large a selection rectangle to draw when text is selected. This is an appropriate use for the usWin\* values. <br><br> Early versions of this specification suggested that the usWinAscent value be computed as the yMax for all characters in the Windows “ANSI” character set. For new fonts, the value should be determined based on the primary languages the font is designed to support, and should take into consideration additional height that could be required to accommodate tall glyphs or mark positioning. |

<a id="anchor-os2-uswindescent"></a>

### usWinDescent

|  |  |
| --- | --- |
| Format: | UFWORD |
| Units: | Font design units |
| Description: | The “Windows descender” metric. This should be used to specify the vertical extent below the baseline for a clipping region. <br><br> This is similar to the [sTypoDescender](#anchor-os2-stypodescender) field, and also to the [descender](hhea.md#anchor-hhea-descender) field in the 'hhea' table. There are important differences between these, however. Some of these differences are described below. In addition, the usWinDescent value treats distances below the baseline as positive values; thus, usWinDescent is usually a positive value, while sTypoDescender and hhea.descender are usually negative. <br><br> In the Windows GDI implementation, the usWinDescent and usWinAscent values have been used to determine the size of the bitmap surface in the TrueType rasterizer. Windows GDI will clip any portion of a TrueType glyph outline that appears below (-1 × usWinDescent). If any clipping is unacceptable, then the value should be set greater than or equal to (-yMin). <br><br> *Note:* This pertains to the default position of glyphs, not their final position in layout after data from the GPOS or 'kern' table has been applied. Also, this clipping behavior interacts with the [VDMX table](vdmx.md): if a VDMX table is present and there is data for the current device aspect ratio and rasterization size, then the VDMX data will supersede the usWinAscent and usWinDescent values. <br><br> Some legacy applications use the usWinAscent and usWinDescent values to determine default line spacing. This is strongly discouraged. The sTypo\* fields should be used for this purpose. <br><br> Note that some applications use either the usWin\* values or the sTypo\* values to determine default line spacing, depending on whether the USE\_TYPO\_METRICS flag (bit 7) of the fsSelection field is set. This could be useful to provide compatibility with legacy documents using older fonts, while also providing better and more-portable layout using newer fonts. See [fsSelection](#anchor-os2-fsselection) for additional details. <br><br> Applications that use the sTypo\* fields for default line spacing can use the usWin\* values to determine the size of a clipping region. Some applications use a clipping region for editing scenarios to determine what portion of the display surface to re-draw when text is edited, or how large a selection rectangle to draw when text is selected. This is an appropriate use for the usWin\* values. <br><br> Early versions of this specification suggested that the usWinDescent value be computed as -yMin for all characters in the Windows “ANSI” character set. For new fonts, the value should be determined based on the primary languages the font is designed to support, and should take into consideration additional vertical extent that could be required to accommodate glyphs with low descenders or mark positioning. |

<a id="anchor-os2-ulcodepagerange"></a>

### ulCodePageRange\*

ulCodePageRange1 (bits 0 – 31)<br> ulCodePageRange2 (bits 32 – 63)

<br>

|  |  |
| --- | --- |
| Format: | uint32\[2\] (64 bits total) |
| Title: | Code Page Character Range |
| Description: | This field is used to specify the code pages encompassed by the font file in the 'cmap' subtable for platform 3, encoding ID 1 (Windows platform, Unicode BMP). If the font file is encoding ID 0, then the Symbol Character Set bit should be set. <br><br> If a given bit is set (1), then the code page is considered functional. If the bit is clear (0) then the code page is not considered functional. Each of the bits is treated as an independent flag and the bits can be set in any combination. The determination of “functional” is left up to the font designer, although character set selection should attempt to be functional by code pages if at all possible. <br><br> Symbol character sets have a special meaning. If the symbol bit (31) is set, and the font file contains a 'cmap' subtable for platform of 3 and encoding ID of 1, then all of the characters in the Unicode range 0xF000 - 0xF0FF (inclusive) will be used to enumerate the symbol character set. If the bit is not set, any characters present in that range will not be enumerated as a symbol character set. <br><br> All reserved fields must be zero. Each uint32 is in Big-Endian form.<br>[See table](#nested-os2-8) |
| Version differences: | **Version 0:** These fields were not defined in version 0. If the size of a version 0 OS/2 table extends beyond the usWinDescent field, additional data beyond the usWinDescent field should be ignored. <br><br> **Version 1:** Bit 8 was not assigned in version 1. All other currently assigned bits were defined in version 1. <br><br> **Version 2 and later:** All currently assigned bits were defined in version 2. |

<a id="nested-os2-8"></a>

The following table was originally nested in row 3, cell 2 of the table above.

| Bit | Code Page | Description |
| --- | --- | --- |
| 0 | 1252 | Latin 1 |
| 1 | 1250 | Latin 2: Eastern Europe |
| 2 | 1251 | Cyrillic |
| 3 | 1253 | Greek |
| 4 | 1254 | Turkish |
| 5 | 1255 | Hebrew |
| 6 | 1256 | Arabic |
| 7 | 1257 | Windows Baltic |
| 8 | 1258 | Vietnamese |
| 9 – 15 |  | Reserved for Alternate ANSI |
| 16 | 874 | Thai |
| 17 | 932 | JIS/Japan |
| 18 | 936 | Chinese: Simplified chars—PRC and Singapore |
| 19 | 949 | Korean Wansung |
| 20 | 950 | Chinese: Traditional chars—Taiwan and Hong Kong SAR |
| 21 | 1361 | Korean Johab |
| 22 – 28 |  | Reserved for Alternate ANSI or OEM |
| 29 |  | Macintosh Character Set (US Roman) |
| 30 |  | OEM Character Set |
| 31 |  | Symbol Character Set |
| 32 – 47 |  | Reserved for OEM |
| 48 | 869 | IBM Greek |
| 49 | 866 | MS-DOS Russian |
| 50 | 865 | MS-DOS Nordic |
| 51 | 864 | Arabic |
| 52 | 863 | MS-DOS Canadian French |
| 53 | 862 | Hebrew |
| 54 | 861 | MS-DOS Icelandic |
| 55 | 860 | MS-DOS Portuguese |
| 56 | 857 | IBM Turkish |
| 57 | 855 | IBM Cyrillic; primarily Russian |
| 58 | 852 | Latin 2 |
| 59 | 775 | MS-DOS Baltic |
| 60 | 737 | Greek; former 437 G |
| 61 | 708 | Arabic; ASMO 708 |
| 62 | 850 | WE/Latin 1 |
| 63 | 437 | US |

<a id="anchor-os2-sxheight"></a>

### sxHeight

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Description: | This metric specifies the distance between the baseline and the approximate height of non-ascending lowercase letters measured in font design units. This value would normally be specified by a type designer but in situations where that is not possible, for example when a legacy font is being converted, the value may be set equal to the top of the unscaled and unhinted glyph bounding box of the glyph encoded at U+0078 (LATIN SMALL LETTER X). If no glyph is encoded in this position the field should be set to 0. <br><br> This metric, if specified, can be used in font substitution: the xHeight value of one font can be scaled to approximate the apparent size of another. |
| Version differences: | **Version 0, version 1:** This field was not defined in version 0 or version 1. If the size of a version 0 OS/2 table extends beyond the usWinDescent field, or if the size of a version 1 OS/2 table extends beyond the code page range fields, this additional data should be ignored. <br><br> **Version 2 and later:** This field was defined in version 2 of the OS/2 table. |

<a id="anchor-os2-scapheight"></a>

### sCapHeight

|  |  |
| --- | --- |
| Format: | FWORD |
| Units: | Font design units |
| Description: | This metric specifies the distance between the baseline and the approximate height of uppercase letters measured in font design units. This value would normally be specified by a type designer but in situations where that is not possible, for example when a legacy font is being converted, the value may be set equal to the top of the unscaled and unhinted glyph bounding box of the glyph encoded at U+0048 (LATIN CAPITAL LETTER H). If no glyph is encoded in this position the field should be set to 0. <br><br> This metric, if specified, can be used in systems that specify type size by capital height measured in millimeters. It can also be used as an alignment metric; the top of a drop capital, for instance, can be aligned to the sCapHeight metric of the first line of text. |
| Version differences: | **Version 0, version 1:** This field was not defined in version 0 or version 1. If the size of a version 0 OS/2 table extends beyond the usWinDescent field, or if the size of a version 1 OS/2 table extends beyond the code page range fields, this additional data should be ignored. <br><br> **Version 2 and later:** This field was defined in version 2 of the OS/2 table. |

<a id="anchor-os2-usdefaultchar"></a>

### usDefaultChar

|  |  |
| --- | --- |
| Format: | uint16 |
| Description: | This is the Unicode code point, in UTF-16 encoding, of a character that can be used for a default glyph if a requested character is not supported in the font. If the value of this field is zero, glyph ID 0 is to be used for the default character. This field cannot represent supplementary-plane character values (code points greater than 0xFFFF), and so applications are strongly discouraged from using this field. |
| Version differences: | **Version 0, version 1:** This field was not defined in version 0 or version 1. If the size of a version 0 OS/2 table extends beyond the usWinDescent field, or if the size of a version 1 OS/2 table extends beyond the code page range fields, this additional data should be ignored. <br><br> **Version 2 and later:** This field was defined in version 2 of the OS/2 table. |

<a id="anchor-os2-usbreakchar"></a>

### usBreakChar

|  |  |
| --- | --- |
| Format: | uint16 |
| Description: | This is the Unicode code point, in UTF-16 encoding, of a character that can be used as a default break character. The break character is used to separate words and justify text. Most fonts specify U+0020 SPACE as the break character. This field cannot represent supplementary-plane character values (code points greater than 0xFFFF), and so applications are strongly discouraged from using this field. |
| Version differences: | **Version 0, version 1:** This field was not defined in version 0 or version 1. If the size of a version 0 OS/2 table extends beyond the usWinDescent field, or if the size of a version 1 OS/2 table extends beyond the code page range fields, this additional data should be ignored. <br><br> **Version 2 and later:** This field was defined in version 2 of the OS/2 table. |

<a id="anchor-os2-usmaxcontext"></a>

### usMaxContext

|  |  |
| --- | --- |
| Format: | uint16 |
| Description: | The maximum length of a target glyph context for any feature in this font. For example, a font which has only a pair kerning feature should set this field to 2. If the font also has a ligature feature in which the glyph sequence “f f i” is substituted by the ligature “ffi”, then this field should be set to 3. This field could be useful to sophisticated line-breaking engines in determining how far they should look ahead to test whether something could change that affects the line breaking. For chaining contextual lookups, the length of the string (covered glyph) + (input sequence) + (lookahead sequence) should be considered. |
| Version differences: | **Version 0, version 1:** This field was not defined in version 0 or version 1. If the size of a version 0 OS/2 table extends beyond the usWinDescent field, or if the size of a version 1 OS/2 table extends beyond the code page range fields, this additional data should be ignored. <br><br> **Version 2 and later:** This field was defined in version 2 of the OS/2 table. |

<a id="anchor-os2-usloweropticalpointsize"></a>

### usLowerOpticalPointSize

|  |  |
| --- | --- |
| Format: | uint16 |
| Units: | TWIPs |
| Description: | This field is used for fonts with multiple optical styles. <br><br> This value is the lower value of the size range for which this font has been designed. The units for this field are TWIPs (one-twentieth of a point, or 1440 per inch). The value is inclusive — meaning that that font was designed to work best at this point size through, but not including, the point size indicated by usUpperOpticalPointSize. When used with other optical-size-variant fonts within a typographic family that also specify usLowerOpticalPointSize and usUpperOpticalPointSize values, it would be expected that another font has the usUpperOpticalPointSize field set to the same value as the value in this field, unless this font is designed for the lowest size range among the fonts in the family. The smallest font in an optical-size set should set this value to 0. When working across multiple optical-size-variant fonts within a typographic family, there should be no intentional gaps or overlaps in the ranges. <br><br> The usLowerOpticalPointSize value must be less than usUpperOpticalPointSize. The maximum valid value is 0xFFFE. <br><br> For fonts that were not designed for multiple optical-size variants, this field should be set to 0 (zero), and usUpperOpticalPointSize should be set to 0xFFFF. <br><br> *Note:* Use of this field has been superseded by the STAT table. See [Recommendations Section](recom.md#anchor-recom-families-with-optical-size-variants) for more information. |
| Version differences: | **Versions 0 – 4:** This field was not defined in versions 0 – 4. If the size of an OS/2 table extends beyond the last field defined for the given version, this additional data should be ignored. <br><br> **Version 5:** This field was defined in version 5 of the OS/2 table. |

<a id="anchor-os2-usupperopticalpointsize"></a>

### usUpperOpticalPointSize

|  |  |
| --- | --- |
| Format: | uint16 |
| Units: | TWIPs |
| Description: | This field is used for fonts with multiple optical styles. <br><br> This value is the upper value of the size range for which this font has been designed. The units for this field are TWIPs (one-twentieth of a point, or 1440 per inch). The value is exclusive — meaning that that font was designed to work best below this point size down to the usLowerOpticalPointSize threshold. When used with other optical-size-variant fonts within a typographic family that also specify usLowerOpticalPointSize and usUpperOpticalPointSize values, it would be expected that another font has the usLowerOpticalPointSize field set to the same value as the value in this field, unless this font is designed for the highest size range among the fonts in the family. The largest font in an optical-size set should set this value to 0xFFFF, which is interpreted as infinity. When working across multiple optical-size-variant fonts within a typographic family, there should be no intentional gaps or overlaps left in the ranges. <br><br> The usUpperOpticalPointSize value must be greater than usLowerOpticalPointSize. The minimum valid value for this field is 2 (two). The largest possible inclusive point size represented by this field is 3276.65 points; any higher values would be represented as infinity. <br><br> For fonts that were not designed for multiple optical-size variants, this field should be set to 0xFFFF, and usLowerOpticalPointSize should be set to 0 (zero). <br><br> *Note:* Use of this field has been superseded by the STAT table. See [Recommendations Section](recom.md#anchor-recom-families-with-optical-size-variants) for more information. |
| Version differences: | **Versions 0 – 4:** This field was not defined in versions 0 – 4. If the size of an OS/2 table extends beyond the last field defined for the given version, this additional data should be ignored. <br><br> **Version 5:** This field was defined in version 5 of the OS/2 table. |

<a id="anchor-os2-os2-table-and-opentype-font-variations"></a>

## OS/2 Table and OpenType Font Variations

In variable fonts, default line metrics should always be set using the sTypoAscender, sTypoDescender and sTypoLineGap values, and the USE\_TYPO\_METRICS flag in the fsSelection field should be set. The ascender, descender and lineGap fields in the 'hhea' table should be set to the same values as sTypoAscender, sTypoDescender and sTypoLineGap. The usWinAscent and usWinDescent fields should be used to specify a recommended clipping rectangle.

In a variable font, various font-metric values within the OS/2 table might need to be adjusted for different variation instances. Variation data for OS/2 entries can be provided in the [metrics variations (MVAR)](mvar.md) table. Different OS/2 entries are associated with particular variation data in the MVAR table using value tags, as follows:

| OS/2 entry | Tag |
| --- | --- |
| <a id="anchor-os2-cpht"></a>sCapHeight | 'cpht' |
| <a id="anchor-os2-hasc"></a>sTypoAscender | 'hasc' |
| <a id="anchor-os2-hdsc"></a>sTypoDescender | 'hdsc' |
| <a id="anchor-os2-hlgp"></a>sTypoLineGap | 'hlgp' |
| <a id="anchor-os2-xhgt"></a>sxHeight | 'xhgt' |
| <a id="anchor-os2-hcla"></a>usWinAscent | 'hcla' |
| <a id="anchor-os2-hcld"></a>usWinDescent | 'hcld' |
| <a id="anchor-os2-stro"></a>yStrikeoutPosition | 'stro' |
| <a id="anchor-os2-strs"></a>yStrikeoutSize | 'strs' |
| <a id="anchor-os2-sbxo"></a>ySubscriptXOffset | 'sbxo' |
| <a id="anchor-os2-sbxs"></a>ySubScriptXSize | 'sbxs' |
| <a id="anchor-os2-sbyo"></a>ySubscriptYOffset | 'sbyo' |
| <a id="anchor-os2-sbys"></a>ySubscriptYSize | 'sbys' |
| <a id="anchor-os2-spxo"></a>ySuperscriptXOffset | 'spxo' |
| <a id="anchor-os2-spxs"></a>ySuperscriptXSize | 'spxs' |
| <a id="anchor-os2-spyo"></a>ySuperscriptYOffset | 'spyo' |
| <a id="anchor-os2-spys"></a>ySuperscriptYSize | 'spys' |

> *Note:* The usWeightClass and usWidthClass values are not adjusted by variation data since these correspond to 'wght' and 'wdth' variation axes that can be used to define a font’s variation space. Appropriate usWeightClass and usWidthClass values for a variation instance can be derived from 'wght' and 'wdth' user coordinates that are used to select a particular variation instance. For 'wdth' values greater than 200, the usWidthClass value is clamped to 9. See the discussion of the 'wght' and 'wdth' axes in the [OpenType Design-Variation Axis Tag Registry](dvaraxisreg.md) for details on the relationship between these OS/2 fields and the corresponding design axes.

> *Note:* The usLowerOpticalPointSize and usUpperOpticalPointSize values are not adjusted by variation data. These values (now superseded by the STAT table) are used to indicate a range of sizes for which a given font has been designed. It is assumed that variation that targets different sizes will be implemented using the 'opsz' variation axis. If a variable font supports 'opsz' as an axis of variation, then the usLowerOpticalPointSize and usUpperOpticalPointSize fields can be set to the same values as the minValue and maxValue fields for the 'opsz' axis in the 'fvar' table.

To have variable line metrics in a variable font, the 'hasc', 'hdsc' and 'hlgp' value tags should be used in the MVAR table to vary the ascender, descender and line gap values from defaults specified in the sTypoAscender, sTypoDescender and sTypoLineGap fields. The 'hcla' and 'hcld' value tags can be used in addition to vary the size of a clipping region from the default specified in the winAscent and winDescent fields. Other metrics can be varied using value tags listed above.

For general information on OpenType Font Variations, see the chapter, [OpenType Font Variations Overview](otvaroverview.md).
