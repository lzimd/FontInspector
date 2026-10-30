---
title: "OpenType Specification Change Log"
description: "OpenType specification change log (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2026-09-17T00:00:00Z"
updated_at: "2026-09-17T18:22:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/4ccd0b67c5532bd6ada3728567e2fbd39510b2a7/typographydocs/opentype/spec/changes.md"
last-modified: "2026-09-17T18:25:02Z"
---

<a id="anchor-changes-opentype-specification-change-log"></a>

# OpenType Specification Change Log

<a id="anchor-changes-version-191"></a>

## Version 1.9.1

Released May 2024

Structure or field names were revised in [base](base.md), [chapter2](chapter2.md), [cff2](cff2.md), [cmap](cmap.md), [eblc](eblc.md), [gdef](gdef.md), [gpos](gpos.md), [hmtx](hmtx.md), and [jstf](jstf.md) chapters; see below for details.

Minor editorial changes (not detailed below) were made in the following chapters: [avar](avar.md), [base](base.md), [baselinetags](baselinetags.md), [cbdt](cbdt.md), [cblc](cblc.md), [cff](cff.md), [chapter2](chapter2.md), [cmap](cmap.md), [colr](colr.md), [cpal](cpal.md), [cvt](cvt.md), [dsig](dsig.md), [dvaraxisreg](dvaraxisreg.md), [ebdt](ebdt.md), [eblc](eblc.md), [ebsc](ebsc.md), [featurelist](featurelist.md), [features\_ae](features_ae.md), [features\_fj](features_fj.md), [features\_ko](features_ko.md), [features\_pt](features_pt.md), [features\_uz](features_uz.md), [featuretags](featuretags.md), [fpgm](fpgm.md), [fvar](fvar.md), [gasp](gasp.md), [gdef](gdef.md), [glyf](glyf.md), [gpos](gpos.md), [gsub](gsub.md), [gvar](gvar.md), [hdmx](hdmx.md), [head](head.md), [hhea](hhea.md), [hvar](hvar.md), [ibmfc](ibmfc.md), [jstf](jstf.md), [kern](kern.md), [languagetags](languagetags.md), [loca](loca.md), [ltsh](ltsh.md), [math](math.md), [merg](merg.md), [meta](meta.md), [mvar](mvar.md), [name](name.md), [os2](os2.md), [otff](otff.md), [otvarcommonformats](otvarcommonformats.md), [otvaroverview](otvaroverview.md), [overview](overview.md), [pclt](pclt.md), [post](post.md), [prep](prep.md), [recom](recom.md), [sbix](sbix.md), [scripttags](scripttags.md), [stat](stat.md), [svg](svg.md), [tt\_instructing\_glyphs](tt_instructing_glyphs.md), [tt\_instructions](tt_instructions.md), [ttch01](ttch01.md), [ttochap1](ttochap1.md), [ttoreg](ttoreg.md), [vdmx](vdmx.md), [vmtx](vmtx.md), [vorg](vorg.md), [vvar](vvar.md).

*Summary of changes:*

- [base](base.md)

  - Changed structure names:

    - “FeatMinMaxRecord” to “FeatMinMax”
    - “BaseLangSysRecord” to “BaseLangSys”

  - Changed field names:

    - FeatMinMax record: “featureTableTag” to “featureTag”
    - BaseCoord tables: “baseCoordFormat” to “format”

- [cblc](cblc.md)

  - Changed field names:

    - BitmapSize record: “indexSubTableArrayOffset” to “indexSubtableListOffset”
    - BitmapSize record: “indexTablesSize” to “indexSubtableListSize”
    - BitmapSize record: “numberOfIndexSubTables” to “numberOfIndexSubtables”

- [cff2](cff2.md)

  - This chapter underwent significant editorial revision.

  - Changed structure, field and operator names:

    - “FDArray” to “FontDICTINDEX”
    - “FDSelect” to “FontDICTSelect”
    - “Variation Store” to “VariationStore”
    - “Top DICT” to “TopDICT”
    - “TopDictLength” to “TopDICTLength”
    - “Font DICT” to “FontDICT”
    - “Private DICT” to “PrivateDICT”
    - “Global Subr INDEX” to “GlobalSubrINDEX”
    - “CharString INDEX” to “CharStringINDEX”
    - “delta” to “deltaArray”
    - “vstore” to “VariationStoreOffset”
    - INDEX “offSize” to “offsetSize”
    - INDEX “offset” array to “offsets”
    - FontDICTSelect: “fds” to “fontDictIDs”
    - FontDICTSelect format 3: “range3” array to “ranges”
    - FontDICTSelect formats 3, 4: “nRanges” to “numRanges”
    - FontDICTSelect format 4: “range4” array to “ranges”
    - Range3, Range4: “fd” to “fontDictID”

  - Changed type of INDEX *offsetSize* field to uint8.

  - Changed the types used for INDEX offsets to *Offset8*, *Offset16*, etc.

  - Changed stack notation conventions.

  - Added PrivateDICT hinting operator descriptions (based on Adobe Type 1 Font Format).

  - Added section describing dependencies on other font tables.

  - Differences between CFF and CFF2 moved to a new appendix ([glyphformatcomparison](glyphformatcomparison.md)).

  - Incorporated the content of CFF2 Charstrings chapter into this chapter.

  - Clarified interaction between blending and stem or edge hint encoding using **hstemhm** and similar operators; and between blending and stem width values specified using **StdHW** and similar operators.

  - Corrected the note describing blending of **StemSnapH** and **StemSnapV** operands, and also the description of blended stem and edge hints and the relationsip between the encoded order of stems and **cntrmask** and **hintmask** bitflags (post-release erratum).

- cff2charstr

  - Content of this chapter was incorporated into the CFF chapter, and this appendex was deleted.

- [chapter2](chapter2.md)

  - Changed structure and field names:

    - ClassDefFormat1: “classValueArray” to “classValues”
    - “ClassRangeRecord” to “ClassRange”
    - “SequenceLookupRecord” to “SequenceLookup”
    - Coverage tables: “coverageFormat” to “format”
    - ClassDef tables: “classFormat” to “format”

  - Changed lookup flag name “MARK\_ATTACHMENT\_TYPE\_MASK” to “MARK\_ATTACHMENT\_CLASS\_FILTER”.

  - Clarified processing of a Lookup table with multiple subtables.

  - SequenceRuleSet table: corrected reference to field for the size of the seqRuleOffsets\[\] array (post-release erratum).

- [cmap](cmap.md)

  - Clarify the modulo arithmetic for idDelta in Format 2 and Format 4.
  - For Format 4, correct the description of the entrySelector field.
  - For Format 4, revert array name to idRangeOffset.
  - For Format 4, correct the entrySelector value in the second example.

- [colr](colr.md)

  - Removed obsoleted references to ColorIndex and VarColorIndex records (proposed in preliminary design but not used in final design).
  - Clarified handling of alpha with palette entries that reference text foreground color.
  - Added clarifications regarding color stop ordering, and provided possible implementation workaround for platforms that limit the range of color stop offsets.
  - Clarified behavior for different extend modes when all stops have the same offset.
  - Clarified radial gradient behavior when variation deltas result in a circle with negative radius, and provided possible implementation workaround for platforms that require non-negative radii.
  - Revised description of sweep gradients and the interpretation of their data representation.
  - Added clarifications about applying variation deltas to F2DOT14 or Fixed values.
  - Replaced the generic description of offset reference for subtable offsets with specific details in description of each structure containing subtable offsets.

- [dvaraxisreg](dvaraxisreg.md)

  - Use title case for axis names.

- [dvaraxistag\_opsz](dvaraxistag_opsz.md)

  - Use title case for axis names.

- [eblc](eblc.md)

  - Changed structure and field names:

    - BitmapSize record: “indexSubTableArrayOffset” to “indexSubtableListOffset”
    - BitmapSize record: “indexTablesSize” to “indexSubtableListSize”
    - BitmapSize record: “numberOfIndexSubTables” to “numberOfIndexSubtables”
    - “IndexSubTableArray” to “IndexSubtableList”
    - “IndexSubTable1” to “IndexSubtableFormat1”
    - “IndexSubTable2” to “IndexSubtableFormat2”
    - “IndexSubTable3” to “IndexSubtableFormat3”
    - “IndexSubTable4” to “IndexSubtableFormat4”
    - “IndexSubTable5” to “IndexSubtableFormat5”

  - Provided a formal description for the IndexSubtableList (renamed from IndexSubtableArray).

  - Clarified ordering requirements for indexSubtableRecords array.

- [ebsc](ebsc.md)

  - Description of the formats is revised to be consistent with other parts of the spec (array of fixed-size structures without offsets described as records).

- [features\_ae](features_ae.md)

  - Added feature 'apkn'.
  - Revised the descriptions for the 'aalt', 'chws', 'clig', 'cswh', 'cv01' – 'cv99', 'dlig' and 'expt' features.

- [features\_fj](features_fj.md)

  - Corrected name for 'flac' feature.
  - Revised the descriptions for the 'falt', 'fina', 'flac', 'fwid', 'halt', 'hkna', 'hngl', 'hwid', 'init', 'isol', 'jalt', 'jp78', 'jp83' and 'jp90' features.

- [features\_ko](features_ko.md)

  - Revised the descriptions for the 'kern', 'liga', 'ljmo', 'lnum', 'locl', 'medi', 'mgrk', 'mset', 'numr' and 'ordn' features.

- [features\_pt](features_pt.md)

  - Revised the descriptions for the 'palt', 'pcap', 'pkna', 'pwid', 'qwid', 'rclt', 'rvrn', 'size', 'smpl', 'ss01' – 'ss20', 'ssty', 'subs', 'sups', 'tjmo', 'tnam', 'trad' and 'twid' features.
  - Clarified that stylistic set features may be used in the GPOS table, and may be used in combination with one another.

- [features\_uz](features_uz.md)

  - Added feature 'vapk'.
  - Revised the descriptions for the 'unic', 'valt', 'vchw', 'vert', 'vhal', 'vjmo', 'vkna', 'vkrn', 'vpal', 'vrt2', 'vrtr' and 'zero' features.

- [fvar](fvar.md)

  - Revised recommendation for instance record name IDs for the default instance.
  - In the example 'fvar' table, corrected the axisSize field name.

- [gdef](gdef.md)

  - Change field names:

    - In CaretValue tables: “caretValueFormat” to “format”

- [glyf](glyf.md)

  - Clarified that a simple glyph with zero contours can have instructions but need not have any glyph data.
  - Revised description of OVERLAP\_SIMPLE to cover a broader range of implementations.
  - A missing bracket was added in the pseudo code for processing component glyph records.
  - Added details for the WE\_HAVE\_INSTRUCTIONS component flag.

- [glyphformatcomparison](glyphformatcomparison.md)

  - Added page.

- [gpos](gpos.md)

  - Changed structure and field names:

    - “PairValueRecord” to “PairValue”
    - “Class1Record” to “Class1”
    - “Class2Record” to “Class2”
    - “EntryExitRecord” to “EntryExit”
    - “Mark2Record” to “Mark2”
    - “ExtensionPosFormat1” to “PosExtensionFormat1”
    - multiple structures: “posFormat” to “format”
    - CursivePosFormat1: “entryExitRecord” to “entryExitRecords”
    - Anchor tables: “anchorFormat” to “format”

  - For Type 3, format 1, clarified that no adjustment is made if either entry or exit Anchor offset is NULL.

- [gsub](gsub.md)

  - Changed structure and field names:

    - “ExtensionSubstFormat1” to “SubstExtensionFormat1”
    - multiple structures: “substFormat” to “format”

  - Clarified the modulo arithmetic for deltaGlyphID in SingleSubstFormat1.

- [gvar](gvar.md)

  - Corrected example for processing composite glyphs.

- [head](head.md)

  - Added clarification regarding flags bit 1.

- [hmtx](hmtx.md)

  - Change data types for font unit values to FWORD, UFWORD.
  - Corrected casing of record name to LongHorMetrics.

- [jstf](jstf.md)

  - Consolidated JstfGSUBModList and JstfGPOSModList table formats into a common JstfModList table.
  - Corrected field name in JstfModList table: “gsubLookupIndices” to “lookupIndices” (post-release erratum)

- [kern](kern.md)

  - Removed obsolete platform-specific details.

- [languagetags](languagetags.md)

  - Added 'AAQ ', 'ACY ', 'ATS ', 'BDC ', 'CAY ', 'CBG ', 'CMI ', 'COO ', 'CTO ', 'EMP ', 'HUR ', 'JDT ', 'KBC ', 'KJJ ', 'LIV ', 'MEV ', 'ONE ', 'ONO ', 'PLG0', 'SEE ', 'SJA ', 'STR ', 'TAQ ', 'TDC ', 'THP ', 'THV ', 'THZ ', 'TLY ', 'TTQ ', 'TUS ', 'UDI ', 'UPPH', 'WBL ', 'WDT ', 'WYN ', 'YUF '.
  - Revised descriptions for 'BEL ', 'IRT ', 'SGA ', 'TMH '.
  - Added BCP 47 info for APPH, IPPH, UPPH (post-release update).
  - Updated BCP 47 info for CPP (post-release update).
  - Added 'KGF ', 'KMG ', 'KSU ', 'KVQ ', 'LUT ', 'NOP ', 'NUK ', 'SJE ' , 'SJU ', 'TBV ' (post-release update).

- [loca](loca.md)

  - Removed recommendation that offsets be two-byte aligned.

- [math](math.md)

  - Changed structure and field names:

    - MathGlyphConstruction: “mathGlyphVariantRecord” to “mathGlyphVariantRecords”.
    - “GlyphPartRecord” to “GlyphPart”.

  - Corrected description of spaceAfterScript.

  - Corrected description of radicalDegreeBottomRaisePercent.

- [meta](meta.md)

  - Added clarifications regarding intended use of 'dlng' and 'slng'.
  - Relaxed ScriptLangTag syntax to allow (but strongly discourage) a language subtag without a script subtag.

- [name](name.md)

  - Added clarifications regarding name ID 2 and interaction with OS/2.fsSelection style bits.
  - Revised description of name ID 13.
  - Corrected details regarding non-Unicode encoding IDs for platform 3.
  - Replaced list of Macintosh language IDs with reference to Apple documentation.
  - Replaced list of Windows language IDs with reference to external Microsoft documentation on language IDs.

- [os2](os2.md)

  - Change data types for font unit values to FWORD, UFWORD.
  - Added note regarding some CJK fonts having unexpected xAvgCharWidth values.
  - Added details related to use of int16 for ySubscriptXSize, ySubscriptYSize, ySuperscriptXSize, ySuperscriptYSize, yStrikeoutSize.
  - Added clarifications for fsSelection bits, including relation between bit 8 and the STAT table.

- [otff](otff.md)

  - Corrected casing of TableRecord in TableDirectory.
  - Added Offset8 in table of data types.

- [otvaroverview](otvaroverview.md)

  - Added clarification regarding rounding of calculated values.
  - Clarified that supplemental deltas for corners of a design space are optional.

- [otvarcommonformats](otvarcommonformats.md)

  - Corrected calculation of size for delta-set index mapping entries.
  - Clarify when variations of F2DOT14 values may need to be clamped.

- [post](post.md)

  - Clarified description of underlinePosition and its difference from the PostScript UnderlinePosition FontInfo key.

- [prep](prep.md)

  - Corrected details regarding when the CV program is executed.

- [sbix](sbix.md)

  - Clarified requirements related to graphicType = 'dupe' (“must”, not “should”).

- [scripttags](scripttags.md)

  - Added script tags for new scripts in Unicode 15.0 and Unicode 16.0.
  - Clarified usage of the 'math' script tag.
  - Added script tags for new scripts in Unicode 17.0 (post-release update).
  - Added script tags for new scripts in Unicode 18.0 (post-release update).

