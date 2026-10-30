---
title: "fpgm — Font Program"
description: "The font program table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-29T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/fpgm.md"
last-modified: "2026-09-17T18:19:03Z"
---

<a id="anchor-fpgm-fpgm-font-program"></a>

# fpgm — Font Program

This table is similar to the Control Value (CV) Program, except that it is only run once, when the font is first used. It is used only for FDEFs and IDEFs. Thus, the CV Program need not contain function definitions. However, the CV Program may redefine existing FDEFs or IDEFs.

This table is optional.

| Type | Description |
| --- | --- |
| uint8\[ *n* \] | Instructions. *n* is the number of uint8 items that fit in the size of the table. |
