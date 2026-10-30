---
title: "Registered Design-Variation Axis Tag: 'wght'"
description: "Registered design-variation axis tag &#39;wght&#39; (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2020-10-08T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7a06e1def6e2f40e43dc8897e5372614bcc413f6/typographydocs/opentype/spec/dvaraxistag_wght.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-dvaraxistag_wght-registered-design-variation-axis-tag-wght"></a>

# Registered Design-Variation Axis Tag: 'wght'

<a id="anchor-dvaraxistag_wght-axis-definition"></a>

## Axis definition

*Tag:* 'wght'

*Name:* Weight

*Description:* Used to vary stroke thicknesses or other design details to give variation from lighter to blacker.

*Valid numeric range:* Values must be in the range 1 to 1000.

*Scale interpretation:* Values can be interpreted in direct comparison to values for [usWeightClass](os2.md) in the OS/2 table, or the CSS font-weight property.

*Recommended or required “Regular” value:* 400 is required.

<a id="anchor-dvaraxistag_wght-additional-information"></a>

## Additional information

The Weight axis has long been used in conjunction with face names such as “Regular”, “Light” or “Bold”. Change in stroke thickness is typically the primary aspect of the design that varies, though other secondary details such as glyph width or thick-thin contrast may also be encompassed in this variation.

The Weight axis can be used as a variation axis within a variable font. It can also be used within a [STAT](stat.md) table in non-variable fonts within a family that has weight variants to provide a complete characterization of a font in relation to its family within the STAT table.

In a variable font that implements 'wght' variations, the value in the usWeightClass field of the OS/2 table must match the default 'wght' value specified in the ['fvar'](fvar.md) table. For non-default instances of a variable font, the 'wght' axis value can be used as the OS/2.usWeightClass value for the instance.