- [tt\_instructions](tt_instructions.md)

  - Corrected description of INSTCTRL.

- [ttch01](ttch01.md)

  - Added clarification on x-axis placement of design grid in relation to pen position.

- [vhea](vhea.md)

  - Change data type for advanceHeightMax to unsigned.
  - Change data types for font unit values to FWORD, UFWORD.

- [vorg](vorg.md)

  - Clarified that VORG may be used with CFF2.

- [vmtx](vmtx.md)

  - Change data types for font unit values to FWORD, UFWORD.

<a id="anchor-changes-version-19"></a>

## Version 1.9

Released December 2021

Structure names were revised in [chapter2](https://learn.microsoft.com/en-us/typography/opentype/otspec190/chapter2) and [fvar](https://learn.microsoft.com/en-us/typography/opentype/otspec190/fvar) chapters; see below for details.

Minor editorial changes (not detailed below) were made in the following chapters: [chapter2](https://learn.microsoft.com/en-us/typography/opentype/otspec190/chapter2), [cmap](https://learn.microsoft.com/en-us/typography/opentype/otspec190/cmap), [dvaraxisreg](https://learn.microsoft.com/en-us/typography/opentype/otspec190/dvaraxisreg), [featurelist](https://learn.microsoft.com/en-us/typography/opentype/otspec190/featurelist), [features\_ae](https://learn.microsoft.com/en-us/typography/opentype/otspec190/features_ae), [glyf](https://learn.microsoft.com/en-us/typography/opentype/otspec190/glyf), [gpos](https://learn.microsoft.com/en-us/typography/opentype/otspec190/gpos), [gsub](https://learn.microsoft.com/en-us/typography/opentype/otspec190/gsub), [gvar](https://learn.microsoft.com/en-us/typography/opentype/otspec190/gvar), [hvar](https://learn.microsoft.com/en-us/typography/opentype/otspec190/hvar), [index](https://learn.microsoft.com/en-us/typography/opentype/otspec190/), [kern](https://learn.microsoft.com/en-us/typography/opentype/otspec190/kern), [languagetags](https://learn.microsoft.com/en-us/typography/opentype/otspec190/languagetags), [name](https://learn.microsoft.com/en-us/typography/opentype/otspec190/name), [otvarcommonformats](https://learn.microsoft.com/en-us/typography/opentype/otspec190/otvarcommonformats), [otvaroverview](https://learn.microsoft.com/en-us/typography/opentype/otspec190/otvaroverview), [prep](https://learn.microsoft.com/en-us/typography/opentype/otspec190/prep), [recom](https://learn.microsoft.com/en-us/typography/opentype/otspec190/recom), [tt\_instructions](https://learn.microsoft.com/en-us/typography/opentype/otspec190/tt_instructions), [ttch01](https://learn.microsoft.com/en-us/typography/opentype/otspec190/ttch01).

*Summary of changes:*

- [chapter2](https://learn.microsoft.com/en-us/typography/opentype/otspec190/chapter2)

  - Changed spellings of field names of ConditionFormat1 table.

- [cmap](https://learn.microsoft.com/en-us/typography/opentype/otspec190/cmap)

  - For platform ID 0, encoding ID 3, removed suggestion of using format 0 subtable.
  - Clarified requirements for UVSes in a format 14 subtable and entries in other 'cmap' Unicode subtables.
  - Corrected description of the entrySelector field (post-release erratum).

- [colr](https://learn.microsoft.com/en-us/typography/opentype/otspec190/colr)

  - Added version 1 header and related structures.
  - Revised introductory sections and other editorial changes.
  - Added recommendation against using bold or italic simulations.

- [cpal](https://learn.microsoft.com/en-us/typography/opentype/otspec190/cpal)

  - Added reference to CSS Color Module Level 4.
  - Added section on interpolation of colors.

- [features\_ae](https://learn.microsoft.com/en-us/typography/opentype/otspec190/features_ae)

  - Modified 'cv*XX*' description.
  - Corrected use of non-preferred region / language / script name (post-release erratum).

- [features\_fj](https://learn.microsoft.com/en-us/typography/opentype/otspec190/features_fj)

  - Modified 'frac' feature description.

- [features\_ko](https://learn.microsoft.com/en-us/typography/opentype/otspec190/features_ko)

  - Modified 'lfbd' feature description.

- [features\_pt](https://learn.microsoft.com/en-us/typography/opentype/otspec190/features_pt)

  - Modified 'rtbd' feature description.

- [fvar](https://learn.microsoft.com/en-us/typography/opentype/otspec190/fvar)

  - Changed record name “Tuple” to “UserTuple”.

- [glyf](https://learn.microsoft.com/en-us/typography/opentype/otspec190/glyf)

  - Added remarks regarding glyph bounding rectangles in variable fonts.
  - Clarified interpretation of X\_SHORT\_VECTOR and Y\_SHORT\_VECTOR flags.
  - Clarified interpretation of the ARGS\_ARE\_XY\_VALUES and ROUND\_XY\_TO\_GRID component flags, and other aspects of composite glyph descriptions.
  - Changed FWord and F2Dot14 to FWORD and F2DOT14.

- [gpos](https://learn.microsoft.com/en-us/typography/opentype/otspec190/gpos)

  - Clarified consistency requirement for extension subtables within a given Lookup table.

- [gsub](https://learn.microsoft.com/en-us/typography/opentype/otspec190/gsub)

  - Clarified consistency requirement for extension subtables within a given Lookup table.
  - Corrected use of non-preferred region / language / script name (post-release erratum).

- [gvar](https://learn.microsoft.com/en-us/typography/opentype/otspec190/gvar)

  - Corrected type in sharedTuples array to Tuple.
  - Corrected spelling of GlyphVariationData and TupleVariationHeader.

- [head](https://learn.microsoft.com/en-us/typography/opentype/otspec190/head)

  - Clarified meaning of unitsPerEm, xMin, yMin, xMax and yMax values.
  - Added remarks regarding glyph bounding rectangles in variable fonts.

- [hvar](https://learn.microsoft.com/en-us/typography/opentype/otspec190/hvar)

  - Moved description of the DeltaSetIndexMap to the OpenType Font Variations Common Table Formats chapter.

- [languagetags](https://learn.microsoft.com/en-us/typography/opentype/otspec190/languagetags)

  - Added information on how to request new language system tags.
  - Added 'MONT', 'TJL '.
  - Added 'INUK' (post-release update).
  - Corrected entries for 'TUL ', 'TUM ' (post-release erratum).
  - Corrected use of non-preferred region / language / script name (post-release erratum).

- [maxp](https://learn.microsoft.com/en-us/typography/opentype/otspec190/maxp)

  - Added CFF2 as requiring version 0.5.

- [meta](https://learn.microsoft.com/en-us/typography/opentype/otspec190/meta)

  - Clarified that 'slng' value should be superset of 'dlng'.
  - Fixed URL for BCP 47 (post-release erratum).
  - Corrected use of non-preferred region / language / script name (post-release erratum).

- [name](https://learn.microsoft.com/en-us/typography/opentype/otspec190/name)

  - Clarified encoding scheme for platform 0 strings.
  - Added note regarding platform 3 and non-conforming legacy CJK fonts.
  - Corrected use of non-preferred region / language / script name (post-release erratum).

- [os2](https://learn.microsoft.com/en-us/typography/opentype/otspec190/os2)

  - Include details for legacy calculation of xAvgCharWidth in OS/2 versions 0 to 2 that were omitted since version 1.8.3.
  - Corrected use of non-preferred region / language / script name (post-release erratum).

- [otff](https://learn.microsoft.com/en-us/typography/opentype/otspec190/otff)

  - Added Offset24 type.
  - Added clarifications regarding NULL subtable offsets.
  - Added recommendation against duplicate tables.

- [otvarcommonformats](https://learn.microsoft.com/en-us/typography/opentype/otspec190/otvarcommonformats)

  - Added COLR as a table using variation data.
  - Moved description of DeltaSetIndexMap from the HVAR chapter to this chapter. Sub-divided the *entryFormat* field into separate *format* and *entryFormat* fields, and added a format 1 DeltaSetIndexMap.
  - Described application of deltas to F2DOT14, Fixed.
  - Revised ItemVariationData subtable adding support for 32-bit deltas. Also changed field name “shortDeltaCount” to “wordDeltaCount”.

- [otvaroverview](https://learn.microsoft.com/en-us/typography/opentype/otspec190/otvaroverview)

  - Clarified that any aspect of appearance can vary in a variable font.
  - Added details regarding integer bit depth in the algorithm for interpolation of instance values.

- [post](https://learn.microsoft.com/en-us/typography/opentype/otspec190/post)

  - Changed FWord to FWORD.

- [recom](https://learn.microsoft.com/en-us/typography/opentype/otspec190/recom)

  - Revised guidance for baseline-to-baseline distance.

- [scripttags](https://learn.microsoft.com/en-us/typography/opentype/otspec190/scripttags)

  - Added script tags for new scripts in Unicode 14.0.
  - Added remarks regarding 'jamo' and 'mymr'.
  - Corrected use of non-preferred region / language / script name (post-release erratum).

- [stat](https://learn.microsoft.com/en-us/typography/opentype/otspec190/stat)

  - Emphasized recommendation to include axis value tables covering all named instances of a variable font.

- [tt\_graphics\_state](https://learn.microsoft.com/en-us/typography/opentype/otspec190/tt_graphics_state)

  - Fix incorrect names of instructions and zone pointers.

- [tt\_instructing\_glyphs](https://learn.microsoft.com/en-us/typography/opentype/otspec190/tt_instructing_glyphs)

  - Added clarification regarding unused distance type 3.

- [tt\_instructions](https://learn.microsoft.com/en-us/typography/opentype/otspec190/tt_instructions) Clarified that FDEF and IDEF must not be invoked in glyph programs.

- [ttch01](https://learn.microsoft.com/en-us/typography/opentype/otspec190/ttch01)

  - Clarified when the interpreter stack is cleared.
  - Clarified where functions and instructions can or cannot be defined or redefined, and the persistence of definitions.
  - Clarified when the control value program is run and the relationship between the control value program, Control Value Table, and the 'cvt ' table.
  - Clarified interaction between the control value program and Graphics State variables.
  - Clarified interactions between zone 0 and the control value and glyph programs.
  - Clarified use of the storage area by font, control value and glyph programs.
  - Added section discussing persistence of storage or CVT values set in a glyph program and interaction with glyph caches.
  - Clarified control of the scan converter mode using SCANCTRL.

- [vvar](https://learn.microsoft.com/en-us/typography/opentype/otspec190/vvar)

  - For description of the DeltaSetIndexMap, changed the cross-reference from the HVAR chapter to the OpenType Font Variations Common Table Formats chapter.

<a id="anchor-changes-version-184"></a>

## Version 1.8.4

Released November 2020

Names of tables, fields or flags in the following chapters were revised to conform to conventions used across this specification:

- [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/base), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/chapter2), [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cmap), [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/colr), [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cpal), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dsig), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/eblc), [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gdef), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gsub), [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/head), [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/jstf), [kern.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/kern), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/math), [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/name), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otvarcommonformats), [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/svg), [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vdmx).

These name changes are enumerated in detail below.

References to “TrueType”, when this specification is intended, have been removed, changed to “OpenType”, or otherwise clarified in the following chapters: [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/chapter2), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dsig), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/hvar), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otff), [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/post), [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/recom), [ttch01.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/ttch01), [vmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vmtx), [vorg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vorg).

Minor editorial changes (not detailed below) were made in the following chapters: [avar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/avar), [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/base), [baselinetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/baselinetags), [cff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cff), [cff2charstr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cff2charstr), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/chapter2), [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cmap), [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/colr), [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cpal), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dsig), [dvaraxistag\_ital.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dvaraxistag_ital), [dvaraxistag\_opsz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dvaraxistag_opsz), [dvaraxistag\_slnt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dvaraxistag_slnt), [dvaraxistag\_wdth.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dvaraxistag_wdth), [dvaraxistag\_wght.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dvaraxistag_wght), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/eblc), [featurelist.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/featurelist), [features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_ae), [features\_fj.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_fj), [features\_ko.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_ko), [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_pt), [features\_uz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_uz), [featuretags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/featuretags), [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gdef), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gsub), [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gvar), [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/hdmx), [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/head), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/hvar), [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/), [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/languagetags), [ltsh.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/ltsh), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/math), [meta.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/meta), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otvarcommonformats), [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/post), [scripttags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/scripttags), [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/stat), [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/svg), [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/tt_instructing_glyphs), [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/tt_instructions), [ttch01.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/ttch01), [ttochap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/ttochap1), [ttoreg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/ttoreg), [vhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vhea), [vmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vmtx), [vorg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vorg), [vvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vvar).

*Summary of changes:*

- [avar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/avar)

  - Moved description of normalization process and example into [otvaroverview.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otvaroverview).

- [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/base)

  - Changed field names:

    - BaseValues table: “baseCoords” to “baseCoordOffsets”
    - MinMax and FeatMinMax tables: “minCoord” to “minCoordOffset”
    - MinMax and FeatMinMax tables: “maxCoord” to “maxCoordOffset”
    - BaseCoordFormat3: “deviceTable” to “deviceOffset”

- [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cbdt)

  - Added descriptions of fields for BigGlyphMetrics, SmallGlyphMetrics.
  - Changed characterization of BitmapSize from table to record.

- [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cblc)

  - Changed characterization of BitmapSize from table to record.
  - Revised description of CBLC header to incorporate BitmapSize records array.

- [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cff2)

  - Added note to description of FDSelect Format 3 regarding the maximum glyph ID of 65534.

- cffspec.htm

  - Page removed. (The page only provided an external link, already in cff.htm.)

- [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/chapter2)

  - Changed table name: “ConditionTableFormat1” to “ConditionFormat1” (table).

  - Changed field names:

    - Script table: “defaultLangSys” to “defaultLangSysOffset”
    - LangSys table: “lookupOrder” to “lookupOrderOffset”
    - Feature table: “featureParams” to “featureParamsOffset”
    - LookupList table: “lookups” to “lookupOffsets”
    - ConditionSet Table: “conditions” to “conditionOffsets”
    - FeatureTableSubstitutionRecord: “alternateFeatureTable” to “alternateFeatureOffset”

  - Changed LookupFlag names:

    - “rightToLeft” to “RIGHT\_TO\_LEFT”
    - “ignoreBaseGlyphs” to “IGNORE\_BASE\_GLYPHS”
    - “ignoreLigatures” to “IGNORE\_LIGATURES”
    - “ignoreMarks” to “IGNORE\_MARKS”
    - “useMarkFilteringSet” to “USE\_MARK\_FILTERING\_SET”
    - “markAttachmentType” to “MARK\_ATTACHMENT\_TYPE\_MASK”

  - Added common formats for use in the GSUB and GPOS tables, replacing formats in GSUB and GPOS chapters that were identical but with different names:

    - SequenceContextFormat1, SequenceContextFormat2, SequenceContextFormat3, and associated subtables (replacing ContextSubstFormat1/ContextPosFormat1, etc.)
    - ChainedSequenceContextFormat1, ChainedSequenceContextFormat2, ChainedSequenceContextFormat3, and associated subtables (replacing ChainContextSubstFormat1/ChainContextPosFormat1, etc.)
    - SequenceLookupRecord (replacing SubstLookupRecord/PosLookupRecord)

  - Replaced Figure 2b with a clearer illustration of language system differences.

  - Clarified optionality of features not referenced by the requiredFeatureIndex field of the LangSys table.

  - Added note regarding GSUB features being processed by applications in stages.

  - Added clarification regarding FeatureParams tables.

  - Added clarification regarding general lookup processing, and regarding filtering lookup flags in relation to the first glyph in input sequences.

  - In relation to contextual lookup types, added clarification regarding lookup flags in the main lookup table and in nested lookup tables.

  - Corrected reference to GPOS type 8 lookups (post-release erratum).

  - Corrected errors in data for Example 3.

- charstr2.htm

  - Page removed. (The page only provided an external link, already in cff.htm.)

- [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cmap)

  - Changed field names:

    - EncodingRecord: “offset” to “subtableOffset”
    - Format 2 subtable: “glyphIndexArray” to “glyphIdArray”
    - Format 4 subtable: “idRangeOffset” to “idRangeOffsets”
    - Format 10 subtable: “glyphs” to “glyphIdArray”

  - Added clarification regarding use of different formats.

  - Added clarification regarding subtables being used exclusively.

  - Changed guidance regarding the Macinthosh platform.

  - Added details regarding the Unicode and ISO platforms (moved from the 'name' chapter).

  - Revised description of encodings for the Windows platform.

  - Revised description of the “Custom” platform (ID 4).

  - Revised descriptions for formats 0, 2, 4, 6, 8, 10, 12, 14.

  - In description of format 4, provided details regarding purpose of searchRange, entrySelector and rangeShift fields as well as recommendations for fonts and parsing. Also corrected glyph mapping example.

  - Corrected description of the entrySelector field (post-release erratum, correction back-ported from version 1.9).

- [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/colr)

  - In BaseGlyphRecord and LayerRecord, changed field names “gID” to “glyphId”.
  - Changed general requirement regarding glyph ID 1 to a compatibility note.

- [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/cpal)

  - Changed field names:

    - “offsetFirstColorRecord” to “colorRecordsArrayOffset”
    - “offsetPaletteTypeArray” to “paletteTypesArrayOffset”
    - “offsetPaletteLabelArray” to “paletteLabelsArrayOffset”
    - “offsetPaletteEntryLabelArray” to “paletteEntryLabelsArrayOffset”

  - Clarified use of sRGB.

  - Clarified meaning of alpha values.

  - In the section on SVG and CPAL, replaced “context-fill” and “context-fill-opacity” with “currentColor”.

- [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dsig)

  - In SignatureRecord, changed field name “offset” to “signatureBlockOffset”.
  - Corrected references for PKCS #7, PKCS #9.
  - Corrected the steps for creating a DSIG table, and clarified steps for creating a DSIG table for a TTC.
  - Removed erroneous reference to DSIG checksum field.

- [dvaraxistag\_opsz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/dvaraxistag_opsz)

  - Revised description for the Optical size axis.

- [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/ebdt)

  - Added descriptions of fields for BigGlyphMetrics, SmallGlyphMetrics.
  - Changed characterization of BitmapSize from table to record.

- [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/eblc)

  - Changed field names:

    - IndexSubtable1 and IndexSubtable3: “offsetArray” to “sbitOffsets”
    - GlyphIDOffsetPair record: “offset” to “sbitOffset”

  - Changed characterization of BitmapSize from table to record.

  - Revised description of EBLC header to incorporate BitmapSize records array.

  - Added descriptions of fields for BigGlyphMetrics, SmallGlyphMetrics.

- [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/ebsc)

  - Changed characterization of BitmapSize from table to record.

- euro.htm

  - Removed file. (Content not part of the font format specification, available elsewhere.)

- [featurelist.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/featurelist)

  - Added features 'chws', 'vchw'.

- [features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_ae)

  - Added 'chws' feature description.
  - Modified feature descriptions: 'aalt', 'abvf', 'abvm', 'abvs', 'afrc', 'akhn', 'blwf', 'blwm', 'blws', 'calt', 'case', 'ccmp', 'cfar', 'cjct', 'clig', 'cpct', 'cpsp', 'cswh', 'curs', 'cv01' – 'cv99', 'c2pc', 'c2sc', 'dist', 'dlig', 'dnom', 'dtls', 'expt'.

- [features\_fj.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_fj)

  - Modified feature descriptions: 'falt', 'fin2', 'fin3', 'fina', 'flac', 'frac', 'fwid', 'half', 'haln', 'halt', 'hist', 'hkna', 'hlig', 'hngl', 'hoji', 'hwid', 'init', 'isol', 'ital', 'jalt', 'jp78', 'jp83', 'jp90', 'jp04'.

- [features\_ko.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_ko)

  - Deprecated 'opbd' feature.
  - Modified feature descriptions: 'kern', 'lfbd', 'liga', 'ljmo', 'lnum', 'locl', 'ltra', 'ltrm', 'mark', 'med2', 'medi', 'mgrk', 'mkmk', 'mset', 'nalt', 'nlck', 'nukt', 'numr', 'onum', 'opbd', 'ordn', 'ornm'.

- [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_pt)

  - Modified feature descriptions: 'palt', 'pcap', 'pkna', 'pnum', 'pref', 'pres', 'pstf', 'psts', 'pwid', 'qwid', 'rand', 'rclt', 'rkrf', 'rlig', 'rphf', 'rtbd', 'rtla', 'rtlm', 'ruby', 'rvrn', 'salt', 'sinf', 'smcp', 'smpl', 'ss01' – 'ss20', 'ssty', 'stch', 'subs', 'sups', 'swsh', 'titl', 'tjmo', 'tnam', 'tnum', 'trad', 'twid'

- [features\_uz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/features_uz)

  - Added 'vchw' feature description.
  - Modified feature descriptions: 'unic', 'valt', 'vatu', 'vert', 'vhal', 'vjmo', 'vkna', 'vkrn', 'vpal', 'vrt2', 'vrtr', 'zero'.

- [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/fvar)

  - Moved recommendation regarding postScriptNameID to Recommendations.

- [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gasp)

  - Clarified version 0 versus version 1.

- [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gdef)

  - Changed table name: “MarkGlyphSetsTable” to “MarkGlyphSets” (table).
  - Changed field name in MarkGlyphSets table: “markGlyphSetsTableFormat” to “format”.

- [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/glyf)

  - Added clarification regarding the number of points in a simple glyph description.
  - Clarified descriptions of xMin, yMin, xMax, yMax.

- [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gpos)

  - In BaseRecord, changed field name “baseAnchorOffset” to “baseAnchorOffsets”.

  - Removed GPOS-specific formats that were identical to formats in GSUB but with different names, replaced by common formats shared between GSUB and GPOS, described in [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/chapter2):

    - ContextPosFormat1, ContextPosFormat2, ContextPosFormat3, and associated subtables (replaced by SequenceContextFormat1, etc.)
    - ChainContextPosFormat1, ChainContextPosFormat2, ChainContextPosFormat3, and associated subtables (replaced by ChainedSequenceContextFormat1, etc.)
    - PosLookupRecord (replaced by SequenceLookupRecord)

  - In section on position lookup records, added note regarding lookup flags in a main lookup table and in nested lookup tables.

- [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/gpos)

  - Removed GSUB-specific formats that were identical to formats in GPOS but with different names, replaced by common formats shared between GSUB and GPOS, described in [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/chapter2):

    - ContextSubstFormat1, ContextSubstFormat2, ContextSubstFormat3, and associated subtables (replaced by SequenceContextFormat1, etc.)
    - ChainContextSubstFormat1, ChainContextSubstFormat2, ChainContextSubstFormat3, and associated subtables (replaced by ChainedSequenceContextFormat1, etc.)
    - SubstLookupRecord (replaced by SequenceLookupRecord)

- [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/hdmx)

  - Changed data types for numRecords, sizeDeviceRecord to unsigned types.

- [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/head)

  - Changed field name: “checkSumAdjustment” to “checksumAdjustment”.
  - Added recommendation regarding flags bit 3 in hinted fonts.
  - Clarified descriptions for xMin, yMin, xMax, yMax.

- [hhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/hhea)

  - Clarified descriptions for minLeftSideBearing, minRightSideBearing.
  - Revised note regarding the ascender, descender and linegap fields.

- [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/hmtx)

  - Clarified wording regarding the hMetrics and leftSideBearings arrays.
  - Clarified the left side bearing value that should be specified for empty glyphs.

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/)

  - Updated version number and reference to ISO/IEC 14496-22.
  - Removed reference to the WGL4.0 character set.
  - Incorporated links to ttch01.htm, tt\_instructing\_glyphs.htm, tt\_instructions.htm, tt\_graphics\_state.htm.
  - Changed links for Adobe Technical Notes #5176, #5177 to be direct, external links, not to cffspec, charstr2 pages.

- [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/jstf)

  - Changed field names in JstfPriority table:

    - “shrinkageEnableGSUB” to “gsubShrinkageEnableOffset”
    - “shrinkageDisableGSUB” to “gsubShrinkageDisableOffset”
    - “shrinkageEnableGPOS” to “gposShrinkageEnableOffset”
    - “shrinkageDisableGPOS” to “gposShrinkageDisableOffset”
    - “shrinkageJstfMax” to “shrinkageJstfMaxOffset”
    - “extensionEnableGSUB” to “gsubExtensionEnableOffset”
    - “extensionDisableGSUB” to “gsubExtensionDisableOffset”
    - “extensionEnableGPOS” to “gposExtensionEnableOffset”
    - “extensionDisableGPOS” to “gposExtensionDisableOffset”
    - “extensionJstfMax” to “extensionJstfMaxOffset”

- [kern.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/kern)

  - In Format 2, changed field names:

    - “leftClassTable” to “leftClassOffset”
    - “rightClassTable” to “rightClassOffset”
    - “array” to “kerningArrayOffset”

- [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/languagetags)

  - Added note clarifying ISO 639 identifiers that may be listed for a given language system tag.
  - Added note about permanent reservation of 'dflt', 'DFLT'.
  - Revised details regarding ISO 639 mappings for language system tags 'AKA ', 'ATH ', 'BAD0', 'BER ', 'BML ', 'CPP ', 'FNE ', 'HAL ', 'IJO ', 'KOH ', 'KRN ', 'MYN ', 'NAH ', 'QIN ', 'SLA ', 'SRB ', 'TMH ', 'TNE ', 'TWI ', 'YCR '.
  - Corrections to show full tags 'HO  ', 'WA  '.
  - Revised descriptions for 'DGO ', 'DGR ', 'ZHH ', 'ZHTM'.
  - Added: 'AKB ', 'BTD ', 'BTK ', 'BTM ', 'BTX ', 'BTZ ', ZHTM.
  - Added 'DAG ' (post-release update).
  - Added 'AVN ', 'KAW ', 'LEF ', 'WCI ' (post-release update).
  - Added 'CTT ', 'HAI0', 'HEI ', 'HMD ', 'HMZ ', 'IRU ', 'KWK ', 'LPO ', 'RHG ', 'SFM ', 'TLI ', 'XUB ', 'XUJ ', 'YGP ', 'YNA ', 'YWQ ' (post-release update).
  - Revised ISO 639 mapping details for 'SXT ' (post-release update.)

- [loca.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/loca)

  - Revised recommended for local offsets to be word aligned.

- [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/math)

  - Changed field name in MathValueRecord: “deviceTableOffset” to “deviceOffset”.
  - Changed flag name “fExtender” to “EXTENDER\_FLAG”.
  - For fields that are values in design grid units, changed data types from int16 to FWORD, and from uint16 to UFWORD.
  - Clarified meaning of “shift” in MathConstants fields.
  - Clarified default rule thickness.
  - Added clarification of suggested value for spaceAfterScript.
  - Added suggested value for radicalKernAfterDegree.

- [maxp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/maxp)

  - Changed type for the version field from Fixed to Version16Dot16.

- [meta.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/meta)

  - Corrected description of example Hant-HK.

- [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/name)

  - Changed field names:

    - Header: “format” to “version”
    - Version 0 and version 1 headers: “stringOffset” to “storageOffset”
    - LangTagRecord: “offset” to “langTagOffset”
    - NameRecord: “offset” to “stringOffset”

  - Re-organized content to move tables of platform, encoding and language IDs to the end of the chapter. Also removed details relevant only to the 'cmap' table.

  - Updated language and region strings for Windows language ID 042F.

  - Changed the language name for Windows language ID 081D to “Swedish”.

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/os2)

  - Corrected details for Unicode range fields regarding bit 92 and versions 3, 4.

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otff)

  - Changed field names:

    - In TableRecord: “checkSum” to “checksum”.
    - In TTC Header version 1.0 and version 2.0: “offsetTable” to “tableDirectoryOffsets”.

  - Clarified that LONGDATETIME values are in UTC time.

  - Defined a Version16Dot16 type (replacing Fixed used for table version).

  - Clarified use of “record” and “table” in describing defined structures.

  - Clarifed statement regarding file extensions.

  - Removed historic reference to Multiple Master support being discontinued. (Details are retained in the change log.)

  - Revised terminology, removing use of “offset table” and making consistent use of “table directory”.

  - Re-organized description of TableDirectory and TableRecord array, adding tableRecords\[\] as a member in TableDirectory.

  - Provided details regarding purpose of searchRange, entrySelector and rangeShift fields as well as recommendations for fonts and parsing.

  - Moved statement of the requirement for four-byte table offsets to follow description of table records.

  - Clarified checksum calculation for tables with length not a multiple of four.

  - Clarified calculation of the 'head' table checksum and checksumAdjustment, and checksums in collection files.

  - Clarified location of DSIG table within a TTC file.

  - Added clarifications regarding custom, vendor-defined tags.

- [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otvarcommonformats)

  - Changed field name in DeltaSet record: “DeltaData” to “deltaData”.
  - Added text defining special meaning of delta-set outer- and inner-level indices 0xFFFF/0xFFFF as an indication of no variation data.
  - Added constraint on VariationRegionList.regionCount to be less than 32,768 (high bit reserved).
  - Added note regarding NULL offsets in the itemVariationDataOffsets array.
  - In DeltaSet record, revised description of deltaSet array to indicate number of elements in array, not byte length.

- [otvaroverview.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/otvaroverview)

  - Moved description of normalization process and example from [avar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/avar) into this chapter.

- [overview.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/overview)

  - Complete re-write of the overview content.

- [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/pclt)

  - Revised member names to use camel case.
  - Clarified note on discouraged usage.

- [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/post)

  - Changed type for the version field from Fixed to Version16Dot16.
  - Clarified the description of version 2.0; this includes changing the type and field name for the string data.
  - Clarified encoding of name strings and moved requirements from Recommendations to here.

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/recom)

  - Removed byte ordering and 'OS/2' sections.
  - Revised the table alignment section.
  - Revised the 'cmap' recommendations.
  - Added 'fvar' section with recommendation regarding postScriptNameID.
  - 'name' section: Revised guidance regarding names for the Macintosh platform.
  - 'post' section: Moved name string requirements to 'post' table chapter. Removed redundant and obsolete recommendations.

- [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/sbix)

  - Revised descriptions of originOffsetX, originOffsetY, and provided clarification regarding positioning of the bitmap graphic.

- [scripttags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/scripttags)

  - Added script tags for new scripts in Unicode 12 and Unicode 13.
  - Corrected script tag for Yi. (Post-release erratum.)

- [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/stat)

  - Relaxed constraint on name IDs used for AxisRecord.axisNameID.
  - Revised constraints and recommendations regarding separate axis value tables having the same information.
  - For AxisValueFormat2, clarified details regarding touching and overlapping ranges.
  - For AxisValueFormat4, clarified precedence when two tables are partial matches, and clarified the axis ordering to be assumed .
  - Adopted consistent spelling for flag names: OLDER\_SIBLING\_FONT\_ATTRIBUTE and ELIDABLE\_AXIS\_VALUE\_NAME.
  - Revised chapter for greater clarity.

- [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/svg)

  - Changed field name “offsetToSVGDocumentList” to “svgDocumentListOffset”.
  - Clarified note regarding glyph advances not changing due to animations.

- [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/tt_graphics_state)

  - Corrected the list of instructions affected by single\_width\_cut\_in and single\_width\_value, and clarified the units for single\_width\_value.

- [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/tt_instructing_glyphs)

  - Removed incorrect statement regarding single\_width\_cut\_in applying to indirect instructions.

- [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/tt_instructions)

  - Corrected figures illustrating stack operations for JROF.
  - Correction in details for SDPVTL.
  - Corrected figures for SFVFS, SZP1, SMD, ALIGNRP, GC.
  - Clarified ISECT and corrected figure.
  - Clarified units for SSW.

- ttinst.htm

  - Removed file: links to child pages incorporated into index.htm; introductory paragraph incorporated into ttch01.htm.

- [ttochap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/ttochap1)

  - Replaced Figure 1h with a clearer illustration of language system differences.
  - Consolidated “TrueType versus OpenType Layout” section into the “OpenType Layout at a glance” section.

- [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vdmx)

  - In VDMX header, changed field name “offset” to “vdmxGroupOffsets”.

- [vhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec184/vhea)

  - Clarified scope of usage for the table.
  - Changed type for the version field from Fixed to Version16Dot16.
  - Revised descriptions of vertTypoAscender, vertTypoDescender.

- wgl4.htm, wgl4b.htm, wgl4c.htm, wgl4d.htm, wgl4e.htm

  - Removed files. (Content was not part of the font format specification; it remains available elsewhere.)

<a id="anchor-changes-version-183"></a>

## Version 1.8.3

Released August 2018

Minor editorial changes were made in the following chapters: [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/base), [baselinetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/baselinetags), [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cbdt), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cblc), [cff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cff), [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cff2), [cff2charstr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cff2charstr), [changes.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/changes), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/chapter2), [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cmap), [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/colr), [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cpal), [cvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cvar), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/dsig), [dvaraxisreg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/dvaraxisreg), [dvaraxistag\_ital.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/dvaraxistag_ital), [dvaraxistag\_opsz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/dvaraxistag_opsz), [dvaraxistag\_slnt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/dvaraxistag_slnt), [dvaraxistag\_wdth.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/dvaraxistag_wdth), [dvaraxistag\_wght.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/dvaraxistag_wght), [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ebdt), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/eblc), [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ebsc), [featurelist.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/featurelist), [features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/features_ae), [features\_fj.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/features_fj), [features\_ko.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/features_ko), [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/features_pt), [features\_uz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/features_uz), [featuretags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/featuretags), [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/fvar), [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/gasp), [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/gdef), [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/glyf), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/gsub), [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/gvar), [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/hdmx), [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/head), [hhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/hhea), [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/hmtx), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/hvar), [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/), [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/jstf), [kern.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/kern), [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/languagetags), [ltsh.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ltsh), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/math), [merg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/merg), [meta.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/meta), [mvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/mvar), [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/name), [namesmp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/namesmp), [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/os2), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/otvarcommonformats), [otvaroverview.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/otvaroverview), [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/pclt), [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/post), [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/recom), [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/sbix), [scripttags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/scripttags), [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/stat), [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/svg), [ttch01.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ttch01), [ttochap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ttochap1), [ttoreg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ttoreg), [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/vdmx), [vhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/vhea), [vmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/vmtx), [vorg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/vorg), [vvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/vvar).

The editorial changes include applying a convention for tag values: single, straight quotation marks are used for lowercase tags; they are not used for uppercase tags except when extra clarification is required, such as when a tag has trailing spaces; and marks are not when a tag is used like an object name, as in “head.macStyle”, or when used like a function name, as in “cmap(j)”.

In the summary of changes below, details given above are not repeated.

*Summary of Changes:*

- [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/base)

  - Corrected figure 5c.

- [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cmap)

  - Corrected field names for format 4.
  - Eliminated outdated references to “UCS-2” and “UCS-4”.
  - Added comments regarding use of formats 8, 10.
  - Corrected typo in glyphId index value equation from “startCount” to “startCode”.

- [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/cff2)

  - Revised name of operand for blend operator.
  - Corrected max number of glyphs supported by FDSelect Format 3 from 65536 to 65536. (Post-release erratum.)

- [changes.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/changes)

  - Re-organized how systemic and minor editorial changes are recorded for Version 1.8.1.
  - Removed reference to proposals.htm (this legacy page was a companion to this specification but not part of it).
  - Replaced references to default.htm (no longer used) with index.htm.
  - Added missing change to ttinst1.doc in OpenType 1.5. (Post-release erratum.)

- [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/chapter2)

  - Corrected the number of GSUB lookup types (eight).
  - Clarifed description of Coverage Indexes for Coverage Format 2.

- [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/dsig)

  - Revised statments regarding anticipated use of signatures.

- [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ebdt)

  - Corrected text typo from “EDBT” to “EBDT” in the Header.

- [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/eblc)

  - Corrected text typo from “EDBT” to “EBDT” in the first paragraph.
  - Corrected text from “16-bit alignment” to “32-bit alignment”.

- [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ebsc)

  - Corrected text typo from “EBLC” to “EBSC” in “EBSC Header”.

- [features\_ko.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/features_ko)

  - Corrected description for 'med2'.

- [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/features_pt)

  - Corrected example for 'ssty'. (Post-release erratum.)
  - Corrected Tag: 'ssty'. (Post-release erratum.)

- [featuretags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/featuretags)

  - Revised comments on implementation of 'init' feature for Arabic text for consistency with description of the 'init' feature.

- [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/gdef)

  - Revised field names in MarkGlyphSetsTable format to conform to conventions.

- [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/glyf)

  - Clarified the description of simple glyph flags.
  - Added the OVERLAP\_SIMPLE flag.
  - Corrected statement regarding numberOfContours for simple glyph descriptions. (Post-release erratum.)

- [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/gpos)

  - Corrected description of the offset to Device / VariationIndex tables within ValueRecord.
  - Clarified placement and advance effects of lookup types 1 – 6.

- grstate.doc

  - Content ported into Web page: [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/tt_graphics_state).

- [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/gsub)

  - For Single Substitition Format 1, indicated that addition is modulo 65536.
  - Corrected error in example 7: DashAndSpaceSubRuleSet is at offset SubRuleSet\[1\].

- [hhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/hhea)

  - Removed references to historic platforms.

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/)

  - Updated version number and reference to ISO/IEC 14496-22.
  - Removed mention of Microsoft Word documents.

- instgly.doc

  - Content ported into Web page: [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/tt_instructing_glyphs).

- [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/jstf)

  - Revised field name, jsftLangSysOffset, to follow conventions.

- [kern.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/kern)

  - Removed references to historic platforms.

- [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/languagetags)

  - Added 'KJZ ', 'MFA ', 'TSJ ', 'XKF '.
  - Added additional ISO 639 mappings.

- [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/math)

  - Revised descriptions for better clarity.
  - Re-ordered content in section on MathKernInfo table for better clarity.
  - In description of formats for MathItalicsCorrectionInfo, MathTopAccentAttachment, MathKernInfo and MathVariants, clarified that the count fields must be the same as the number of glyph IDs referenced in the Coverage tables.
  - Revised structure and field names to follow conventions.

- [maxp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/maxp)

  - Clarified maxStackElements.

- [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/name)

  - Replaced obsolete recommendation to have Macintosh strings for legacy version-control implementations with advisory that apps might display incorrect strings.
  - Added link to BCP 47.
  - Eliminated outdated references to “UCS-2” and “UCS-4”.
  - Corrected Macintosh platform language ID for Inuktitut; corrected typos (Quechua, Tagalog).
  - In the table for the Platform ID enumeration, corrected the description for language IDs for Platform ID 0 (error introduced in version 1.5).
  - Revised descriptions for name IDs 1 and 2.

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/os2)

  - Incorporated relevant information regarding OS/2 versions 0 to 4. (Separate pages removed.)
  - Added note regarding truncated version 0 definition in Apple’s TrueType Reference Manual.
  - Corrected units for xAvgCharWidth.
  - fsType: Clarified “embedding”; revised presentation of flags; noted that bit 0 is *permanently* reserved.
  - yStrikeoutSize, yStrikeoutPosition: Removed legacy statements intended for bitmap fonts; added reference to post.underlineThickness.
  - panose: Clarified the contingent meaning of bytes other than the first byte.
  - ulUnicodeRange: Eliminated outdated references to “UCS-2” and “UCS-4”; added note that available bits are exhausted, and reference to 'dlng' and 'slng' tags in the 'meta' table; clarified some issues for early OS/2 versions.
  - achVendID: Revised description.
  - sTypoAscender, sTypoDescender, sTypoLineGap: Revised descriptions; clarified the *non-*requirement that sTypoAscender - sTypoDescender equal unitsPerEm.
  - usWinAscent, usWinDescent: Revised description; clarified clipping behavior in Windows GDI, and added note regarding interaction with VDMX.
  - Added more information about setting default line metric values in variable fonts, and varying line metric values in variable fonts.
  - Added more information about setting usLowerOpticalPointSize and usUpperOpticalPointSize values in variable fonts.

- os2ver0.htm, os2ver1.htm, os2ver2.htm, os2ver3.htm, os2ver4.htm

  - Pages removed; relevant content integrated into os2.htm.

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/otff)

  - Added .TTC and .OTC to cited filename extensions, and removed recommendation details, which are already provided in the Recommendations chapter.
  - Added table and design-variation axis to items identified using Tag.
  - Moved the specification for valid Tag values from the Table Record description into the data types section.
  - Made clarifications regarding representations of version numbers
  - Changed the data type for the first member of the Table Record to Tag, and changed the member name and description.
  - For underlineThickness, added reference to OS/2.strikeoutSize.

- [otvaroverview.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/otvaroverview)

  - Corrected the arithmetic details in the last part of the example in the Interpolation Example section.
  - Corrected typo “wiht” to “with” in “Coordinate Scales and Normalization”.

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/recom)

  - Added filename recommendation related to CFF and revised wording related to font collections.
  - Eliminated outdated references to “UCS-2”, “UCS-4” and legacy products in 'cmap' section.
  - Removed obsolete guidance for use of 'vrt2' feature in CJK fonts.

- [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/stat)

  - Revised the introduction to Axis Value Tables for better clarity.
  - Corrected typo changing “appliations” to “applications”.

- [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/svg)

  - Revised organization and descriptive text for better clarity.
  - Revised structure names to follow conventions.
  - Prohibited use of “HTML dialect” SVG documents.
  - Restricted usage of XML namespace declarations.
  - Limited capabilities to SVG 1.1. Deprecated use of context-\* properties from SVG2 (support was required in earlier versions).
  - Added section detailing SVG 1.1 capability requirements and restrictions. (Several capabilities not clearly discussed in earlier versions are now discouraged or not supported.)
  - Clarified use of CSS custom properties and integration of CPAL, including interpretation of CPAL alpha values.
  - Added use of currentColor (supersedes use of context-fill, context-stroke).
  - Clarified relationship of coordinate system and viewport to glyph design grid, and also viewport clip behavior.
  - Removed references to “user agent style sheets”.
  - Removed section on security considerations and glyph rendering restrictions (superseded by the added section on SVG 1.1 capability requirements and restrictions).
  - Added Example 1.
  - Revised Example 5, replacing context-fill with currentColor.

- [ttinst.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ttinst)

  - Revised links to refer to content ported from Microsoft Word files to Web pages. (Post-release update, August 2018.)

- ttinst1.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/tt_instructions). (Post-release update, August 2018.)

- ttinst2.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/tt_instructions). (Post-release update, August 2018.)

