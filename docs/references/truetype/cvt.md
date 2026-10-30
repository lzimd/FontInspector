---
title: "The 'cvt ' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-cvt-cvt"></a>

# The `'cvt '` table

The `'cvt '` table is optional. It can be used by fonts that contain instructions. It contains an array of FWords that can be accessed by instructions. The `'cvt '` is used to tie together certain font features when their values are sufficiently close to the table value. The number of control value table entries can be calculated by dividing the length of the `'cvt '` table, as given in the table directory, by 4.

Use of the `'cvt '` table in instructing fonts is described in [A sample control value program](https://developer.apple.com/fonts/TrueType-Reference-Manual/RM03/Chap3.html#value_program).

**Table 12**: The `'cvt '` table

| Type | Name | Description |
| --- | --- | --- |
| FWord | controlValues\[\] | array of FWords accessible by instructions |
