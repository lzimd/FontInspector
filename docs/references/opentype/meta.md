---
title: "meta — Metadata Table"
description: "The meta table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-29T00:00:00Z"
updated_at: "2025-03-20T05:52:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/615fcb67c5a36454308c83c41326f43fa105495b/typographydocs/opentype/spec/meta.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-meta-meta-metadata-table"></a>

# meta — Metadata Table

The metadata table contains various metadata values for the font. Different categories of metadata are identified by four-character tags. Values for different categories can be either binary or text.

<a id="anchor-meta-table-formats"></a>

## Table formats

The metadata table begins with a header, structured as follows:

<a id="anchor-meta-metaTable_10"></a>

*MetaHeader*

| Type | Name | Description |
| --- | --- | --- |
| uint32 | version | Version number of the metadata table — set to 1. |
| uint32 | flags | Flags — currently unused; set to 0. |
| uint32 | (reserved) | Not used; set to 0. |
| uint32 | dataMapsCount | The number of data maps in the table. |
| DataMap | dataMaps\[dataMapsCount\] | Array of data map records. |

> *Note:* The reserved field was originally documented in Apple’s TrueType specification as a data offset. This was redundant: DataMap records include offsets from the start of the 'meta' table, therefore an additional offset is not used.

The data map record has the following format:

<a id="anchor-meta-dataMapRec"></a>

*DataMap record*

| Type | Name | Description |
| --- | --- | --- |
| Tag | tag | A tag indicating the type of metadata. |
| Offset32 | dataOffset | Offset in bytes from the beginning of the metadata table to the data for this tag. |
| uint32 | dataLength | Length of the data, in bytes. The data is not required to be padded to any byte boundary. |

The data for a given record may be either textual or binary. The representation format is specified for each tag. Depending on the tag, multiple records for a given tag may be permitted, or multiple, delimited values may be permitted in the data referenced by a single record, as specified for each tag. If only one record or value is permitted for a tag, then any instances after the first may be ignored.

<a id="anchor-meta-metadata-tags"></a>

## Metadata tags

Metadata tags identify the category of information provided and representation format used for a given metadata value. A registry of commonly-used tags is maintained, but private, vendor-determined tags can also be used.

Like other OpenType tags, metadata tags are four unsigned bytes that can equivalently be interpreted as a string of four ASCII characters. Metadata tags must begin with a letter (0x41 to 0x5A, 0x61 to 0x7A) and must use only letters, digits (0x30 to 0x39) or space (0x20). Space characters must only occur as trailing characters in tags that have fewer than four letters or digits.

Privately-defined metadata tags must begin with an uppercase letter (0x41 to 0x5A), and must use only uppercase letters or digits. Registered metadata tags must not use that pattern, but may be any other valid pattern.

Every registered tag defines the semantics of the associated metadata values, and the representation format of those values. Values for registered tags may be either textual or binary. If textual, it will be in UTF-8 encoding unless explicitly indicated otherwise.

The following registered tags are defined or reserved at this time:

| Tag | Name | Format | Description |
| --- | --- | --- | --- |
| appl | (reserved) |  | Reserved — used by Apple. |
| bild | (reserved) |  | Reserved — used by Apple. |
| dlng | Design languages | Text, using only Basic Latin (ASCII) characters. | Indicates languages and/or scripts for the user audiences that the font was primarily designed for. Only one instance is used. See below for additional details. |
| slng | Supported languages | Text, using only Basic Latin (ASCII) characters. | Indicates languages and/or scripts that the font is declared to be capable of supporting. Only one instance is used. See below for additional details. |

<a id="anchor-meta-dlng-and-slng-design-and-supported-languages"></a>

## 'dlng' and 'slng': design and supported languages

The values for 'dlng' and 'slng' are comprised of a series of comma-separated ScriptLangTags, which are described in detail below. Spaces may follow the comma delimiters and are ignored. Each ScriptLangTag identifies a language or script. A list of tags is interpreted to imply that all the languages or scripts are included.

The 'dlng' value is used to indicate the languages or scripts of the primary user audiences for which the font was designed. This value can be useful for selecting default font formatting based on content language, for presenting filtered font options based on user language preferences, or similar applications involving the language or script of content or user settings.