- [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/tt_instructions)

  - Corrected MIRP Code range to 0xE0 - 0xFF.
  - Corrected errors introducted when porting from Word documents (some changes from earlier versions were not retained). (Post-release erratum.)
  - Changed “NPUSHB” to “NPUSHW” in GETVARIATION. (Post-release erratum.)
  - Corrected error in “FLIPRGOFF” regarding on-curve versus off-curve points. (Post-release erratum.)
  - Removed extra, incorrect uses from “IUP”. (Post-release erratum.)
  - Corrected text in GETVARIATION\[\] normalized coordinates. (Post-release erratum.)
  - Corrected error in code range of MIRP inadvertently introduced when porting from Word documents. (Post-release erratum.)
  - Corrected error in description of “logical OR” inadvertently added when porting from Word documents. (Post-release erratum.)
  - Removed incorrect text inadvertently added to description of Round to Half Grid (RTHG) when porting from Word documents. (Post-release erratum.)

- [ttochap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/ttochap1)

  - Fixed typo in image (fig1i.gif).

- [vhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec183/vhea)

  - Made corrections to the description for vertTypoDescender.

<a id="anchor-changes-version-182"></a>

## Version 1.8.2

Released July 2017.

Many editorial changes have been made, including revision of structure and field names in several chapters to conform to conventions used across this specification. Such changes were made in the following chapters:

