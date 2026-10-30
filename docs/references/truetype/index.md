---
title: "Font Tables"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-index-chapterContent"></a>

# Font Tables

<a id="anchor-index-Intro"></a>

## Introduction

This chapter documents the tables that make up a TrueType font file, including AAT extensions to the core TrueType specification. Documentation is not included for OpenType-specific tables, even those supported on OS X and iOS. For further information on those tables, see the [OpenType specification](http://www.microsoft.com/typography/otspec/).

Table 1 describes the data types used in TrueType font files on all platforms.

With the exception of the font directory which must appear first in the font file, the tables that make up a font can appear in any order. For convenience in accessing the information presented in this chapter, tables are described in alphabetical order.

<a id="anchor-index-Types"></a>

## Data Types

In addition to standard integer data types, the TrueType font format uses the following:

**Table 1** : The `'sfnt'` data types

| Data type | Description |
| --- | --- |
| shortFrac | 16-bit signed fraction |
| Fixed | 16.16-bit signed fixed-point number |
| FWord | 16-bit signed integer that describes a quantity in FUnits, the smallest measurable distance in em space. |
| uFWord | 16-bit unsigned integer that describes a quantity in FUnits, the smallest measurable distance in em space. |
| F2Dot14 | 16-bit signed fixed number with the low 14 bits representing fraction. |
| longDateTime | The long internal format of a date in seconds since 12:00 midnight, January 1, 1904. It is represented as a signed 64-bit integer. |

**NOTE**: A `shortFrac` is an `int16_t` with a bias of 14. This means it can represent numbers between 1.999 `(0x7fff)` and -2.0 `(0x8000)`. 1.0 is stored as 16384 `(0x4000)` and -1.0 is stored as -16384 `(0xc000)`.

<a id="anchor-index-Overview"></a>

## TrueType Font files: an overview

A TrueType font file consists of a sequence of concatenated tables. A table is a sequence of words. Each table must be long aligned and padded with zeroes if necessary.

The first of the tables is the font directory, a special table that facilitates access to the other tables in the font. The directory is followed by a sequence of tables containing the font data. These tables can appear in any order. Certain tables are required for all fonts. Others are optional depending upon the functionality expected of a particular font.

The tables have names known as tags. Tags have the type uint32. Currently defined tag names consist of four characters. Tag names with less than four characters have trailing spaces. When tag names are shown in text they are enclosed in straight quotes.

Tables that are required must appear in any valid TrueType font file. The required tables and their tag names are shown in Table 2.

**Table 2**: The required tables

| Tag | Table |
| --- | --- |
| `'cmap'` | character to glyph mapping |
| `'glyf'` | glyph data |
| `'head'` | font header |
| `'hhea'` | horizontal header |
| `'hmtx'` | horizontal metrics |
| `'loca'` | index to location |
| `'maxp'` | maximum profile |
| `'name'` | naming |
| `'post'` | PostScript |

<a id="anchor-index-part-1"></a>

### Warning!

Apple makes a distinction between a "TrueType font" (which refers to a particular font outline definition technology) and an "sfnt-housed font," which refers to any font which uses the same packaging format as a TrueType font: that is, it uses the same directory structure and the same table format and meaning for any tables present.

This is an important distinction, because Apple supports other varieties of sfnt-housed font on OS X and iOS, most notably bitmap-only fonts and OpenType fonts. Informally, people often refer to any sfnt-housed font as a "TrueType font," but this is strictly speaking inaccurate.

The "required" tables listed in Table 2 are *only required for TrueType fonts*. Other varieites of sfnt-housed font may not have them. For example, bitmap-only sfnt-housed fonts do not have an `'hmtx'`, `'hhea'` or `'head'` table. CoreText, Apple's rendering system for Unicode-encoded text, does require that any sfnt-housed font have a `'cmap'` and `'name'` table.

*For font vendors*: If you are unsure whether a particular table should be included for your non-TrueType sfnt-housed font, it is generally safe to include it, or you may contact Apple for advice.

*For font users*: Never assume that any particular table is present in a font on OS X. Fonts may be non-TrueType sfnt-housed fonts and lack some of TrueType's required tables. Moreover, fonts may be ill-formed and yet installed. Provide graceful error handling if a font you are using lacks a table you require.

Optional tables may be needed depending upon the functionality expected of a given font file'. The optional tables and their tag names are listed in Table 3. The `'hdmx'` table is used on Macintosh platforms only. The `'OS/2'` table is required for fonts that are to be used on that platform but appears in the optional table because it is not required for all TrueType font files.

Apple Advanced Typography (AAT) Tables are used with the Line Layout capability of Apple's CoreText.

Additional tables may be defined to support other platforms, such as OpenType, or to provide for future expansion. Tags for these tables must be registered. Contact Apple Developer Technical Support for information regarding the registration process. Tag names consisting of all lower case letters are reserved for Apple's use.

**Table 3**: The optional tables

| Tag | Table |
| --- | --- |
| `'cvt '` | control value |
| `'fpgm'` | font program |
| `'hdmx'` | horizontal device metrics |
| `'kern'` | kerning |
| `'OS/2'` | OS/2 |
| `'prep'` | control value program |

<a id="anchor-index-Directory"></a>

## The Font Directory

The font directory, the first of the tables, is a guide to the contents of the font file. It provides the information required to access the data in the other tables. The directory consists of two parts: the offset subtable and the table directory. The offset subtable records the number of tables in the font and provides offset information enabling quick access to the directory tables. The table directory consists of a sequence of entries, one for each table in the font.

<a id="anchor-index-part-2"></a>

### The offset subtable

The offset subtable, documented in Table 4, begins with the scaler type of the font. The number of tagged tables in the `'sfnt'` follows. The table directory itself and any subtables are not included in this count. The entries for searchRange, entrySelector and rangeShift are used to facilitate quick binary searches of the table directory that follows. Unless a font has a large number of tables, a sequential search will be fast enough.

If a faster search is necessary, a binary search is most easily done on a number of entries that is a power of two. This makes it possible to cut the number of items to search in half by shifting. The remaining offset subtable entries should be set as follows:

- searchRange is the largest power of two less than or equal to the number of items in the table, i.e. the largest number of items that can be easily searched.

- rangeShift is the number of items minus searchRange; i.e. the number of items that will not get looked at if you only look at searchRange items.

  Before the search loop starts, compare the target item to the item with number rangeShift. If the target item is less than rangeShift, search from the beginning of the table. If it is greater, search starting at the item with number rangeShift.

- entrySelector is log₂(searchRange). It tells how many iterations of the search loop are needed. (i.e. how many times to cut the range in half)

Note that the searchRange, the entrySelector and the rangeShift are all multiplied by 16 which represents the size of a directory entry.

**Table 4** : The offset subtable

| Type | Name | Description |
| --- | --- | --- |
| uint32 | scaler type | A tag to indicate the OFA scaler to be used to rasterize this font; see the [note on the scaler type](#anchor-index-ScalerTypeNote) below for more information. |
| uint16 | numTables | number of tables |
| uint16 | searchRange | (maximum power of 2 \<= numTables)\*16 |
| uint16 | entrySelector | log₂(maximum power of 2 \<= numTables) |
| uint16 | rangeShift | numTables\*16-searchRange |

<a id="anchor-index-ScalerTypeNote"></a>

#### The scaler type

The scaler type is used by OS X and iOS to determine which scaler to use for this font, that is, to determine how to extract glyph data from the font. Different font scalers wrap different font formats within the basic structure of a TrueType font; the scaler type in the offset subtable of the font's directory is used to indicate which scaler should be used with a particular font. (Non-TrueType fonts housed within the same structure as a TrueType font are referred to as "sfnt-housed fonts.")

The values `'true'` (0x74727565) and 0x00010000 are recognized by OS X and iOS as referring to TrueType fonts. The value `'typ1'` (0x74797031) is recognized as referring to the old style of PostScript font housed in a sfnt wrapper. The value `'OTTO'` (0x4F54544F) indicates an OpenType font with PostScript outlines (that is, a `'CFF '` table instead of a `'glyf'` table). Other values are not currently supported.

Fonts with TrueType outlines produced for OS X or iOS only are encouraged to use `'true'` (0x74727565) for the scaler type value. Fonts for Windows or Adobe products *must* use 0x00010000.

<a id="anchor-index-part-3"></a>

### The table directory

The table directory follows the offset subtable. Entries in the table directory must be sorted in ascending order by tag. Each table in the font file must have its own table directory entry. Table 5 documents the structure of the table directory.

**Table 5**: The table directory

| Type | Name | Description |
| --- | --- | --- |
| uint32 | tag | 4-byte identifier |
| uint32 | checkSum | checksum for this table |
| uint32 | offset | offset from beginning of sfnt |
| uint32 | length | length of this table in byte (actual length not padded length) |

The table directory includes checkSum, a number which can be used to verify the identity of and the integrity of the data in its associated tagged table. Table checksums are the unsigned sum of the longs in a table. The following C function can be used to determine the checksum of a given table:

```
uint32 CalcTableChecksum(uint32 *table, uint32 numberOfBytesInTable)
	{
	uint32 sum = 0;
	uint32 nLongs = (numberOfBytesInTable + 3) / 4;
	while (nLongs-- > 0)
		sum += *table++;
	return sum;
	}
```

To calculate the checkSum for the `'head'` table which itself includes the checkSumAdjustment entry for the entire font, do the following:

- Set the checkSumAdjustment to 0.
- Calculate the checksum for all the tables including the `'head'` table and enter that value into the table directory.
- Calculate the checksum for the entire font.
- Subtract that value from the hex value B1B0AFBA.
- Store the result in checkSumAdjustment.

The checkSum for the `'head'` table which includes the checkSumAdjustment entry for the entire font is now incorrect. That is not a problem. Do not change it. An application attempting to verify that the `'head'` table has not changed should calculate the checkSum for that table by not including the checkSumAdjustment value, and compare the result with the entry in the table directory.

The table directory also includes the offset of the associated tagged table from the beginning of the font file and the length of that table.
