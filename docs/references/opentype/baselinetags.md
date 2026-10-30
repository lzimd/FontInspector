---
title: "Baseline Tags"
description: "Baseline tags (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-07-06T00:00:00Z"
updated_at: "2024-07-07T00:57:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/2a569f93648490448500e34f476f3378792d2213/typographydocs/opentype/spec/baselinetags.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-baselinetags-baseline-tags"></a>

# Baseline Tags

<a id="anchor-baselinetags-base"></a>

Baseline tags are used in the [BASE](base.md) table to provide additional font metric values that may apply to particular scripts or usage contexts.

Baseline tags can be used in the BASE table’s HorizAxis subtable for horizontal layout, or in the VertAxis subtable for vertical layout. A given baseline tag has a specific meaning for each layout direction. For example, the 'romn' baseline tag is used to specify the horizontal baseline for Latin text in horizontal layout, and the vertical baseline for rotated Latin text in vertical layout; the 'icfb' baseline tag is used to specify the bottom edge of an “ideographic character face” region (described below) in horizontal layout, and the left edge in vertical layout.

All tags are four-character strings composed of a limited set of ASCII characters; for details regarding the Tag data type, see [Data Types](otff.md#anchor-otff-data-types). By convention, registered baseline tags use four lowercase letters.

Within this section, the notation **\<axis\>.\<baseline tag\>** is used to mean the given baseline tag when used in the specified layout-direction axis table within the BASE table. For example, **HorizAxis.ideo** means the 'ideo' baseline tag used in the HorizAxis subtable of the BASE table.

The following table describes the registered baseline tags. Sections that follow provide more details related to certain baseline tags.

| Baseline tag | Baseline for HorizAxis | Baseline for VertAxis |
| --- | --- | --- |
| 'hang' | The hanging baseline. This is the horizontal line from which syllables seem to hang in Tibetan and other similar scripts. | The hanging baseline, (which now appears vertical) for Tibetan (or some other similar script) characters rotated 90 degrees clockwise, for vertical writing mode. |
| 'icfb' | Ideographic character face bottom edge. (See [Ideographic Character Face](#anchor-baselinetags-ideographic-character-face) below for usage.) | Ideographic character face left edge. (See [Ideographic Character Face](#anchor-baselinetags-ideographic-character-face) below for usage.) |
| 'icft' | Ideographic character face top edge. (See [Ideographic Character Face](#anchor-baselinetags-ideographic-character-face) below for usage.) | Ideographic character face right edge. (See [Ideographic Character Face](#anchor-baselinetags-ideographic-character-face) below for usage.) |
| 'ideo' | Ideographic em-box bottom edge. (See [Ideographic em-box](#anchor-baselinetags-ideographic-em-box) below for usage.) | Ideographic em-box left edge. If this tag is present in the VertAxis, the value must be set to 0. (See [Ideographic em-box](#anchor-baselinetags-ideographic-em-box) below for usage.) |
| 'idtp' | Ideographic em-box top edge. (See [Ideographic em-box](#anchor-baselinetags-ideographic-em-box) below for usage.) | Ideographic em-box right edge. If this tag is present in the VertAxis, the value is strongly recommended to be set to head.unitsPerEm. (See [Ideographic em-box](#anchor-baselinetags-ideographic-em-box) below for usage.) |
| 'math' | The baseline about which characters in mathematical formulas are centered. | The baseline about which characters in mathematical formulas are centered when formulas are rotated 90 degrees clockwise for vertical writing mode. |
| 'romn' | The baseline used by alphabetic scripts such as Latin, Cyrillic and Greek. | The alphabetic baseline for characters rotated 90 degrees clockwise for vertical writing mode. (This would not apply to alphabetic characters that remain upright in vertical writing mode, since these characters are not rotated.) |

<a id="anchor-baselinetags-ideographic-em-box"></a>

## Ideographic em-box

Some applications use *ideographic em-box* metrics for layout of CJK text. A font’s ideographic em-box is the rectangle that defines a standard escapement around the full-width ideographic glyphs of the font, for both the horizontal and vertical writing directions. It is usually a square, but may be non-square, as in the case of fonts used in Japanese newspaper layout that have a vertically condensed design.

The left, right, top and bottom edges of the ideographic em-box are determined as follows:

> ideoEmboxLeft = 0<br> If **HorizAxis.ideo** is defined:
>
> > ideoEmboxBottom = **HorizAxis.ideo**<br> If **HorizAxis.idtp** is defined:
> >
> > > ideoEmboxTop = **HorizAxis.idtp**
> >
> > Else:
> >
> > > ideoEmboxTop = **HorizAxis.ideo** + head.unitsPerEm
> >
> > If **VertAxis.idtp** is defined:
> >
> > > ideoEmboxRight = **VertAxis.idtp**
> >
> > Else:
> >
> > > ideoEmboxRight = head.unitsPerEm
> >
> > If **VertAxis.ideo** is defined and is non-zero:
> >
> > > Warning: Bad **VertAxis.ideo** value
>
> Else If this is a CJK font:
>
> > ideoEmboxBottom = OS/2.sTypoDescender<br> ideoEmboxTop = OS/2.sTypoAscender<br> ideoEmboxRight = head.unitsPerEm
>
> Else:
>
> > ideoEmbox cannot be determined for this font

Determining whether a font is CJK (Chinese, Japanese, or Korean) or not, as in the second-last “Else” clause above, can be done by checking the 'dlng' entry (if present) of the ['meta'](meta.md) table, the CJK-related bits of the [OS/2.ulUnicodeRange](os2.md#anchor-os2-ulunicoderange) fields, or the [OS/2.ulCodePageRange](os2.md#anchor-os2-ulcodepagerange) fields.

Note that non-CJK fonts can specify a **HorizAxis.ideo** baseline; this can be used by applications when aligning the font with an ideographic font used on the same line of text, when alignment based on the ideographic em-box is used.

The ideographic em-box center baseline is defined as halfway between the ideographic em-box top and bottom baselines in the horizontal axis, and halfway between the ideographic em-box left and right baselines in the vertical axis. These center baselines are calculated in whole font design units. The division used in the calculation must be rounded to the unit nearest 0 if needed. Thus, for maximal precision of center baseline placement, vendors should ensure that opposite edges of the ideographic em-box box are an even number of design units apart.

<a id="anchor-baselinetags-example"></a>

### Example

The values of the ideographic baseline tags for the Kozuka Mincho font family (designed on a 1000-unit em) are:

> **HorizAxis.ideo** = -120; **HorizAxis.idtp** = 880.

Since this describes a square ideographic em-box, it is sufficient to record only the following:

> **HorizAxis.ideo** = -120.<br>

If **HorizAxis.ideo** is not present, then the following will be used for the ideographic em-box bottom and top, since this is a CJK font:

> OS/2.sTypoDescender = -120; OS/2.sTypoAscender = 880.

<a id="anchor-baselinetags-compatibility-notes"></a>

### Compatibility notes

Most applications expect the width of full-width ideographs in a CJK font to be exactly one em, thus it is strongly recommended that **VertAxis.idtp**, if present, be set to head.unitsPerEm.

The OS/2.sTypoDescender and OS/2.sTypoAscender fields in a CJK font may specify metrics different from the **HorizAxis.ideo** and **HorizAxis.idtp** values in the BASE table. However, CJK font developers should be aware that some applications might not read the BASE table at all but simply use the OS/2.sTypoDescender and OS/2.sTypoAscender fields to describe the bottom and top edges of the ideographic em-box. If developers want their fonts to work correctly with such applications, they should ensure that any ideographic em-box values in the BASE table of their CJK fonts describe the same bottom and top edges as the OS/2.sTypoDescender and OS/2.sTypoAscender fields.

Some legacy platforms or applications might not use OS/2 fields at all. Thus, CJK fonts generally should have the same descender value recorded in hhea.descender, OS/2.sTypoDescender, and **HorizAxis.ideo** (if present) fields, and the same ascender value recorded in hhea.ascender, OS/2.sTypoAscender, and **HorizAxis.idtp** (if present) fields.

See the section [“OpenType CJK Font Guidelines”](recom.md#anchor-recom-opentype-cjk-font-guidelines) for more information about constructing CJK fonts.

<a id="anchor-baselinetags-ideographic-character-face"></a>

## Ideographic character face

In addition to ideographic em-box metrics, some applications also use *ideographic character face* metrics for layout of CJK documents. The ideographic character face (ICF) specifies an average or approximate bounding box of the ideographic glyphs in a CJK font. (This is different from the **FontBBox** operator in the PostScript programming language, which is the bounding box of all glyphs in the font superimposed.) It can also be used in a font that does not contain ideographs (for example, a kana-only font) to indicate metrics for ideographs that would balance with other existing glyphs in the font.

In Japanese, the term for ICF is *heikin jizura*.

ICF metrics are not typically used as a text baseline, though they can be used in this way. Rather, ICF metrics allow an application to provide improved visual alignment of page elements to text.

ICF metrics are often expressed in applications as a percentage that represents the ratio of the length of an ICF box edge to the length of an ideographic em-box edge, and is conceptualized as a square centered within the ideographic em-box. OpenType, however, allows for finer specification of ICF metrics, with the left, bottom, right, and top edges of the ICF box specified using **VertAxis.icfb**, **HorizAxis.icfb**, **VertAxis.icft**, and **HorizAxis.icft** values, respectively. This provides font designers with the flexibility to specify a non-square or non-centered ICF box.

Font designers should set the value of the ICF box edges based on how tight or loose they want the font to appear when text is set with no tracking or kerning (*beta gumi* in Japanese). Therefore, the left-over boundary of the ideographic em-box around the ICF box is the default escapement of the font.

Applications can use the ICF box as an alignment tool, to ensure that glyphs touch the edges of the text frame and that page objects are visually aligned to text edges. It is also useful for aligning glyphs of different sizes on the same line. In Japanese traditional paper-based workflow, the ICF box was often used for these purposes. It provides optically aligned results that are superior to using the ideographic em-box.

**HorizAxis.icfb** is the minimum piece of information required in a CJK font to define the ICF metrics. First, the ideographic em-box dimensions must be calculated as described above. The ICF edges are then calculated in the following order:

> If **HorizAxis.icfb** is defined:
>
> > icfBottom = **HorizAxis.icfb**<br> margin = **HorizAxis.icfb** - ideoEmboxBottom<br> If **HorizAxis.icft** is defined:
> >
> > > icfTop = **HorizAxis.icft**
> >
> > Else:
> >
> > > icfTop = ideoEmboxTop - margin
> >
> > If **VertAxis.icfb** is defined:
> >
> > > icfLeft = **VertAxis.icfb**
> >
> > Else:
> >
> > > icfLeft = margin
> >
> > If **VertAxis.icft** is defined:
> >
> > > icfRight = **VertAxis.icft**
> >
> > Else:
> >
> > > icfRight = ideoEmboxRight - icfLeft
>
> Else:
>
> > ICF cannot be determined for this font

For the last case above (i.e., fonts that don’t have ICF information in their BASE table), an application may choose to apply a heuristic such as calculating the bounding box of some or all of the ideographic and kana glyphs, and then averaging its margin with the ideographic em-box.

The ICF center baseline is defined as halfway between the ICF top and bottom baselines in the horizontal axis, and halfway between the ICF left and right baselines in the vertical axis. These center baselines are defined in whole character units. The division used in the calculation must round to the character unit nearest 0 if needed. Thus, for maximal precision of center baseline placement, vendors should ensure that opposite edges of the ICF box are an even number of character units apart.

<a id="anchor-baselinetags-example-1"></a>

### Example

The values of the ICF baselines for the Extra Light and Heavy weights of the Kozuka Mincho font family (designed on a 1000-unit em, with ideographic em-box as given in the example in the previous section) are:

> Kozuka Mincho Extra Light:<br> **VertAxis.icfb** = 41; **HorizAxis.icfb** = -79;<br> **VertAxis.icft** = 959; **HorizAxis.icft** = 839.
>
> Since this describes a square ICF centered in a square ideographic em-box, it is sufficient to record only the following:<br> **HorizAxis.icfb** = -79.

> Kozuka Mincho Heavy:<br> **VertAxis.icfb** = 26; **HorizAxis.icfb** = -94;<br> **VertAxis.icft** = 974; **HorizAxis.icft** = 854.
>
> It is sufficient to record only:<br> **HorizAxis.icfb** = -94.

It is strongly recommended that each of the edges of the ICF box be equidistant from the corresponding edge of the ideographic em-box. Following this will result in more predictable results in applications that use these values. That is, for fonts based on a square ideographic em-box, the ICF box should be a centered square.

See the section [“OpenType CJK Font Guidelines”](recom.md#anchor-recom-opentype-cjk-font-guidelines) for more information about constructing CJK fonts.