- Revision of structure or field names: [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/base), [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cff2), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/chapter2), [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/colr), [cvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cvar), [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/ebdt), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/eblc), [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/ebsc), [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/fvar), [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gasp), [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gdef), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gsub), [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gvar), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/hvar), [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/jstf), [merg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/merg), [mvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/mvar), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/otvarcommonformats), [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/sbix), [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/stat), [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/svg), [vvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/vvar).

A significant editorial change pertains to documentation of design-variation axes and axis tags: previously, these were documented within the ['fvar'](https://learn.microsoft.com/en-us/typography/opentype/otspec182/fvar) table chapter. The axis tags are also used in other tables, however, and may be relevant for non-variable fonts. Also, the set of registered axes may grow over time. Hence, documentation of axes and axis tags has been moved to a separate section, [OpenType Design-Variation Axis Tag Registry](https://learn.microsoft.com/en-us/typography/opentype/otspec182/dvaraxisreg).

Minor editorial changes were made in the following chapters: [avar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/avar), [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/base), [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cbdt), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cblc), [cff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cff), [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cff2), [cff2charstr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cff2charstr), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/chapter2), [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cmap), [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/colr), [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cpal), [cvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cvar), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/dsig), [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/ebdt), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/eblc), [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/ebsc), [features\_fj.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/features_fj), [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/fvar), [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gasp), [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gdef), [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/glyf), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gsub), [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gvar), [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/hdmx), [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/head), [hhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/hhea), [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/hmtx), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/hvar), [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/jstf), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/math), [maxp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/maxp), [merg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/merg), [mvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/mvar), [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/os2), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/otvarcommonformats), [otvaroverview.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/otvaroverview), [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/post), [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/sbix), [scripttags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/scripttags), [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/stat), [vvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/vvar), [wgl4b.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/wgl4b).

In the summary of changes below, details given above are not repeated.

*Summary of Changes:*

- [avar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/avar)

  - Clarified requirements on AxisValueMap records within a SegmentMap.

- [cff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cff)

  - Added note about Name INDEX entry, name ID 6 and collections.

- [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cff2)

  - In Top DICT (section 7), indicated that FontMatrix operator is required only if head.unitsPerEm does not equal 1000, and limited the FontMatrix operand array values. Also deprecated use of FontMatrix operator in Font DICTs (section 10 and Appendix C).
  - Corrected description of blend and vsindex operators (section 8).
  - Corrected description of operands for the Private operator (section 10).
  - Corrected error in numeric range of reserved two-byte DICT operators (Appendix C).
  - Removed the maxstack operator.

- [cff2charstr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cff2charstr)

  - In 3.2, CharString Number Encoding, corrected the described range of values represented for byte values 251 to 254.
  - Revised argument stack limit in Appendix B to 513, and removed reference to maxstack operator.

- [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/chapter2)

  - Relaxed constraint on DFLT script table and LangSysCount.

- [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/cmap)

  - Clarified description for defaultUVSOffset and nonDefaultUVSOffset.
  - Re-organized introductory paragraphs and details on platform/encoding IDs.

- [dvaraxisreg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/dvaraxisreg)

  - Created new page.

- [dvaraxistag\_ital.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/dvaraxistag_ital)

  - Created new page.

- [dvaraxistag\_opsz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/dvaraxistag_opsz)

  - Created new page.

- [dvaraxistag\_slnt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/dvaraxistag_slnt)

  - Created new page.

