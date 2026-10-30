---
title: "The 'OS/2' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-OS2-OS-2"></a>

# The `'OS/2'` table

<a id="anchor-OS2-part-1"></a>

## General table information

The `'OS/2'` table consists of a set of metrics that are required by Windows. It is not fully used by Apple platforms.

The format of this table has changed over time. The original TrueType specification had this table at 68 bytes long. The first OpenType version had it at 78 bytes long, and the current OpenType version is even larger. To determine which kind of table your software is dealing with, it is necessary both to consider the table's version and its size.

The layout of the (68-byte) table is shown in Table 1 below. For details on later OpenType extensions, consult the [OpenType specification](http://www.microsoft.com/typography/otspec/).

**Table 1**: `'OS/2'` table

| Type | Name | Description |
| --- | --- | --- |
| uint16 | version | table version number (set to 0) |
| int16 | xAvgCharWidth | average weighted advance width of lower case letters and space |
| uint16 | usWeightClass | visual weight (degree of blackness or thickness) of stroke in glyphs |
| uint16 | usWidthClass | relative change from the normal aspect ratio (width to height ratio) as specified by a font designer for the glyphs in the font |
| int16 | fsType | characteristics and properties of this font (set undefined bits to zero) |
| int16 | ySubscriptXSize; | recommended horizontal size in pixels for subscripts |
| int16 | ySubscriptYSize | recommended vertical size in pixels for subscripts |
| int16 | ySubscriptXOffset | recommended horizontal offset for subscripts |
| int16 | ySubscriptYOffset | recommended vertical offset form the baseline for subscripts |
| int16 | ySuperscriptXSize | recommended horizontal size in pixels for superscripts |
| int16 | ySuperscriptYSize | recommended vertical size in pixels for superscripts |
| int16 | ySuperscriptXOffset | recommended horizontal offset for superscripts |
| int16 | ySuperscriptYOffset | recommended vertical offset from the baseline for superscripts |
| int16 | yStrikeoutSize | width of the strikeout stroke |
| int16 | yStrikeoutPosition | position of the strikeout stroke relative to the baseline |
| int16 | sFamilyClass | classification of font-family design. |
| PANOSE | panose | 10 byte series of number used to describe the visual characteristics of a given typeface |
| uint32 | ulUnicodeRange\[4\] | Field is split into two bit fields of 96 and 36 bits each. The low 96 bits are used to specify the Unicode blocks encompassed by the font file. The high 32 bits are used to specify the character or script sets covered by the font file. Bit assignments are pending. Set to 0 |
| int8 | achVendID\[4\] | four character identifier for the font vendor |
| uint16 | fsSelection | 2-byte bit field containing information concerning the nature of the font patterns |
| uint16 | fsFirstCharIndex | The minimum Unicode index in this font. |
| uint16 | fsLastCharIndex | The maximum Unicode index in this font. |

<a id="anchor-OS2-part-2"></a>

## Version

The version number of the table documented above is zero. The current version used by OpenType is five.<br>

<a id="anchor-OS2-part-3"></a>

## Additional Fields

The fields added since the original version of the `'OS/2'` table format are:

| Type | Name | Description |
| --- | --- | --- |
| int16 | sTypoAscender | The typographic ascender for this font. This is not necessarily the same as the ascender value in the `'hhea'` table. |
| int16 | sTypoDescender | The typographic descender for this font. This is not necessarily the same as the descender value in the `'hhea'` table. |
| int16 | sTypoLineGap | The typographic line gap for this font. This is not necessarily the same as the line gap value in the `'hhea'` table. |
| uint16 | usWinAscent | The ascender metric for Windows. `usWinAscent` is computed as the `yMax` for all characters in the Windows ANSI character set. |
| uint16 | usWinDescent | The descender metric for Windows. `usWinDescent` is computed as the `-yMin` for all characters in the Windows ANSI character set. |
| uint32 | ulCodePageRange1 | Bits 0-31 |
| uint32 | ulCodePageRange2 | Bits 32-63 |
| int16 | sxHeight | The distance between the baseline and the approximate height of non-ascending lowercase letters measured in FUnits. |
| int16 | sCapHeight | The distance between the baseline and the approximate height of uppercase letters measured in FUnits. |
| uint16 | usDefaultChar | The default character displayed by Windows to represent an unsupported character. (Typically this should be 0.) |
| uint16 | usBreakChar | The break character used by Windows. |
| uint16 | usMaxContext | The maximum length of a target glyph OpenType context for any feature in this font. |
| uint16 | usLowerPointSize | *Proposed for version 5* The lowest size (in twentieths of a typographic point), at which the font starts to be used. This is an inclusive value. |
| uint16 | usUpperPointSize | *Proposed for version 5* The highest size (in twentieths of a typographic point), at which the font starts to be used. This is an exclusive value. Use `0xFFFFU` to indicate no upper limit. |

<a id="anchor-OS2-part-4"></a>

## xAvgCharWidth

The xAvgCharWidth parameter specifies the arithmetic average of the advance width of all of the 26 lowercase letters of the Latin alphabet and the space character. If any of the 26 lowercase letters are not present, this parameter should equal zero.

This parameter is a descriptive attribute of the font that specifies the spacing of characters used for comparing one font to another for selection or substitution. For proportionally spaced fonts, this value is useful in estimating the length for lines of text. The weighting factors provided in Table 2 below are only valid for Latin lowercase letters. If other character sets, or capital letters are used, different frequency of use values should be substituted. Care must be taken when comparing fonts that use different frequency of use values for font mapping. The average character width is calculated according to this formula:

`For the lowercase letters only, sum the individual character widths multiplied by the following weighting factors and then divide by 1000.`

**Table 2** : Weight Factors

| Letter | Weight Factor | Letter | Weight Factor |
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

<a id="anchor-OS2-part-5"></a>

## usWeightClass

The usWeightClass indicates the visual weight (degree of blackness or thickness of strokes) of the characters in the font. Table 3 below explains the possible values for this entry.

**Table 3** : Visual Weight

| Value | Description |
| --- | --- |
| 1 | Ultra-light |
| 2 | Extra-light |
| 3 | Light |
| 4 | Semi-light |
| 5 | Medium (normal) |
| 6 | Semi-bold |
| 7 | Bold |
| 8 | Extra-Bold |
| 9 | Ultra-bold |

<br>

<a id="anchor-OS2-part-6"></a>

## usWidthClass

The usWidthClass indicates a relative change from the normal aspect ratio (width to height ratio) as specified by a font designer for the glyphs in a font.

Although every character in a font may have a different numeric aspect ratio, each character in a font of normal width has a relative aspect ratio of one. When a new type style is created of a different width class (either by a font designer or by some automated means) the relative aspect ratio of the characters in the new font is some percentage greater or less than those same characters in the normal font it is this difference that this parameter specifies.

**Table 4** : Aspect ratio

| Value | Description | % of normal |
| --- | --- | --- |
| 1 | Ultra-condensed | 50 |
| 2 | Extra-condensed | 62.5 |
| 3 | Condensed | 75 |
| 4 | Semi-condensed | 87.5 |
| 5 | Medium (normal) | 100 |
| 6 | Semi-expanded | 112.5 |
| 7 | Expanded | 125 |
| 8 | Extra-expanded | 150 |
| 9 | Ultra-expanded | 200 |

<a id="anchor-OS2-part-7"></a>

## fsType

The fsType is a 2-byte bit field indicating the embedding characteristics of the font. The meaning of the bits is summarized in Table 5. Set all undefined bits to zero.

**Table 5** : Embedding flags

| Bit | Description |
| --- | --- |
| 0 | Reserved; must be 0 |
| 1 | Licensed (protected) font; should not be 1 if bits 2 or 3 are one. Fonts that have only this bit set *must not be modified, embedded, or exchanged in any manner* without first obtaining permission of the legal owner. |
| 2 | Preview and print embedding; should not be 1 if bits 1 or 3 are one. Fonts that have only this bit set may be embedded in documents and temporarily loaded on the remote system. Documents containing such fonts must be opened “read-only;” no edits can be applied to the document. |
| 3 | Editable embedding; should not be 1 if bits 1 or 2 are one. Fonts that have only this bit set may be embedded in documents and temporarily loaded on the remote system. Documents containing such fonts may be editable. |
| 4–7 | Reserved; must be 0 |
| 8 | No subsetting. When this bit is set, the font may not be subsetted prior to embedding. Other embedding restrictions specified in bits 1–3 and 9 also apply. |
| 9 | Bitmap embedding only. When this bit is set, only bitmaps contained in the font may be embedded. No outline data may be embedded. Other embedding restrictions specified in bits 1–3 and 8 also apply. |
| 10–15 | Reserved; must be 0 |

Fonts that are not licensed may be encapsulated within a document and shipped freely to other users. Fonts subject to a licensing agreement are legally protected or licensed. They must not be modified or exchanged in any manner without first assuring that the action is within the terms of the protection agreement and obtaining permission from the holder of the protection agreement.

The next eight entries apply to subscripts and superscripts. Two (one each for x and y) apply to size, two to offset for each of subscripts and superscripts.

**Table 6** : Superscripts

|  |  |
| --- | --- |
| ySubscriptXSize | If a font has two recommended sizes for subscripts, e.g., numerics and other, the numeric sizes should be stressed. This size field maps to the em square size of the font being used for a subscript. The horizontal font size specifies a font designer's recommended horizontal font size for subscript characters associated with this font. If a font does not include all of the required subscript characters for an application, and the application can substitute characters by scaling the character of a font or by substituting characters from another font, this parameter specifies the recommended em square for those subscript characters.<br> For example, if the em square for a font is 2048 and ySubScriptXSize is set to 205, then the horizontal size for a simulated subscript character would be 1/10th the size of the normal character. |
| ySubscriptYSize | If a font has two recommended sizes for subscripts, e.g. numerics and other, the numeric sizes should be stressed. This size field maps to the emHeight of the font being used for a subscript. The horizontal font size specifies a font designer's recommendation for horizontal font size of subscript characters associated with this font. If a font does not include all of the required subscript characters for an application, and the application can substitute characters by scaling the characters in a font or by substituting characters from another font, this parameter specifies the recommended horizontal EmInc for those subscript characters.<br> For example, if the em square for a font is 2048 and ySubScriptYSize is set to 205, then the vertical size for a simulated subscript character would be 1/10th the size of the normal character. |
| ySubscriptXOffset | The Subscript X Offset parameter specifies a font designer's recommended horizontal offset -- from the character origin of the font to the character origin of the subscript's character -- for subscript characters associated with this font. If a font does not include all of the required subscript characters for an application, and the application can substitute characters, this parameter specifies the recommended horizontal position from the character escapement point of the last character before the first subscript character. For upright characters, this value is usually zero; however, if the characters of a font have an incline (italic characters) the reference point for subscript characters is usually adjusted to compensate for the angle of incline. |
| ySubscriptYOffset | The Subscript Y Offset parameter specifies a font designer's recommended vertical offset from the character baseline to the character baseline for subscript characters associated with this font. Values are expressed as a positive offset below the character baseline. If a font does not include all of the required subscript for an application, this parameter specifies the recommended vertical distance below the character baseline for those subscript characters. |
| ySuperscriptXSize | If a font has two recommended sizes for subscripts, e.g., numerics and other, the numeric sizes should be stressed. This size field maps to the em square size of the font being used for a subscript. The horizontal font size specifies a font designer's recommended horizontal font size for superscript characters associated with this font. If a font does not include all of the required superscript characters for an application, and the application can substitute characters by scaling the character of a font or by substituting characters from another font, this parameter specifies the recommended em square for those superscript characters.<br> For example, if the em square for a font is 2048 and ySuperScriptXSize is set to 205, then the horizontal size for a simulated superscript character would be 1/10th the size of the normal character. |
| ySuperscriptYSize | If a font has two recommended sizes for subscripts, e.g., numerics and other, the numeric sizes should be stressed. This size field maps to the emHeight of the font being used for a subscript. The vertical font size specifies a font designer's recommended vertical font size for superscript characters associated with this font. If a font does not include all of the required superscript characters for an application, and the application can substitute characters by scaling the character of a font or by substituting characters from another font, this parameter specifies the recommended EmHeight for those superscript characters.<br> For example, if the em square for a font is 2048 and ySuperScriptYSize is set to 205, then the vertical size for a simulated superscript character would be 1/10th the size of the normal character. |
| ySuperscriptXOffset | he Superscript X Offset parameter specifies a font designer's recommended horizontal offset -- from the character origin to the superscript character's origin for the superscript characters associated with this font. If a font does not include all of the required superscript characters for an application, this parameter specifies the recommended horizontal position from the escapement point of the character before the first superscript character. For upright characters, this value is usually zero; however, if the characters of a font have an incline (italic characters) the reference point for superscript characters is usually adjusted to compensate for the angle of incline. |
| ySuperscriptYOffset | The Superscript Y Offset parameter specifies a font designer's recommended vertical offset -- from the character baseline to the superscript character's baseline associated with this font. Values for this parameter are expressed as a positive offset above the character baseline. If a font does not include all of the required superscript characters for an application, this parameter specifies the recommended vertical distance above the character baseline for those superscript characters. |

The next two entries contain strikeout information.

**Table 7** : Strikeout

|  |  |
| --- | --- |
| yStrikeoutSize | This field should normally be the width of the em-dash for the current font. If the size is one, the strikeout line will be the line represented by the strikeout position field. If the value is two, the strikeout line will be the line represented by the strikeout position and the line immediately above the strikeout position. |
| yStrikeoutPosition | Positive values represent distances above the baseline, while negative values represent distances below the baseline. A value of zero falls directly on the baseline, while a value of one falls one pixel above the baseline. The value of strikeout position should not interfere with the recognition of standard characters, and therefore should not line up with crossbars in the font. |

The next section describes the information in sFamilyClass.

The font class and font subclass are registered values assigned by IBM to each font family. This parameter is intended for use in selecting an alternate font when the requested font is not available. The font class is the most general and the font subclass is the most specific. The high byte of this field contains the family class, while the low byte contains the family subclass.

This section defines the IBM Font Class and the IBM Font Subclass parameter values to be used in the classification of font designs by the font designer or supplier. These values classify a font design as to its appearance, but do not identify the specific font family, typeface variation, designer, supplier, size, or metric table differences. It should be noted that some font designs may be classified equally well into more than IBM Font Class or Subclass. Such designs should be matched to a classification for which substitution of another font design from the same class or subclass would generally result in a similar appearance of the presented document.

**Table 8** : sFamily Class

| ClassID | Class Name | Description |
| --- | --- | --- |
| 0 | No classification | This class ID is used to indicate that the associated font has no design classification or that the design classification is not of significance to the creator or user of the font resource. |
| 1 | OldStyle Serifs | This style is generally based upon the Latin printing style of the 15th to 17th century, with a mild diagonal contrast in stroke emphasis (lighter in upper left to lower right, heavier in upper right to lower left) and bracketed serifs. This IBM Class reflects the ISO Serif Class, Oldstyle and Legibility Subclasses as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Transitional Serifs | This style is generally based upon the Latin printing style of the 18th to 19th century, with a pronounced vertical contrast in stroke emphasis (vertical strokes being heavier than the horizontal strokes) and bracketed serifs. This IBM Class reflects the ISO Serif Class, Transitional Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 3 | Modern Serifs | This style is generally based upon the Latin printing style of the 20th century, with an extreme contrast between the thick and thin portion of the strokes. This IBM Class reflects the ISO Serif Class, Modern Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 4 | Clarendon Serifs | This style is a variation of the Oldstyle Serifs and the Transitional Serifs, with a mild vertical stroke contrast and bracketed serifs. This IBM Class reflects the ISO Serif Class, Square Serif Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 5 | Slab Serifs | This style is characterized by serifs with a square transition between the strokes and the serifs (no brackets). This IBM Class reflects the ISO Serif Class, Square Serif Subclass (except the Clarendon Specific Group) as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 6 | Reserved | This class ID is reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 7 | Freeform Serifs | This style includes serifs, but which expresses a design freedom that does not generally fit within the other serif design classifications. This IBM Class reflects the remaining ISO Serif Class subclasses as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 8 | Sans Serif | This style includes most basic letter forms (excluding Scripts and Ornamentals) that do not have serifs on the strokes. This IBM Class reflects the ISO Sans Serif Class as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 9 | Ornamentals | This style includes highly decorated or stylized character shapes that are typically used in headlines. This IBM Class reflects the ISO Ornamental Class and the ISO Blackletter Class as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 10 | Scripts | This style includes those typefaces that are designed to simulate handwriting. This IBM Class reflects the ISO Script Class and Uncial Class as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 11 | reserved | This class ID is reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 12 | Symbolic | This style is generally design independent, making it suitable for Pi and special characters (icons, dingbats, technical symbols, etc.) that may be used equally well with any font. This IBM Class reflects various ISO Specific Groups, as noted below and documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 13 | reserved | This class ID is reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 14 | reserved | This class ID is reserved for future assignment, and shall not be used without formal assignment by IBM. |

A number of the class defined above have subclasses as documented below.

**Table 9** : OldStyle Serifs (ClassID = 1)

| Subclass | Name | Description |
| --- | --- | --- |
| 0 | No classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design subclassification is not of significance to the creator or user of the font resource. |
| 1 | IBM Rounded Legibility | This style is generally characterized by a large x-height, with short ascenders and descenders. Specifically, it is distinguished by a medium resolution, hand tuned, bitmap rendition of the more general rounded legibility subclass. An example of this font style is the IBM Sonoran Serif family. This IBM Subclass reflects the ISO Serif Class, Legibility Subclass, and Rounded Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Garalde | This style is generally characterized by a medium x-height, with tall ascenders. An example of this font style is the ITC Garamond family. This IBM Subclass reflects the ISO Serif Class, Oldstyle Subclass, and Garalde Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 3 | Venetian | This style is generally characterized by a medium x-height, with a relatively monotone appearance and sweeping tails based on the designs of the early Venetian printers. An example of this font style is the Goudy family. This IBM Subclass reflects the ISO Serif Class, Oldstyle Subclass, and Venetian Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 4 | Modified Venetian | This style is generally characterized by a large x-height, with a relatively monotone appearance and sweeping tails based on the designs of the early Venetian printers. An example of this font style is the Allied Linotype Palatino family. This IBM Subclass reflects the ISO Serif Class, Transitional Subclass, and Modified Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 5 | Dutch Modern | This style is generally characterized by a large x-height, with wedge shaped serifs and a circular appearance to the bowls similar to the Dutch Traditional Subclass below, but with lighter stokes. An example of this font style is the Monotype Times New Roman family. This IBM Subclass reflects the ISO Serif Class, Oldstyle Subclass, and Dutch Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 6 | Dutch Traditional | This style is generally characterized by a large x-height, with wedge shaped serifs and a circular appearance of the bowls. An example of this font style is the IBM Press Roman family. This IBM Subclass reflects the ISO Serif Class and Legibility Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 7 | Contemporary | This style is generally characterized by a small x-height, with light stokes and serifs. An example of this font style is the University family. This IBM Subclass reflects the ISO Serif Class and Contemporary Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 8 | Calligraphic | This style is generally characterized by the fine hand writing style of calligraphy, while retaining the characteristic Oldstyle appearance. This IBM Subclass is not reflected in the 12/87 ISO/IEC 9541-5 draft standard. |
| 9-14 | reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

**Table 10** : Transitional Serifs (ClassID=2)

| Subclass | Name | Description |
| --- | --- | --- |
| 0 | No Classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1 | Direct Line | This style is generally characterized by a medium x-height, with fine serifs, noticeable contrast, and capitol letters of approximately the same width. An example of this font style is the Monotype Baskerville family. This IBM Subclass reflects the ISO Serif Class, Transitional Subclass, and Direct Line Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Script | This style is generally characterized by a hand written script appearance while retaining the Transitional Direct Line style. An example of this font style is the IBM Nasseem (Arabic) family. This IBM Subclass is not specifically reflected in the 12/87 ISO/IEC 9541-5 draft standard, though the ISO Serif Class, Transitional Subclass, and Direct Line Specific Group would be a close approximation. |
| 3-14 | reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

**Table 11** : Modern Serifs (ClassID=3)

| Subclass | Name | Description |
| --- | --- | --- |
| 0 | No Classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1 | Italian | This style is generally characterized by a medium x-height, with thin hairline serifs. An example of this font style is the Monotype Bodoni family. This IBM Subclass reflects the ISO Serif Class, Modern Subclass, and Italian Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Script | This style is generally characterized by a hand written script appearance while retaining the Modern Italian style. An example of this font style is the IBM Narkissim (Hebrew) family. This IBM Subclass is not specifically reflected in the 12/87 ISO/IEC 9541-5 draft standard, though the ISO Serif Class, Modern Subclass, and Italian Specific Group would be a close approximation. |
| 3-14 | reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

**Table 12** : Clarendon Serifs (ClassID=4)

| Subc.ass | Name | Description |
| --- | --- | --- |
| 0 | No Classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1 | Clarendon | This style is generally characterized by a large x-height, with serifs and strokes of equal weight. An example of this font style is the Allied Linotype Clarendon family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Clarendon Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Modern | This style is generally characterized by a large x-height, with serifs of a lighter weight than the strokes and the strokes of a lighter weight than the Traditional. An example of this font style is the Monotype Century Schoolbook family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Clarendon Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 3 | Traditional | This style is generally characterized by a large x-height, with serifs of a lighter weight than the strokes. An example of this font style is the Monotype Century family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Clarendon Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 4 | Newspaper | This style is generally characterized by a large x-height, with a simpler style of design and serifs of a ligher weight than the strokes. An example of this font style is the Allied Linotype Excelsior Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Clarendon Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 5 | Stub Serif | This style is generally characterized by a large x-height, with short stub serifs and relatively bold stems. An example of this font style is the Cheltenham Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Short Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 6 | Monotone | This style is generally characterized by a large x-height, with monotone stems. An example of this font style is the ITC Korinna Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 7 | Typewriter | This style is generally characterized by a large x-height, with moderate stroke thickness characteristic of a typewriter. An example of this font style is the Prestige Elite Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Typewriter Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 8-14 | reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

This style is characterized by serifs with a square transition between the strokes and the serifs (no brackets). This IBM Class reflects the ISO Serif Class, Square Serif Subclass (except the Clarendon Specific Group) as documented in the 12/87 ISO/IEC 9541-5 draft standard.

**Table 13** : Slab Serifs (ClassID=5)

| Subc.ass | Name | Description |
| --- | --- | --- |
| 0 | No classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1 | Monotone | This style is generally characterized by a large x-height, with serifs and strokes of equal weight. An example of this font style is the ITC Lubalin Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Humanist | This style is generally characterized by a medium x-height, with serifs of lighter weight that the strokes. An example of this font style is the Candida Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 3 | Geometric | This style is generally characterized by a large x-height, with serifs and strokes of equal weight and a geometric (circles and lines) design. An example of this font style is the Monotype Rockwell Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 4 | Swiss | This style is generally characterized by a large x-height, with serifs and strokes of equal weight and an emphasis on the white space of the characters. An example of this font style is the Allied Linotype Serifa Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 5 | Typewriter | This style is generally characterized by a large x-height, with serifs and strokes of equal but moderate thickness, and a geometric design. An example of this font style is the IBM Courier Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 6-14 | reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

class ID 6 is reserved for future assignment, and shall not be used without formal assignment by IBM.

This style includes serifs, but which expresses a design freedom that does not generally fit within the other serif design classifications. This IBM Class reflects the remaining ISO Serif Class subclasses as documented in the 12/87 ISO/IEC 9541-5 draft standard.

**Table 14** : Freeform Serifs (ClassID=7)

| Subclass | Name | Description |
| --- | --- | --- |
| 0 | No classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1 | Modern | This style is generally characterized by a medium x-height, with light contrast in the strokes and a round full design. An example of this font style is the ITC Souvenir Family. This IBM Subclass is not reflected in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2-14 | reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

This style includes most basic letter forms (excluding Scripts and Ornamentals) that do not have serifs on the strokes. This IBM Class reflects the ISO Sans Serif Class as documented in the 12/87 ISO/IEC 9541-5 draft standard.

**Table 15** : Sans Serif (ClassID=8)

| Subc.ass | Name | Description |
| --- | --- | --- |
| 0 | No classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1 | IBM Neo-grotesque Gothic | This style is generally characterized by a large x-height, with uniform stroke width and a simple one story design distinguished by a medium resolution, hand tuned, bitmap rendition of the more general Neo-grotesque Gothic Subclass. An example of this font style is the IBM Sonoran Sans Serif family. This IBM Subclass reflects the ISO Sans Serif Class, Gothic Subclass, and Neo-grotesque Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Humanist | This style is generally characterized by a medium x-height, with light contrast in the strokes and a classic Roman letterform. An example of this font style is the Allied Linotype Optima family. This IBM Subclass reflects the ISO Sans Serif Class, Humanist Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 3 | Low-x Round Geometric | This style is generally characterized by a low x-height, with monotone stroke weight and a round geometric design. An example of this font style is the Fundicion Tipograficia Neufville Futura family. This IBM Subclass reflects the ISO Sans Serif Class, Geometric Subclass, Round Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 4 | High-x Round Geometric | This style is generally characterized by a high x-height, with uniform stroke weight and a round geometric design. An example of this font style is the ITC Avant Garde Gothic family. This IBM Subclass reflects the ISO Sans Serif Class, Geometric Subclass, Round Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 5 | Neo-grotesque Gothic | This style is generally characterized by a high x-height, with uniform stroke width and a simple one story design. An example of this font style is the Allied Linotype Helvetica family. This IBM Subclass reflects the ISO Sans Serif Class, Gothic Subclass, Neo-grotesque Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 6 | Modified neo-grotesque Gothic | This style is similar to the Neo-grotesque Gothic style, with design variations to the G and Q. An example of this font style is the Allied Linotype Univers family. This IBM Subclass reflects the ISO Sans Serif Class, Gothic Subclass, Neo-grotesque Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 7-8 | Reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 9 | Typewriter Gothic | This style is similar to the Neo-grotesque Gothic style, with moderate stroke thickness characteristic of a typewriter. An example of this font style is the IBM Letter Gothic family. This IBM Subclass reflects the ISO Sans Serif Class, Gothic Subclass, Typewriter Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 10 | Matrix | This style is generally a simple design characteristic of a dot matrix printer. An example of this font style is the IBM Matrix Gothic family. This IBM Subclass is not reflected in the 12/87 ISO/IEC 9541-5 draft standard. |
| 11-14 | Reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

**Table 16** : Ornamental (ClassID = 9)

| Subc.ass | Name | Description |
| --- | --- | --- |
| 0 | No classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1 | Engraver | This style is characterized by fine lines or lines engraved on the stems. An example of this font style is the Copperplate family. This IBM Subclass reflects the ISO Ornamental Class and Inline Subclass, or the Serif Class and Engraving Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Black Letter | This style is generally based upon the printing style of the German monasteries and printers of the 12th to 15th centuries. An example of this font style is the Old English family. This IBM Subclass reflects the ISO Blackletters Class as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 3 | Decorative | This style is characterized by ornamental designs (typically from nature, such as leaves, flowers, animals, etc.) incorporated into the stems and strokes of the characters. An example of this font style is the Saphire family. This IBM Subclass reflects the ISO Ornamental Class and Decorative Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 4 | Three Dimensional | This style is characterized by a three dimensional (raised) appearance of the characters created by shading or geometric effects. An example of this font style is the Thorne Shaded family. This IBM Subclass reflects the ISO Ornamental Class and Three Dimensional Subclass as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 5-14 | Reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

This style includes highly decorated or stylized character shapes that are typically used in headlines. This IBM Class reflects the ISO Ornamental Class and the ISO Blackletter Class as documented in the 12/87 ISO/IEC 9541-5 draft standard.

**Table 17** : Scripts (ClassID=10)

| Subc.ass | Name | Description |
| --- | --- | --- |
| 0 | No classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1 | Uncial | This style is characterized by unjoined (nonconnecting) characters that are generally based on the hand writing style of Europe in the 6th to 9th centuries. An example of this font style is the Libra family. This IBM Subclass reflects the ISO Uncial Class as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 2 | Brush Joined | This style is characterized by joined (connecting) characters that have the appearance of being painted with a brush, with moderate contrast between thick and thin strokes. An example of this font style is the Mistral family. This IBM Subclass reflects the ISO Script Class, Joined Subclass, and Informal Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 3 | Formal Joined | This style is characterized by joined (connecting) characters that have a printed (or drawn with a stiff brush) appearance with extreme contrast between the thick and thin strokes. An example of this font style is the Coronet family. This IBM Subclass reflects the ISO Script Class, Joined Subclass, and Formal Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 4 | Monotone Joined | This style is characterized by joined (connecting) characters that have a uniform appearance with little or no contrast in the strokes. An example of this font style is the Kaufmann family. This IBM Subclass reflects the ISO Script Class, Joined Subclass, and Monotone Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 5 | Calligraphic | This style is characterized by beautifully hand drawn, unjoined (non-connecting) characters that have an appearance of being drawn with a broad edge pen. An example of this font style is the Thompson Quillscript family. This IBM Subclass reflects the ISO Script Class, Unjoined Subclass, and Calligraphic Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 6 | Brush Unjoined | This style is characterized by unjoined (non-connecting) characters that have the appearance of being painted with a brush, with moderate contrast between thick and thin strokes. An example of this font style is the Saltino family. This IBM Subclass reflects the ISO Script Class, Unjoined Subclass, and Brush Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 7 | Formal Unjoined | This style is characterized by unjoined (non-connecting) characters that have a printed (or drawn with a stiff brush) appearance with extreme contrast between the thick and thin strokes. An example of this font style is the Virtuosa family. This IBM Subclass reflects the ISO Script Class, Unjoined Subclass, and Formal Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 8 | Monotone Unjoined | This style is characterized by unjoined (non-connecting) characters that have a uniform appearance with little or no contrast in the strokes. An example of this font style is the Gilles Gothic family. This IBM Subclass reflects the ISO Script Class, Unjoined Subclass, and Monotone Specific Group as documented in the 12/87 ISO/IEC 9541-5 draft standard. |
| 9-14 | Reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

This style includes those typefaces that are designed to simulate handwriting. This IBM Class reflects the ISO Script Class and Uncial Class as documented in the 12/87 ISO/IEC 9541-5 draft standard.

Class ID = 12: Symbolic

This style is generally design independent, making it suitable for Pi and special characters (icons, dingbats, technical symbols, etc.) that may be used equally well with any font. This IBM Class reflects various ISO Specific Groups, as noted below. It is documented in the 12/87 ISO/IEC 9541-5 draft standard.

**Table 18** : Symbolic (ClassID=12)

| Subc.ass | Name | Description |
| --- | --- | --- |
| 0 | No classification | This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource. |
| 1-2 | Reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 3 | Mixed serif | This style is characterized by either both or a combination of serif and sans serif designs on those characters of the font for which design is important (e.g., superscript and subscript characters, numbers, copyright or trademark symbols, etc.). An example of this font style is found in the IBM Symbol family. This IBM Subclass is not reflected in the 12/87 ISO/IEC 9541-5 draft standard. |
| 4-5 | Reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 6 | Oldstyle Serif | This style is characterized by a Oldstyle Serif IBM Class design on those characters of the font for which design is important (e.g., superscript and subscript characters, numbers, copyright or trademark symbols, etc.). An example of this font style is found in the IBM Sonoran Pi Serif family. This IBM Subclass is not directly reflected in the 12/87 ISO/IEC 9541-5 draft standard, though it is indirectly by the ISO Serif Class and Legibility Subclass (implies that all characters of the font exhibit the design appearance, while only a subset of the characters actually exhibit the design). |
| 7 | Neo-grotesque Sans Serif | This style is characterized by a Neo-grotesque Sans Serif IBM Font Class and Subclass design on those characters of the font for which design is important (e.g., superscript and subscript characters, numbers, copyright or trademark symbols, etc.). An example of this font style is f ound in the IBM Sonoran Pi Sans Serif family. This IBM Subclass is not directly reflected in the 12/87 ISO/IEC 9541-5 draft standard, though it is indirectly by the ISO Sans Serif Class and Gothic Subclass (implies that all characters of the font exhibit the design appearance, while only a subset of the characters actually exhibit the design). |
| 8-14 | Reserved | These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM. |
| 15 | Miscellaneous | This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass. |

<br>

<a id="anchor-OS2-part-8"></a>

## PANOSE

Table 19 documents a 10 byte array describing the PANOSE classification number. Tables 20 through 29 documents the contents of each of the byte arrays. Additional specifications required for PANOSE to specify non-Latin character sets.

The PANOSE definition contains ten digits each of which currently describes up to sixteen variations.

This 10 byte series of numbers are used to describe the visual characteristics of a given typeface. These characteristics are then used to associate the font with other fonts of similar appearance having different names. The variables for each digit are listed below. The specifications for each variable can be obtained in the specification PANOSE v2.0 Numerical Evaluation from available from Microsoft.

**Table 19** : PANOSE

| Type | Name |
| --- | --- |
| uint8\_t | bFamilyType; |
| uint8\_t | bSerifStyle; |
| uint8\_t | bWeight; |
| uint8\_t | bProportion; |
| uint8\_t | bContrast; |
| uint8\_t | bStrokeVariation; |
| uint8\_t | bArmStyle; |
| uint8\_t | bLetterform; |
| uint8\_t | bMidline; |
| uint8\_t | bXHeight; |

<br> **Table 20** : bFamilyType

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Text and Display |
| 3 | Script |
| 4 | Decorative |
| 5 | Pictorial |

<br> **Table 21** : bSerifStyle

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Cove |
| 3 | Obtuse Cove |
| 4 | Square Cove |
| 5 | Obtuse Square Cove |
| 6 | Square |
| 7 | Thin |
| 8 | Bone |
| 9 | Exaggerated |
| 10 | Triangle |
| 11 | Normal Sans |
| 12 | Obtuse Sans |
| 13 | Perp Sans |
| 14 | Flared |
| 15 | Rounded |

<br> **Table 22** : bWeight

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Very Light |
| 3 | Light |
| 4 | Thin |
| 5 | Book |
| 6 | Medium |
| 7 | Demi |
| 8 | Bold |
| 9 | Heavy |
| 10 | Black |
| 11 | Nord |

<br> **Table 23** : bProportion

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Old Style |
| 3 | Modern |
| 4 | Even Width |
| 5 | Expanded |
| 6 | Condensed |
| 7 | Very Expanded |
| 8 | Very Condensed |
| 9 | Monospaced |

<br> **Table 24** : bContrast

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | None |
| 3 | Very Low |
| 4 | Low |
| 5 | Medium Low |
| 6 | Medium |
| 7 | Medium High |
| 8 | High |
| 9 | Very High |

<br> **Table 25** : bStrokeVariatoon

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Gradual/Diagonal |
| 3 | Gradual/Transitional |
| 4 | Gradual/Vertical |
| 5 | Gradual/Horizontal |
| 6 | Rapid/Vertical |
| 7 | Rapid/Horizontal |
| 8 | Instant/Vertical |

<br> **Table 26** : bArmStyle

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Straight Arms/Horizontal |
| 3 | Straight Arms/Wedge |
| 4 | Straight Arms/Vertical |
| 5 | Straight Arms/Single Serif |
| 6 | Straight Arms/Double Serif |
| 7 | Non-Straight Arms/Horizontal |
| 8 | Non-Straight Arms/Wedge |
| 9 | Non-Straight Arms/Vertical |
| 10 | Non-Straight Arms/Single Serif |
| 11 | Non-Straight Arms/Double Serif |

<br> **Table 27** : bLetterform

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Normal/Contact |
| 3 | Normal/Weighted |
| 4 | Normal/Boxed |
| 5 | Normal/Flattened |
| 6 | Normal/Rounded |
| 7 | Normal/Off Center |
| 8 | Normal/Square |
| 9 | Oblique/Contact |
| 10 | Oblique/Weighted |
| 11 | Oblique/Boxed |
| 12 | Oblique/Flattened |
| 13 | Oblique/Rounded |
| 14 | Oblique/Off Center |
| 15 | Oblique/Square |

<br> **Table 28**

*bMidline*

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Standard/Trimmed |
| 3 | Standard/Pointed |
| 4 | Standard/Serifed |
| 5 | High/Trimmed |
| 6 | High/Pointed |
| 7 | High/Serifed |
| 8 | Constant/Trimmed |
| 9 | Constant/Pointed |
| 10 | Constant/Serifed |
| 11 | Low/Trimmed |
| 12 | Low/Pointed |
| 13 | Low/Serifed |

<br> **Table 29** : bXHeight

| Bit | Meaning |
| --- | --- |
| 0 | Any |
| 1 | No Fit |
| 2 | Constant/Small |
| 3 | Constant/Standard |
| 4 | Constant/Large |
| 5 | Ducking/Small |
| 6 | Ducking/Standard |
| 7 | Ducking/Large |

<a id="anchor-OS2-part-9"></a>

## ulUnicodeRange

`ulUnicodeRange` is an array of four 32-bit unsigned integers treated as a single bitfield, indicating the Unicode blocks or ranges covered by the font, with a value of 1 signifying that the given block or range is considered "covered" and a value of 0 signifying that it is not.

The exact semantics of "covered" are not defined, which gives font designers some flexibility. To illustrate, consider bit 33, which corresponds to the Unicode Currency Symbols block (U+20A0–U+20CF).

As of Unicode 8.0, this block has 31 defined characters. One (U+20A0 EURO-CURRENCY SIGN) does not correspond to any actual currency used either at present or in the past. Several others (e.g., U+20A3 FRENCH FRANC SIGN) correspond to currencies no longer in use. Moreover, as new currency symbols are created, new characters may be added to this block in the future, as, for example, U+20BE LARI SYMBOL was added to Unicode 8.0.

To require a font vendor to cover *every* defined character in this block in order to claim "coverage" by bit 33 of the `ulUnicodeRange` field is therefore unreasonable. Some of the characters are unlikely to be needed in practice, and complete coverage of the block for a given version of the Unicode standard may not be complete coverage for a later version.

The mapping of bits in this field to Unicode blocks and ranges is to be found [in the OpenType spec](https://www.microsoft.com/typography/otspec/os2.htm#ur).

<a id="anchor-OS2-part-10"></a>

## achVendID

`achVendID` is a 4-byte character array specifying the font vendor identification.

It is not the royalty owner of the original artwork but the company responsible for the marketing and distribution of the typeface that is being classified. It is reasonable to assume that there will be 6 vendors of ITC Zapf Dingbats for use on desktop platforms in the near future (if not already). It is also likely that the vendors will have other inherent benefits in their fonts (more kern pairs, unregularized data, hand hinted, etc.). This identifier will allow for the correct vendors type to be used over another, possibly inferior, font file. These id's are assigned by Microsoft; the currently assigned vendor id's are shown in Table 30.

**Table 30** : Vendor identification

| Vendor ID | Vendor Name |
| --- | --- |
| `'ACG '` | AGFA Compugraphic |
| `'Adbe'` | Adobe |
| `'Appl'` | Apple |
| `'Alts'` | Altsys |
| `'B&H '` | Bigelow & Holmes |
| `'Bert'` | Berthold |
| `'Bits'` | Bitstream |
| `'DTC '` | Digital Typeface Corp. |
| `'HP  '` | Hewlett-Packard |
| `'IBM '` | IBM |
| `'KATF'` | Kingsley/ATF |
| `'Lans'` | Lanston Type Co., Ltd. |
| `'LETR'` | Letraset |
| `'Lino'` | Linotype |
| `'Mono'` | Monotype |
| `'MS  '` | Microsoft |
| `'QMSI'` | QMS/Imagen |
| `'URW '` | URW |
| `'ZSFT'` | ZSoft |

<br>

<a id="anchor-OS2-part-11"></a>

## fsSelection

fsSelection is a 2-byte bit field containing information concerning the nature of the font patterns, as follows:

**Table 31** : Font patterns

| Bit # | C definition | Description |
| --- | --- | --- |
| 0 | ITALIC | Font contains Italic characters, otherwise they are upright. |
| 1 | UNDERSCORE | Characters are underscored. |
| 2 | NEGATIVE | Characters have their foreground and background reversed. |
| 3 | OUTLINED | Outline (hollow) characters, otherwise they are solid. |
| 4 | STRIKEOUT | Characters are overstruck. |
| 5 | BOLD | Characters are emboldened. |

<a id="anchor-OS2-part-12"></a>

## Platform-specific Information

This table is not fully used by macOS; however, it is used extensively by other platforms and non-Apple products.

Font vendors should fill in *all* the data in this table accurately, even if the font is intended for use on macOS only.

Many fonts have inaccurate information in their `'OS/2'` table. Apple recommends that macOS client applications not depend on accurate information in the `'OS/2'` table.

<a id="anchor-OS2-part-13"></a>

## Dependencies

A number of fields in the `'OS/2'` table replicate data found elsewhere in the font; most notably, the various ascent and descent fields mirror some of the contents of the [horizontal header table](hhea.md). The macOS derives ascent and descent information from the latter; Windows from the former.

Fonts intended to be used on both platforms *must* have consistent values for the font's ascent and descent in these two tables.