The 'slng' value is used to declare languages or scripts that the font is functionally capable of supporting. This value can be useful for font fallback mechanisms or other applications involving the language or script of content or user settings.

'slng' values can be used to provide more insight than could otherwise be obtained by inspecting a font’s 'cmap' table. For example, a font created for displaying a large range of Unicode characters in code charts could be capable of displaying default glyphs for Latin script and Devanagari script characters, but not support correct shaping for Devanagari script. Inspection of the 'cmap' table would indicate support for both Latin and Devanagari characters, but other analysis would be needed to detect that the font functionally supports Latin script but does not functionally support Devanagari script. In this case, it would be appropriate to use 'slng' data to declare that the font functionally supports Latin script, but not Devanagari script.

The Unicode range fields in the OS/2 table (see 5.1.8.18) are somewhat similar to 'slng' metadata values but operate on the level of Unicode blocks, which do not always correspond to languages or scripts, and which do not support any characters encoded in Unicode later than Unicode 5.1. Implementations that use 'slng' values in a font may ignore Unicode-range bits set in the OS/2 table.

> *Note:* A font developer can choose not to declare that a font supports certain languages or scripts even if the font is functionally capable of doing so. For example, an operating system could include several fonts designed for different scripts and include glyphs for a basic set of Latin characters in those fonts. If the Latin support in those fonts does not add functionality for Latin script in the overall product, however, the vendor could choose not to declare support for Latin script in those fonts.

'dlng' values can be used to provide further insight beyond that provided by 'slng': not only is the font functionally *capable* of supporting certain languages, but it is also *designed* to provide value for content in those scripts or languages. For example, a font designed for supporting Japanese could be functionally capable of supporting Latin script but not be a particularly useful option to offer in a font picker for French or German documents. In this case, it could be appropriate to declare Latin script as an 'slng' value but not as a 'dlng' value.

In many cases, the 'dlng' and 'slng' values declared in a font could be the same, and in general the 'slng' values should be the same as or a superset of those provided by 'dlng'. Font developers should consider whether there are appropriate differences between the 'slng' and 'dlng' declarations added into a font, and applications should make appropriate use of the differences.

If a font contains 'dlng' values but not 'slng' values, applications may infer that an 'slng' declaration using the 'dlng' values. The opposite should not be done, however: if a font has 'slng' values but not 'dlng' values, applications should not infer a 'dlng' declaration from the 'slng' declaration.

Some additional examples will help to understand the distinction between design and supported languages:

- Consider the case of accented Latin letters: Although the accents are used in common by a number of languages, the precise shape of the accents can depend on the typographic traditions of a specific language. Polish, for example, prefers steeper accents than French. A font that was designed with accents specifically for Polish could declare Polish as a design language ('dlng'), but declare support ('slng') for any language using Latin script.
- Fonts designed for East Asian markets will generally include glyphs for Latin, Greek and Cyrillic because these characters are included in important East Asian character set standards, but using East Asian fonts for languages that are written with those scripts is generally unsatisfactory. Such fonts could include these scripts in the 'slng' value, but omit them from their 'dlng' value.
- There are some systematic differences in glyph design for the characters shared by Simplified and Traditional Chinese, such as the way the “bone” radical is drawn in all characters using it. A font specifically designed for use with Simplified Chinese could be used to display Traditional Chinese, but any character with the “bone” radical will look wrong to readers of Traditional Chinese. Such a font could include Simplified Chinese 'dlng' value, but both Simplified and Traditional Chinese in its 'slng' value.

<a id="anchor-meta-scriptlangtag-values"></a>

### ScriptLangTag values

The 'dlng' and 'slng' metadata use ScriptLangTag values, defined here.