- [dvaraxistag\_wdth.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/dvaraxistag_wdth)

  - Created new page.

- [dvaraxistag\_wght.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/dvaraxistag_wght)

  - Created new page.

- [features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/features_ae)

  - Revised 'ccmp' feature description.

- [features\_ko.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/features_ko)

  - Corrected the friendly name for the 'med2' feature.

- [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/fvar)

  - Added a new flag definition for VariationAxisRecord.
  - Removed Variation Axis Tags section and made reference instead to OpenType Design-Variation Axis Tag Registry page.

- [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gasp)

  - Revised documentation of behavior flags, and indicated that reserved bits must be set to zero.

- [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/glyf)

  - Added clarifying information about table organization, side bearings, point numbers, scale for coordinate values, packed representation of flags and coordinates in simple glyph descriptions, and the SCALED\_COMPONENT\_OFFSET and UNSCALED\_COMPONENT\_OFFSET composite glyph flags.
  - Clarified use of negative numberOfContours values to indicate composite glyphs, and the recommendation that -1 be used.
  - Revised documentation of flags, and indicated that reserved bits must be set to zero.

- grstate.doc

  - Content ported into Web page: [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/tt_graphics_state). (Post-release update, August 2018.)

- [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/gvar)

  - Amend the algorithm for inferring deltas of un-referenced points to avoid division by zero and to completely cover possible cases.

- [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/hmtx)

  - Revise errors in the informative description.

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/)

  - Version update.
  - Added link to OpenType Design-Variation Axis Tag Registry page.
  - Removed mention of Microsoft Word documents. (Post-release update, August 2018.)

- instgly.doc

  - Content ported into Web page: [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/tt_instructing_glyphs). (Post-release update, August 2018.)

- [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/languagetags)

  - Added CCHN.

- [meta.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/meta)

  - Corrected the format of the table version (post-release erratum).

- [mvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/mvar)

  - Changed reference for variation axis tags from 'fvar' chapter to OpenType Design-Variation Axis Tag Registry page.

- [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/name)

  - Clarified that the string data referenced by 3/1 or 3/0 name records must be encoded in UTF-16BE.
  - Revised descriptions for name IDs 1, 2 and 4, and also the paragraph describing key names for Microsoft platforms.

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/os2)

  - Changed reference for variation axis tags from 'fvar' chapter to OpenType Design-Variation Axis Tag Registry page.
  - Corrected link to PANOSE specification (post-release erratum).

- os2ver0.htm

  - Corrected link to PANOSE specification (post-release erratum).

- os2ver1.htm

  - Corrected link to PANOSE specification (post-release erratum).

- os2ver2.htm

  - Corrected link to PANOSE specification (post-release erratum).

- os2ver3.htm

  - Corrected link to PANOSE specification (post-release erratum).

- os2ver4.htm

  - Corrected link to PANOSE specification (post-release erratum).

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/otff)

  - Clarify that table lengths measure a contiguous byte range encompassing the data for the table.

- [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/pclt)

  - Corrected the data type of the MajorVersion field (post-release erratum).
  - Corrected the description for SerifStyle (post-release erratum).

- [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/post)

  - Changed reference for variation axis tags from 'fvar' chapter to OpenType Design-Variation Axis Tag Registry page.
  - Corrected link to Adobe glyph naming guide (post-release erratum).

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/recom)

  - Clarified that the string data referenced by 3/0 name records must be encoded in UTF-16BE.
  - For optical size variants, clarified representation within a STAT axis value table for an upper text size of effective infinity.
  - Corrected link to Adobe glyph naming guide (post-release erratum).
  - Corrected link to PANOSE specification (post-release erratum).

- [scripttags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/scripttags)

  - Removed details on processing of script tags, and replaced with link to details in the OpenType Layout Common Table Formats (post-release erratum).
  - Added tags for additional scripts in Unicode 10, Unicode 11 (post-release update).

- [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/stat)

  - Added axis value table format 4.
  - Revised Introduction to clarify purpose and use of the table as a whole; and revised introduction in the Axis Value Tables section to clarify purpose and use of axis value tables.
  - Added clarifications regarding axes, mapping to legacy font-family models, and serialized representation of document text-formatting properties.
  - Clarified representation of effective infinity and negative infinity in range min/max fields of format 2 axis value tables.
  - Added note regarding use of OlderSiblingFontAttribute.
  - Changed reference for tag requirements from 'fvar' table to the Opentype Design Variation Tag Registry.
  - Revised the axis ordering in example 3 to reflect recommendation given in Axis Value Tables section.

- [ttinst.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/ttinst)

  - Revised links to refer to content ported from Microsoft Word files to Web pages. (Post-release update, August 2018.)

- ttinst1.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/tt_instructions). (Post-release update, August 2018.)

- ttinst2.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/tt_instructions). (Post-release update, August 2018.)

- [ttochap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/ttochap1)

  - Added hyperlink to OpenType Mirroring Pairs List file (ompl.txt).

- [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/tt_instructions)

  - Corrected errors introduced when porting from Word documents (some changes from earlier versions were not retained). (Post-release erratum.)
  - Corrected error in description of “logical OR” inadvertently added when porting from Word documents. (Post-release erratum.)
  - Removed incorrect text inadvertently added to description of Round to Half Grid (RTHG) when porting from Word documents. (Post-release erratum.)
  - Corrected error in code range of MIRP inadvertently introduced when porting from Word documents. (Post-release erratum.)

- [vhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/vhea)

  - Corrected the calculation given in the description of yMaxExtent (post-release erratum).

- [wgl4.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/wgl4)

  - Corrected link to Adobe glyph naming guide (post-release erratum).

- [wgl4b.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/wgl4b)

  - Corrected link to Adobe glyph naming guide (post-release erratum).

- [wgl4c.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/wgl4c)

  - Corrected link to Adobe glyph naming guide (post-release erratum).

- [wgl4d.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/wgl4d)

  - Corrected link to Adobe glyph naming guide (post-release erratum).

- [wgl4e.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec182/wgl4e)

  - Corrected link to Adobe glyph naming guide (post-release erratum).

<a id="anchor-changes-version-181"></a>

## Version 1.8.1

Released January 2017.

Many editorial changes have been made, including global changes to the names of data types used. Some technical corrections were made that do not affect structure definitions. One structure change was introduced: a field was added in the STAT table.

Changes to names of data types were made in various chapters, as follows:

- A single Fixed version field changed to uint16 major/minor version fields: [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cbdt), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cblc), [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebdt), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/eblc), [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebsc), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/math), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/pclt).
- Instances of “GlyphID” as a type changed to uint16: [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/chapter2), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gsub), [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/jstf), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/math).
- “2-byte signed short” changed to int16: [ibmfc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ibmfc).
- BYTE to uint8: [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cbdt), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cblc), [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cmap), [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cpal), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/dsig), [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebdt), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/eblc), [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebsc), [fpgm.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/fpgm), [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/glyf), [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hdmx), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hvar), [ltsh.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ltsh), [merg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/merg), [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/os2), os2ver0.htm, os2ver1.htm, os2ver2.htm, os2ver3.htm, os2ver4.htm, [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvarcommonformats), [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/pclt), [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/recom), [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/sbix), [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vdmx).
- Card8, Card16 and Card32 to uint8, uint16 and uint32: [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cff2).
- CHAR to Tag: [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/os2), os2ver0.htm, os2ver1.htm, os2ver2.htm, os2ver3.htm, os2ver4.htm.
- CHAR to int8: [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cbdt), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cblc), [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebdt), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/eblc), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvarcommonformats), [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/pclt), [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/post).
- LONG to int32: [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hdmx), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [ttinst1.docx](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions), [ttinst2.docx](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions).
- Offset to Offset16: [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/base), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/chapter2), [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gdef), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gsub), [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/jstf), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/math), [merg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/merg), [mvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/mvar), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff).
- SHORT to int16: [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cmap) ,[gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gdef), [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/glyf), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gsub), [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hdmx), [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/head), [hhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hhea), [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hmtx), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/math), [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/os2), os2ver0.htm, os2ver1.htm, os2ver2.htm, os2ver3.htm, os2ver4.htm, [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvarcommonformats), [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/sbix), [ttinst1.docx](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions), [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vdmx), [vhea.hdm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vhea), [vmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vmtx), [vorg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vorg).
- UINT24 to uint24: [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cmap) ,[features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/features_ae), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff).
- ULONG used as a long offset changed to Offset32: [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/base), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cblc), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/chapter2), [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cmap), [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/colr), [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cpal), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/dsig), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/eblc), [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gdef), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gsub), [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gvar), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hvar), [loca.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/loca), [meta.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/meta), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvarcommonformats), [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/sbix), [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/stat), [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/svg), [vvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vvar).
- ULONG not used as an offset changed to uint32: [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cbdt), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cblc), [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cff2), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/chapter2), [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cmap), [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cpal), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/dsig), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/eblc), [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebsc), [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/head), [meta.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/meta), [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/os2), os2ver0.htm, os2ver1.htm, os2ver2.htm, os2ver3.htm, os2ver4.htm, [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/pclt), [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/post), [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/sbix), [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/svg), [ttinst1.docx](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions), [ttinst2.docx](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions).
- USHORT used as an offset changed to Offset16: [cvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cvar), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/eblc), [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/fvar), [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gvar), [kern.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/kern), [loca.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/loca), [merg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/merg), [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/name), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvarcommonformats), [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/stat), [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vdmx), [vorg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vorg).
- USHORT not used as an offset changed to uint16: [avar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/avar), [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/base), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cblc), [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cmap), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/chapter2), [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/colr), [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cpal), [cvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cvar), [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/dsig), [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebdt), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/eblc), [features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/features_ae), [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/features_pt), [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/fvar), [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gasp), [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gdef), [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/glyf), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gsub), [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gvar), [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hdmx), [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/head), [hhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hhea), [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hmtx), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hvar), [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/jstf), [kern.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/kern), [ltsh.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ltsh), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/math), [maxp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/maxp), [merg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/merg), [meta.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/meta), [mvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/mvar), [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/name), [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/os2), os2ver0.htm, os2ver1.htm, os2ver2.htm, os2ver3.htm, os2ver4.htm, [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvarcommonformats), [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/pclt), [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/post), [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/sbix), [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/stat), [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/svg), [ttinst1.docx](tt_instructions.md), [ttinst2.docx](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions), [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vdmx), [vhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vhea), [vmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vmtx), [vorg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vorg), [vvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vvar).

Minor editorial changes were made in the following chapters: [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/base), [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cbdt), [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cblc), [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cff2), [cff2charstr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cff2charstr), [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/chapter2), [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/colr), [cvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cvar), [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebdt), [eblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/eblc), [ebsc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ebsc), [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/fvar), [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gpos), [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gsub), [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gvar), [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hdmx), [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hmtx), [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hvar), [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/), [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/jstf), [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/languagetags), [loca.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/loca), [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/math), [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff), [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvarcommonformats), [otvaroverview.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvaroverview), [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/post), [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/stat), [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vdmx).

In the summary of changes below, details given above are not repeated.

*Summary of Changes:*

- [avar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/avar)

  - Corrected header definition, adding missing reserved field (post-release erratum).
  - Corrected SegmentMaps record definition, showing axisValueMaps as an array (post-release erratum).

- [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cff2)

  - Revised Table 1, CFF Data Layout.
  - Revised description of operands in section 4, DICT Data, including removal of the boolean operand type from Table 6.
  - Revised description of Top DICT data (section 7).
  - Deleted section 8, Glyph Organization
  - Revised description of CharString INDEX (now section 8).
  - Revised description of local and global subr indices (now section 9).
  - Revised description of Font DICT INDEX, Font DICTs and FDSelect (now section 10).
  - Revised description of Private DICT Data (now section 11).
  - Revised description of extensions for Font Variations (now section 12).
  - Added example CFF2 table in Appendix A.
  - Revised description of differences from CFF 1 (sections D1 to D4 of Appendix D).
  - Deleted sections D5 and D6 from Appendix D.

- [cff2charstr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cff2charstr)

  - Revised description of subroutines (section 2.3).
  - Revised description of CFF2 CharString organization (section 3.1), and CharString number encoding (section 3.2).
  - Correction in Table 1, “CFF2 CharString Encoding Values” for byte values 251 – 254.
  - Revised description of CharString operators (section 4).
  - Revised description of path construction operators (section 4.1). Note that changes to the individual operator descriptions are editorial only.
  - Revised description of finishing a CharString outline definition (section 4.2).
  - Revised description of subroutine operators (section 4.4).
  - Revised description of variation data operators (section 4.5).
  - Revised summaries of one- and two-byte operators in Appendix A.
  - In Appendix B, revised description of argument stack limits, and removed TransientArray elements from the list of limits.
  - Deleted Appendix C, “Compatibility and Deprecated Operators”.

- [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/chapter2)

  - Correction of type of MarkFilteringSet index in Lookup table from “unit16” (sic) to uint16.
  - Removed erroneous reference to ConditionSet version.
  - Renamed FeatureVariationRecordsCount in FeatureVariations table to FeatureVariationRecordCount
  - Renamed AlternateFeatureTableOffset field in FeatureTableSubstitutionRecord to AlternateFeatureTable.

- [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/cmap)

  - Revised presentation of formats to give names to records and to integrate record arrays into the presentation of the format for the parent structure containing the array.

- [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/dsig)

  - Changed field names away from Hungarian notation (“ulVersion” to “version”, etc.).

- [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/features_pt)

  - Added note for the 'size' feature regarding the STAT table.

- [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/fvar)

  - Changed the countSizePairs field to permanently reserved, and removed note about this field.
  - Clarified usage of the axisSize and instanceSize fields.
  - Clarified expected behavior if axisCount is zero or if instanceCount is zero.

- [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/glyf)

  - Clarified types for items with variable types depending on flags.

- grstate.doc

  - Content ported into Web page: [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_graphics_state). (Post-release update, August 2018.)

- [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/gvar)

  - Corrected definition of flags field (post-release erratum).

- [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/hmtx)

  - Re-ordered columns in table for the hmtx format to match the convention in other chapters. Also presented the format of the longHorMetric record using the same table conventions.
  - Added explanatory text for better clarity.

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/)

  - Updated version number.
  - Removed mention of Microsoft Word documents. (Post-release update, September 2018.)

- instgly.doc

  - Content ported into Web page: [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructing_glyphs). (Post-release update, August 2018.)

- [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/languagetags)

  - Added tags: 'CJA ', 'CJM '

- [mvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/mvar)

  - Changed the axisCount field to reserved/not used. (The item variation store already contains the axis count.)
  - Renamed offsetToItemVariationStore field to itemVariationStore.
  - Clarified usage of valueRecordSize field.
  - Added validation details for header fields.

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/os2)

  - Added a comment regarding PANOSE values in variable fonts.
  - Added comments for usLowerOpticalPointSize and usUpperOpticalPointSize regarding the STAT table.

- [os2ver0.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/os2ver0)

  - Renamed ulCharRange array to ulUnicodeRange, and revised description.

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otff)

  - Added type Offset32.
  - Removed FUNIT, GlyphID as types.
  - Revised description of version numbers, including clarification of requirement for unrecognized major version changes.
  - Minor revisions to TTC header field names.
  - In the “Font Tables” section, changed the recommendation that tables be 4-byte aligned to be a requirement — this is stated as a requirement earlier in the discussion of checksum calculation.
  - Clarified that 'cvt ', 'fpgm' and 'prep' tables are all optional.

- [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/otvarcommonformats)

  - Renamed regionCount and regionIndices field names in ItemVariationData subtable to regionIndexCount and regionIndexes.

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/recom)

  - In 'kern' table section, added a comment about kerning in variable fonts.
  - In 'maxp' table section, revised comment about CFF to include CFF2.
  - In OS/2 table section, added a comment regarding PANOSE values in variable fonts.
  - Removed “Device Resolutions” section.
  - Added section on families with optical size variants, and related comment in OS/2 section.
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/stat)

  - Added elidableFallbackNameID.
  - Clarified usage of designAxisSize field.
  - Added validation details for header fields.
  - Clarified usage of axisOrdering values.
  - Clarified behaviour of AxisValueFormat2 tables if two tables have overlapping ranges on the same axis.

