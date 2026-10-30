---
title: "prep — Control Value Program"
description: "The control value program table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2023-04-13T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/prep.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-prep-prep-control-value-program"></a>

# prep — Control Value Program

The Control Value (CV) Program consists of a set of TrueType instructions that can be used to make font-wide changes in the Control Value Table. Any instruction is valid in the CV Program but since no glyph is associated with it, instructions intended to move points within a particular glyph outline have no effect in the CV Program.

The CV Program can potentially be executed before any glyph is processed, as determined by the rasterizer implementation. The CV Program will always be executed before the first glyph is processed after a change in font, point size, global transformation matrix, or other values that can be obtained from the [GET INFOrmation instruction](tt_instructions.md#anchor-tt_instructions-get-information). The CV Program is not re-executed for components in a composite glyph, including cases in which a composite glyph description applies a transform to a component.

> *Note:* The tag 'prep' is anachronistic: in earlier specifications, the table was referred to as the *Pre Program* table.

| Type | Description |
| --- | --- |
| uint8\[ *n* \] | Set of instructions executed whenever point size or font or transformation change. *n* is the number of uint8 items that fit in the size of the table. |