A ScriptLangTag denotes a particular language or script associated with a font. These are adapted from the IETF BCP 47 specification, “Tags for Identifying Languages” (see [https://www.rfc-editor.org/info/bcp47](https://www.rfc-editor.org/info/bcp47)).

BCP 47 language tags can include various subtags that provide different types of qualifiers, such as language, script or region. In a BCP 47 language tag, a language subtag element is mandatory and other subtags are optional. ScriptLangTag values used for 'dlng' and 'slng' metadata values use a modification of the BCP 47 syntax: a tag must include either a language or a script subtag; other subtags are optional. The following augmented BNF syntax, adapted from BCP 47, is used:

```
    ScriptLangTag = (language | script | language "-" script)
                    ["-" region]
                    *("-" variant)
                    *("-" extension)
                    ["-" privateuse]
```

The expansion of the elements and the intended semantics associated with each are as defined in BCP 47. Script subtags are taken from ISO 15924. At present, no extensions are defined for use in ScriptLangTags, and any extension may be ignored. Private-use elements, which are prefixed with “-x”, are defined by private agreement between the source and recipient and may be ignored.

Subtags must be valid for use in BCP 47 and contained in the Language Subtag Registry maintained by IANA. See [http://www.iana.org/assignments/language-subtag-registry/language-subtag-registry](http://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) and section 3 of BCP 47 for details.

> *Note:* OpenType Layout script and language system tags are not the same as those used in BCP 47 and should not be referenced when creating or processing ScriptLangTags.

A ScriptLangTag that has a language subtag without a script subtag may be used but is strongly discouraged; a ScriptLangTag should always include a script subtag. Use of a language subtag without a script subtag should only be considered if the record for the language subtag in the IANA Language Subtag Registry includes a "Suppress-Script" value (see [section 3.1.9](https://www.rfc-editor.org/rfc/rfc5646.html#section-3.1.9) of BCP 47), in which case applications may infer that script subtag. Even in such cases, however, omission of the script subtag is not recommended. Applications may ignore tags that do not include a script subtag.

Any ScriptLangTag value not conforming to these specifications must be ignored.

A ScriptLangTag can denote fairly specific information; for example, “en-Latn-IN” would represent *Latin script as used for the English language in India*. In most cases, however, generic tags should be used, and it is anticipated that most tags used in 'dlng' and 'slng' metadata declarations will consist only of a script subtag. Language or other subtags may be included, however, and could be appropriate in some cases. Implementations must allow for ScriptLangTags that include additional subtags, but they may also choose to interpret only the script subtag and ignore other subtags.

Examples:

- “Latn” denotes Latin script (and any language or writing system using Latin script).
- “Cyrl” denotes Cyrillic script.
- “sr-Cyrl” denotes Cyrillic script as used for writing the Serbian language; a font that has this property value might not be suitable for displaying text in Russian or other languages written using Cyrillic script.
- “en-Dsrt” denotes English written with the Deseret script.
- “Hant” denotes Traditional Chinese.
- “Hant-HK” denotes Traditional Chinese as used in Hong Kong SAR.
- “Jpan” denotes Japanese writing — ISO 15924 defines “Jpan” as an alias for Han + Hiragana + Katakana.
- “Kore” denotes Korean writing — ISO 15924 defines “Kore” as an alias for Hangul + Han.
- “Hang” denotes Hangul script (exclusively — Hanja are not implied by “Hang”).

The Unicode Standard uses the ISO 15924 identifiers “Zinh” (inherited) and “Zyyy” (undetermined). These should not be used in ScriptLangTags. Similarly, “Zxxx” (unwritten document) and “Zzzz” (unencoded script) should never be used.

On the other hand, “Zmth” (mathematical notation), “Zsym” (symbols) and “Zsye” (Symbols (Emoji variant)) are not used in the Unicode Standard, yet they can be very useful as declarations in font files.

In relation to East Asian scripts, a declaration of “Jpan” can be used to cover hiragana, katakana and kanji. Similarly, “Kore” can be used to cover Hangul and hanja, though a Korean font with only Hangul support should use “Hang”. For Chinese fonts, “Hans” and “Hant” should normally be used to distinguish between Simplified and Traditional orthographies rather than the more generic declaration “Hani”. Region-specific variations such as “Hant-HK” can also be declared. In some cases, it could be appropriate to describe a font capability (but probably not design target) using the generic declaration “Hani” (denoting Han ideographs / Hanzi / Kanji / Hanja).

The BCP 47 specification for region subtags allows for continental and sub-continental regions. For example, “039” can be used to denote Southern Europe. Use of such extended-region subtags in ScriptLangTag values is not recommended as software implementations might not have the logic to make appropriate correlations to more specific regions or languages associated with those regions.