- [ttinst.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ttinst)

  - Revised links to refer to content ported from Microsoft Word files to Web pages. (Post-release update, August 2018.)

- ttinst1.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions). (Post-release update, August 2018.)

- ttinst2.doc

  - Changed “NPUSHB” to “NPUSHW” in GETVARIATION example.
  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions). (Post-release update, August 2018.)

- [ttochap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/ttochap1)

  - Clarified expected behavior for OpenType Layout processing when glyph runs are formatted with different variation instances of a variable font.

- [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/tt_instructions)

  - Corrected errors introducted when porting from Word documents (some changes from earlier versions were not retained). (Post-release erratum.)
  - Corrected error in description of “logical OR” inadvertently added when porting from Word documents. (Post-release erratum.)
  - Removed incorrect text inadvertently added to description of Round to Half Grid (RTHG) when porting from Word documents. (Post-release erratum.)
  - Corrected error in code range of MIRP inadvertently introduced when porting from Word documents. (Post-release erratum.)

- [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec181/vdmx)

  - Revised names of member structures.
  - Removed VDMX groups from the header format description — these are subtables referenced via offsets.

<a id="anchor-changes-version-18"></a>

## Version 1.8

Released September 2016.

*Summary of Changes:*

- [avar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/avar)

  - Axis variations table added.

- [base.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/base)

  - Changed single Fixed version field to USHORT major/minor versions.
  - Changed int16/uint16 to SHORT/USHORT.
  - Added version 1.1 header.
  - Added section on OpenType Font Variations.
  - Revised description of BaseCoord Format 3 to accommodate Font Variations.
  - Added section for the Item Variation Store table.

- [cff2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/cff2)

  - Compact Font Format 2 table added.

- [cff2charstr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/cff2charstr)

  - CFF 2 CharString Format added.

- [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/chapter2)

  - Changed int16/uint16 to SHORT/USHORT.
  - Added section on OpenType Font Variations.
  - Added VariationIndex table.
  - Added FeatureVariations table and constituent formats.

- [cvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/cvar)

  - CVT variations table added.

- [featurelist.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/featurelist)

  - Added Required Variation Alternates feature.
  - Added Vertical Alternates for Rotation feature.

- [features\_fj.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/features_fj)

  - Revised feature descriptions for 'fina', 'halt', 'init', 'isol' (similar to ISO/IEC 14496-22:2015 Draft Amendment 2).
  - Marked the 'hngl' feature as deprecated (following ISO/IEC 14496-22:2015 Draft Amendment 2).

- [features\_ko.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/features_ko)

  - Revised feature descriptions for 'medi' (similar to ISO/IEC 14496-22:2015 Draft Amendment 2).

- [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/features_pt)

  - Added Required Variation Alternates feature.

- [features\_uz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/features_uz)

  - Revised feature description for 'vert' (similar to ISO/IEC 14496-22:2015 Amendment 1).
  - Added Vertical Alternates for Rotation feature (similar to ISO/IEC 14496-22:2015 Amendment 1).
  - Revised feature description for 'vhal' (similar to ISO/IEC 14496-22:2015 Draft Amendement 2).

- [fvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/fvar)

  - Font variations table added.

- [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/gasp)

  - Added section on OpenType Font Variations.

- [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/gdef)

  - Added missing sections describing Mark Attachment Class and Mark Glyph Sets tables.
  - Added sections for the Item Variation Store table.
  - Changed single Fixed version field to USHORT major/minor versions.
  - Changed int16/uint16 to SHORT/USHORT.
  - Added version 1.2 header.
  - Revised description of CaretValue Format 3 to accommodate Font Variations.

- [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/glyf)

  - Revised description of WE\_HAVE\_A\_TWO\_BY\_TWO flag (following ISO/IEC 14496-22:2015 Amendment 1).
  - In table of composite flags, revised descriptions for OVERLAP\_COMPOUND, SCALED\_COMPONENT\_OFFSET and UNSCALED\_COMPONENT\_OFFSET (similar to changes in ISO/IEC 14496-22:2015 Amendment 1).

- [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/gpos)

  - Changed single Fixed version field to USHORT major/minor versions.
  - Changed int16/uint16 to SHORT/USHORT.
  - Added section on OpenType Font Variations.
  - Added version 1.1 header and FeatureVariations table.
  - Revised descriptions of ValueRecord and ValueFormat to allow for VariationIndex table.
  - Revised reserved mask for ValueFormat to 0xFF00.
  - Revised description of Anchor format 3 to allow for VariationIndex table.

- grstate.doc

  - Content ported into Web page: [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/tt_graphics_state). (Post-release update, September 2018.)

- [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/gsub)

  - Changed single Fixed version field to USHORT major/minor versions.
  - Changed int16/uint16 to SHORT/USHORT.
  - Added section on OpenType Font Variations.
  - Added version 1.1 header and FeatureVariations table.

- [gvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/gvar)

  - Glyph variations table added.

- [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/head)

  - Changed single Fixed version field to USHORT major/minor versions.
  - Changed description of checkSumAdjustment (following ISO/IEC 14496-22:2015 Amendment 1).
  - Revised description of flags bits 1, 5 and 6 – 10.
  - Added note about variable fonts.

- [hhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/hhea)

  - Changed single Fixed version field to USHORT major/minor versions.
  - Added section on OpenType Font Variations.

- [hvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/hvar)

  - Horizontal metrics variations table added.

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/)

  - Added chapters: OpenType Font Variations Overview, OpenType Font Variations Common Table Formats, The CFF 2 CharString Format, Adobe Technical Note #5209.
  - Reordered entries between “Specification” and “Appendices” sections.
  - Removed mention of Microsoft Word documents. (Post-release update, September 2018.)

- instgly.doc

  - Content ported into Web page: [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/tt_instructing_glyphs). (Post-release update, September 2018.)

- [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/jstf)

  - Changed single Fixed version field to USHORT major/minor versions.
  - Changed int16/uint16 to SHORT/USHORT.
  - Added section and other remarks on OpenType Font Variations.

- [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/languagetags)

  - Revised introductory text regarding tag syntax.
  - Revised ISO 639 values for 'QIN ', 'SYR '.
  - Added tags: SYRE, SYRJ, SYRN.

- [merg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/merg)

  - Merge table added.

- [meta.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/meta)

  - Added meta table.

- [mvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/mvar)

  - Metrics variations table added.

- [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/name)

  - Changed description of name ID 6 (following ISO/IEC 14496-22:2015 Amendment 1).
  - Added new name ID 25.

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/os2)

  - Added comment for usWeightClass regarding variable fonts and 'wght' style axis.
  - Added comment for usWidthClass regarding variable fonts and 'wdth' style axis.
  - Corrected misspelling of field name (following ISO/IEC 14496-22:2015 Amendment 1).
  - Added section on OpenType Font Variations.
  - Added note regarding fsSelection bit 15.

- [os2ver0.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/os2ver0)

  - Corrected misspelling of field name (following ISO/IEC 14496-22:2015 Amendment 1).
  - Added footer.

- [os2ver1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/os2ver1)

  - Corrected misspelling of field name (following ISO/IEC 14496-22:2015 Amendment 1).
  - Added footer.

- [os2ver2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/os2ver2)

  - Corrected misspelling of field name (following ISO/IEC 14496-22:2015 Amendment 1).

- [os2ver3.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/os2ver3)

  - Corrected misspelling of field name (following ISO/IEC 14496-22:2015 Amendment 1).

- [os2ver4.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/os2ver4)

  - Corrected misspelling of field name.

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/otff)

  - Changed sfntVersion to ULONG, and clarified discussion of version numbers.
  - Revised description of font collections (similar to changes in ISO/IEC 14496-22:2015 Amendment 1).
  - Added new tables (CFF2, 'avar', 'cvar', 'gvar', 'gvar', HVAR, MVAR, VVAR, STAT) and notes on OpenType Font Variations.
  - Removed obsolete reference to ATM.

- [otvarcommonformats.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/otvarcommonformats)

  - Added OpenType Font Variations Common Table Formats chapter.

- [otvaroverview.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/otvaroverview)

  - Added OpenType Font Variations Overview chapter.

- [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/post)

  - Revised descriptions of Versions 1.0, 2.0 and 3.0 to allow for use in fonts with CFF 2 outlines.
  - Added section on OpenType Font Variations.

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/recom)

  - Added note in Filenames recommendations about naming of files for variable fonts.
  - Removed section on first four glyphs (following ISO/IEC 14496-22:2015 Amendment 1).
  - Revised title and content of section on .notdef (similar to ISO/IEC 14496-22:2015 Amendment 1).
  - Added notes in 'name' table recommendations about naming of variable fonts.
  - Revised 'name' table recommendation for name ID 6 (increased length limit from 63 to 127).
  - Revised OS/2 table recommendation regarding PANOSE value (following ISO/IEC 14496-22:2015 Amendment 1), and fixed external link.
  - Revised symbol-font recommendations regarding PANOSE value (following ISO/IEC 14496-22:2015 Amendment 1).
  - Added section on stroke reduction in variable fonts.
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [sbix.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/sbix)

  - Standard bitmap graphics table added.

- [stat.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/stat)

  - Style attributes table added.

- [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/svg)

  - Added requirement that SVG documents must be encoded in UTF-8 (following ISO/IEC 14496-22:2015 Draft Amendment 2).
  - Added clarification for rendering multiple glyphs from a shared SVG document.
  - Removed context-\* properties from default stylesheet applied to SVG documents.
  - Revised language for handling different SVG versions (following ISO/IEC 14496-22:2015 Draft Amendment 2).
  - Added SVG Glyph Examples section (following ISO/IEC 14496-22:2015 Draft Amendment 2).
  - Minor typo corrections and clarifications.

- [ttinst.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/ttinst)

  - Revised links to refer to content ported from Microsoft Word files to Web pages. (Post-release update, September 2018.)

- ttinst1.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/tt_instructions). (Post-release update, September 2018.)

- ttinst2.doc

  - Clarified description of the GET INFO instruction.
  - Added GET VARIATION instruction.
  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/tt_instructions). (Post-release update, September 2018.)

- [ttochap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/ttochap1)

  - Added section on OpenType Font Variations.

- [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/tt_instructions)

  - Corrected error in description of “logical OR” inadvertently added when porting from Word documents. (Post-release erratum.)
  - Removed incorrect text inadvertently added to description of Round to Half Grid (RTHG) when porting from Word documents. (Post-release erratum.)
  - Corrected error in code range of MIRP inadvertently introduced when porting from Word documents. (Post-release erratum.)

- [vhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/vhea)

  - Added section on OpenType Font Variations.

- [vvar.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec180/vvar)

  - Vertical metrics variations table added.

<a id="anchor-changes-version-17"></a>

## Version 1.7

Released March 2015.

*Summary of Changes:*

- [cbdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/cbdt)

  - Created new page

- [cblc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/cblc)

  - Created new page

- [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/cmap)

  - Minor text change in format 4

- [colr.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/colr)

  - Created new page

- [cpal.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/cpal)

  - Created new page

- [featurelist.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/featurelist)

  - Added Dotless Forms, Flattened accent forms, Math script style alternates, Required Contextual Alternates and Stretching Glyph Decomposition

- [features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/features_ae)

  - Updated 'cv*XX*'
  - Added Dotless forms

- [features\_fj.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/features_fj)

  - Added Flattened ascent forms
  - Updated UI suggestion for 'halt'

- [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/features_pt)

  - Updated Stylistic sets and Optical size
  - Added Math script style alternates, Required Contextual Alternates and Stretching Glyph Decomposition

- [features\_uz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/features_uz)

  - Updated UI suggestion for 'vhal'

- [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/gasp)

  - Added bit flag

- grstate.doc

  - Content ported into Web page: [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/tt_graphics_state). (Post-release update, September 2018.)

- [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/gsub)

  - Fixed typo in ligature substitution

- [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/head)

  - Clarified date description
  - Update description of bit 11

- [hmtx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/hmtx)

  - Updated text beneath table

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/)

  - Updated version number
  - Removed mention of Microsoft Word documents. (Post-release update, September 2018.)

- instgly.doc

  - Content ported into Web page: [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/tt_instructing_glyphs). (Post-release update, September 2018.)

- [jstf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/jstf)

  - Fixed typo in Jstf priority table

- [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/languagetags)

  - Added new tags

- [math.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/math)

  - Added new table

- [maxp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/maxp)

  - Updated maxFunctionDefs description

- [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/name)

  - Changed name IDs 16 and 17 from Preferred name to Typographic name and updated descriptions
  - Added name IDs 23 and 24
  - Updated description for name ID 6
  - Updated description for name ID 20

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/os2)

  - Updated version to 5.0
  - Updated formats
  - Added usLowerOpticalPointSize and usUpperOpticalPointSize

- os2ver4.htm

  - Added page to archive version 4.0

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/otff)

  - Changed Mantissa to Integer
  - Changed Truetype collection to Font Collection
  - Added new tables (CBDT, CBLC, COLR, CPAL and MATH)
  - Moved 'gasp' table to TT Outline table
  - Marked VORG table as optional in relation to Postscript outlines

- [post.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/post)

  - Updated reference to glyph list
  - Updated reference to index numbers

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/recom)

  - Added info on .OTC
  - Added post table note
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [scripttags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/scripttags)

  - Added new tags

- [svg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/svg)

  - Created new page

- [ttinst.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/ttinst)

  - Revised links to refer to content ported from Microsoft Word files to Web pages. (Post-release update, September 2018.)

- ttinst1.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/tt_instructions). (Post-release update, September 2018.)

- ttinst2.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/tt_instructions). (Post-release update, September 2018.)

- [vorg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec170/vorg)

  - Indicated table is optional

<a id="anchor-changes-version-16"></a>

## Version 1.6

Released April 2009; updated July 2010.

*Summary of Changes:*

- Updated HTML to be compliant with W3C standards

- [cff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/cff)

  - Appended description(July 2010)

- [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/chapter2)

  - Added information regarding GDEF table requirements
  - Updated page to show correct number of LookupTypes for GSUB and GPOS
  - Added MarkFilteringSet to Lookup table

- [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/cmap)

  - Updated outdated terminology
  - Added note to 'cmap' header explaining where to find definitions of ID values
  - Changed platform name from Microsoft to Windows
  - Added Format 13 (updated July 2010)
  - Updated note on the language field in 'cmap' subtables (July 2010)

- [featurelist.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/featurelist)

  - Updated feature list

- [features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/features_ae)

  - Added Character Variants feature
  - Clarified script/language sensitivity for 'c2sc' feature

- [features\_ko.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/features_ko)

  - Added Left-to-right alternates
  - Added Left-to-right mirrored forms
  - Updated 'lnum' and 'onum' (July 2010)

- [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/features_pt)

  - Added to recommended implementation for Stylistic Sets
  - Updated Right-to-left alternates
  - Added Right-to-left mirrored forms
  - Fixed link to 'name' table
  - Clarified script/language sensitivity for 'smcp' feature
  - Clarified script/language sensitivity for 'size' feature

- [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/gdef)

  - Updated information relating to GSUB and GPOS tables
  - Added MarkGlyphSetsDef to GDEF header
  - Updated version number
  - Change version number from fixed to ULONG
  - Updated GDEF header description (July 2010)

- [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/gpos)

  - Updated text in Pair Positioning Adjustment: Format 2

- grstate.doc

  - Content ported into Web page: [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/tt_graphics_state). (Post-release update, August 2018.)

