---
title: "The 'post' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-post-post"></a>

# The `'post'` table

<a id="anchor-post-part-1"></a>

## General table information

The `'post'` table contains information needed to use a TrueType font on a PostScript printer. It contains the data needed for the FontInfo dictionary entry as well as the PostScript names for all of the glyphs in the font. It also contains memory usage information needed by the PostScript driver for memory management.

The `'post'` table is documented in Table 72 below. The first item specifies the table format. There are five possibilities: format 1, format 2, format 2.5, format 3 and format 4. Each version is documented below. Only formats 2, 2.5 and 4 require subtables.

**Table 72**: `'post'` table

| Type | Name | Description |
| --- | --- | --- |
| Fixed | format | Format of this table |
| Fixed | italicAngle | Italic angle in degrees |
| FWord | underlinePosition | Underline position |
| FWord | underlineThickness | Underline thickness |
| uint32 | isFixedPitch | Font is monospaced; set to 1 if the font is monospaced and 0 otherwise (N.B., to maintain compatibility with older versions of the TrueType spec, accept any non-zero value as meaning that the font is monospaced) |
| uint32 | minMemType42 | Minimum memory usage when a TrueType font is downloaded as a Type 42 font |
| uint32 | maxMemType42 | Maximum memory usage when a TrueType font is downloaded as a Type 42 font |
| uint32 | minMemType1 | Minimum memory usage when a TrueType font is downloaded as a Type 1 font |
| uint32 | maxMemType1 | Maximum memory usage when a TrueType font is downloaded as a Type 1 font |

The `isFixedPitch` flag is used to indicate that the font is monospaced. A monospaced font is one in which all glyphs have the same horizontal width at all point sizes (that is, in the [`'hmtx'`](hmtx.md) and [`'hdmx'`](hdmx.md) tables), or have zero width. A monospaced font will also have to have the maximum width field in the [`'hhea'` table](hhea.md) set appropriately. Note that on OS X, it is also necessary to make sure that glyph widths from 'NFNT' bitmap fonts are consistent with the monospaced metrics in the TrueType font.

The entries minMemType42, maxMemType42, minMemType1, and maxMemType1 are necessary because PostScript drivers can do better memory management if the virtual memory requirements of a downloadable TrueType font are known before the font is downloaded. This information should be supplied if known. If it is not known, set the values to zero.

Maximum memory usage is minimum memory usage plus maximum runtime memory use. Maximum runtime memory use depends on the maximum band size of any bitmap potentially rasterized by the TrueType font scaler. Runtime memory usage could be calculated by rendering characters at different point sizes and comparing the memory use.

The memory usage of a downloaded TrueType font will vary with whether it is defined as a TrueType or Type 1 font on the printer. Minimum memory usage can be calculated by calling VMStatus, downloading the font, and calling VMStatus a second time.

<a id="anchor-post-part-2"></a>

## `'post'` Format 1

The order in which glyphs are placed in a font is at the convenience of the font developer To use format 1, a font must contain exactly the 258 glyphs in the standard Macintosh ordering. For such fonts, the glyph names are taken from the system. As a result, this format does not require a special subtable.

The names for these 258 glyphs are, in order:

| Glyph ID | Name |
| --- | --- |
| 0 | .notdef |
| 1 | .null |
| 2 | nonmarkingreturn |
| 3 | space |
| 4 | exclam |
| 5 | quotedbl |
| 6 | numbersign |
| 7 | dollar |
| 8 | percent |
| 9 | ampersand |
| 10 | quotesingle |
| 11 | parenleft |
| 12 | parenright |
| 13 | asterisk |
| 14 | plus |
| 15 | comma |
| 16 | hyphen |
| 17 | period |
| 18 | slash |
| 19 | zero |
| 20 | one |
| 21 | two |
| 22 | three |
| 23 | four |
| 24 | five |
| 25 | six |
| 26 | seven |
| 27 | eight |
| 28 | nine |
| 29 | colon |
| 30 | semicolon |
| 31 | less |
| 32 | equal |
| 33 | greater |
| 34 | question |
| 35 | at |
| 36 | A |
| 37 | B |
| 38 | C |
| 39 | D |
| 40 | E |
| 41 | F |
| 42 | G |
| 43 | H |
| 44 | I |
| 45 | J |
| 46 | K |
| 47 | L |
| 48 | M |
| 49 | N |
| 50 | O |
| 51 | P |
| 52 | Q |
| 53 | R |
| 54 | S |
| 55 | T |
| 56 | U |
| 57 | V |
| 58 | W |
| 59 | X |
| 60 | Y |
| 61 | Z |
| 62 | bracketleft |
| 63 | backslash |
| 64 | bracketright |
| 65 | asciicircum |
| 66 | underscore |
| 67 | grave |
| 68 | a |
| 69 | b |
| 70 | c |
| 71 | d |
| 72 | e |
| 73 | f |
| 74 | g |
| 75 | h |
| 76 | i |
| 77 | j |
| 78 | k |
| 79 | l |
| 80 | m |
| 81 | n |
| 82 | o |
| 83 | p |
| 84 | q |
| 85 | r |
| 86 | s |
| 87 | t |
| 88 | u |
| 89 | v |
| 90 | w |
| 91 | x |
| 92 | y |
| 93 | z |
| 94 | braceleft |
| 95 | bar |
| 96 | braceright |
| 97 | asciitilde |
| 98 | Adieresis |
| 99 | Aring |
| 100 | Ccedilla |
| 101 | Eacute |
| 102 | Ntilde |
| 103 | Odieresis |
| 104 | Udieresis |
| 105 | aacute |
| 106 | agrave |
| 107 | acircumflex |
| 108 | adieresis |
| 109 | atilde |
| 110 | aring |
| 111 | ccedilla |
| 112 | eacute |
| 113 | egrave |
| 114 | ecircumflex |
| 115 | edieresis |
| 116 | iacute |
| 117 | igrave |
| 118 | icircumflex |
| 119 | idieresis |
| 120 | ntilde |
| 121 | oacute |
| 122 | ograve |
| 123 | ocircumflex |
| 124 | odieresis |
| 125 | otilde |
| 126 | uacute |
| 127 | ugrave |
| 128 | ucircumflex |
| 129 | udieresis |
| 130 | dagger |
| 131 | degree |
| 132 | cent |
| 133 | sterling |
| 134 | section |
| 135 | bullet |
| 136 | paragraph |
| 137 | germandbls |
| 138 | registered |
| 139 | copyright |
| 140 | trademark |
| 141 | acute |
| 142 | dieresis |
| 143 | notequal |
| 144 | AE |
| 145 | Oslash |
| 146 | infinity |
| 147 | plusminus |
| 148 | lessequal |
| 149 | greaterequal |
| 150 | yen |
| 151 | mu |
| 152 | partialdiff |
| 153 | summation |
| 154 | product |
| 155 | pi |
| 156 | integral |
| 157 | ordfeminine |
| 158 | ordmasculine |
| 159 | Omega |
| 160 | ae |
| 161 | oslash |
| 162 | questiondown |
| 163 | exclamdown |
| 164 | logicalnot |
| 165 | radical |
| 166 | florin |
| 167 | approxequal |
| 168 | Delta |
| 169 | guillemotleft |
| 170 | guillemotright |
| 171 | ellipsis |
| 172 | nonbreakingspace |
| 173 | Agrave |
| 174 | Atilde |
| 175 | Otilde |
| 176 | OE |
| 177 | oe |
| 178 | endash |
| 179 | emdash |
| 180 | quotedblleft |
| 181 | quotedblright |
| 182 | quoteleft |
| 183 | quoteright |
| 184 | divide |
| 185 | lozenge |
| 186 | ydieresis |
| 187 | Ydieresis |
| 188 | fraction |
| 189 | currency |
| 190 | guilsinglleft |
| 191 | guilsinglright |
| 192 | fi |
| 193 | fl |
| 194 | daggerdbl |
| 195 | periodcentered |
| 196 | quotesinglbase |
| 197 | quotedblbase |
| 198 | perthousand |
| 199 | Acircumflex |
| 200 | Ecircumflex |
| 201 | Aacute |
| 202 | Edieresis |
| 203 | Egrave |
| 204 | Iacute |
| 205 | Icircumflex |
| 206 | Idieresis |
| 207 | Igrave |
| 208 | Oacute |
| 209 | Ocircumflex |
| 210 | apple |
| 211 | Ograve |
| 212 | Uacute |
| 213 | Ucircumflex |
| 214 | Ugrave |
| 215 | dotlessi |
| 216 | circumflex |
| 217 | tilde |
| 218 | macron |
| 219 | breve |
| 220 | dotaccent |
| 221 | ring |
| 222 | cedilla |
| 223 | hungarumlaut |
| 224 | ogonek |
| 225 | caron |
| 226 | Lslash |
| 227 | lslash |
| 228 | Scaron |
| 229 | scaron |
| 230 | Zcaron |
| 231 | zcaron |
| 232 | brokenbar |
| 233 | Eth |
| 234 | eth |
| 235 | Yacute |
| 236 | yacute |
| 237 | Thorn |
| 238 | thorn |
| 239 | minus |
| 240 | multiply |
| 241 | onesuperior |
| 242 | twosuperior |
| 243 | threesuperior |
| 244 | onehalf |
| 245 | onequarter |
| 246 | threequarters |
| 247 | franc |
| 248 | Gbreve |
| 249 | gbreve |
| 250 | Idotaccent |
| 251 | Scedilla |
| 252 | scedilla |
| 253 | Cacute |
| 254 | cacute |
| 255 | Ccaron |
| 256 | ccaron |
| 257 | dcroat |

When OS X 8.5 was released, the MacRoman character set was redefined to replace the Universal Currency Symbol with the Euro. The standard Macintosh ordering of glyphs was not updated, however, in order to avoid breaking fonts and software that used it. Font vendors should update their fonts as possible to include the Euro for proper functioning on OS X 8.5 and later. Fonts with the Euro cannot use `'post'` formats 1 or 2.5.

