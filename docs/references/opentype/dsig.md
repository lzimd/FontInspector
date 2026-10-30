---
title: "DSIG — Digital Signature Table"
description: "The digital signature table specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-02-09T00:00:00Z"
updated_at: "2024-05-31T17:41:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/810414e13e39f68adfb5f12d525e6b50c850fbbc/typographydocs/opentype/spec/dsig.md"
last-modified: "2026-09-17T18:19:03Z"
---

<a id="anchor-dsig-dsig-digital-signature-table"></a>

# DSIG — Digital Signature Table

<a id="anchor-dsig-overview"></a>

## Overview

The DSIG table contains the digital signature of the OpenType™ font. Signature formats are widely documented and rely on a key pair architecture. Software developers, or publishers posting material on the Internet, create signatures using a private key. Operating systems or applications authenticate the signature using a public key.

The W3C and major software and operating system developers have specified security standards that describe signature formats, specify secure collections of web objects, and recommend authentication architecture. OpenType fonts with signatures will support these standards.

OpenType fonts offer many security features:

- Operating systems and browsing applications can identify the source and integrity of font files before using them,
- Font developers can specify embedding restrictions in OpenType fonts, and these restrictions cannot be altered in a font signed by the developer.

The enforcement of signatures is an administrative policy that may be supported by the host environment in which fonts are used. Systems may restrict use of unsigned fonts, or may allow policy to be controlled by a system administrator.

Anyone can obtain identity certificates and encryption keys from a certifying agency, such as Verisign or GTE’s Cybertrust, free or at a very low cost.

<a id="anchor-dsig-table-structure"></a>

## Table structure

The DSIG table is organized as follows. The first portion of the table is the header.

<a id="anchor-dsig-header"></a>

*DsigHeader*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-dsig-version"></a>uint32 | version | Version number of the DSIG table (0x00000001) |
| <a id="anchor-dsig-numSignatures"></a>uint16 | numSignatures | Number of signatures in the table |
| <a id="anchor-dsig-flags"></a>uint16 | flags | Permission flags:<br> bit 0: cannot be resigned<br> bits 1-7: Reserved (Set to 0) |
| <a id="anchor-dsig-signatureRecs"></a>SignatureRecord | signatureRecords\[numSignatures\] | Array of signature records |

The version of the DSIG table is expressed as a uint32, beginning at 0. The version of the DSIG table currently used is version 1 (0x00000001).

Permission bit 0 allows a party signing the font to prevent any other parties from also signing the font (counter-signatures). If this bit is set to zero (0) the font may have a signature applied over the existing digital signature(s). A party who wants to ensure that their signature is the last signature can set this bit.

The DSIG header has an array of signature records that specify the format and offset of signature blocks.

<a id="anchor-dsig-signatureRec"></a>

*SignatureRecord*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-dsig-format"></a>uint32 | format | Format of the signature |
| <a id="anchor-dsig-length"></a>uint32 | length | Length of signature in bytes |
| <a id="anchor-dsig-offset"></a>Offset32 | signatureBlockOffset | Offset to the signature block from the beginning of the table |

Signatures are contained in one or more signature blocks. Signature blocks may have various formats; currently one format is defined. The format identifier specifies both the format of the signature block, as well as the hashing algorithm used to create and authenticate the signature.

<a id="anchor-dsig-signatureBlock_1"></a>

*Signature Block Format 1*

| Type | Name | Description |
| --- | --- | --- |
| <a id="anchor-dsig-reserved1"></a>uint16 | reserved1 | Reserved for future use; set to zero. |
| <a id="anchor-dsig-reserved2"></a>uint16 | reserved2 | Reserved for future use; set to zero. |
| <a id="anchor-dsig-signatureLength"></a>uint32 | signatureLength | Length (in bytes) of the PKCS#7 packet in the signature field. |
| <a id="anchor-dsig-signature"></a>uint8 | signature\[signatureLength\] | PKCS#7 packet |

For more information about PKCS#7 signatures, see *RFC 2315, PKCS #7: Cryptographic Message Syntax, Version 1.5* ([https://www.rfc-editor.org/info/rfc2315](https://www.rfc-editor.org/info/rfc2315)).

For more information about counter-signatures, see *RFC 2985, PKCS #9: Selected Object Classes and Attribute Types, Version 2.0* ([https://www.rfc-editor.org/info/rfc2985](https://www.rfc-editor.org/info/rfc2985)).

**Format 1: For whole fonts, with either TrueType outlines and/or CFF or CFF2 data**

PKCS#7 or PKCS#9. The signed content digest is created as follows:

1. If there is an existing DSIG table in the font:<br> a. Remove the DSIG table from font.<br> b. Remove the DSIG table entry from the [table directory](otff.md#anchor-otff-table-directory).<br> c. Adjust table offsets as necessary.<br> d. Recalculate the checksumAdjustment in the 'head' table.
2. Select the flags value and append it to a copy of the revised font data.
3. Hash the revised font data using a secure one-way hash (such as MD5) to create the content digest.
4. Create the PKCS#7 signature block using the content digest.
5. Create a new DSIG table containing the signature block.
6. Add the DSIG table to the font, adjusting table offsets as necessary.
7. Add a DSIG table entry to the table directory.
8. Recalculate the checksumAdjustment in the 'head' table.

Validation of a signature in a font file is done by repeating steps 1 – 4 in an in-memory copy of the font file, using the flags value from the font file in step 2. Note that changing the checksumAdjustment in the last step does not break the signature because validation is done on an in-memory copy with these changes.

Prior to signing a font file, ensure that all the following attributes are true:

- The magic number in the 'head' table is correct.
- Given the numTables value in the table directory, the other values in the table directory are consistent.
- The table records in the table directory are ordered alphabetically by the table tags, and there are no duplicate tags.
- The offset of each table is a multiple of 4. (That is, tables are long word aligned.)
- The first actual table in the file comes immediately after the directory of tables.
- If the tables are sorted by offset, then for all tables i (where index 0 means the table with the smallest offset), Offset\[i\] + Length\[i\] \<= Offset\[i+1\] and Offset\[i\] + Length\[i\] \>= Offset\[i+1\] - 3. In other words, the tables do not overlap, and there are at most 3 bytes of padding between tables.
- The pad bytes between tables are all zeros.
- The offset of the last table in the file plus its length is not greater than the size of the file.
- The checksums of all tables are correct.
- The 'head' table’s checksumAdjustment field is correct.

<a id="anchor-dsig-signatures-for-font-collection-files"></a>

## Signatures for font collection files

The DSIG table for a font collection file (.ttc or .otc) must be the last table in the file. The offset to the table is put in the TTCHeader (version 2). Signatures of font collection files must be Format 1 signatures.

The signature of a font collection file applies to the entire file, not to the individual fonts contained within the file. Signing the font collection file ensures that other contents are not added to the file.

Individual fonts included in a font collection file should not be individually signed as the process of making the font collection file could invalidate the signature on individual fonts.

When DSIG table is created for a font collection file, the steps given above are used, with these revisions:

- In step 1: if there is an existing DSIG table referenced in a version 2.0 TTC header, the DSIG table is removed, and the DSIG fields in the TTC header are set to NULL. No recalculation of a checksumAdjustment is required.
- In steps 6 and 7: the DSIG table is added to the file, not to any individual font within the collection. A version 2.0 TTC header is required, with the DSIG fields in the TTC header set to reference the DSIG table.
- Step 8 is not applicable.

See the [TTC Header](otff.md#anchor-otff-ttc-header) section of the OpenType Font File chapter for related information.