- [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/head)

  - Deprecated fontDirectionHint
  - Updated description for bit 14 (July 2010)

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/)

  - Updated version number
  - Added appendix for OMPL
  - Removed mention of Microsoft Word documents. (Post-release update, August 2018.)

- instgly.doc

  - Content ported into Web page: [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/tt_instructing_glyphs). (Post-release update, August 2018.)

- [kern.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/kern)

  - Updated definition (July 2010)

- [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/languagetags)

  - Removed the word “standard” from French and German tags
  - Added IPPH and AMPH tags
  - Added additional expanatory text
  - Added column for ISO 639

- [loca.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/loca)

  - Added information about zero length glyphs at the end of the table

- [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/name)

  - Changed platform name from Microsoft to Windows
  - Updated outdated terminology
  - Added Format 1 Naming table
  - Removed “set to zero” from name ID 15
  - Updated Unicode Platform Specific encoding ID table (July 2010)
  - Updated description for Name ID 4 (July 2010)

- [ompl.txt](https://learn.microsoft.com/en-us/typography/opentype/otspec160/ompl)

  - Added OpenType Mirrored Pairs List

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/os2)

  - Fixed typo in Telugu range
  - Updated bit 61 (July 2010)
  - Corrected comments under fsSelection bit table (July 2010)

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/otff)

  - Changed ULONG to FIXED for TTC Header version numbers
  - Changed “Table Directory” to “Table Record” since it is refering to a single entry in the directory

- [prep.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/prep)

  - Fixed typo (changed CVT to CV)
  - Added reference to table’s previous name

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/recom)

  - Updated recommendations for 'glyf' table, 'kern' table, 'name' table and non-standard (symbol) fonts (July 2010)
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [ttchap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/ttochap1)

  - Added text processing information for ltr and rtl text

- [ttinst.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/ttinst)

  - Revised links to refer to content ported from Microsoft Word files to Web pages. (Post-release update, August 2018.)

- ttinst1.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/tt_instructions). (Post-release update, August 2018.)

- ttinst2.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec160/tt_instructions). (Post-release update, August 2018.)

<a id="anchor-changes-version-15"></a>

## Version 1.5

Released May 2008.

*Summary of Changes:*

- [changes.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/changes)

  - Reversed order so newest changes are at the top

- [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/cmap)

  - Added Format 14: Unicode Variation Sequences

- [featurelist.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/featurelist)

  - Added new features to list

- [features\_ae.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/features_ae)

  - Added Centered CJK Punctuation, Conjunct Forms and Conjunct Form after Ro
  - Updated Akhand and Below-base Forms

- [features\_fj.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/features_fj)

  - Updated Half Forms

- [features\_ko.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/features_ko)

  - Explained 'kern'/'palt' interaction
  - Added date to JIS reference in NLC Kanji Forms
  - Updated Nukta Forms

- [features\_pt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/features_pt)

  - Explained 'kern'/'palt' interaction
  - Added Proportional Kana
  - Updated Pre-base, Post-base and Reph Forms
  - Added Rakar Forms

- [features\_uz.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/features_uz)

  - Explained 'vpal'/'vkrn' interaction
  - Updated Vattu Variants

- [gasp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/gasp)

  - Changed version number to 1 in 'gasp' table
  - Added flags for symmetric gridfit and symmetric smoothing

- [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/gdef)

  - Fixed typo regarding the number of tables within the Glyph Definition table
  - Fixed spelling error under CaretValue Format 1

- grstate.doc

  - Content ported into Web page: [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/tt_graphics_state). (Post-release update, August 2018.)

- [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/gsub)

  - Corrected title for ContextSubstFormat3 subtable

- [glyf.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/glyf)

  - Fixed typo in simple glyph description

- [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/head)

  - Updated description for bit 13

- [ibmfc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/ibmfc)

  - Removed examples that were inaccurate
  - Updated references to ISO standard
  - Adjusted wording for subclasses not specifically refected in ISO standard

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/)

  - Updated version number
  - Added ISO information
  - Removed mention of Microsoft Word documents. (Post-release update, August 2018.)

- instgly.doc

  - Content ported into Web page: [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/tt_instructing_glyphs). (Post-release update, August 2018.)

- [languagetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/languagetags)

  - Updated list of tags

- [loca.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/loca)

  - Removed incorrect example
  - Changed “should” to “must”

- [maxp.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/maxp)

  - Removed redundant sentence

- [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/name)

  - Added platform 0 encoding ID 5 for Unicode variation sequences
  - Added Name IDs 21 and 22
  - Updated Microsoft language IDs

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/os2)

  - Updated text describing ulUnicodeRange1 – ulUnicodeRange4
  - Added bits 7, 8 and 9 to fsSelection table
  - Updated version number
  - Updated ulUnicodeRange with latest range bits and added block ranges
  - Added recommendation to usDefaultChar and usBreakChar description
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [os2ver0.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/os2ver0)

  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [os2ver1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/os2ver1)

  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [os2ver2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/os2ver2)

  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [os2ver3.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/os2ver3)

  - Created new page to archive previous version of OS/2 table
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/otff)

  - Added new data type (UINT24) to handle Unicode variation sequences
  - Added recommendation regarding VORG table

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/recom)

  - Added additional cross-platform recommendations
  - Added additional BASE table recommendations
  - Added recommendation regarding VORG table
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [scripttags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/scripttags)

  - Added script tags for scripts recently added to Unicode
  - Changed 'dflt' script to DFLT script in the description at the bottom of the page

- [ttinst.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/ttinst)

  - Revised links to refer to content ported from Microsoft Word files to Web pages. (Post-release update, August 2018.)

- ttinst1.doc

  - INSTCTRL: Correct value stated for selector flag 3.
  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/tt_instructions). (Post-release update, August 2018.)

- ttinst2.doc

  - Updated GETINFO with ClearType information
  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/tt_instructions). (Post-release update, August 2018.)

- [ttochap1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/ttochap1)

  - Removed outdated information about behavior on Windows 95

- [wgl4d.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec150/wgl4d)

  - Added four Macedonian characters

<a id="anchor-changes-version-14"></a>

## Version 1.4

Released 11 October 2002.

*Summary of Changes:*

- [baselinetags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/baselinetags)

  - Corrected typographic error.
  - Changed hanging baseline references from Hindi to Tibetan.

- [chapter2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/chapter2)

  - Corrected link to GDEF table.
  - Add documentation on new script tag DFLT.

- [cmap.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/cmap)

  - Add Name column to tabular data to make consistent with other parts of spec.
  - Correct description of Encoding Record.

- [cvt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/cvt)

  - Indicate that length must be integral value of FWORD units.

- [dsig.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/dsig)

  - Provide information for ulVersion to be 0x00000001.
  - Update to show usFlag bits that are assigned.
  - Add section on signatures for TrueType Collections.

- [ebdt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/ebdt)

  - Change wording to indicate EBDT is superset of 'bdat'. These are not the same.

- [featurelist.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/featurelist)

  - Added new features: 'abvf', 'c2pc', 'ljmo', 'nlck', 'pcap', 'pref', 'rtla', 'tjmo', 'unic', and 'vjmo'.
  - Change friendly name of 'calt' from Connection Forms to Contextual Alternates.

- [fpgm.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/fpgm)

  - Add comment that array size *n* is the number of bytes in the table.

- [gdef.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/gdef)

  - Example 6, typos in the comments column for increasing 15 and 16ppem corrected.

- [gpos.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/gpos)

  - Clarify origin of Cartesian coordinate system at baseline of the left side.
  - Specify all values are done in font unit measurements.
  - Update images for better presentation.
  - PairPosFormat1 subtable ValueRecord changed to Offset, PairSetOffset\[PairSetCount\].
  - Update wording on MarkToMark attachment.

- grstate.doc

  - Content ported into Web page: [tt\_graphics\_state.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/tt_graphics_state). (Post-release update, August 2018.)

- [gsub.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/gsub)

  - Add Lookup Type 8, Reverse Chaining contextual single substitution.

- [hdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/hdmx)

  - Remove references to EGA.
  - Add statement that bit 2 of head.flag must be set to 1.
  - Add Name columns to tabular data for consistency with spec.

- [head.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/head)

  - Updated macStyle bit descriptions for bits 2 to 15.
  - unitsPerEm annotated that it should be a power of 2.

- [hhea.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/hhea)

  - Change FWord to FWORD for correct data type spelling.

- [ibmfc.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/ibmfc)

  - Fix formatting to indent subclasses for better readability.

- [index.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/)

  - Update the version number to 1.4.
  - Removed mention of Microsoft Word documents. (Post-release update, August 2018.)

- instgly.doc

  - Content ported into Web page: [tt\_instructing\_glyphs.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/tt_instructing_glyphs). (Post-release update, August 2018.)

- [name.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/name)

  - Add Name column to tabular data for consistency with spec.
  - Correct descriptions in Naming Table for count and nameRecord\[count\].
  - Clarified description of encoding ID 0/3. Added encoding ID 0/4. Changed description of encoding ID 3/10 to UTF-32.
  - Added description and example, for use of name ID 4 in CFF fonts.
  - Clarified working for use of name ID 5 (Version string).
  - Changed wording for name ID 16 (Preferred Family) and name ID 17 (Preferred Subfamily).
  - Suggest that style strings (name ID 2 or 17) match with OS/2.usWeightClass and OS/2.usWidthClass.

- [os2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/os2)

  - Updated version number to 0x0003
  - Updated Unicode sub-range bits to be aligned with Unicode 3.2.
  - Remove weighted calculation of xAvgCharWidth.
  - Make fsType bits 0-3 to be mutually exclusive. In other words, only one of those bits may be set to “1” at a time. This is to avoid problems of ambiguity in what the font designer intends.
  - Change link to PANOSE specification.
  - Updated description of usFirstCharIndex, usLastCharIndex, usDefaultChar, usBreakChar; in context of fonts that provide surrogate character support.
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [os2ver0.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/os2ver0)

  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [os2ver1.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/os2ver1)

  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [os2ver2.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/os2ver2)

  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [otff.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/otff)

  - Update filename information for TrueType outline fonts.
  - Add data types for FWORD and UFWORD.
  - Corrected content and description of TTC header v1 and v2.
  - Moved VORG table to PostScript Outlines group.

- [pclt.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/pclt)

  - Change to discourage use of this table.

- [recom.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/recom)

  - Added recommendation for first four glyphs in font.
  - Added recommendation for shape of .notdef glyph.
  - Corrected link to PANOSE specification. (Post-release update, September 2018.)

- [scripttags.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/scripttags)

  - Add script tags for Byzantine Music and Default.

- [ttinst.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/ttinst)

  - Revised links to refer to content ported from Microsoft Word files to Web pages. (Post-release update, August 2018.)

- ttinst1.doc

  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/tt_instructions). (Post-release update, August 2018.)

- ttinst2.doc

  - Corrected description in Logical\_Functions.Greater\_Than.
  - Content ported into Web page: [tt\_instructions.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/tt_instructions). (Post-release update, August 2018.)

- [ttoreg.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/ttoreg)

  - Reworded and reorganized for better readability.

- [vdmx.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/vdmx)

  - Change ratio record and vTable record to tabular format.
  - Recommend use of version 1 VDMX.

