---
title: "The 'cmap' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-cmap-cmap"></a>

# The `'cmap'` table

<a id="anchor-cmap-part-1"></a>

## General table information

The `'cmap'` table maps character codes to glyph indices. The choice of encoding for a particular font is dependent upon the conventions used by the intended platform. A font intended to run on multiple platforms with different encoding conventions will require multiple encoding tables. As a result, the `'cmap'` table may contain multiple subtables, one for each supported encoding scheme.

Character codes that do not correspond to any glyph in the font should be mapped to glyph index 0. At this location in the font there must be a special glyph representing a missing character, typically a box. No character code should be mapped to glyph index -1 (0xFFFF), which is a special value reserved in processing to indicate the position of a glyph deleted from the glyph stream.

The `'cmap'` table begins with a table version number followed by the number of encoding tables. The encoding subtables follow.

Note that only one of these encoding subtables is used at a time. If multiple encoding subtables are found, the `'cmap'` parsing software determines which one to use. The exception is a type 14 encoding subtable, which can only be used in conjunction with another subtable. If multiple type 14 encoding subtables are present, which one is used is undefined.

The original definition of the `'cmap'` table used either eight or sixteen bits for character codes. In support for versions of Unicode from 2.0 onwards, it is possible that fonts may require references to data that uses a mixture of sixteen and thirty-two bits per character, or simply thirty-two bits per character.

*The `'cmap'` index*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | version | Version number (Set to zero) |
| UInt16 | numberSubtables | Number of encoding subtables |

<a id="anchor-cmap-part-2"></a>

## The `'cmap'` encoding subtables

Each `'cmap'` subtable consists of three fields:

*The `'cmap'` subtable*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | platformID | Platform identifier |
| UInt16 | platformSpecificID | Platform-specific encoding identifier |
| UInt32 | offset | Offset of the mapping table |

The `'cmap'` subtables must be sorted first in ascending order by platform identifier and then by platform-specific identifier.

