---
title: "The 'ltag' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-ltag-ltag"></a>

# The `'ltag'` table

<a id="anchor-ltag-part-1"></a>

## Introduction

The `'ltag'` table provides a mapping between numeric codes and IETF language tags. The numeric codes are used in language field of the `'name'` table for strings with a Unicode platform. The codes are also used in conjunction with the `'feat'` and `'morx'` tables to provide language-specific shaping.

IETF language tags are used for a number of reasons. First, they are standard and in common use. In particular, they're used by locales on OS X and iOS. Secondly, they are extensible and don't require a pre-determined ennumeration of supported languages.

The table uses two structures.

*The `'ltag'` FTStringRange*

| Type | Name | Description |
| --- | --- | --- |
| UInt16 | offset | Offset from the start of the table to the beginning of the string |
| UInt16 | length | String length (in bytes) |

*The `'ltag'` header*

| Type | Name | Description |
| --- | --- | --- |
| UInt32 | version | Table version; currently 1 |
| UInt32 | flags | Table flags; currently none defined |
| UInt32 | numTags | Number of language tags which follow |
| FTStringRange\[\] | tagRange | Range for each tag's string |

There is one range per tag. Offsets are from the beginning of the table.

The flags field is currently unused and should be 0. The current version is 1.

IETF language tags are in ASCII and can therefore be interpreted as UTF-8 or any other ASCII-compatible text-encoding.

If we had a font with both English and Spanish names, we could build the following `'ltag'` table:

*Sample `'ltag'` table*

| Type | Value | Description |
| --- | --- | --- |
| UInt32 | 1 | Version |
| UInt32 | 0 | Flags |
| UInt32 | 2 | numTags |
| FTStringRange | 0,2 | First tag |
| FTStringRange | 2,2 | Second tag |
| char\[\] | "ensp" | Tag strings |

This maps English to language code 0 and Spanish to language code 1. We could then use this in the name table with Unicode-platform names:

*How the `'ltag'` is used*

| Language Code | Value |
| --- | --- |
| -1 (don't care) | Geneva |
| 0 | Geneva |
| 1 | Ginebra |

Language tags are also used by `'feat'` and `'morx'` tables using the new always-exclusive feature 39 (language code).

A standard example of this is a case where Cyrillic italic letters are written one way in Serbia and another way everywhere else. We can add to our `'ltag'` table:

*Sample `'ltag'` table*

| Type | Value | Description |
| --- | --- | --- |
| UInt32 | 1 | Version |
| UInt32 | 0 | Flags |
| UInt32 | 3 | numTags |
| FTStringRange | 0,2 | First tag |
| FTStringRange | 2,2 | Second tag |
| FTStringRange | 4,2 | Third tag |
| char\[\] | "enspsr" | Tag strings |

We can then define a font feature with feature type 39 and selector type 3. (We add one to the `'ltag'` index here because a selector type of 0 means "no change" for an exclusive feature.) We can then define a `'morx'` subtable that maps the standard Cyrillic glyphs to the Serbian-specific ones.

Note that the use of the `'ltag'` means that language tag IDs are internal to a specific font. This is similar to the way that glyphIDs are specific to a font. Anything which needs to know the identity of a glyph outside the context of the specific font needs to convert its glyph ID to a PostScript name via the `'post'` table. Similarly, anything which needs to know the identity of a language tag outside the context of a specific font would need to convert the tag ID to an IETF tag via the `'ltag'` table.

<a id="anchor-ltag-part-2"></a>

## UI concerns:

IETF language tie naturally in to the OS X and iOS user interface and tools such as `ftxdumperfuser`. One could use a statement like

`[[NSLocale autoupdatingCurrentLocale] displayNameForKey:NSLanguageIdentifier value:tag]`

to get the proper string to use in the UI. This also ties in well with locale information as used elsewhere in the system.

<a id="anchor-ltag-part-3"></a>

## Platform-specific Information

Support for the `'ltag'` table is available on OS X 10.9 (Mavericks) and later, and on iOS 7.0 and later. The `'ltag'` table is currently supported only in conjunction with [`'morx'` (extended metamorphosis)](morx.md) and [`'feat'` (font feature)](feat.md) tables.

<a id="anchor-ltag-part-4"></a>

## Tools

`'ltag'` tables are fully supported by ftxdumperfuser. ftxenhancer will generate or extended `'ltag'` tables as needed when processing an ATIF.
