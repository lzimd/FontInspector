---
title: "Registered Design-Variation Axis Tag: 'ital'"
description: "Registered design-variation axis tag &#39;ital&#39; (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2020-10-08T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7a06e1def6e2f40e43dc8897e5372614bcc413f6/typographydocs/opentype/spec/dvaraxistag_ital.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-dvaraxistag_ital-registered-design-variation-axis-tag-ital"></a>

# Registered Design-Variation Axis Tag: 'ital'

<a id="anchor-dvaraxistag_ital-axis-definition"></a>

## Axis definition

*Tag:* 'ital'

*Name:* Italic

*Description:* Used to vary between non-italic and italic.

*Valid numeric range:* Values must be in the range 0 to 1.

*Scale interpretation:* A value of 0 can be interpreted as “Roman” (non-italic); a value of 1 can be interpreted as (fully) italic.

*Recommended or required “Regular” value:* 0 is required.

<a id="anchor-dvaraxistag_ital-additional-information"></a>

## Additional information

The Italic axis has long been treated as a kind of design variation within a font family. The 'ital' axis tag is used within a [STAT](stat.md) table of italic fonts to provide a complete characterization of a font in relation to its family within the STAT table. The Italic axis can be used as a variation axis within a variable font, though this is not expected to be common.

The Italic axis is distinct from the Slant axis ('slnt'). Fonts may use one or the other, depending on the nature of the design, but should rarely use both. While an italic design often incorporates some slant in the design, use of the Italic axis does not require use of the Slant axis. An italic font should not be characterized in the STAT table as being italic *and also* having some slant, unless the font family includes multiple italic designs with different amounts of slant.
