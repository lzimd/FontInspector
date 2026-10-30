---
title: "OpenType 1.9.1 errata"
description: "OpenType 1.9.1 errata"
author: "PeterCon"
ms.date: "2025-03-19T00:00:00Z"
updated_at: "2025-03-20T05:52:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/6282dcf07034c3584933986fc8dde2a921e45e61/typographydocs/opentype/spec/errata.md"
last-modified: "2026-09-17T18:19:04Z"
---

<a id="anchor-errata-opentype-191-errata"></a>

# OpenType 1.9.1 errata

This page documents errors in the OpenType specification that have technical significance and could lead to incorrect implementations. The scope is limited to issues in which the OpenType 1.9.1 specification as originally published implies technical details that are contrary to the intended design. Corrections may include corrections to incorrect values related to certain table fields, incorrect formulas for computing certain values, or similar issues. Corrections will not include any changes to data structures. If the textual change required for the correction is minor, the correction will be made in the specification and also listed here. If larger textual changes are required, the issue may be described here, but actual changes may be left to a future version. In either case, the status will be indicated in the table below.

Certain minor, editorial errors such as mis-spelling of words with no technical impact may on occasion be corrected silently, without notice or version update.

| Date | Page | Description | Status |
| --- | --- | --- | --- |
| 9 October 2024 | [CFF2 — Compact Font Format (CFF) Version 2](cff2.md) | The description of **StemSnapH** and **StemSnapV** included a statement suggesting that, if the values are blended in a variable font and the derived instance values are not in increasing order, then behavior is not defined. That is incorrect: the values are still valid.<br><br> Similarly, the discussion of blended stem and end hints included a statement suggesting that, if derived instance values for stems are not in order, then behavior is not defined. That is incorrect: the values are still valid, and the bit flag operands for **cntrmask** and **hintmask** operators reference stems in their encoded order. | Corrected in 1.9.1 (2024-10-9). |
| 6 July 2024 | [OpenType™ Layout Common Table Formats](chapter2.md) | In the description for the SequenceRuleSet table, the size for the seqRuleOffsets\[\] array incorrectly referred to a field name “posRuleCount” instead of the “seqRuleCount” field. | Corrected in 1.9.1 (2024-7-6). |
| 19 March 2025 | [JSTF — Justification Table](jstf.md) | The field name “gsubLookupIndices" in the JstfModList table is incorrect. In OpenType 1.9 and earlier, two justification modification list tables were documented, JstfGSUBModList and JstfGPOSModList, that were identical except for having distinct field names with “GSUB” and “GPOS”. In working drafts for ISO/IEC 14496-22 Open Font Format, 5th Edition, the separate tables were consolidated into the one JstfModList table. When incorporating a corresponding change in OpenType 1.9.1, revision of this field name was overlooked: the field name in the consolidated table should be “lookupIndices”. | Corrected in 1.9.1 (2025-3-19). |
|  |  |  |  |
