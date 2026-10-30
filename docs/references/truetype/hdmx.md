---
title: "The 'hdmx' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-hdmx-hdmx"></a>

# The `'hdmx'` table

The `'hdmx'` table is used only with fonts intended for use on the Macintosh platform. If this table is present in a font, the values in contains will be used where appropriate. If this table is missing, the values in the `'hmtx'` table will be scaled and rounded. Using this table will improve performance at the sizes for which it contains metric information because it allows the Macintosh Font Manager to build integer width tables without calling the scaler for each glyph.

The horizontal device metrics table stores integer advance widths scaled to particular pixel per em sizes. Typically, the `'hdmx'` table is used only for selected screen sizes.

Device records in this table are sorted by pixel per em size. The checksum for this table includes all device records. Note that each device record subtable is padded with zeros to make it long aligned.

**Table 20**: The `'hdmx'` table

| Type | Description |
| --- | --- |
| int16 | format version number |
| int16 | number of device records |
| int32 | size of a device record, long aligned |
| DeviceRecord | records\[number of device records\] |

Each device record for format 0 has the structure shown in Table 21.

**Table 21**: Device Record

| Type | Description |
| --- | --- |
| uint8 | pixel size for following widths |
| uint8 | maximum width |
| uint8 | widths\[number of glyphs\] |
