---
title: "Registered Design-Variation Axis Tag: 'opsz'"
description: "Registered design-variation axis tag &#39;opsz&#39; (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-29T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/dvaraxistag_opsz.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-dvaraxistag_opsz-registered-design-variation-axis-tag-opsz"></a>

# Registered Design-Variation Axis Tag: 'opsz'

<a id="anchor-dvaraxistag_opsz-axis-definition"></a>

## Axis definition

*Tag:* 'opsz'

*Name:* Optical Size

*Description:* Used to vary design to suit different text sizes.

*Valid numeric range:* Values must be strictly greater than zero.

*Scale interpretation:* Values can be interpreted as text size, in typographic points, as defined in the OpenType specification: a physical unit equal to 1/72 of a standard physical inch.

*Recommended or required “Regular” value:* A value in the range 10 to 16 is recommended for typical text settings.

*Suggested programmatic interactions:* Applications may choose to select an optical-size variant automatically based on the displayed text size.

<a id="anchor-dvaraxistag_opsz-additional-information"></a>

## Additional information

The Optical size axis can be used as a variation axis within a variable font. It can also be used within a [STAT](stat.md) table in non-variable fonts within a family that has optical-size variants to provide a complete characterization of a font in relation to its family within the STAT table. In the STAT table of a non-variable font, a format 2 axis value table is recommended to characterize the range of text sizes for which the optical-size variant is intended.

Typical font implementation of optical size design variants involves adapting glyph proportions, stem weights, and details to be appropriate to specific sizes of displayed text. These adaptations may be both functional and aesthetic, ensuring legibility at smaller sizes and refinement of fine details and overall width at larger sizes. The nature of the adaptations may depend on aspects of the individual typeface design, the characters or scripts involved, targeted devices on which the font may be displayed, and known or intended distance from which text will be viewed.

Type designers may develop size-specific design variations based on print or screen rendering, typically evaluating the design of these variations at a reading distance of 14 to 16 inches, or 35 to 40 cm. This can be used as a basis for determining appropriate optical size variants for different distances. For example, if the design of a given optical size variant is appropriate for 12-point text viewed from a reading distance of 15 inches, it should also be appropriate for 24 point text viewed from a reading distance of 30 inches.

The scale for the Optical size axis is text size in points. For these purposes, the text size is as determined by the document or application for its intended use; the actual physical size on a display may be different due to platform or application scaling methods or intended viewing distance.

The target of size-specific design is optical, i.e., tailored to what the reader is seeing. For this reason, Optical size axis variant selection should be determined, so far as possible, by as much information as available regarding displayed size of text *as seen by the reader*. Factors to be taken into account should include the scaling of type on specific platforms and the translation of document and platform units to 1/72 of a physical inch, as well as typical reading distances for applications and devices. This may mean that a nominally specified text size in a document could result in a different Optical size axis variant selection on different platforms and devices, determined by the actual size of text seen by the reader.

> *Note:* User-perceived size is very dependent on viewing distance, not only physical size on the display. For example, when viewing text on a large-screen TV, the physical size on the display will be many times larger than the size perceived by the user. In this case, selecting an Optical size variant based only on the physical size on the display would likely result in reduced legibility for the user.

When translating between document units and the point (1/72 inch) scale for this axis, care should be taken not to assume equivalences between units that may apply on some platforms but not others.

In applications that automatically select an Optical size variant, this should normally be done based on the text size with a default or “100%” zoom level, not on a combination of text size and zoom level. Types of zoom that do not trigger re-layout of text should not change Optical size variant selection, while content enlarging or diminishing operations that change re-layout of text should make a new Optical size variant selection based on the new displayed sized.

If the size of displayed text is smaller or greater than the minimum and maximum extent of the axis range, Optical size axis variant selection should be clamped to the appropriate minimum or maximum axis value, not reset to the default instance.

It is recommended that software provide means to override automatic Optical size variant selection, as may be appropriate for particular platforms, intended use, known viewing distance, or accessibility.