- [wgl4e.htm](https://learn.microsoft.com/en-us/typography/opentype/otspec140/wgl4e)

  - Optional glyphs identified and marked. Added a footnote.

<a id="anchor-changes-version-13"></a>

## Version 1.3

Released April, 2001.

*Summary of Changes:*

- Multiple Master support in OpenType, discontinued. The following tables pertaining to it have been removed from this version of the OpenType specification: 'fvar', MMSD, MMFX.

- base.htm

  - *BaseTagList Table*<br> Added a sentence with a link to the baseline tags in the tags registry.
  - *BaseCoord Format 4*<br> Removed.

- cff.htm

  - Removed references to MM fonts in the CFF and Type 2 CharString Format specifications. See the change log in each specification for additional changes made.

- chapter2.htm

  - *Table Organisation*<br> In paragraph 3, changed the number of types of GSUB and GPOS lookups. Phrase added to Paragraph 4 to exclude the Extension lookup.
  - *LookupFlag bit enumeration*<br> Name of the first bit reverted back to RightToLeft. Provided newer description of its use.
  - *Coverage Table*<br> Phrase added to exclude the Extension lookup.

- cmap.htm

  - Merged paragraph 3 and 4 in the introduction section.
  - Added notes that fonts for Windows that support UCS-4 characters (surrogates), need to use an encoding ID 10 and format 12.
  - The version field has been renamed as “language”, to align it with Apple’s TT spec. Added a note to clarify the use of this field.
  - Added information that platform ID 3, encoding ID 7,8 and 9 are reserved.
  - Added platform ID 3, encoding ID 10.
  - Swapped the description of encoding ID 3 and 4. They were incorrectly mapped to Big5 and PRC respectively, in earlier versions of the specification.
  - Added a note on OTF Windows compatibility mapping.
  - *Formats 2, 4, 6.*<br> Made the description of the length field in these formats consistent with the rest of the formats.
  - *Format 2*<br> Removed the duplicate entry for subHeaders\[ \].
  - *Format 4*<br> Corrected endCode and startCode values in the example for this format.
  - *Supporting 4-byte character codes (Formats 8, 10, 12)*<br> Added these new formats.

- ebdt.htm

  - Minor typo in the name of ebdtComponent corrected.

- feattags.htm

  - Added features 'ccmp', 'fin2', 'fin3', 'med2' and 'rlig'.
  - Clarified the Feature Interaction sections for 'kern', 'vkrn'.
  - Updated GSUB lookup type to be used, in the Recommended implementation section of 'ordn'.

- fvar.htm

  - This table removed.

- gdef.htm

  - *Introduction*<br> Added information on the MarkAttachClassDef field.
  - *Overview*<br> Updated image to contain MarkAttachClassDef.
  - *GDEF Header*<br> Added missing information on the MarkAttachClassDef field.
  - *GDEF Header Table*<br> Added the note that offsets might be null for the GlyphClassDef, AttachList, LigCaretList, MarkAttachClassDef
  - *GlyphClassDef Enumeration List*<br> An explanatory note added for definition of ligatures and component glyphs.
  - *Mark Attachment Class Definition Table*<br> An explanatory section and example 7 added.
  - *CaretValue: Format 4*<br> This format used by MM fonts removed.

- gpos.htm

  - Corrected the link “Common Table Formats” to read “OpenType Common Table Formats” throughout table.
  - *Table Organization*<br> Updated the image. Added links for all lookup types. Added Extension positioning as LookupType 9, types 10+ are now Reserved.
  - *PairPosFormat1 subtable*<br> PairSet field corrected to specify it as an array of Offsets.
  - *Lookup Type 6*<br> Sentence added to clarify input context for MarkToBase, MarkToLigature and MarkToMark positioning tables.
  - *LookupType 9: Extension Positioning*<br> This new lookup type added.
  - *ValueRecord table*<br> Removed XIdPlacement, YIdPlacement, XIdAdvance, YIdAdvance and the sentence following the table.
  - *ValueFormat bit enumeration*<br> Removed XIdPlacement, YIdPlacement, XIdAdvance, YIdAdvance and the sentence following the table.
  - *Anchor Table: Format 4*<br> Removed.

- gsub.htm

  - Corrected the link “Common Table Formats” to read “OpenType Common Table Formats” throughout table.
  - *Substituting Glyphs with OpenTypeTM*<br> Types of lookups corrected to six. Added an explanation to the ligature substitution section, to clarify the location occupied by a ligature glyph when it replaces a sequence of glyphs. Missing paragraph on Chaining contextual substitution added.
  - *Table Organization*<br> Updated image.
  - *LookupType Enumeration table for glyph substitution*<br> Added links for all lookup types. Added Extension Substitution as the 7th lookup type. This hence classifies types 8+ as Reserved.
  - *LookupType 2:*<br> Prohibited the deletion of an input glyph, and added that GlyphCount should always be greater than 0.
  - *Chaining Context Substitution Format 1: Simple Chaining Context Glyph Substitution*<br> Added that the match for the string *backtrack sequence + input sequence + lookahead sequence* takes place in the simplest of cases; and that lookup flag values affect backtrack/lookahead sequences. Since the input sequence includes the covered glyph, removed “covered glyph” from the above string.
  - *LookupType 7: Extension Substitution*<br> This new lookup type added.

- head.htm

  - *table*<br> Clarified description for bit 1, 5-10.<br> Added specification for bit 13.

- hhea.htm

  - *table*<br> Added a footnote for the fields Ascender, Descender and LineGap.

- hmtx.htm

  - Added a note that the advanceWidth for each glyph in CFF OpenType fonts must match its x width in the CFF table.

- loca.htm

  - Corrected minor typo.

- maxp.htm

  - Added a note to indicate the difference in representing the fractional part of a version number when it is non-zero.

- mmfx.htm

  - This table removed.

- mmsd.htm

  - This table removed.

- name.htm

  - Minor rewording of text done in the introduction section related to fonts for the Macintosh.
  - *Platform ID, specific encoding ID and languageId information combined into one table.*
  - *Unicode platform-specific encoding IDs (platform ID = 0)*<br> This new table added.
  - *Microsoft platform-specific encoding IDs*<br> This table replaced with a more comprehensive table from the cmap.htm.
  - *Mac platform-specific encoding IDs:*<br> Clarified IDs 2 and 25. Corrected typo in ID 32.
  - *Mac language IDs:*<br> Newer IDs added 23-150.
  - *ISO specific encodings (platform ID=2)*<br> Marked as deprecated. Minor typo in the sentence below the table corrected.
  - *Custom platform-specific encoding IDs (platform ID = 4)*<br> Newer platform ID added.
  - *Name IDs*<br> Added newer description for nameID 5. Added nameID 19 and 20.
  - *Examples*<br> Added example for nameID 19.
  - *LCID-CP list*<br> Updated this list.

- os2.htm

  - *xAvgCharWidth.description*<br> Comments for this field updated.
  - *fsType.table*<br> Added Bit Mask and description details for the case when no bit is set; added Bit Mask value 0x0001.
  - *fsType.comments*<br> Information on setting Bit Masks consolidated into the description column of the table. Removed the redundant section below the table.
  - *yStrikeoutPosition.description*<br> Added that this is the distance of the top of the strikeout stroke.
  - *panose.description*<br> Removed dead URL for the PANOSE evaluation document, added that the “greybook” reference could be used instead.
  - *ulUnicodeRange.table*<br> Updated the Unicode standard version number to 3.0 in the description for these fields. Added bits 70- 127. Added a footnote for setting bit 57 (Surrogates).
  - *usFirstCharIndex.description*<br> Minor correction: added the word platform specific.
  - *sTypoAscender and sTypodescender*<br> Minor corrections done; “design space” now referred to as “ideo em box” in the descriptions; added a links to recom.htm for these fields.
  - *usWinAscent*<br> Explanatory note added to explain the circumstances in which clipping will take place.
  - *usWinDescent*<br> Explanatory note added to explain the circumstances in which clipping will take place.
  - *sxHeight*<br> Added a note that this metric can be used in font substitution.
  - *usDefaultChar*<br> Added that for a given font, missing glyphs will be displayed using the content of glyph 0 in the selected font.

- otff.htm

  - *Version Numbers*<br> Added explanation that representation of a non-zero fractional part in version numbers, differs from the representation of the matissa.
  - *Tables Related to PostScript Outlines*<br> Removed links and description details for the fvar, MMSD and MMFX tables.
  - *Advanced Typographic Tables*<br> Added a link to OpenType Layout Common Table Formats.
  - *Other OpenType Tables*<br> Added the VORG table name to the list.

- otover.htm

  - *Related documentation*<br> Removed sections in the description related to MM fonts.

- post.htm

  - *table.version.description*<br> Added versions 2.5 and 3.0
  - *table.underlinePosition.description*<br> PostScript information added.
  - *version2.0*<br> Updated name and description details in the table contents
  - *version2.5*<br> Updated table contents, added that this version has been deprecated.

- recom.htm

  - *BASE Table*<br> This section added.
  - *'cmap' table*<br> Added details on requirements that need to be satisfied by surrogate fonts on Windows.
  - *'head' Table*<br> Added details regarding usage of the fontRevision value.
  - *'hhea' Table*<br> Removed sentence which incorrectly stated that OpenType fonts that include CFF data must set numberOfHMetrics equal to the number of glyphs in the font.
  - *'post' Table*<br> Updated content related to glyph names in the post table.
  - *OS/2 Table*<br> Added section on sTypoAscender, sTypoDescender, sTypoLineGap.
  - *General Recommendations*<br> Updated the table ordering list for OpenType fonts containing CFF data by adding the 'maxp' table; and, removing the 'fvar' and MMSD tables.
  - *Baseline to Baseline Distances*<br> Added a paragraph on the recommended use of sTypoAscender, sTypoDescender, and sTypoLineGap.
  - *OpenType CJK Font Guidelines*<br> This new section added.

- ttochap1.htm

  - *Introduction*<br> Removed MMSD reference.<br> Expanded the brief description of the content of Registered OpenType Layout Tags to reflect all OpenType tags: scripts, languages, baselines, features.
  - *How Multiple Master OpenType Fonts Use OpenType Layout Tables*<br> This section removed.

- ttoreg.htm

  - Added links in the introduction section, to help jump to the script, language, baseline and feature tag sections.
  - *Script tags*<br> Corrected script tag length description.<br> Added newer script tags.
  - *Language system tags*<br> Added newer language tags.
  - *Baseline tags*<br> Added newer baseline tags: 'icfb', 'icft' and 'idtp'. Expanded the description of existing tags into two categories: “Baseline for HorizAxis” and “Baseline for VertAxis”.
  - *Ideographic Em-Box*<br> This new section added.
  - *Ideographic Character Face*<br> This new section added.

- vhea.htm

  - *Introduction*<br> Added a link each for the vmtx table and the CJK guidelines section.
  - *table.version.description*<br> Version number increased to 1.1. Added a note to indicate the difference in representing the fractional part of a version number when it is non-zero.
  - *table.ascent*<br> Replaced by vertTypoAscender.
  - *table.descent*<br> Replaced by vertTypoDescender.
  - *table.lineGap*<br> Replaced by vertTypoLineGap.
  - *Vertical Header Table Example*<br> Changed version value to 1.1. Corrected the name for vertTypoLineGap

- vmtx.htm

  - *Introduction*<br> Added a link for accessing the CJK guidelines section.
  - *Vertical Origin and Advance Height*<br> This new section added.
  - *Vertical Metrics Table Format*<br> Added note on the calculating the top side bearing.

- vorg.htm

  - This new table added. This is needed by CFF OpenType fonts to locate the origin of vertical glyphs.

- wgl4d.htm

  - Added a missing asterisk for PostScriptName.macron
  - Added U+02DC (tilde) — was missing from the list.

<a id="anchor-changes-version-125"></a>

## Version 1.25

Released July, 2000.

*Summary of Changes:*

- feattags.htm (Feature Tags) -

  - *Features added:*<br> 'abvm' (Above-base Mark Positioning); 'abvs' (Above-base Substitutions); 'akhn' (Akhand); 'blwf' (Below-base Forms); 'blws' (Below-base Substitutions); 'clig' (Contextual Ligatures); 'cswh' (Contextual Swash); 'curs' (Cursive Positioning); 'dist' (Distances); 'falt' (Final Glyph on Line Alternates); 'half' (Half Forms); 'haln' (Halant Forms); 'hkna' (Horizontal Kana Alternates); 'isol' (Isolated Forms); 'jalt' (Justification Alternates); 'locl' (Localized Forms) (replaces 'jajp', 'kokr', 'vivn', 'zhch', and 'zhtw'); 'mkmk' (Mark to Mark Positioning); 'nukt' (Nukta Forms); 'pres' (Pre-base substitutions); 'pstf' (Post-base Forms); 'psts' (Post-base Substitutions); 'rphf' (Reph Forms); 'ruby' (Ruby Notation Forms); 'size' (Optical Size); 'vatu' (Vattu Variants); 'vhal' (Alternate Vertical Half Metrics); 'vkna' (Vertical Kana Alternates); 'vkrn' (Vertical Kerning) 'vpal' (Proportional Alternate Vertical Metrics).
  - *Features removed:*<br> 'crcy' (Currency), 'dpng' (Diphthongs), 'jajp' (Japanese Forms), 'kokr' (Korean Forms), 'vivn' (Vietnamese Forms), 'zhcn' (Simplified Chinese Forms), 'zhtw' (Traditional Chinese Forms).
  - *Features modified:*<br> 'aalt': Added ordering suggestion, reworked user interface suggestions, clarified implementation recommendation, feature interaction and function.<br> 'altv': changed tag to 'valt'.<br> 'c2sc', 'dlig': Clarified function, example and feature interaction.<br> 'calt', 'case', 'dnom', 'expt', 'halt', 'hist', 'hwid', 'jp78', 'jp83', 'jp90', 'kern', 'lfbd', 'liga', 'lnum', 'numr', 'onum', 'pwid', 'qwid', 'rtbd', 'smpl', 'sups', 'titl', 'twid', 'valt': Clarified feature interaction.<br> 'fina', 'init', 'medi', 'rand', 'salt', 'swsh': Clarified user interface suggestion and feature interaction.<br> 'frac': Added 'numr' and 'dnom' extensions, clarified feature interaction.<br> 'fwid', 'palt': Clarified feature interaction and function.<br> 'hngl': Clarified feature interaction and implementation recommendation.<br> 'ital': Clarified function and feature interaction.<br> 'mark': Added example, application interface, user interface suggestion, script sensitivity, feature interaction. Modified recommended implementation.<br> 'mset': Added example.<br> 'nalt': Clarified user interface suggestion, implementation recommendation and feature interaction.<br> 'opbd': Added 'lfbd' and 'rtbd' extensions; clarified user interface suggestion and feature interaction.<br> 'ordn': Clarified script sensitivity, corrected lookup type, clarified implementation recommendation and feature interaction.  'ornm': Clarified user interface suggestion, implementation recommendation, feature interaction and function description.<br> 'smcp': Added note about dotlessi; clarified function and feature interaction.<br> 'trad': corrected terminology (hanzi, not hanja), clarified user interface suggestion and implementation recommendation.<br> 'vert': Clarified feature interaction and added ordering recommendation; extended application interface notes.<br> 'vrt2': Changed “friendly” name, clarified feature interaction and added ordering recommendation; added ATM/OTF driver information and descriptions of how to construct the rotated glyphs in the Function section.<br> 'zero': Clarified user interface suggestion.
  - *Features relocated:*<br> 'mark' and 'mset' have been moved from the Metric Behaviors category, to the Other Substitutions category for consistency in classification.

- chapter2.htm - modified description of FeatureParams field for a non-null offset (the 'size' feature uses it).

<a id="anchor-changes-version-12"></a>

## Version 1.2

Released November, 1998.

*Summary of Changes:*

- Data type notation and spelling corrected throughout
- base.htm - added BaseCoord Table Format 4
- chapter2.htm - corrected example 3; refined description of next glyph; reserved RightToLeft lookup flag; corrected descriptions of LookupFlag bits
- cmap.htm - removed legacy encodings
- dsig.htm - updated field names and format of signature record; added step to creation of content digest
- feattags.htm - registered new features 'crcy', 'dnom', 'jajp', 'kokr', 'lfbd', 'numr', 'rtbd', 'vivn', 'vrt2', 'zhcn', 'zhtw'; removed features 'trak', 'vrot'; edited and clarified descriptions of features 'afrc', 'altv', 'c2sc', 'calt', 'case', 'cpsp', 'dlig', 'dpng', 'expt', 'fina', 'frac', 'fwid', 'halt', 'hlig', 'lngl', 'hwid', 'init', 'ital', 'jp78', 'jp90', 'kern', 'lnum', 'medi', 'mgrk', 'onum', 'opbd', 'ordn', 'ornm', 'palt', 'pnum', 'pwid', 'qwid', 'smcp', 'smpl', 'sups', 'tnam', 'tnum', 'trad', 'twid', 'vert'
- gdef.htm - added MarkAttachClassDef to header, and MarkAttachmentType bit setting to LookupFlag bits; added CaretValue Table Format 4
- glyf.htm - added table detailing component record structure
- gsub.htm - added format 6, for chaining contextual substitution; general editing
- gpos.htm - added format 8, for chaining contextual positioning; clarified pair positioning operations; corrected Example 10; clarified coordinate system description; refined description of when a lookup is finished; added AnchorTable Format 4; general editing
- head.htm - added note about fontRevision field; clarified description of compression flag
- hhea.htm - corrected description of numberOfHMetrics
- mmfx.htm - corrections throughout; added MMFXIdZero
- name.htm - general editing
- os2.htm - renamed usMaxLookup to usMaxContext; edited descriptions of defaultChar and breakChar; updated registered vendors
- otff.htm - general editing; added ulDsigTag and related fields to TTC header; added datatypes LONGDATETIME; clarified checksum calculations; added tag name restrictions; clarified use of version numbers
- post.htm - renamed FormatType to Version
- vhea.htm - replaced mention of centerline with vertical baseline; corrected description of numOfLongVerMetrics
- CFF.pdf and Type2.pdf updated (December 1998)
- Several PostScript glyph names corrected in the WGL tables (18 December 1998)
- name.htm - Descriptions of name ID 13 and 14 corrected (29 January 1999)
- mmsd.htm - Attribute flags corrected (29 January 1999)
- head.htm - Data type of xMin corrected (29 January 1999)

<a id="anchor-changes-version-11"></a>

## Version 1.1

Released April, 1998.

*Summary of Changes:*

- CFF and Type2 specs updated
- chapter2.htm - corrected typo in figure 2d (fig2d.gif)
- dsig.htm - added info about location of DSIG table; added list of sfnt structural requirements
- feattags.htm - created more comprehensive list and description of layout feature tags
- gpos.htm - corrected illustration 4f (fig4f.gif)
- head.htm - added bit 12 (converted) to flags field
- hhea.htm - removed CFF restriction listed in numberOfHMetrics field; added caretOffset field.
- maxp.htm - added version 0.5 table (numGlyphs field); general editing
- name.htm - added name IDs 16, 17, and 18; corrected name ID example
- os2.htm - added new version (2), adding new fields sxHeight, sCapHeight, usDefaultChar, usBreakChar, usMaxLookup; clarified sTypoAscender and sTypoDescender fields; changed some Unicode range values to reflect Unicode 2; updated registered vendors
- otff.htm - general editing; added description of two types of TTC headers, and DSIG table location
- recom.htm - general editing

<a id="anchor-changes-version-101"></a>

## Version 1.01

Released October, 1997.

*Summary of Changes:*

- mmfx.htm, fvar.htm, mmsd.htm, otover.htm, recom.htm - edits throughout
- loca.htm - changed long-aligned to word-aligned for local offsets
- wgl4.htm - added reference to Euro symbol
- dsig.htm - added note about system use of DSIG table to distinguish OT from TT fonts
- ttoreg.htm - added 'VIT ', 'TRK ', and 'ROM ' lang sys tags
- otff.htm - rearranged table list
- base.htm - change to basecoordformat3 data type
- gpos.htm - pairposformat1 subtable valuerecord becomes offset
- kern.htm - GPOS clarification
- name.htm - added name IDs 13 and 14
- ltsh.htm - clarified option for fixed-pitch fonts
- vdmx.htm - version 1 added to VDMX table
- os2.htm - added codepage range 8 for Vietnamese; added new vendor IDs, including UNKN

<a id="anchor-changes-version-10"></a>

## Version 1.0

Released April, 1997.
