---
title: "The 'prep' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-prep-prep"></a>

# The `'prep'` table

The `'prep'` table stores the instructions that make up the control value program, a set of TrueType instructions that will be executed once when the font is first accessed and again whenever the font, point size or transformation matrix change. It consists of an ordered list of instructions opcodes. Each opcode is a byte. The tag `'prep'`, referring to the preProgram, is anachronistic but some people still call the control value program the preProgram.

More information on the control value program can be found in [Instructing Fonts](https://developer.apple.com/fonts/TrueType-Reference-Manual/RM03/Chap3.html).

**Table 75**: `'prep'` table

| Type | Name | Description |
| --- | --- | --- |
| uint8 | controlValueProgram\[length\] | Set of instructions executed whenever the point size or font transformation change |
