---
title: "The 'meta' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-meta-maxp"></a>

# The `'meta'` table

<a id="anchor-meta-part-1"></a>

## General table information

The `'meta'` table contains metadata for the font. This metadata can be either binary or text. It begins with a header which is structured as follows:

*The `'meta'` Table*

| Type | Name | Description |
| --- | --- | --- |
| uint32\_t | version | The version of the table format, currently 1 |
| uint32\_t | flags | Flags, currently unused and set to 0 |
| uint32\_t | dataOffset | Offset from the beginning of the table to the data |
| uint32\_t | numDataMaps | The number of data maps in the table |

Following the header is a series of data maps. Each maps a four-character tag to a range of data within the table:

*Data Maps*

| Type | Name | Description |
| --- | --- | --- |
| FourCharCode | tag | A tag indicating the type of metadata |
| uint32\_t | dataOffset | Offset from the beginning of the table to the data for this tag |
| uint32\_t | dataLength | Length of the data. The data is not required to be padded to any byte boundary. |

Tag data may be either textual or binary. If textual, it should be in UTF-8.

<a id="anchor-meta-part-2"></a>

## Metadata tags

The following metadata tags are currently defined:

<a id="anchor-meta-part-3"></a>

### The `'dlng'` (design languages) tag

The `'dlng'` lists the languages and/or scripts which the font is specifically intended to cover. The list is a series of comma-separated ScriptLangTags based on the IETF BCP 47 specification. Detailed discussion is below. Spaces may be used between tags but are not required. "cy, mi" and "cy,mi" are both valid.

<a id="anchor-meta-part-4"></a>

### The `'slng'` (supported languages) tag

The `'slng'` lists the languages and/or scripts which the font is known to be capable of supporting. Again, this list is a series of comma-separated ScriptLangTags.

To understand the distinction between design and supported languages, consider the case of accented Latin letters. Although the accents are used in common by a number of languages, the precise shape of the accents can depend on the typographic traditions of a specific language. Polish, for example, prefers steeper accents than French. A font which was designed with accents specifically for Polish would then have `po-Latn` among its `'dlng'` tags but `Latn` among its `'slng'` tags.

As another example, fonts designed for East Asian markets will generally include glyphs for Latin, Greek, and Cyrillic because these characters are included in the relevant East Asian characer set standards, but using them for actual Latin, Greek, or Cyrillic text is generally unsatisfactory. Such fonts would therefore include `Latn`, `Grek`, and `Cyril` among their `'slng'` tags but not their `'dlng'` tags.

Finally, there are some systematic differences in glyph design for the characters shared by simplified and traditional Chinese. (The most notable is the way the “bone” radical is drawn in all characters using it.) A font specifically designed for use with simplified Chinese can usually be used with traditional Chinese, but any character with the “bone” radical will look wrong to readers of traditional Chinese. Such a font would include `Hans` in its `'dlng'` tags but both `Hans` and `Hant` in its `'slng'` tags.

<a id="anchor-meta-part-5"></a>

### The `'appl'` and `'bild'` tag

These tags are used internally by Apple. They use binary, and not text, data.

Font designers are not limited to the use of these metadata tags. Any metadata tag beginning with a capital letter (e.g., `'Foob'`) is to be considered private use. Other cross-platform tags will be added as needed.

(Note that the `'appl'` and `'bild'` tags are strictly-speaking private use, as they are Apple-internal tags. Their use is retained for historical reasons.)

<a id="anchor-meta-part-6"></a>

## ScriptLangTag Values

The `'dlng'` and `'slng'` metadata use *ScriptLangTag* values, defined here.