<a id="anchor-post-part-3"></a>

## `'post'` Format 2

Format 2 is used for fonts that contain some glyphs not in the standard set or whose glyph ordering is non-standard. The glyph name index array in this subtable maps the glyphs in this font to a name index. If the name index is between 0 and 257, treat the name index as a glyph index in the Macintosh standard order. If the name index is between 258 and 32767, then subtract 258 and use that to index into the list of Pascal strings at the end of the table. In this manner a font may map some of its glyphs to the standard glyph names, and some to its own names.

Index numbers 32768 through 65535 are reserved for future use. If you do not want to associate a PostScript name with a particular glyph, use index number 0 which points to the name `.notdef`.

Note that the `numberOfGlyphs` field must be equal to the `numGlyphs` field of the [`'maxp'` (Maximum Profile)](maxp.md) table.

**Table 73**: `'post'` format 2

| Type | Name | Description |
| --- | --- | --- |
| uint16 | numberOfGlyphs | number of glyphs |
| uint16 | glyphNameIndex\[numberOfGlyphs\] | Ordinal number of this glyph in `'post'` string tables. This is not an offset. |
| Pascal string | names\[numberNewGlyphs\] | glyph names with length bytes \[variable\] (a Pascal string) |

<a id="anchor-post-part-4"></a>

## `'post'` Format 2.5

Format 2.5 is a space saving format for fonts which contain a pure subset of the standard glyph set or which contain a reordering of the standard set. This format is useful for fonts that contain only glyphs in the standard Apple glyph set but which have those glyphs arranged in a non-standard order or fonts which are missing some glyphs. The table contains one byte for each glyph in the font. The byte is treated as a signed offset that maps the glyph index used in this font into the standard glyph index. For example, assume that the font contains the three glyphs A, B, and C. Assume that C appears first, B second and A third. These glyphs are the 37th, 38th, and 39th glyphs in the standard ordering. The `'post'` table would contain the bytes +39, +37, +35 because:

offset\[0\] indexes C and 0 + 39 = 39 the standard index for C

offset\[1\] indexes B and 1 + 37 = 38 the standard index for B

offset\[2\] indexes A and 2 + 35 = 37 the standard index for A

Note that the `numberOfGlyphs` field must be equal to the `numGlyphs` field of the [`'maxp'` (Maximum Profile)](maxp.md) table.

**Table 74**: `'post'` Format 2.5

| Type | Name | Description |
| --- | --- | --- |
| uint16 | numberOfGlyphs | Number of glyphs |
| int8 | offset\[number of glyphs\] | Difference between graphic index and standard order of glyph |

When OS X 8.5 was released, the MacRoman character set was redefined to replace the Universal Currency Symbol with the Euro. The standard Macintosh ordering of glyphs was not updated, however, in order to avoid breaking fonts and software that used it. Font vendors should update their fonts as possible to include the Euro for proper functioning on OS X 8.5 and later. Fonts with the Euro cannot use `'post'` formats 1 or 2.5.

As of February 2000, use the `'post'` format 2.5 is deprecated. Font vendors should not put `'post'` tables in their fonts using format 2.5 and should convert existing fonts to different `'post'` table formats.

<a id="anchor-post-part-5"></a>

## `'post'` Format 3

Format 3 makes it possible to create a special font that is not burdened with a large `'post'` table set of glyph names. This format specifies that no PostScript name information is provided for the glyphs in this font. The printing behavior of this format on PostScript printers is unspecified, except that it should not result in a fatal or unrecoverable error. Some drivers may print nothing, other drivers may attempt to print using a default naming scheme. This format does not require a special subtable.

Apple recommends against using `'post'` table format 3 under most circumstances, as it can create problems with some printer drivers and PDF documents. The savings in disk space usually does not justify the potential loss in functionality.

<a id="anchor-post-part-6"></a>

## `'post'` Format 4

Composite fonts on Japanese, Chinese or Korean printers work only with character codes. AAT printer drivers only know about glyph index values. The TrueType scaler uses format 4 `'post'` table to reencode a font that maps to a composite font on a printer. This encoding consists of naming the glyphs by using their character codes. The driver has PostScript code that knows how to take this ASCII string, strip the leading "a," and convert the rest to hexadecimal. The resulting hexadecimal number is the character code of the glyph. In this manner, the composite fonts on the printer are used.

Any font that maps to a composite font on the printer needs to include a format 4 `'post'` table. The structure of a format 4 `'post'` table is as follows: the `'post'` table header is followed by an array of uint16 values. An entry for every glyph is required. The index into the array is the glyph index. The data in the array is the character code that maps to that glyph, or 0xFFFF if there is no associated character code for that glyph.

As a rule, format 4 `'post'` tables are no longer necessary and should be avoided.

<a id="anchor-post-part-7"></a>

## Dependencies

If a `'post'` table implies a number of glyphs in the font—which is true for every `'post'` table format other than 3—the number of glyphs in the font implied by the `'post'` table must match the number of glyphs found in the [Maximum Profile (`'maxp'`)](maxp.md) table.
