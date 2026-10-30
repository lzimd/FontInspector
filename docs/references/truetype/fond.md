---
title: "The 'fond' table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---

<a id="anchor-fond-hmtx"></a>

# The `'fond'` table

<a id="anchor-fond-part-1"></a>

## General table information

The `'fond'` table contains contents comparable to the old `'FOND'` and `'NFNT'` resources. It provides the ability to have true data-fork fonts to behave as if they were in a font suitcase with associated `'FOND'` and `'NFNT'` data.

The table begins with a header giving the table version and the number of `'FOND'` and `'NFNT'` resources it replaces. The current version is 2.

```
struct TableHeader_fond {
	uint16_t fVersion;
	uint16_t fCount_fond;
	uint16_t fCount_nfnt;
	uint16_t fUnused;
}
```

The `fUnused` field should be set to 0. It provides better data alignment and room for future extensions of the table.

The header is followed by `fCount_fond` `TableEntry_fond` entries, each of which contains the equivalent of the data the Resource Manager provides for a single `'FOND'` resource.

The resource name can be treated as a Pascal string (by taking its start as `&fNameLength`), but it's actually stored as a C string. The `fScript` and `fLanguage` fields are used to determine how to convert the resource name to Unicode.

It is recommended that unused bytes in the `fName` field be set to a value such as `0xFF` or `0x00`.

The table entries also indicate where the `'FOND'` data is found within the `'fond'` table.

As a rule, the `fResourceID` and `fFamilyID` fields will be the same; there are some exceptional cases, however, where they are different. The `fResourceID` field is the resource ID for the specific `'FOND'` table, and the `fFamilyID` field is the family ID field within the `'FOND'` resource.

The `fFlags` field contains the value of returned by `GetResAttrs()` for the `'FOND'` resource.

The `fStyle` field is used to store the QuickDraw style value for *this* particular TrueType font. That is, if the font containing the `'fond'` table is the one corresponding to the `'FOND'` resource's plain style, the value of `fStyle` would be 0. If it's the TrueType font corresponding to the `'FOND'` resource's bold style, it would be 1, and so on.

The `fOffset` field is the offset of the appropriate `Resource_fond`structure from the beginning of the `'fond'` table. The `fLength` field is the total length of the `Resource_fond` and following embedded `'FOND'` resource.

```
struct TableEntry_fond {
	int16_t fResourceID;
	int16_t fFamilyID;
	ResAttributes fFlags;
	uint16_t fStyle;
	int16_t fScript;
	int16_t fLanguage;
	uint32_t fOffset;
	uint32_t fLength;
	uint8_t fNameLength;
	uint8_t fName[ 255 ];
}
```

The `TableEntry_fond` array is followed by an array of `TableHeader_fond.fCount_nfnt` `TableEntry_nfnt` structures, which are described below.

`'FOND'` resources identify TrueType fonts via the resource ID of the associated `'sfnt'` resource. This is obviously not possible in a data-fork font, where there are no resources. For this reason, the actual `'FOND'` data is preceded by a table mapping resource ID's to the PostScript names of the associated TrueType fonts. This mapping table is found in a `Resource_fond` structure, which is a count of mappings followed by indviidual `ResourceMapping` structures:

```
struct Resource_fond {
	uint32_t fNumMappings;
	ResourceMapping fEntries[ kVariableLengthArray ];
}
```

```
struct ResourceMapping {
	int32_t fResourceID;
	uint8_t fPostScriptName[ 62 ];
}
```

Since the `ResourceMapping` structure contains PostScript names, these are stored as ASCII, zero-terminated. It is recommended that unused bytes of the `fPostScriptName` field be set to a value such as `0xFF` or `0x00`.

The resource mappings are followed by the `'FOND'` data as documented in *Inside Macintosh* with two exceptions, both having to do with the Font Association Table (FAT).

QuickDraw uses the FAT to provide a mapping between styles and `'sfnt'` resources and style/pointsize combinations and `'NFNT'` resources. The `'fond'` table retains the FAT, but is not required to include references to `'sfnt'` resources other than the one for the font containing the table.

`'NFNT'` resources are handled similarly to `'FOND'` resources. A `TableEntry_nfnt` entry is used to store Resource Manager data regarding the `'NFNT'` table. The fields are similar to those for the `TableEntry_fond` structure.

```
struct TableEntry_nfnt {
	int16_t fResourceID;
	ResAttributes fFlags;
	uint16_t fStyle;
	int16_t fScript;
	int16_t fLanguage;
	uint32_t fOffset;
	uint32_t fLength;
	uint8_t fNameLength;
	uint8_t fName[ 255 ];
}
```

Again, value of the the `fOffset` field is relative to the beginning of the `'fond'` table and, together with the `fLength` field indicates the location of an `'NFNT'` resource embedded in the `'fond'` table. Since `'NFNT'` resources do not make reference to other resources, there is no need for a `Resource_fond` structure.

The `'fond'` table is supported in OS X beginning with OS X 10.6.
