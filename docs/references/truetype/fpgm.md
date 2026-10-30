---
title: "The 'fpgm' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-fpgm-fpgm"></a>

# The `'fpgm'` table

The `'fpgm'` table is optional. It is needed by fonts that are instructed. Like the `'cvt '`, it is an ordered list which is stored as an array. Since it contains instructions, it contains 8 bit values. It consists of a list of instructions that are executed once when a font is first used. These instructions are known as the font program. The main use of this table is for the definition of functions that are used in many different glyph programs.

More information on the font program can be found in [A sample font program](https://developer.apple.com/fonts/TrueType-Reference-Manual/RM03/Chap3.html#font_program).

**Table 13** : The `'fpgm'` table

| Type | Name | Description |
| --- | --- | --- |
| uint8 | instructions\[\] | array of bytes |
