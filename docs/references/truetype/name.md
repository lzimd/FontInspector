---
title: "The 'name' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-name-name"></a>

# The `'name'` table

<a id="anchor-name-part-1"></a>

## General table information

The *name table* (tag: `'name'`) allows you to include human-readable names for features and settings, copyright notices, font names, style names, and other information related to your font. These name character strings containing font-related information can be provided in any language. Entries in the name table are referenced by other TrueType font tables and can be used by applications and utilities to provide useful information to the user. Name table entries can be added by the font designer in any language at any time to provide information to world-wide users of the font.

The name table is the vehicle by which you convey information about your font to applications and users. You should assume that your font may be used in virtually every part of the globe. As a result, your font should be localized for other languages and cultural environments. This allows your font to be used by many users around the world.

The information included for each name record in the name table follows:

- Platform identifier code (`platformID`)
- Specific identifier code (`platformSpecificID`)
- Language identifier code (`languageID`)
- Name identifier code (`nameID`)
- Name information (multi-lingual character string)

The platform identifier code designates the computer on which the font is to be used. The specific identifier code designates the script system supported. The language identifier code is the language of the text used in the name fields. The name identifier code is a single word or number descriptor. The name information character strings provide information associated with the font. The name strings are raw character string data. The character set encoding used for the raw name data is determined by the platform and specific identifier codes. For example, if the platform identifier is for macOS and the specific identifier is Roman, then the raw string data is MacRoman. If the platform identifier is Unicode, then the raw string data is Unicode text in the UTF-16BE encoding format. The character strings can thus be localized to any language and script.

<a id="anchor-name-part-2"></a>

## Name Table Format

The name table header gives the format of the table, the number of name records (rows) in the table, and the offset in bytes to the multilingual character name strings. The format of the name table header is as follows:

*The `'name'` Table*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | format | Format selector. Set to 0. |
| UInt16 | count | The number of nameRecords in this name table. |
| UInt16 | stringOffset | Offset in bytes to the beginning of the name character strings. |
| NameRecord | nameRecord\[count\] | The name records array. |
| variable | name | Character strings. The character strings of the names. Note that these are not necessarily ASCII! |

