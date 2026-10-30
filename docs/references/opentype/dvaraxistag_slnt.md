---
title: "Registered Design-Variation Axis Tag: 'slnt'"
description: "Registered design-variation axis tag &#39;slnt&#39; (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2020-10-08T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7a06e1def6e2f40e43dc8897e5372614bcc413f6/typographydocs/opentype/spec/dvaraxistag_slnt.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-dvaraxistag_slnt-registered-design-variation-axis-tag-slnt"></a>

# Registered Design-Variation Axis Tag: 'slnt'

<a id="anchor-dvaraxistag_slnt-axis-definition"></a>

## Axis definition

*Tag:* 'slnt'

*Name:* Slant

*Description:* Used to vary between upright and slanted text.

*Valid numeric range:* Values must be greater than -90 and less than +90.

*Scale interpretation:* Values can be interpreted as the angle, in counter-clockwise degrees, of oblique slant from whatever the designer considers to be upright for that font design.

*Recommended or required “Regular” value:* 0 is required.

<a id="anchor-dvaraxistag_slnt-additional-information"></a>

## Additional information

The Slant axis can be used as a variation axis within a variable font. It can also be used within a [STAT](stat.md) table in non-variable, oblique fonts to provide a complete characterization of a font in relation to its family within the STAT table.

The Slant axis is distinct from the Italic axis ('ital'). Fonts may use one or the other, depending on the nature of the design, but should rarely use both. While an italic design often incorporates some slant in the design, use of the Italic axis does not require use of the Slant axis. An italic font should not be characterized in the STAT table as being italic *and also* having some slant, unless the font family includes multiple italic designs with different amounts of slant.

Note that the scale for the Slant axis is interpreted as the angle of slant in *counter-clockwise* degrees from upright. This means that a typical, right-leaning oblique design will have a negative slant value. This matches the scale used for the italicAngle field in the ['post'](post.md) table.

In a variable font that implements 'slnt' variations, the value in the italicAngle field of the 'post' table must match the default 'slnt' value specified in the ['fvar'](fvar.md) table. For non-default instances of a variable font, the 'slnt' axis value can be used as the post.italicAngle value for the instance.