A ScriptLangTag denotes a particular script or language associated with a font. They are based on the IETF BCP 47 specification, “Tags for Identifying Languages”. (See [http://tools.ietf.org/html/bcp47](http://tools.ietf.org/html/bcp47)). BCP 47 tags can include various subtags that provide different types of qualifiers, such as language, script or region. In the BCP 47 specification, a language subtag is mandatory and other subtags are optional. ScriptLangTags used for `'dlng'` and `'slng'` metadata declarations use a modification of the BCP 47 syntax: a script subtag is mandatory, while other subtags are optional. The following augmented BNF syntax, adapted from BCP 47, is used:

```
ScriptLangTag = [language "-"]
				script
				["-" region]
				*("-" variant)
				*("-" extension)
				["-" privateuse]
```

The expansion of the language, script, region, variant, extension and private-use rules, and the intended semantics associated with each are as defined in BCP 47. At present, no extensions are defined for use in name `'dlng'` and `'slng'` metadata declarations, and any extensions encountered will be ignored. Any privateuse subtag sequences may be ignored by applications interpreting name `'dlng'` and `'slng'` metadata strings.

Subtags must be valid for use in BCP 47 and contained in the Language Subtag Registry maintained by IANA. See [http://www.iana.org/assignments/language-subtag-registry/language-subtag-registry](http://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) and section 3 of BCP 47 for details. Implementations may use a dated snapshot of the IANA subtag registry and are not required to interpret every subtag defined in the registry. Any subtag that is interpreted, however, must be interpreted in conformance with the description in the registry.

**Note: OpenType Layout script and language system tags are not the same as those used in BCP 47 and should not be referenced when creating or processing ScriptLangTags.**

Any ScriptLangTag that does not conform to these specifications is ignored.

It should be noted that the various elements in a BCP 47 tag have different length requirements that, together with ordering requirements, allow for unambiguous interpretation. A script subtag is always exactly four characters long and is derived from the ISO 15924 standard. (See [http://www.unicode.org/iso15924/](http://www.unicode.org/iso15924/).) Also, language subtags cannot be four characters long.

A ScriptLangTag can denote fairly specific information; for example, “en-Latn-IN” would represent ‘Latin script as used for the English language in India’. In most cases, however, generic tags should be used, and it is anticipated that most tags used in `'dlng'` and `'slng'` metadata declarations will consist only of a script subtag. Language or other subtags can be included, however, and may be appropriate in some cases. Implementations must allow for ScriptLangTags that include additional subtags, but they may also choose to interpret only the script subtag and ignore other subtags.

Examples:

- “Latn” denotes Latin script (and any language or writing system using Latin script)
- “Cyrl” denotes Cyrillic script
- “sr-Cyrl” denotes Cyrillic script as used for the Serbian language
- “en-Dsrt” denotes English written with the Deseret script
- “Hant” denotes Traditional Chinese
- “Hant-HK” denotes Traditional Chinese as used in Hong Kong
- “Jpan” denotes Japanese writing — ISO 15924 defines “Jpan” as an alias for Han + Hiragana + Katakana
- “Kana” denotes Katakana script (exclusively — no Han or Hiragana characters)
- “Kore” denotes Korean writing — ISO 15924 defines “Kore” as an alias for Hangul + Han
- “Hang” denotes Hangul script (exclusively —Hanja are not implied by “Hang”)

The Unicode Standard uses the ISO 15924 script identifiers “Zinh” (‘inherited’) and “Zyyy” (‘undetermined’). These should not be used in ScriptLangTags for `'dlng'` and `'slng'` metadata. Similarly, “Zxxx” (‘unwritten document’) and “Zzzz” (‘unencoded script’) should never be used.

On the other hand, “Zmth” (‘Mathematical notation’) and “Zsym” (‘Symbols”) are not used in the Unicode Standard, yet they may be very useful as declarations in font files. (They were, in fact, added to ISO 15924 for use in relation to fonts.)

In relation to East Asian scripts, a declaration of “Jpan” can be used to cover hiragana, katakana and kanji. Similarly, “Kore” can be used to cover Hangul and hanja, though a Korean font with only Hangul support should use “Hang”. For Chinese fonts, “Hans” and “Hant” should normally be used to distinguish between Simplified and Traditional orthographies rather than the more generic declaration “Hani”. Region-specific variations such as “Hant-HK” can also be declared. In some cases, it may be appropriate to describe a font capability (but probably not design target) using the generic declaration “Hani” (‘Han (Hanzi, Kanji, Hanja)’).

The BCP 47 specification for region subtags allows for continental and sub-continental regions. For example, “039” can be used to denote Southern Europe. Use of such extended-region subtags in ScriptLangTag values is not recommended as software implementations may not have the logic to make appropriate correlations to more specific regions or languages associated with those regions.