[OpenType](https://docs.microsoft.com/en-us/typography/opentype/spec/name) also defines `'name'` tables with a `format` of 1. Such `'name'` tables are not supported on Apple platforms.

The name records array follows the name table header. Six entries are provided for each name record. Here is the format of a `NameRecord`:

*Name Records*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | platformID | Platform identifier code. |
| UInt16 | platformSpecificID | Platform-specific encoding identifier. |
| UInt16 | languageID | Language identifier. |
| UInt16 | nameID | Name identifier. |
| UInt16 | length | Name string length in bytes. |
| UInt16 | offset | Name string offset in bytes from stringOffset. |

<a id="anchor-name-part-3"></a>

### The platform identifier

<a id="anchor-name-ID"></a>

The supported platform identifier (`platformID`) codes are given in the following table. `platformID` codes have been assigned for Unicode, Macintosh, and Microsoft. `platformID` codes 240 through 255 have been reserved for user-defined platforms and are not available for registration. Names with `platformID`s other than 0, 1, and 3 are ignored on all Apple platforms.

*Platform Identifiers*

| Platform ID | Platform | Platform-specific ID |
| --- | --- | --- |
| 0 | Unicode | Indicates Unicode version. |
| 1 | Macintosh | QuickDraw Script Manager code. |
| 2 | (reserved; do not use) | <!-- colspan --> |
| 3 | Microsoft | Microsoft encoding. |

Names with `platformID` 1 were required by earlier versions of macOS. Its use on modern platforms is discouraged. Use names with `platformID` 3 instead for maximum compatibility. Some legacy software, however, may still require names with `platformID` 1, `platformSpecificID` 0.

The platform ID 2 was originally to use with ISO/IEC 10646. That use is now deprecated, because ISO/IEC 10646 and Unicode have identical character code assignments.

<a id="anchor-name-part-4"></a>

### The platform-specific ID

<a id="anchor-name-Specifics"></a>

To fully specify an encoding, it is necessary to state not only the platform identifier code, `platformID`, but also the platform-specific code, `platformSpecificID`. The semantics of a particular platform-specific code depend on the platform code used.

<a id="anchor-name-part-5"></a>

#### The Unicode platform

The Unicode platform-specific codes used with the `'name'` table are as follows:

*Unicode Platform-specific Encoding Identifiers*

| Platform-specific ID code | Meaning |
| --- | --- |
| 0 | Version 1.0 semantics |
| 1 | Version 1.1 semantics |
| 2 | ISO 10646 1993 semantics (deprecated) |
| 3 | Unicode 2.0 or later semantics (BMP only) |
| 4 | Unicode 2.0 or later semantics (non-BMP characters allowed) |

The preferred platform-specific code for Unicode is 4. The main distinction between Unicode 1.1 and later versions is that there is a block of some 6600 precomposed Hangul syllables in Unicode 1.1 starting at `U+3400` that was removed in Unicode 2.0 and replaced by a block of ideographs in Unicode 3.0. Use of the platform-specific code 1 for Unicode implies that characters from `U+3400` through `U+4DFF` are to be interpreted as Hangul syllables.

Because ISO/IEC 10646 is code-point identical with the Unicode Standard and any valid text encoded in 10646 is also valid as Unicode, there is no need to use the platform-specific code of 2 for Unicode text, and its use is now deprecated.

The Unicode platform-specific codes 5 and 6 not used by the `'name'` table. They are used only by the [`'cmap'` table](cmap.md).

All Unicode-based names must be in UTF-16BE (big-endian, two-byte encoding). UTF-8 and UTF-32 (one- and four-byte encodings) are not allowed.

<a id="anchor-name-part-6"></a>

#### The Macintosh platform

The Macintosh platform (`platformID` = 1) uses Macintosh script manager codes for the `platformSpecificID`. These are:

*Macintosh Platform-specific Encoding Identifiers*

| Platform-specific ID code | Script | Platform-specific ID code | Script |
| --- | --- | --- | --- |
| 0 | Roman | 17 | Malayalam |
| 1 | Japanese | 18 | Sinhalese |
| 2 | Traditional Chinese | 19 | Burmese |
| 3 | Korean | 20 | Khmer |
| 4 | Arabic | 21 | Thai |
| 5 | Hebrew | 22 | Laotian |
| 6 | Greek | 23 | Georgian |
| 7 | Russian | 24 | Armenian |
| 8 | RSymbol | 25 | Simplified Chinese |
| 9 | Devanagari | 26 | Tibetan |
| 10 | Gurmukhi | 27 | Mongolian |
| 11 | Gujarati | 28 | Geez |
| 12 | Oriya | 29 | Slavic |
| 13 | Bengali | 30 | Vietnamese |
| 14 | Tamil | 31 | Sindhi |
| 15 | Telugu | 32 | (Uninterpreted) |
| 16 | Kannada |  | <!-- colspan --> |

<a id="anchor-name-part-7"></a>

#### The Microsoft platform

For information on Microsoft platform-specific encoding identifiers, consult [the OpenType specification](https://docs.microsoft.com/en-us/typography/opentype/spec/).

<a id="anchor-name-part-8"></a>

### The language identifier

The language identifier (`languageID`) code uniquely defines the language in which the name character string is written for the name record. As with the `platformSpecificID`, the interpretation of the `languageID` is platform-specific.

<a id="anchor-name-part-9"></a>

#### The Unicode platform

For names with a Unicode `platformID`, the language code is unused and should be set to 0.

<a id="anchor-name-part-10"></a>

#### The Macintosh platform

If a name has a Macintosh `platformID`, the language code is interpreted as follows:

*Macintosh Language Codes*

| Language ID code | Language | Language ID code | Language |
| --- | --- | --- | --- |
| 0 | English | 59 | Pashto |
| 1 | French | 60 | Kurdish |
| 2 | German | 61 | Kashmiri |
| 3 | Italian | 62 | Sindhi |
| 4 | Dutch | 63 | Tibetan |
| 5 | Swedish | 64 | Nepali |
| 6 | Spanish | 65 | Sanskrit |
| 7 | Danish | 66 | Marathi |
| 8 | Portuguese | 67 | Bengali |
| 9 | Norwegian | 68 | Assamese |
| 10 | Hebrew | 69 | Gujarati |
| 11 | Japanese | 70 | Punjabi |
| 12 | Arabic | 71 | Oriya |
| 13 | Finnish | 72 | Malayalam |
| 14 | Greek | 73 | Kannada |
| 15 | Icelandic | 74 | Tamil |
| 16 | Maltese | 75 | Telugu |
| 17 | Turkish | 76 | Sinhalese |
| 18 | Croatian | 77 | Burmese |
| 19 | Chinese (traditional) | 78 | Khmer |
| 20 | Urdu | 79 | Lao |
| 21 | Hindi | 80 | Vietnamese |
| 22 | Thai | 81 | Indonesian |
| 23 | Korean | 82 | Tagalog |
| 24 | Lithuanian | 83 | Malay (Roman script) |
| 25 | Polish | 84 | Malay (Arabic script) |
| 26 | Hungarian | 85 | Amharic |
| 27 | Estonian | 86 | Tigrinya |
| 28 | Latvian | 87 | Galla |
| 29 | Sami | 88 | Somali |
| 30 | Faroese | 89 | Swahili |
| 31 | Farsi/Persian | 90 | Kinyarwanda/Ruanda |
| 32 | Russian | 91 | Rundi |
| 33 | Chinese (simplified) | 92 | Nyanja/Chewa |
| 34 | Flemish | 93 | Malagasy |
| 35 | Irish Gaelic | 94 | Esperanto |
| 36 | Albanian | 128 | Welsh |
| 37 | Romanian | 129 | Basque |
| 38 | Czech | 130 | Catalan |
| 39 | Slovak | 131 | Latin |
| 40 | Slovenian | 132 | Quechua |
| 41 | Yiddish | 133 | Guarani |
| 42 | Serbian | 134 | Aymara |
| 43 | Macedonian | 135 | Tatar |
| 44 | Bulgarian | 136 | Uighur |
| 45 | Ukrainian | 137 | Dzongkha |
| 46 | Byelorussian | 138 | Javanese (Roman script) |
| 47 | Uzbek | 139 | Sundanese (Roman script) |
| 48 | Kazakh | 140 | Galician |
| 49 | Azerbaijani (Cyrillic script) | 141 | Afrikaans |
| 50 | Azerbaijani (Arabic script) | 142 | Breton |
| 51 | Armenian | 143 | Inuktitut |
| 52 | Georgian | 144 | Scottish Gaelic |
| 53 | Moldavian | 145 | Manx Gaelic |
| 54 | Kirghiz | 146 | Irish Gaelic (with dot above) |
| 55 | Tajiki | 147 | Tongan |
| 56 | Turkmen | 148 | Greek (polytonic) |
| 57 | Mongolian (Mongolian script) | 149 | Greenlandic |
| 58 | Mongolian (Cyrillic script) | 150 | Azerbaijani (Roman script) |

<a id="anchor-name-part-11"></a>

#### The Microsoft platform

For information on Microsoft language identifiers, consult [the OpenType specification](https://docs.microsoft.com/en-us/typography/opentype/spec/).

<a id="anchor-name-part-12"></a>

### The name identifier codes

The name identifier (`nameID`) codes provide a single word or number description relating to the name character string. Codes 0 through 25 are predefined. Codes 26 through 255 are reserved. Codes 256 through 32767 are reserved for font-specific names for variation axes and instances, layout features and settings, etc. The predefined name identifier codes are given in the following table:

*Name Identifiers*

| NameID code(s) | Description |
| --- | --- |
| 0 | Copyright notice. |
| 1 | Font Family. |
| 2 | Font Subfamily. |
| 3 | Unique subfamily identification. |
| 4 | Full name of the font. |
| 5 | Version of the name table. |
| 6 | PostScript name of the font. All PostScript names in a font must be identical. They may not be longer than 63 characters and the characters used are restricted to the set of printable ASCII characters (U+0021 through U+007E), less the ten characters '\[', '\]', '(', ')', '{', '}', '\<', '\>', '/', and '%'. |
| 7 | Trademark notice. |
| 8 | Manufacturer name. |
| 9 | Designer; name of the designer of the typeface. |
| 10 | Description; description of the typeface. Can contain revision information, usage recommendations, history, features, and so on. |
| 11 | URL of the font vendor (with procotol, e.g., http://, ftp://). If a unique serial number is embedded in the URL, it can be used to register the font. |
| 12 | URL of the font designer (with protocol, e.g., http://, ftp://) |
| 13 | License description; description of how the font may be legally used, or different example scenarios for licensed use. This field should be written in plain language, not legalese. |
| 14 | License information URL, where additional licensing information can be found. |
| 15 | Reserved |
| 16 | Preferred Family. In Windows, the Family name is displayed in the font menu, and the Subfamily name is presented as the Style name. For historical reasons, font families have contained a maximum of four styles, but font designers may group more than four fonts to a single family. The Preferred Family and Preferred Subfamily IDs allow font designers to include the preferred family/subfamily groupings. These IDs are only present if they are different from IDs 1 and 2. |
| 17 | Preferred Subfamily. In Windows, the Family name is displayed in the font menu, and the Subfamily name is presented as the Style name. For historical reasons, font families have contained a maximum of four styles, but font designers may group more than four fonts to a single family. The Preferred Family and Preferred Subfamily IDs allow font designers to include the preferred family/subfamily groupings. These IDs are only present if they are different from IDs 1 and 2. |
| 18 | Compatible Full (macOS only). In QuickDraw, the menu name for a font is constructed using the FOND resource. This usually matches the Full Name. If you want the name of the font to appear differently than the Full Name, you can insert the Compatible Full Name in ID 18. This name is not used by macOS itself, but may be used by application developers (e.g., Adobe). |
| 19 | Sample text. This can be the font name, or any other text that the designer thinks is the best sample text to show what the font looks like. |
| 20–24 | Defined by OpenType. |
| 25 | Variations PostScript Name Prefix. If present in a variable font, it may be used as the family prefix in the algorithm to generate PostScript names for variation fonts. See [Adobe Technical Note #5902: “PostScript Name Generation for Variation Fonts”](https://wwwimages2.adobe.com/content/dam/acom/en/devnet/font/pdfs/5902.AdobePSNameGeneration.pdf) for details. |
| 26–255 | Reserved for future expansion. |
| 256–32767 | Font-specific names (e.g., names for layout features and settings, variations axes and instances). |

<a id="anchor-name-part-13"></a>

### Name strings

The name character strings follow the last name record. Their length and offset location in bytes are defined in their corresponding name record. It is important to remember that each name character string appears in the `'name'` table in the format relevant to its specified platform and platform-specific ID. For example, if the platform and platform-specific ID were Unicode 2.0, then the text strings would be encoded according to that standard.

In particular, Unicode names should be in UTF-16BE (i.e., big-endian two-byte characters). UTF-8 and UTF-32 must not be used. (For more information on Unicode encoding forms, see the Unicode Consortium's [UTF-8, UTF-16, UTF-32 & BOM FAQ](http://www.unicode.org/faq/utf_bom.html)). This is true for both strings with the Unicode `platform` and for strings with the Windows `platformID` and a `platformSpecificID` of either 1 or 10.

<a id="anchor-name-part-14"></a>

### Sample `'name'` table

The following example shows how the strings might be used.

*Sample `'name'` Table*

| Name ID | Platform ID | Platform-specific ID | Language ID | Name text |
| --- | --- | --- | --- | --- |
| 0 (Copyright) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | © 2020 Apple Inc. All rights reserved. |
| 1 (Family) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | Apple Biro |
| 2 (Style) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | Regular |
|  | 3 (Microsoft) | 1 (Unicode) | 1028 (Traditional Chinese) | 標準體 |
|  | 3 (Microsoft) | 1 (Unicode) | 1036 (French) | Normal |
|  | 3 (Microsoft) | 1 (Unicode) | 1040 (Italian) | Regolare |
|  | 3 (Microsoft) | 1 (Unicode) | 2052 (Simplified Chinese) | 常规体 |
| 3 (Unique) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | Apple Biro; 14.0d1e7; 2020-09-23 |
| 4 (Full) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | Apple Biro Regular |
| 5 (Version) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | Version 14.0d1e7 |
| 6 (PostScript) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | AppleBiro-Regular |
| 8 (Manufacturer) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | Apple Inc. |
| 9 (Designer) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | Apple Inc. |
| 11 (VendorURL) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | http://www.apple.com/ |
| 12 (DesignerURL) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | http://www.apple.com/ |
| 19 (Sample text) | 3 (Microsoft) | 1 (Unicode) | 1033 (English, United States) | The quick brown fox jumps over the lazy dog and runs away. |
|  | 3 (Microsoft) | 1 (Unicode) | 1036 (French) | Buvez de ce whisky que le patron juge fameux. |
|  | 3 (Microsoft) | 1 (Unicode) | 1106 (Welsh) | Parciais fy jac codi baw hud llawn dŵr ger tŷ Mabon. |
|  | 3 (Microsoft) | 1 (Unicode) | 1142 (Latin) | Sic fugiens, dux, zelotypos, quam Karus haberis. |

---

<a id="anchor-name-part-15"></a>

## Platform-specific Information

It is no longer recommended that fonts for use on macOS have PostScript names with the Macintosh platform ID and MacRoman platform-specific ID.

If two fonts are installed with the same PostScript name, Apple platforms treat them as duplicates and only one will be available for use.

If a font has two, inconsistent PostScript names, which one will be used is not defined.

Fonts in font suitcases will have PostScript names in the `'FOND'` resources. These should match the PostScript names in the corresponding `'sfnt'` resources' `'name'` tables. For legacy reasons, `'FOND'` PostScript names are preferred and may override the `'name'` table PostScript names.

When fonts are grouped into families by the font panel or Font Book on macOS, the Preferred Family and Preferred Style Names will be used if present.

On Apple platforms, `'name'` tables should include the following entries:

- Family (or Preferred Family)
- Style (or Preferred Style)
- Full
- PostScript

Each of these must be available in Unicode or a Macintosh platform ID form. The Unicode form may use the Unicode platform ID or a Microsoft platform ID with an appropriate platform-specific ID (1 or 10).

<a id="anchor-name-part-16"></a>

## Dependencies

The `'name'` table itself does not depend on other tables in the font. However, other tables (such as the [`'feat'` (feature name) table](feat.md) or the [`'fvar'` (font variations) table](fvar.md)) contain name identifiers which are to be used for UI elements providing control of font features or variations. Any name identifier found in one of these other tables must have at least one instance in the `'name'` table.
