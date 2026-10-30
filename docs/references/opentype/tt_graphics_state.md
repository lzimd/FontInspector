---
title: "Graphics State Summary"
description: "Graphics State Summary (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2021-11-05T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/7a06e1def6e2f40e43dc8897e5372614bcc413f6/typographydocs/opentype/spec/tt_graphics_state.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-tt_graphics_state-graphics-state-summary"></a>

# Graphics State Summary

The following tables summarize the variables that make up the Graphics State. Nearly all of the Graphics State variables have a default value as shown below. That value is reestablished for every glyph in a font. Instructions are available for resetting the value of all Graphics State variables. Some state variables can be reset in the CVT Program. In such cases the value set becomes the new default and will be reestablished for each glyph. When value of a state variable is changed by instructions associated with a particular glyph, it will hold only for that glyph.

The setting of the Graphics State variables will affect the actions of certain instructions. Affected instructions are listed for each variable.

| **Graphics State Variable** | **Default** | **Set With** | **Affects** |
| --- | --- | --- | --- |
| auto\_flip | TRUE | FLIPOFF<br>FLIPON | MIAP<br> MIRP |
| control\_value\_cut\_in | 17/16 pixels | SCVTCI | MIAP<br>MIRP |
| delta\_base | 9 | SDB | DELTAP1<br>DELTAP2<br>DELTAP3<br>DELTAC1<br>DELTAC2<br>DELTAC3 |
| delta\_shift | 3 | SDS | DELTAP1<br>DELTAP2<br>DELTAP3<br>DELTAC1<br>DELTAC2<br>DELTAC3 |
| dual\_projection\_vectors | — | SDPVTL | IP<br>GC<br>MD<br>MDRP<br>MIRP |
| freedom\_vector | x-axis | SFVTCA<br>SFVTL<br>SFTPV<br>SVTCA<br>SFVFS | GFV |
| zp0 | 1 | SZP0<br>SZPS | AA<br>ALIGNPTS<br>ALIGNRP<br>DELTAP1<br>DELTAP2<br>DELTAP3<br>IP<br>ISECT<br>MD<br>MDAP<br>MIAP<br>MIRP<br>MSIRP<br>SHC<br>SHZ<br>SHP<br>UTP |
| zp1 | 1 | SZP1<br>SZPS | AA<br>ALIGNPTS<br>ALIGNRP<br>IP<br>MD<br>MDRP<br>MIRP<br>MSIRP<br>SHC<br>SHZ<br>SHP<br>SFVTL<br>SPVTL |
| zp2 | 1 | SZP2<br>SZPS | ISECT<br>IUP<br>GC<br>SHC<br>SHP<br>SFVTL<br>SHPIX<br>SPVTL<br>SC |
| instruct\_Control | 0 | INSTCTRL | all instructions |
| loop | 1 | SLOOP | ALIGNRP<br>FLIPPT<br>IP<br>SHP<br>SHPIX |
| minimum\_distance | 1 pixel | LMD | MDRP<br>MIRP |
| projection\_vector | x-axis | SPVTCA<br>SPVTL<br>SVTCA<br>SPVFS | GPV |
| round\_state | 1 | RDTG<br>ROFF<br>RTDG<br>RTG<br>RTHG<br>RUTG<br>SROUND<br>S45ROUND | MDAP<br>MIAP<br>MDRP<br>MIRP<br>ROUND |
| rp0 | 0 | SRP0 | IP<br>MDAP<br>MIAP<br>MIRP<br>MSIRP<br>SHC<br>SHZ<br>SHP |
| rp1 | 0 | SRP1 | IP<br>MDAP<br>MDRP<br>MIAP<br>MSIRP<br>SHC<br>SHZ<br>SHP |
| rp2 | 0 | SRP2 | IP<br>MDRP<br>MIRP<br>MSIRP<br>SHC<br>SHZ<br>SHP |
| scan\_control | FALSE | SCANCTRL<br>SCANTYPE |  |
| singe\_width\_cut\_in | 0 pixels | SSWCI | MDRP<br>MIRP |
| single\_width\_value | 0 pixels | SSW\* | MDRP<br>MIRP |

\* The SSW argument is expressed in FUnits. The interpreter will convert this to pixels (F26Dot6).
