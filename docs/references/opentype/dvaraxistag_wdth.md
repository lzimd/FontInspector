---
title: "Registered Design-Variation Axis Tag: 'wdth'"
description: "Registered design-variation axis tag &#39;wdth&#39; (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2020-10-08T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7a06e1def6e2f40e43dc8897e5372614bcc413f6/typographydocs/opentype/spec/dvaraxistag_wdth.md"
last-modified: "2026-09-17T18:19:03Z"
---

<a id="anchor-dvaraxistag_wdth-registered-design-variation-axis-tag-wdth"></a>

# Registered Design-Variation Axis Tag: 'wdth'

<a id="anchor-dvaraxistag_wdth-axis-definition"></a>

## Axis definition

*Tag:* 'wdth'

*Name:* Width

*Description:* Used to vary width of text from narrower to wider.

*Valid numeric range:* Values must be strictly greater than zero.

*Scale interpretation:* Values can be interpreted as a percentage of whatever the font designer considers “normal width” for that font design.

*Recommended or required “Regular” value:* 100 is required.

*Suggested programmatic interactions:* Applications may choose to select a width variant in a variable font automatically in order to fit a span of text into a target width.

<a id="anchor-dvaraxistag_wdth-additional-information"></a>

## Additional information

The Width axis has long been used in conjunction with face names such as “Condensed” or “Extended”. Change in glyph width is typically the primary aspect of the design that varies, though other secondary details such as stroke thickness may also be encompassed in this variation.

The Width axis can be used as a variation axis within a variable font. It can also be used within a [STAT](stat.md) table in non-variable fonts within a family that has width variants to provide a complete characterization of a font in relation to its family within the STAT table.

The Width axis uses a scale that correlates with but is different from the scale used for the [usWidthClass](os2.md) field of the OS/2 table. The description of usWeightClass in the OS/2 table documentation provides a table of mappings from usWidthClass values to “% of normal” values. Because usWidthClass is limited to nine integer values, it has much less granularity than the Width axis.

When mapping from 'wdth' values to usWidthClass, interpolate fractional values between the mapped values and then round, and clamp to the range 1 to 9.

In a variable font that implements 'wdth' variations, the value in the usWidthClass field of the OS/2 table must correspond to the default 'wdth' value specified in the ['fvar'](fvar.md) table. For non-default instances of a variable font, the 'wdth' axis value can be used to derive the OS/2.usWidthClass value for that instance.

Percentage of normal width is a comparitive scale that will depend on the specific items being compared. The width of a line of text very much depends on the content of the text. No specific reference string is specified here as the basis for comparisons; a font designer can choose what they consider to be representative strings assigning a 'wdth' value to a design variant. Ideally, the 'wdth' value should provide a good estimate for most strings in the target languages of how the width of the string formatted with that 'wdth' variant compares to the width of the same string when formatted with the “normal” variant.

When using a variable font, applications may choose to make small, automated 'wdth' adjustments in order to fit a span of text to some target size. This might be done, for instance, to fit headings within a column, or to improve paragraphy layout. The relative change in 'wdth' value (ratio of the original 'wdth' to the adjusted 'wdth') may be used as a first approximation of the adjustment needed. Since the relative change in width may depend on the actual text content, however, this may not provide the exact adjustment needed to obtain the desired width adjustment. The application will likely need to refine the adjustment over multiple attempts.
