---
title: "The 'xref' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-xref-vmtx"></a>

# The `'xref'` table

<a id="anchor-xref-part-1"></a>

## Introduction

The `'xref'` (*cross-reference table*) table is used by Apple's font tools **ftxdumperfuser** and **ftxenhancer**. **ftxenhancer** lets font designers generate `'just'`, `'kern'`, and `'morx'` tables using symbolic names. These names are not used by the tables themselves, however, and so are lost when **ftxenhancer** is run. The `'xref'` table is used to store these symbolic names.

The table begins with a header which is structured as follows:

*The `'xref'` Table*

| Type | Name | Description |
| --- | --- | --- |
| uint32\_t | version | The version of the table format, currently 1 |
| uint32\_t | flags | Flags, currently unused and set to 0 |
| uint32\_t | numEntries | The number of entries in the table |
| uint32\_t | stringOffset | Offset from the beginning of the table to the string data |

The header is followed by a number of entries which map from data in the font table to strings:

*The `'xref'` Table Entry*

| Type | Name | Description |
| --- | --- | --- |
| FourCharCode | tableTag | The tag for the table that uses this entry (currently `'just'`, `'kerx'`, or `'morx'`) |
| int16\_t | chainIndex | The `'morx'` chain corresponding to this name |
| int16\_t | subtableIndex | The index of the subtable corresponding to this name |
| int16\_t | tableType | The type of object corresponding to this name. Values are 0 (class name), 1 (state name), 2 (entry/transition name), 3 (action name), 4 (column class name), and 5 (row class name). |
| int16\_t | tableIndex | The index of the object corresponding to this name |
| uint16\_t | stringOffset | The offset from the beginning of the string data to this name |
| uint16\_t | stringLength | The length of the string data for this name |

For the `chainIndex`, `subtableIndex`, `tableType`, and `tableIndex` fields can all use -1 as a wildcard, rarely though that may be appropriate.

String data is in UTF-8. Indices are zero-based.

For example, let us suppose that a font's `'morx'` table has one chain with four subtables. The fourth subtable is a contextual subtable with two classes defined in addition to the standard four, and the first of the two one is named "myClass." The entry `{ tableTag:'morx', chainIndex:0, subtableIndex:3, tableType:0, tableIndex:4 }`. The offset and length would indicate the bytes `6D 79 43 6C 61 73 73`. Note that the tableIndex field counts the four implicit classes, even though they have standard names. Similarly, data for state tables counts the two implicit states, "StartOfText" and "StartOfLine."

<a id="anchor-xref-part-2"></a>

## Warning

The `'xref'` table is generally useful for production purposes only and should be removed from shipping fonts accordingly.
