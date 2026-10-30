---
title: "Name String Examples"
description: "Name string examples (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2018-08-16T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7a06e1def6e2f40e43dc8897e5372614bcc413f6/typographydocs/opentype/spec/namesmp.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-namesmp-name-string-examples"></a>

# Name String Examples

The following is an example of how name strings would be made for the Arial family.

| Font | Name ID 1 | Name ID 2 | Name ID 4 | Name ID 16 | Name ID 17 |
| --- | --- | --- | --- | --- | --- |
| Arial Narrow | Arial Narrow | Regular | Arial Narrow | Arial | Narrow |
| Arial Narrow Italic | Arial Narrow | Italic | Arial Narrow Italic | Arial | Narrow Italic |
| Arial Narrow Bold | Arial Narrow | Bold | Arial Narrow Bold | Arial | Narrow Bold |
| Arial Narrow Bold Italic | Arial Narrow | Bold Italic | Arial Narrow Bold Italic | Arial | Narrow Bold Italic |
| Arial | Arial | Regular | Arial | Arial |  |
| Arial Italic | Arial | Italic | Arial Italic | Arial | Italic |
| Arial Bold | Arial | Bold | Arial Bold | Arial | Bold |
| Arial Bold Italic | Arial | Bold Italic | Arial Bold Italic | Arial | Bold Italic |
| Arial Black | Arial Black | Regular | Arial Black | Arial | Black |
| Arial Black Italic | Arial Black | Italic | Arial Black Italic | Arial | Black Italic |

In addition to name strings, OS/2.usWeightClass, OS/2.usWidthClass, OS/2.fsSelection style bits, and head.macStyle bits are shown. These settings allow the fonts to fit together into a single family of varying weight and compression/expansion.

| Font | OS/2 usWeightClass | OS/2 usWidthClass | OS/2 fsSelection Italic | OS/2 fsSelection Bold | OS/2 fsSelection Regular | 'head' macStyle Bold | 'head' macStyle Italic | 'head' macStyle Condensed | 'head' macStyle Extended |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Arial Narrow | 400 | 3 |  |  | x |  |  | x |  |
| Arial Narrow Italic | 400 | 3 | x |  |  |  | x | x |  |
| Arial Narrow Bold | 700 | 3 |  | x |  | x |  | x |  |
| Arial Narrow Bold Italic | 700 | 3 | x | x |  | x | x | x |  |
| Arial | 400 | 5 |  |  | x |  |  |  |  |
| Arial Italic | 400 | 5 | x |  |  |  | x |  |  |
| Arial Bold | 700 | 5 |  | x |  | x |  |  |  |
| Arial Bold Italic | 700 | 5 | x | x |  | x | x |  |  |
| Arial Black | 900 | 5 |  | x |  | x |  |  |  |
| Arial Black Italic | 900 | 5 | x | x |  | x | x |  |  |
