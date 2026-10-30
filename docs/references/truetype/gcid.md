---
title: "The 'gcid' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-gcid-chapterContent"></a>

# The `'gcid'` table

<a id="anchor-gcid-part-1"></a>

## General table information

This table provides data to map characters in the font to CIDs. It is structured as follows:

**gcid Table**

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | version | Version number (set to 0) |
| UInt16 | format | Data format (set to 0) |
| UInt32 | size | Size of the table, including header |
| UInt16 | registry | The registry ID |
| char\[64\] | registryName | The registry name in ASCII; unused bytes should be set to 0 |
| UInt16 | order | The order ID |
| char\[64\] | orderName | The order name in ASCII; unused bytes should be set to 0 |
| UInt16 | supplementVersion | The supplement version |
| UInt16 | count | The number of CIDs that follow; this should not exceed the number of glyphs in the font |
| UInt16\[\] | CIDs | The CIDs for the glyphs in the font, starting with glyph 0. If a glyph does not correspond to a CID in the identified collection, 0xFFFF is used. |

For example, one would specify that the CIDs are for Adobe-CNS1-4 by setting the registry to 0, the registry name to "Adobe", the order to 2, the order name to "CNS1", and the supplementVersion to 4.
