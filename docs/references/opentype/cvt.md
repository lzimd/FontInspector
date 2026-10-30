---
title: "cvt — Control Value Table"
description: "The control value table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2017-01-04T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7a06e1def6e2f40e43dc8897e5372614bcc413f6/typographydocs/opentype/spec/cvt.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-cvt-cvt-control-value-table"></a>

# cvt — Control Value Table

This table contains a list of values that can be referenced by instructions. They can be used, among other things, to control characteristics for different glyphs. The length of the table must be an integral number of FWORD units.

| Type | Description |
| --- | --- |
| FWORD\[ *n* \] | List of *n* values referenceable by instructions. *n* is the number of FWORD items that fit in the size of the table. |