The `platformID` and `platformSpecificID` fields use the same values as are used by the equivalent fields in the [`'name'`](https://developer.apple.com/fonts/TrueType-Reference-Manual/Chap6name.html) table:

*`'cmap'` Platforms*

| Platform ID | Platform | Platform-specific ID |
| --- | --- | --- |
| 0 | Unicode | Indicates Unicode version. |
| 1 | Macintosh | Script Manager code. |
| 2 | (reserved; do not use) | <!-- colspan --> |
| 3 | Microsoft | Microsoft encoding. |

<a id="anchor-cmap-part-3"></a>

### Unicode encoding

When the `platformID` is 0 (Unicode), the `platformSpecificID` is interpreted as follows:

*Unicode Platform-specific Encoding Identifiers*

| Platform-specific ID code | Meaning |
| --- | --- |
| 0 | Version 1.0 semantics |
| 1 | Version 1.1 semantics |
| 2 | ISO 10646 1993 semantics (deprecated) |
| 3 | Unicode 2.0 or later semantics (BMP only) |
| 4 | Unicode 2.0 or later semantics (non-BMP characters allowed) |
| 5 | Unicode Variation Sequences |
| 6 | Last Resort |

`platformID` values other than 0, 1, or 3 are allowed but cmaps using them will be ignored.

The Unicode platform's platform-specific ID 6 was intended to mark a `'cmap'` subtable as one used by a last resort font. This is not required by any Apple platform.

<a id="anchor-cmap-part-4"></a>

### Macintosh encoding

When the `platformID` is 1 (Macintosh), the `platformSpecificID` is a QuickDraw script code. See [the `'name'` table documentation](name.md) for a list of these.

The use of the Macintosh `platformID` is currently discouraged. Subtables with a Macintosh `platformID` are only required for backwards compatibility with QuickDraw and will be synthesized from Unicode-based subtables if ever needed.

<a id="anchor-cmap-part-5"></a>

### Windows encoding

When the `platformID` is 3 (Windows), the `platformSpecificID` is a is interpreted as follows:

*Windows Platform-specific Encoding Identifiers*

| Platform-specific ID code | Meaning |
| --- | --- |
| 0 | Symbol |
| 1 | Unicode BMP-only (UCS-2) |
| 2 | Shift-JIS |
| 3 | PRC |
| 4 | BigFive |
| 5 | Johab |
| 10 | Unicode UCS-4 |

<a id="anchor-cmap-part-6"></a>

### Subtable requirements

There are three basic types of encoding subtables:

- Unicode subtables
- Unicode variation sequence subtables
- Non-Unicode subtables (everything else)

A Unicode subtable is one supporting the [Unicode text-encoding standard](https://www.unicode.org/). Such subtables have a Unicode `platformID` and a `platformSpecificID` other than 14, or a Microsoft `platformID` and a `platformSpecificID` of 1 or 10.

A Unicode variation sequence subtable is one with a Unicode `platformID` and a `platformSpecificID` of 14.

<a id="anchor-cmap-part-7"></a>

#### Unicode subtable requirements

Most fonts should have a Unicode encoding subtable. Fonts with a Windows/Symbol encoding subtable (3/0) should have no Unicode cmaps.

If a font has multiple Unicode encoding subtables, each character should be mapped to the same glyph by every Unicode subtable in which it appears.

<a id="anchor-cmap-part-8"></a>

#### Unicode variation sequence subtable requirements

Fonts should not have more than one Unicode variation sequence subtable. If a font does have multiple variation sequence subtables, only one will be used and the others ignored. Which one is used is not defined.

Fonts with a Unicode variation sequence subtable require a Unicode encoding subtable of format 4 or 12.

<a id="anchor-cmap-part-9"></a>

#### Non-Unicode subtable requirements

Fonts with a Windows/Symbol encoding subtable (3/0) should have no Unicode cmaps.

The use of subtables with a Macintosh `platformID` is discouraged.

<a id="anchor-cmap-part-10"></a>

### Subtable search order

Other than a Unicode variation sequence subtable, exactly one encoding subtable will be used to map characters to glyphs. The encoding subtables are searched for the one most appropriate for use, determined by their `platform`/`platformSpecificID` values. Apple does not guarantee that Unicode encoding subtables will be looked for in any particular order. However:

- Unicode encoding subtables are used in preference to non-Unicode encoding subtables.
- Unicode encoding subtables not restricted to the BMP are used in preference to subtables restricted to the BMP.
- Unicode variation sequence subtables are always processed if another Unicode cmap of type 4 or 12 is present.

For example, if a font has both a 0/4 (Unicode, UCS-4) cmap and a 0/3 (Unicode/BMP-only) cmap, the former will be used and the latter ignored. Nonetheless, they should have identical mappings for Unicode's BMP.

If a font has a 3/10 cmap (Windows, UCS-4), it should also have a 3/1 (Windows, BMP-only) cmap as well for backwards compatibility with Windows XP. There is no equivalent requirement for Apple platforms.

See the [OpenType specification](http://www.microsoft.com/typography/otspec/cmap.htm) for further requirements for the Windows platform.

Note that because a encoding subtable uses offsets to the actual data for any `platform`/`platformSpecificID`, it's possible for a type 0/4 and type 3/10 cmap to have the same actual data, not just identical data.

<a id="anchor-cmap-part-11"></a>

## The `'cmap'` table and language codes

Each `'cmap'` subtable has a two-byte language code associated with it. This language code is only used for subtables with a Macintosh `platformID`. For such subtables, it is interpreted as one more than a QuickDraw language code, or zero if the subtable is language independent. In all other subtables, it should be zero.

Note that the use of the Macintosh `platformID` is currently discouraged. Subtables with a Macintosh `platformID` are only required for backwards compatibility with QuickDraw and will be synthesized from Unicode-based subtables if ever needed.

<a id="anchor-cmap-part-12"></a>

## The `'cmap'` formats

Each `'cmap'` subtable is in one of nine currently available formats. These are format 0, format 2, format 4, format 6, format 8, format 10, format 12, format 13, and format 14 described in the next section.

The Macintosh standard character to glyph mapping is supported by format 0. Format 2 supports a mixed 8/16 bit mapping useful for Japanese, Chinese and Korean. Format 4 is used for 16 bit mappings. Format 6 is used for dense 16 bit mappings.

Formats 8, 10, and 12, 13, and 14 are used for mixed 16/32-bit and pure 32-bit mappings. This supports text encoded with surrogates in Unicode 2.0 and later.

Many of the cmap formats are either obsolete or were designed to meet anticipated needs which never materialized. Modern font generation tools might not need to be able to write general-purpose cmaps in formats other than 4 and 12. Formats 13 and 14 are both for specialized uses. Format 13 is structurally the same as format 12 (but with a different interpretation of the data), so support for it (if needed) is relatively easy to provide. Support for format 14 encoding subtables is required for use with Unicode variation selectors.

All cmap formats are supported by Apple platforms except 0, 8, and 10. See [the OpenType specification](https://docs.microsoft.com/en-us/typography/opentype/spec/cmap) for information on encoding subtable format support on other platforms.

<a id="anchor-cmap-part-13"></a>

### `'cmap'` format 0

Format 0 is suitable for fonts whose character codes and glyph indices are restricted to single bytes. This was a very common situation when TrueType was introduced but is rarely encountered now.

*`'cmap'` format 0*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | format | Set to 0 |
| UInt16 | length | Length in bytes of the subtable (set to 262 for format 0) |
| UInt16 | language | Language code (see above) |
| UInt8 | glyphIndexArray\[256\] | An array that maps character codes to glyph index values |

<a id="anchor-cmap-part-14"></a>

### `'cmap'` format 2

The format 2 mapping subtable type is used for fonts containing Japanese, Chinese, or Korean characters. The code standards used in this table are supported on Macintosh systems in Asia. These fonts contain a mixed 8/16-bit encoding, in which certain byte values are set aside to signal the first byte of a 2-byte character. These special values are also legal as the second byte of a 2-byte character.

The following table shows the format of a format 2 encoding subtable. The `subHeaderKeys` array maps each possible high byte into a particular member of the suborders array. This allows the determination of whether or not a second byte is used. In either case, the path leads into the `glyphIndexArray` from which the mapped glyph index is obtained. The sequence of operations is as follows:

Consider a high byte, `i`, designating an integer between 0 and 255. The value `subHeaderKeys[i]`, divided by 8, is the index `k` into the `subHeaders` array. The value `k` equals 0 is special. It means that `i` is a one-byte code and no second byte will be referenced. If `k` is positive, then `i` is the high-byte of a two-byte code and its second byte, `j`, will be consumed.

*`'cmap'` format 2*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | format | Set to 2 |
| UInt16 | length | Total table length in bytes |
| UInt16 | language | Language code (see above) |
| UInt16 | subHeaderKeys\[256\] | Array that maps high bytes to subHeaders: value is index \* 8 |
| UInt16 \* 4 | subHeaders\[variable\] | Variable length array of subHeader structures |
| UInt16 | glyphIndexArray\[variable\] | Variable length array containing subarrays |

The subHeader data type is a 4-word structure defined by the C-language structure shown below:

```
typedef struct {
	UInt16	firstCode;
	UInt16	entryCount;
	int16	idDelta;
	UInt16	idRangeOffset;
} subheader;
```

If `k` is positive, then the four values belonging to `subheaders[k]` are used as follows with `firstCode` and `entryCount` defining the allowable range for the second byte `j`:

`firstCode <= j < (firstCode + entryCount)`

If `j` is outside this range, index 0 (the missing character glyph) is returned. Otherwise, `idRangeOffset` is used to identify the associated range within the `glyphIndexArray`. The `glyphIndexArray` immediately follows the `subHeaders` array and may be loosely viewed as an extension to it. The value of the `idRangeOffset` is the number of bytes past the actual location of the `idRangeOffset` word where the `glyphIndexArray` element corresponding to `firstCode` appears. If `p` is zero, it is returned directly. If `p` is nonzero, `p = p + idDelta` is returned. The sum is reduced modulo 65536, if necessary.

For the one-byte case with `k` = 0, the structure `subHeaders[0]` will show `firstCode` = 0, `entryCount` = 256, and `idDelta` = 0. The `idRangeOffset` will point, as previously discussed, to the beginning of the `glyphIndexArray`. Indexing `i` words into this array gives the returned value `p = glyphIndexArray[i]`.

The format 2 cmap is targeted at mixed 8/16-bit encodings such as Big Five and Shift-JIS. Such encodings are still widely used, and Apple platforms will correctly support them even if a format 2 cmap is not present.

<a id="anchor-cmap-part-15"></a>

### `'cmap'` format 4

Format 4 is a two-byte encoding format. It should be used when the character codes for a font fall into several contiguous ranges, possibly with holes in some or all of the ranges. That is, some of the codes in a range may not be associated with glyphs in the font. Two-byte fonts that are densely mapped should use Format 6.

The table begins with the format number, the length and language. The format-dependent data follows. It is divided into three parts:

- A four-word header giving parameters needed for an optimized search of the segment list
- Four parallel arrays describing the segments (one segment for each contiguous range of codes)
- A variable-length array of glyph IDs

*`'cmap'` format 4*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | format | Format number is set to 4 |
| UInt16 | length | Length of subtable in bytes |
| UInt16 | language | Language code (see above) |
| UInt16 | segCountX2 | 2 \* segCount |
| UInt16 | searchRange | 2 \* (2\*\*FLOOR(log₂(segCount))) |
| UInt16 | entrySelector | log₂(searchRange/2) |
| UInt16 | rangeShift | (2 \* segCount) - searchRange |
| UInt16 | endCode\[segCount\] | Ending character code for each segment, last = 0xFFFF. |
| UInt16 | reservedPad | This value should be zero |
| UInt16 | startCode\[segCount\] | Starting character code for each segment |
| UInt16 | idDelta\[segCount\] | Delta for all character codes in segment |
| UInt16 | idRangeOffset\[segCount\] | Offset in bytes to glyph indexArray, or 0 |
| UInt16 | glyphIndexArray\[variable\] | Glyph index array |

The number of segments is specified by the variable `segCount`. This variable is not explicitly used in the Format 4 table, however it is the number from which all of the table parameters are derived. The `segCount` is the number of contiguous code ranges in the font. The `searchRange` value is twice the largest power of 2 that is less than or equal to `segCount`.

The `searchRange`, `entrySelector`, and `rangeShift` fields are not used on Apple platforms but should be set correctly for compatibility with other platforms.

Example Format 4 subtable values are shown in this table:

|  |  |  |
| --- | --- | --- |
| segCount | 39 | Not calculated; determined from the organization of the glyph indices |
| searchRange | 64 | (2 \* (largest power of 2 \<= 39)) = 2 \* 32 |
| entrySelector | 5 | (log₂(the largest power of 2 \< segCount)) |
| rangeShift | 14 | (2 \* segCount) - searchRange = (2 \* 39) - 64 |

Each segment is described by a `startCode`, an `endCode`, an `idDelta` and an `idRangeOffset`. These are used for mapping the character codes in the segment. The segments are sorted in order of increasing endCode values.

To use these arrays, it is necessary to search for the first `endCode` that is greater than or equal to the character code to be mapped. If the corresponding `startCode` is less than or equal to the character code, then use the corresponding `idDelta` and `idRangeOffset` to map the character code to the glyph index. Otherwise, the missing character glyph is returned. To ensure that the search will terminate, the final `endCode` value must be `0xFFFF`. This segment need not contain any valid mappings. It can simply map the single character code `0xFFFF` to the missing character glyph, glyph 0.

If the `idRangeOffset` value for the segment is not 0, the mapping of the character codes relies on the `glyphIndexArray`. The character code offset from `startCode` is added to the `idRangeOffset` value. This sum is used as an offset from the current location within `idRangeOffset` itself to index out the correct `glyphIdArray` value. This indexing method works because `glyphIdArray` immediately follows `idRangeOffset` in the font file. The address of the glyph index is given by the following equation:

`glyphIndexAddress = idRangeOffset[i] + 2 * (c - startCode[i]) + (Ptr) &idRangeOffset[i]`

Multiplication by 2 in this equation is required to convert the value into bytes.

Alternatively, one may use an expression such as:

`glyphIndex = *( &idRangeOffset[i] + idRangeOffset[i] / 2 + (c - startCode[i]) )`

This form depends on `idRangeOffset` being an array of `UInt16'`s.

Once the glyph indexing operation is complete, the glyph ID at the indicated address is checked. If it's not 0 (that is, if it's not the missing glyph), the value is added to `idDelta[i]` to get the actual glyph ID to use.

If the `idRangeOffset` is 0, the `idDelta` value is added directly to the character code to get the corresponding glyph index:

`glyphIndex = idDelta[i] + c`

**NOTE**: All `idDelta[i]` arithmetic is modulo 65536.

The following table gives an example of the parameters required to map characters 10-20, 30-90, and 100-153 to a contiguous range of glyph indices. The parameter `segCount` = 4 for this example. This table gives the mapping variant parameter values for a Format 4 subtable example. The example data demonstrates how the character-to glyph index mapping values are calculated. Assumptions for this table are that `segCountX2` is 8, `searchRange` is 8, `entrySelector` is 2, `rangeShift` is 0.

| Name | Segment 1 Chars 10-20 | Segment 2 Chars 30-90 | Segment 3 Chars 100-153 | Segment 4 Missing Glyph |
| --- | --- | --- | --- | --- |
| endCode | 20 | 90 | 153 | 0xFFFF |
| startCode | 10 | 30 | 100 | 0xFFFF |
| idDelta | -9 | -18 | -27 | 1 |
| idRangeOffset | 0 | 0 | 0 | 0 |

This table performs the following mappings:

```
		10 is mapped to 10-9 or 1
		20 is mapped to 20-9 or 11
		30 is mapped to 30-18 or 12
		90 is mapped to 90-18 or 72
```

and so on.

Type 4 cmaps are required for backwards compatibility in Windows and are generally useful for BMP-only Unicode fonts. The redundancies in the header are for historical purposes—by pre-calculating these values, the performance of the lookup algorithm was substantially improved on older, slower processors.

<a id="anchor-cmap-part-16"></a>

### `'cmap'` format 6

Format 6 is used to map 16-bit, 2-byte, characters to glyph indexes. It is sometimes called the trimmed table mapping. It should be used when character codes for a font fall into a single contiguous range. This results in what is termed a *dense mapping*. Two-byte fonts that are not densely mapped (due to their multiple contiguous ranges) should use Format 4. Character-to-glyph index mapping subtable Format 6 is shown in the following table:

*`'cmap'` format 6*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | format | Format number is set to 6 |
| UInt16 | length | Length in bytes |
| UInt16 | language | Language code (see above) |
| UInt16 | firstCode | First character code of subrange |
| UInt16 | entryCount | Number of character codes in subrange |
| UInt16 | glyphIndexArray\[entryCount\] | Array of glyph index values for character codes in the range |

The `firstCode` and `entryCount` values in the subtable specify the useful subrange within the range of possible character codes. The range begins with `firstCode` and has a length equal to `entryCount`. Codes outside of this subrange are assumed to be missing and are mapped to the glyph with index 0. For a code within the subrange, its offset from the `firstCode` in the subrange is used as an index into the `glyphIndexArray`. That array provides the glyph index associated with that character code.

Type 6 cmaps are primarily useful for BMP-only Unicode fonts.

<a id="anchor-cmap-part-17"></a>

### `'cmap'` format 8–Mixed 16-bit and 32-bit coverage

Format 8 is a bit like format 2, in that it provides for mixed-length character codes. If a font contains Unicode surrogates, it's likely that it will also include other, regular 16-bit Unicodes as well. This requires a format to map a mixture of 16-bit and 32-bit character codes, just as format 2 allows a mixture of 8-bit and 16-bit codes. A simplifying assumption is made: namely, that there are no 32-bit character codes which share the same first 16 bits as any 16-bit character code. This means that the determination as to whether a particular 16-bit value is a standalone character code or the start of a 32-bit character code can be made by looking at the 16-bit value directly, with no further information required.

Here's the format 8 subtable format:

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | format | Subtable format; set to 8 |
| UInt16 | reserved | Set to 0 |
| UInt32 | length | Byte length of this subtable (including the header) |
| UInt32 | language | Language code (see above) |
| UInt8 | is32\[65536\] | Tightly packed array of bits (8K bytes total) indicating whether the particular 16-bit (index) value is the start of a 32-bit character code |
| UInt32 | nGroups | Number of groupings which follow |

Here follow the individual groups. Each group has the following format:

| Type | Name | Description |
| --- | --- | --- |
| UInt32 | startCharCode | First character code in this group; note that if this group is for one or more 16-bit character codes (which is determined from the is32 array), this 32-bit value will have the high 16-bits set to zero |
| UInt32 | endCharCode | Last character code in this group; same condition as listed above for the startCharCode |
| UInt32 | startGlyphCode | Glyph index corresponding to the starting character code |

A few notes here. The `endCharCode` is used, rather than a count, because comparisons for group matching are usually done on an existing character code, and having the `endCharCode` be there explicitly saves the necessity of an addition per group.

The presence of the packed array of bits indicating whether a particular 16-bit value is the start of a 32-bit character code is useful even when the font contains no glyphs for a particular 16-bit start value. This is because the system software often needs to know how many bytes ahead the next character begins, even if the current character maps to the missing glyph. By including this information explicitly in this table, no "secret" knowledge needs to be encoded into the OS.

Thus, although cmap format 8 is theoretically well-suited for Unicode text encoded using surrogates, it also has the flexibility to be used with other character set encodings.

To determine if a particular word (`cp`) is the first half of thirty-two bit code points, one can use an expression such as `( is32[ cp / 8 ] & ( 1 << ( cp % 8 ) ) )`. If this is non-zero, then the word is the first half of a thirty-two bit code point.

0 is *not* a special value for the high word of a 32-bit code point. A font may *not* have both a glyph for the code point `0x0000` and glyphs for code points with a high word of `0x0000`.

Type 8 cmaps have not seen any particular use since the format was introduced. Rendering engines generally do not deal with Unicode surrogates directly—the character codes are usually converted to UTF-32 before conversion to glyphs—and no other character encoding uses mixed 16/32-bit characters. The use of this format is discouraged.

<a id="anchor-cmap-part-18"></a>

### `'cmap'` format 10–Trimmed array

Format 10 is a bit like format 6, in that it defines a trimmed array for a tight range of 32-bit character codes:

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | format | Subtable format; set to 10 |
| UInt16 | reserved | Set to 10 |
| UInt32 | length | Byte length of this subtable (including the header) |
| UInt32 | language | Language code (see above) |
| UInt32 | startCharCode | First character code covered |
| UInt32 | numChars | Number of character codes covered |
| UInt16 | glyphs\[\] | Array of glyph indices for the character codes covered |

The format 10 cmap has seen little use since its introduction. It not supported on Windows and is the best choice only for fonts whose character repertoire is almost entirely in a contiguous block outside of Unicode's BMP. Such fonts are rare.

<a id="anchor-cmap-part-19"></a>

### `'cmap'` format 12–Segmented coverage

Format 12 is a bit like format 4, in that it defines segments for sparse representation in 4-byte character space. Here's the subtable format:

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | format | Subtable format; set to 12 |
| UInt16 | reserved | Set to 0. |
| UInt32 | length | Byte length of this subtable (including the header) |
| UInt32 | language | Language code (see above) |
| UInt32 | nGroups | Number of groupings which follow |

Here follow the individual groups, each of which has the following format:

| Type | Name | Description |
| --- | --- | --- |
| UInt32 | startCharCode | First character code in this group |
| UInt32 | endCharCode | Last character code in this group |
| UInt32 | startGlyphCode | Glyph index corresponding to the starting character code; subsequent charcters are mapped to sequential glyphs |

Again, the `endCharCode` is used, rather than a count, because comparisons for group matching are usually done on an existing character code, and having the `endCharCode` be there explicitly saves the necessity of an addition per group.

Format 12 is required for Unicode fonts covering characters above U+FFFF on Windows. It is the most useful of the cmap formats with 32-bit support.

<a id="anchor-cmap-part-20"></a>

### `'cmap'` format 13–Many-to-one mappings

Format 13 is a modified version of the type 12 `'cmap'` subtable, used internally by Apple for its last resort font and by Unicode's last resort font. It would, in general, not be appropriate for any font other than a last resort font.

Structurally, formats 13 and 12 are identicial. The only difference lies in the intepretation of the glyph code in each range. In a format 13 `'cmap'` subtable, all the glyphs in the range are mapped to the same glyph code, whereas in a type 12 `'cmap'` subtable they are mapped to sequential glyph codes, starting with the given one.

To illustrate, suppose we have the following group in both a format 12 `'cmap'` table and a format 13 `'cmap'` subtable:

| Type | Name | Value | Description |
| --- | --- | --- | --- |
| UInt32 | startCharCode | 0x4E00 | First character code in this group |
| UInt32 | endCharCode | 0x9FCB | Last character code in this group |
| UInt32 | glyphCode | 47 | Glyph index for this group |

In a type 12 `'cmap'` subtable, U+4E95 would be mapped to glyph (0x4E95 - 0x4E00) + 47 = 196. In a format 13 `'cmap'` subtable, it would be mapped to glyph 47.

Type 13 cmaps are only useful for fonts which use the same glyph for all the characters in a Unicode block—that is, only a Last Resort-like font will ever be likely to need one.

<a id="anchor-cmap-part-21"></a>

### Format 14: Unicode Variation Sequences

Subtable format 14 specifies the Unicode Variation Sequences (UVSes) supported by the font. A Variation Sequence, according to the Unicode Standard, comprises a base character followed by a variation selector; e.g. \<U+82A6, U+E0101\>.

The subtable partitions the UVSes supported by the font into two categories: “default” and “non-default” UVSes. Given a UVS, if the glyph obtained by looking up the base character of that sequence in the Unicode encoding subtable (i.e. the UCS-4 or the BMP encoding subtable) is the glyph to use for that sequence, then the sequence is a “default” UVS; otherwise it is a “non-default” UVS, and the glyph to use for that sequence is specified in the format 14 subtable itself.

The example below shows how a font vendor can use format 14 for a JIS-2004–aware font.

(Note the presence of 24-bit integers in the structures used. The type 14 `'cmap'` subtable does not keep data aligned to four-byte boundaries. This is also the only `'cmap'` subtable which does not stand by itself and is not completely independent of all others; a `'cmap'` may not consist of a type 14 subtable alone.)

*Format 14 header*

| Type | Name | Description |
| --- | --- | --- |
| uint16 | format | Subtable format. Set to 14. |
| uint32 | length | Byte length of this subtable (including this header) |
| uint32 | numVarSelectorRecords | Number of variation Selector Records |

This is immediately followed by ‘numVarSelectorRecords’ Variation Selector Records.

*Variation Selector Record*

| Type | Name | Description |
| --- | --- | --- |
| uint24 | varSelector | Variation selector |
| uint32 | defaultUVSOffset | Offset to Default UVS Table. May be 0. |
| uint32 | nonDefaultUVSOffset | Offset to Non-Default UVS Table. May be 0. |

The Variation Selector Records are sorted in increasing order of ‘varSelector’. No two records may have the same ‘varSelector’. All offsets in a record are relative to the beginning of the format 14 encoding subtable.

A Variation Selector Record and the data its offsets point to specify those UVSes supported by the font for which the variation selector is the ‘varSelector’ value of the record. The base characters of the UVSes are stored in the tables pointed to by the offsets. The UVSes are partitioned by whether they are default or non-default UVSes.

Glyph IDs to be used for non-default UVSes are specified in the Non-Default UVS table.

<a id="anchor-cmap-part-22"></a>

#### Default UVS Table

A Default UVS Table is simply a range-compressed list of Unicode scalar values, representing the base characters of the default UVSes which use the `varSelector` of the associated Variation Selector Record.

*Default UVS Table header*

| Type | Name | Description |
| --- | --- | --- |
| uint32 | numUnicodeValueRanges | Number of ranges that follow |

This is immediately followed by `numUnicodeValueRanges` Unicode Value Ranges, each of which represents a contiguous range of Unicode values.

*Unicode Value Range*

| Type | Name | Description |
| --- | --- | --- |
| uint24 | startUnicodeValue | First value in this range |
| BYTE | additionalCount | Number of additional values in this range |

For example, the range U+4E4D–U+4E4F (3 values) will set `startUnicodeValue` to 0x004E4D and `additionalCount` to 2. A singleton range will set `additionalCount` to 0.

`(startUnicodeValue + additionalCount)` must not exceed 0xFFFFFF.

The Unicode Value Ranges are sorted in increasing order of `startUnicodeValue`. The ranges must not overlap; i.e., `(startUnicodeValue + additionalCount)` must be less than the `startUnicodeValue` of the following range (if any).

<a id="anchor-cmap-part-23"></a>

## Non-Default UVS Table

A Non-Default UVS Table is a list of pairs of Unicode scalar values and glyph IDs. The Unicode values represent the base characters of all non-default UVSes which use the ‘varSelector’ of the associated Variation Selector Record, and the glyph IDs specify the glyph IDs to use for the UVSes.

*Non-Default UVS Table header*

| Type | Name | Description |
| --- | --- | --- |
| uint32 | numUVSMappings | Number of UVS Mappings that follow |

This is immediately followed by ‘numUVSMappings’ UVS Mappings.

*UVS Mapping*

| Type | Name | Description |
| --- | --- | --- |
| uint24 | unicodeValue | Base Unicode value of the UVS |
| uint16 | glyphID | Glyph ID of the UVS |

The UVS Mappings are sorted in increasing order of `unicodeValue`. No two mappings in this table may have the same `unicodeValue` values.

<a id="anchor-cmap-part-24"></a>

## Example

Here is an example of how a format 14 encoding subtable may be used in a font that is aware of JIS-2004 variant glyphs. The CIDs (character IDs) in this example refer to those in the Adobe Character Collection “Adobe-Japan1”, and may be assumed to be identical to the glyph IDs in the font in our example.

JIS-2004 changed the default glyph variants for some of its code points. For example:

JIS-90: U+82A6 ⇒ CID 1142<br> JIS-2004: U+82A6 ⇒ CID 7961

Both of these glyph variants are supported through the use of UVSes, as the following examples from Unicode’s UVS registry show:

U+82A6 U+E0100 ⇒ CID 1142<br> U+82A6 U+E0101 ⇒ CID 7961

If the font wants to support the JIS-2004 variants by default, it will:

- encode glyph ID 7961 at U+82A6 in the Unicode encoding subtable,
- specify \<U+82A6, U+E0101\> in the UVS encoding subtable’s Default UVS Table (‘varSelector’ will be 0x0E0101 and ‘defaultUVSOffset’ will point to data containing a 0x0082A6 Unicode value)
- specify \<U+82A6, U+E0100\> ⇒ glyph ID 1142 in the UVS encoding subtable’s Non-Default UVS Table (‘varSelector’ will be 0x0E0100 and ‘nonDefaultBaseUVOffset’ will point to data containing a ‘unicodeValue’ 0x0082A6 and ‘glyphID’ 1142).

If, however, the font wants to support the JIS-90 variants by default, it will:

- encode glyph ID 1142 at U+82A6 in the Unicode encoding subtable,
- specify \<U+82A6, U+E0100\> in the UVS encoding subtable’s Default UVS Table
- specify \<U+82A6, U+E0101\> ⇒ glyph ID 7961 in the UVS encoding subtable’s Non-Default UVS Table

<a id="anchor-cmap-part-25"></a>

## Platform-specific Information

Apple platforms do not support format 0, 8, or 10 encoding subtables.
