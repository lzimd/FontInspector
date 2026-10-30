---
title: "IBM Font Family Classifications"
description: "IBM Font Family Classifications (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-29T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/ibmfc.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-ibmfc-ibm-font-family-classifications"></a>

# IBM Font Family Classifications

The section defines the family class and subclass values that may be used in the [sFamilyClass](os2.md#anchor-os2-sfamilyclass) field of a font’s OS/2 table. A font designer or supplier can assign these values in a font to provide a classification of the font family design. The registered values documented here were originally defined by IBM.

These values classify a font design as to its appearance, but do not identify the specific font family, typeface variation, designer, supplier, size, or metric table differences. It should be noted that some font designs can be classified equally well into more than class or subclass. Such designs should be matched to a classification for which substitution of another font design from the same class or subclass would generally result in a similar appearance of the presented document.

<a id="anchor-ibmfc-class-id-0-no-classification"></a>

## Class ID = 0 No Classification

This class ID is used to indicate that the associated font has no design classification or that the design classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-class-id-1-oldstyle-serifs"></a>

## Class ID = 1 Oldstyle Serifs

This style is generally based upon the Latin printing style of the 15th to 17th century, with a mild diagonal contrast in stroke emphasis (lighter in upper left to lower right, heavier in upper right to lower left) and bracketed serifs. This IBM Class reflects the ISO Serif Class, Oldstyle and Legibility Subclasses as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design subclassification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-ibm-rounded-legibility"></a>

### Subclass ID = 1: IBM Rounded Legibility

This style is generally characterized by a large x-height, with short ascenders and descenders. Specifically, it is distinguished by a medium resolution, hand tuned, bitmap rendition of the more general rounded legibility subclass. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-garalde"></a>

### Subclass ID = 2: Garalde

This style is generally characterized by a medium x-height, with tall ascenders. An example of this font style is the ITC Garamond family. This IBM Subclass reflects the ISO Serif Class, Oldstyle Subclass, and Garalde Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-3-venetian"></a>

### Subclass ID = 3: Venetian

This style is generally characterized by a medium x-height, with a relatively monotone appearance and sweeping tails based on the designs of the early Venetian printers. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-4-modified-venetian"></a>

### Subclass ID = 4: Modified Venetian

This style is generally characterized by a large x-height, with a relatively monotone appearance and sweeping tails based on the designs of the early Venetian printers. An example of this font style is the Allied Linotype Palatino family. This IBM Subclass reflects the ISO Serif Class, Transitional Subclass, and Modified Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-5-dutch-modern"></a>

### Subclass ID = 5: Dutch Modern

This style is generally characterized by a large x-height, with wedge shaped serifs and a circular appearance to the bowls similar to the Dutch Traditional Subclass below, but with lighter strokes. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-6-dutch-traditional"></a>

### Subclass ID = 6: Dutch Traditional

This style is generally characterized by a large x-height, with wedge shaped serifs and a circular appearance of the bowls. An example of this font style is the IBM Press Roman family. This IBM Subclass reflects the ISO Serif Class and Legibility Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-7-contemporary"></a>

### Subclass ID = 7: Contemporary

This style is generally characterized by a small x-height, with light strokes and serifs. An example of this font style is the University family. This IBM Subclass reflects the ISO Serif Class and Contemporary Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-8-calligraphic"></a>

### Subclass ID = 8: Calligraphic

This style is generally characterized by the fine handwriting style of calligraphy, while retaining the characteristic Oldstyle appearance. This IBM Subclass is not reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-9-14-reserved-for-future-use"></a>

### Subclass ID = 9-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-2-transitional-serifs"></a>

## Class ID = 2 Transitional Serifs

This style is generally based upon the Latin printing style of the 18th to 19th century, with a pronounced vertical contrast in stroke emphasis (vertical strokes being heavier than the horizontal strokes) and bracketed serifs. This IBM Class reflects the ISO Serif Class, Transitional Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-1"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-direct-line"></a>

### Subclass ID = 1: Direct Line

This style is generally characterized by a medium x-height, with fine serifs, noticeable contrast, and capital letters of approximately the same width. An example of this font style is the Monotype Baskerville family. This IBM Subclass reflects the ISO Serif Class, Transitional Subclass, and Direct Line Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-script"></a>

### Subclass ID = 2: Script

This style is generally characterized by a handwritten script appearance while retaining the Transitional Direct Line style. An example of this font style is the IBM Nasseem (Arabic) family. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard, though the ISO Serif Class, Transitional Subclass, and Direct Line Specific Group would be a close approximation.

<a id="anchor-ibmfc-subclass-id-3-14-reserved-for-future-use"></a>

### Subclass ID = 3-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-1"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-3-modern-serifs"></a>

## Class ID = 3 Modern Serifs

This style is generally based upon the Latin printing style of the 20th century, with an extreme contrast between the thick and thin portion of the strokes. This IBM Class reflects the ISO Serif Class, Modern Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-2"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-italian"></a>

### Subclass ID = 1: Italian

This style is generally characterized by a medium x-height, with thin hairline serifs. An example of this font style is the Monotype Bodoni family. This IBM Subclass reflects the ISO Serif Class, Modern Subclass, and Italian Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-script-1"></a>

### Subclass ID = 2: Script

This style is generally characterized by a handwritten script appearance while retaining the Modern Italian style. An example of this font style is the IBM Narkissim (Hebrew) family. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard, though the ISO Serif Class, Modern Subclass, and Italian Specific Group would be a close approximation.

<a id="anchor-ibmfc-subclass-id-3-14-reserved-for-future-use-1"></a>

### Subclass ID = 3-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-2"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-4-clarendon-serifs"></a>

## Class ID = 4 Clarendon Serifs

This style is a variation of the Oldstyle Serifs and the Transitional Serifs, with a mild vertical stroke contrast and bracketed serifs. This IBM Class reflects the ISO Serif Class, Square Serif Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-3"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-clarendon"></a>

### Subclass ID = 1: Clarendon

This style is generally characterized by a large x-height, with serifs and strokes of equal weight. An example of this font style is the Allied Linotype Clarendon family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Clarendon Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-modern"></a>

### Subclass ID = 2: Modern

This style is generally characterized by a large x-height, with serifs of a lighter weight than the strokes and the strokes of a lighter weight than the Traditional. An example of this font style is the Monotype Century Schoolbook family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Clarendon Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-3-traditional"></a>

### Subclass ID = 3: Traditional

This style is generally characterized by a large x-height, with serifs of a lighter weight than the strokes. An example of this font style is the Monotype Century family.This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Clarendon Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-4-newspaper"></a>

### Subclass ID = 4: Newspaper

This style is generally characterized by a large x-height, with a simpler style of design and serifs of a lighter weight than the strokes. An example of this font style is the Allied Linotype Excelsior Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Clarendon Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-5-stub-serif"></a>

### Subclass ID = 5: Stub Serif

This style is generally characterized by a large x-height, with short stub serifs and relatively bold stems. An example of this font style is the Cheltenham Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Short Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-6-monotone"></a>

### Subclass ID = 6: Monotone

This style is generally characterized by a large x-height, with monotone stems. An example of this font style is the ITC Korinna Family. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-7-typewriter"></a>

### Subclass ID = 7: Typewriter

This style is generally characterized by a large x-height, with moderate stroke thickness characteristic of a typewriter. An example of this font style is the Prestige Elite Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Typewriter Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-8-14-reserved-for-future-use"></a>

### Subclass ID = 8-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-3"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-5-slab-serifs"></a>

## Class ID = 5 Slab Serifs

This style is characterized by serifs with a square transition between the strokes and the serifs (no brackets). This IBM Class reflects the ISO Serif Class, Square Serif Subclass (except the Clarendon Specific Group) as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-4"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-monotone"></a>

### Subclass ID = 1: Monotone

This style is generally characterized by a large x-height, with serifs and strokes of equal weight. An example of this font style is the ITC Lubalin Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-humanist"></a>

### Subclass ID = 2: Humanist

This style is generally characterized by a medium x-height, with serifs of lighter weight that the strokes. An example of this font style is the Candida Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-3-geometric"></a>

### Subclass ID = 3: Geometric

This style is generally characterized by a large x-height, with serifs and strokes of equal weight and a geometric (circles and lines) design. An example of this font style is the Monotype Rockwell Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-4-swiss"></a>

### Subclass ID = 4: Swiss

This style is generally characterized by a large x-height, with serifs and strokes of equal weight and an emphasis on the white space of the characters. An example of this font style is the Allied Linotype Serifa Family. This IBM Subclass reflects the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-5-typewriter"></a>

### Subclass ID = 5: Typewriter

This style is generally characterized by a large x-height, with serifs and strokes of equal but moderate thickness, and a geometric design. An example of this font style is the IBM Courier Family. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard, though the ISO Serif Class, Square Serif Subclass, and Monotone Specific Group would be a close approximation.

<a id="anchor-ibmfc-subclass-id-6-14-reserved-for-future-use"></a>

### Subclass ID = 6-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-4"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-6-reserved-for-future-use"></a>

## Class ID = 6 (reserved for future use)

This class ID is reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-class-id-7-freeform-serifs"></a>

## Class ID = 7 Freeform Serifs

This style includes serifs, but which expresses a design freedom that does not generally fit within the other serif design classifications. This IBM Class reflects the remaining ISO Serif Class subclasses as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-5"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-modern"></a>

### Subclass ID = 1: Modern

This style is generally characterized by a medium x-height, with light contrast in the strokes and a round full design. An example of this font style is the ITC Souvenir Family. This IBM Subclass is not reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-14-reserved-for-future-use"></a>

### Subclass ID = 2-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-5"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-8-sans-serif"></a>

## Class ID = 8 Sans Serif

This style includes most basic letter forms (excluding Scripts and Ornamentals) that do not have serifs on the strokes. This IBM Class reflects the ISO Sans Serif Class as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-6"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-ibm-neo-grotesque-gothic"></a>

### Subclass ID = 1: IBM Neo-grotesque Gothic

This style is generally characterized by a large x-height, with uniform stroke width and a simple one-story design distinguished by a medium resolution, hand tuned, bitmap rendition of the more general Neo-grotesque Gothic Subclass. An example of this font style is the IBM Sonoran Sans Serif family. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-humanist-1"></a>

### Subclass ID = 2: Humanist

This style is generally characterized by a medium x-height, with light contrast in the strokes and a classic Roman letterform. An example of this font style is the Allied Linotype Optima family. This IBM Subclass reflects the ISO Sans Serif Class, Humanist Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-3-low-x-round-geometric"></a>

### Subclass ID = 3: Low-x Round Geometric

This style is generally characterized by a low x-height, with monotone stroke weight and a round geometric design. An example of this font style is the Fundicion Tipograficia Neufville Futura family. This IBM Subclass reflects the ISO Sans Serif Class, Geometric Subclass, Round Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-4-high-x-round-geometric"></a>

### Subclass ID = 4: High-x Round Geometric

This style is generally characterized by a high x-height, with uniform stroke weight and a round geometric design. An example of this font style is the ITC Avant Garde Gothic family. This IBM Subclass reflects the ISO Sans Serif Class, Geometric Subclass, Round Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-5-neo-grotesque-gothic"></a>

### Subclass ID = 5: Neo-grotesque Gothic

This style is generally characterized by a high x-height, with uniform stroke width and a simple one-story design. An example of this font style is the Allied Linotype Helvetica family. This IBM Subclass reflects the ISO Sans Serif Class, Gothic Subclass, Neo-grotesque Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-6-modified-neo-grotesque-gothic"></a>

### Subclass ID = 6: Modified Neo-grotesque Gothic

This style is similar to the Neo-grotesque Gothic style, with design variations to the G and Q. An example of this font style is the Allied Linotype Univers family. This IBM Subclass is not specifically reflected in the ISO/IEC 9541-1 Amendment 1 standard, though the ISO Sans Serif Class, Gothic Subclass, Neo-grotesque Specific Group would be a close approximation.

<a id="anchor-ibmfc-subclass-id-7-8-reserved-for-future-use"></a>

### Subclass ID = 7-8: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-9-typewriter-gothic"></a>

### Subclass ID = 9: Typewriter Gothic

This style is similar to the Neo-grotesque Gothic style, with moderate stroke thickness characteristic of a typewriter. An example of this font style is the IBM Letter Gothic family. This IBM Subclass reflects the ISO Sans Serif Class, Gothic Subclass, Typewriter Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-10-matrix"></a>

### Subclass ID = 10: Matrix

This style is generally a simple design characteristic of a dot matrix printer. An example of this font style is the IBM Matrix Gothic family. This IBM Subclass is not reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-11-14-reserved-for-future-use"></a>

### Subclass ID = 11-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-6"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-9-ornamentals"></a>

## Class ID = 9 Ornamentals

This style includes highly decorated or stylized character shapes that are typically used in headlines. This IBM Class reflects the ISO Ornamental Class and the ISO Blackletter Class as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-7"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-engraver"></a>

### Subclass ID = 1: Engraver

This style is characterized by fine lines or lines engraved on the stems. An example of this font style is the Copperplate family. This IBM Subclass reflects the ISO Ornamental Class and Inline Subclass, or the Serif Class and Engraving Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-black-letter"></a>

### Subclass ID = 2: Black Letter

This style is generally based upon the printing style of the German monasteries and printers of the 12th to 15th centuries. An example of this font style is the Old English family. This IBM Subclass reflects the ISO Blackletters Class as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-3-decorative"></a>

### Subclass ID = 3: Decorative

This style is characterized by ornamental designs (typically from nature, such as leaves, flowers, animals, etc.) incorporated into the stems and strokes of the characters. An example of this font style is the Saphire family. This IBM Subclass reflects the ISO Ornamental Class and Decorative Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-4-three-dimensional"></a>

### Subclass ID = 4: Three Dimensional

This style is characterized by a three-dimensional (raised) appearance of the characters created by shading or geometric effects. An example of this font style is the Thorne Shaded family. This IBM Subclass reflects the ISO Ornamental Class and Three Dimensional Subclass as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-5-14-reserved-for-future-use"></a>

### Subclass ID = 5-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-7"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-10-scripts"></a>

## Class ID = 10 Scripts

This style includes those typefaces that are designed to simulate handwriting. This IBM Class reflects the ISO Script Class and Uncial Class as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-8"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-uncial"></a>

### Subclass ID = 1: Uncial

This style is characterized by unjoined (nonconnecting) characters that are generally based on the handwriting style of Europe in the 6th to 9th centuries. An example of this font style is the Libra family. This IBM Subclass reflects the ISO Uncial Class as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-2-brush-joined"></a>

### Subclass ID = 2: Brush Joined

This style is characterized by joined (connecting) characters that have the appearance of being painted with a brush, with moderate contrast between thick and thin strokes. An example of this font style is the Mistral family. This IBM Subclass reflects the ISO Script Class, Joined Subclass, and Informal Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-3-formal-joined"></a>

### Subclass ID = 3: Formal Joined

This style is characterized by joined (connecting) characters that have a printed (or drawn with a stiff brush) appearance with extreme contrast between the thick and thin strokes. An example of this font style is the Coronet family. This IBM Subclass reflects the ISO Script Class, Joined Subclass, and Formal Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-4-monotone-joined"></a>

### Subclass ID = 4: Monotone Joined

This style is characterized by joined (connecting) characters that have a uniform appearance with little or no contrast in the strokes. An example of this font style is the Kaufmann family. This IBM Subclass reflects the ISO Script Class, Joined Subclass, and Monotone Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-5-calligraphic"></a>

### Subclass ID = 5: Calligraphic

This style is characterized by beautifully hand drawn, unjoined (non-connecting) characters that have an appearance of being drawn with a broad edge pen. An example of this font style is the Thompson Quillscript family. This IBM Subclass reflects the ISO Script Class, Unjoined Subclass, and Calligraphic Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-6-brush-unjoined"></a>

### Subclass ID = 6: Brush Unjoined

This style is characterized by unjoined (non-connecting) characters that have the appearance of being painted with a brush, with moderate contrast between thick and thin strokes. An example of this font style is the Saltino family. This IBM Subclass reflects the ISO Script Class, Unjoined Subclass, and Brush Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-7-formal-unjoined"></a>

### Subclass ID = 7: Formal Unjoined

This style is characterized by unjoined (non-connecting) characters that have a printed (or drawn with a stiff brush) appearance with extreme contrast between the thick and thin strokes. An example of this font style is the Virtuosa family. This IBM Subclass reflects the ISO Script Class, Unjoined Subclass, and Formal Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-8-monotone-unjoined"></a>

### Subclass ID = 8: Monotone Unjoined

This style is characterized by unjoined (non-connecting) characters that have a uniform appearance with little or no contrast in the strokes. An example of this font style is the Gilles Gothic family. This IBM Subclass reflects the ISO Script Class, Unjoined Subclass, and Monotone Specific Group as documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-9-14-reserved-for-future-use-1"></a>

### Subclass ID = 9-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-8"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-11-reserved-for-future-use"></a>

## Class ID = 11 (reserved for future use)

This class ID is reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-class-id-12-symbolic"></a>

## Class ID = 12 Symbolic

This style is generally design independent, making it suitable for Pi and special characters (icons, dingbats, technical symbols, etc.) that may be used equally well with any font. This IBM Class reflects various ISO Specific Groups, as noted below and documented in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-0-no-classification-9"></a>

### Subclass ID = 0: No Classification

This subclass ID is used to indicate that the associated font has no design sub-classification or that the design sub-classification is not of significance to the creator or user of the font resource.

<a id="anchor-ibmfc-subclass-id-1-2-reserved-for-future-use"></a>

### Subclass ID = 1-2: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-3-mixed-serif"></a>

### Subclass ID = 3: Mixed Serif

This style is characterized by either both or a combination of serif and sans serif designs on those characters of the font for which design is important (e.g., superscript and subscript characters, numbers, copyright or trademark symbols, etc.). An example of this font style is found in the IBM Symbol family. This IBM Subclass is not reflected in the ISO/IEC 9541-1 Amendment 1 standard.

<a id="anchor-ibmfc-subclass-id-4-5-reserved-for-future-use"></a>

### Subclass ID = 4-5: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-6-oldstyle-serif"></a>

### Subclass ID = 6: Oldstyle Serif

This style is characterized by a Oldstyle Serif IBM Class design on those characters of the font for which design is important (e.g., superscript and subscript characters, numbers, copyright or trademark symbols, etc.). An example of this font style is found in the IBM Sonoran Pi Serif family. This IBM Subclass is not directly reflected in the ISO/IEC 9541-1 Amendment 1 standard, though it is indirectly by the ISO Serif Class and Legibility Subclass (implies that all characters of the font exhibit the design appearance, while only a subset of the characters actually exhibit the design).

<a id="anchor-ibmfc-subclass-id-7-neo-grotesque-sans-serif"></a>

### Subclass ID = 7: Neo-grotesque Sans Serif

This style is characterized by a Neo-grotesque Sans Serif IBM Font Class and Subclass design on those characters of the font for which design is important (e.g., superscript and subscript characters, numbers, copyright or trademark symbols, etc.). An example of this font style is found in the IBM Sonoran Pi Sans Serif family. This IBM Subclass is not directly reflected in the ISO/IEC 9541-1 Amendment 1 standard, though it is indirectly by the ISO Sans Serif Class and Gothic Subclass (implies that all characters of the font exhibit the design appearance, while only a subset of the characters actually exhibit the design).

<a id="anchor-ibmfc-subclass-id-8-14-reserved-for-future-use-1"></a>

### Subclass ID = 8-14: (reserved for future use)

These subclass IDs are reserved for future assignment, and shall not be used without formal assignment by IBM.

<a id="anchor-ibmfc-subclass-id-15-miscellaneous-9"></a>

### Subclass ID = 15: Miscellaneous

This subclass ID is used for miscellaneous designs of the associated design class that are not covered by another Subclass.

<a id="anchor-ibmfc-class-id-13-reserved"></a>

## Class ID = 13 Reserved

<a id="anchor-ibmfc-class-id-14-reserved"></a>

## Class ID = 14 Reserved
