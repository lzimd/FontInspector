# Design overview

Status: design for review. This document specifies the fetch and build system. It doesn't implement it.

SpecMirror creates a committed, deterministic Markdown mirror of two documentation sources:

- the current OpenType specification published by Microsoft Learn
- the `Chap6` pages of Apple's TrueType Reference Manual.

The system is deliberately split into three stages. `fetch pages` performs discovery and page downloads. `fetch images` performs image downloads and publishes the snapshot. `build` is a pure offline transformation of that snapshot into Markdown. The two fetch stages are the only stages that perform network I/O, and together they produce a reusable local snapshot.

SpecMirror keeps corrections as versioned data, not as edits to generated Markdown.

## 1. Goals and constraints

The design must satisfy the following requirements.

1. Each source has independent `fetch pages`, `fetch images`, and `build` commands.
2. Fetch results are cacheable, reusable, and safe to inspect.
3. Builds are reproducible from a complete snapshot and from checked-in correction data.
4. The build converts upstream HTML into a semantic document tree before rendering. It copies no raw HTML into the committed output.
5. The committed output contains only Markdown files and images.
6. The output contains only `<a>`, `<br>`, `<sup>`, and `<sub>` HTML elements, plus the exact span-placeholder comments defined in this document.
7. Adapters contain source-specific behavior. All sources share the fetch transport, cache, manifest, AST, correction engine, table lowering, and renderer.
8. A failed pages stage never publishes a new page plan. A failed images stage never publishes a new manifest. A build refuses incomplete or mixed snapshots.
9. Page-specific corrections fail loudly when their expected source no longer matches.
10. Local fetch time, wall-clock time, random values, locale, filesystem order, and file modification times don't influence the committed output.
11. Each mirror lives under `docs/references/<source>/` and contains a generated `README.md` whose page list covers every mirrored page.
12. `index.md` uses the same page pipeline as every other mirrored page and carries no generated navigation.

The following are non-goals:

- mirroring other Apple manual chapters
- mirroring archived OpenType versions
- executing JavaScript or reproducing client-side behavior
- preserving site navigation, styling, scripts, or tracking attributes
- providing a general-purpose HTML-to-Markdown converter
- editing generated Markdown by hand.

## 2. Command-line interface

The package lives under `scripts/` and runs as:

```text
uv run -m specmirror opentype fetch
uv run -m specmirror opentype fetch pages
uv run -m specmirror opentype fetch images
uv run -m specmirror opentype build
uv run -m specmirror truetype fetch
uv run -m specmirror truetype fetch pages
uv run -m specmirror truetype fetch images
uv run -m specmirror truetype build
```

The command-line tool uses a standard argument parser and exits non-zero on failure.

`fetch` accepts an optional stage: `pages`, `images`, or `all`. An omitted stage means `all`, which runs the pages stage and then the images stage in one process. The sequence `fetch pages` followed by `fetch images` produces the same snapshot as `fetch all` when neither the upstream source nor the code changes between commands.

### 2.1 Stages and options

| Stage | Network work | Persistent writes | Manifest |
| --- | --- | --- | --- |
| `fetch pages` | Discovery refresh and page downloads | Discovery cache, page cache, `staging/page-plan.json`, pages report | No manifest change |
| `fetch images` | Image downloads | Image cache, `manifest.json`, images report | Publishes the manifest |
| `fetch all` | Both stages in order | Both sets of writes | Publishes the manifest |

| Option | Stage | Meaning |
| --- | --- | --- |
| `--dry-run` | fetch, build | Perform all read-only work and validation, print the plan, and make no persistent writes. |
| `--refresh` | fetch pages, fetch images, fetch all | Bypass cache reuse for the selected stage. The pages stage also refreshes discovery. |
| `--check` | build | Build into a temporary location and compare file names and bytes with the committed output. Make no writes. Exit non-zero on any difference. |
| `--verbose` | fetch, build | Emit detailed progress and diagnostics to standard error. |

`fetch pages --dry-run` performs the same planning and validation as a real pages stage, but it keeps results in memory or temporary files. It always refreshes discovery. It reads the previous manifest and page plan when present, verifies cached page hashes, and downloads only pages without a trusted cache match. With `--refresh`, it downloads every page to a temporary location. It validates page media types, UTF-8, slugs, and image candidates, then prints the proposed page inventory. It makes no image requests.

| Work | Network request during pages dry-run |
| --- | --- |
| Discovery refresh | Always |
| Page with a trusted cached hash, without `--refresh` | No |
| New, missing, corrupt, or `--refresh` page | Yes, to a temporary file |
| Image | No |
| Conditional request | No |

`fetch images --dry-run` validates the page plan, the discovery file, and every page hash, then lists planned image work. It performs no network I/O and downloads no images. Neither stage writes cache files, staging state, a manifest, or a report during a dry run. The dry run discards downloaded bytes, so a later real pages stage repeats those page requests.

`fetch all --dry-run` chains both plans in memory.

`build --dry-run` parses and validates the full output but writes nothing. `--check` implies no persistent writes and serves CI and pre-commit use.

Fetch reports are diagnostic artifacts and aren't inputs to a build. Build reports are deterministic and contain no local timestamps.

### 2.2 Fetch cache policy

By default, each fetch stage reuses only cache entries whose bytes match a trusted hash. The pages stage always refreshes discovery.

It reuses a page when its cached bytes match either the previous manifest or the existing page plan for the same URL. The images stage reuses an image when its cached bytes match the previous manifest. Both stages re-download missing or corrupt entries automatically.

The images stage never downloads or changes pages. It requires a page plan from a successful pages stage.

`fetch pages --refresh` re-downloads every page. `fetch images --refresh` re-downloads every image. `fetch all --refresh` does both. Only the pages stage refreshes discovery.

A normal pages stage doesn't check whether an already cached page has changed upstream. `fetch pages --refresh` detects upstream page changes. The design intentionally omits conditional HTTP requests: for these servers, a `304 Not Modified` response doesn't materially reduce request latency compared with a `200` response.

Each stage deduplicates its downloads by normalized absolute URL. No `If-None-Match` or `If-Modified-Since` logic is part of the design.

## 3. Repository, cache, and output layout

Planned package layout:

```text
scripts/
  specmirror/
    __main__.py
    cli.py
    paths.py
    errors.py
    notice.py
    progress.py
    storage.py
    schema.py
    manifest.py
    dom.py
    text.py
    urls.py
    fetch/
      http.py
      models.py
      stage.py
      runner.py
      pages.py
      page_content.py
      page_plan.py
      reuse.py
      images.py
      naming.py
    sources/
      base.py
      opentype.py
      truetype.py
    reports/
      fetch.py
      build.py
    build/
      front_matter.py
      links.py
      pipeline.py
      readme.py
      validate.py
    convert/
      ast.py
      build_page_ast.py
      normalize.py
      table.py
      patch.py
      render.py
      html_model.py
      markdown_model.py
    corrections/
      data/
        opentype/
        truetype/
  tests/
```

The top level is the shared core. It owns no network I/O and no parser import except `dom.py`. It carries the storage helpers, the snapshot contract in `schema.py` and `manifest.py`, the parser-neutral DOM contract, and the shared URL, text, path, error, notice, and progress layers. Both main lines consume it, so neither main line can hide domain behavior there.

The `sources` package owns discovery and content extraction. The `reports` package owns report artifacts for both main lines.

The `fetch` package owns network access, the cache policy, staging state, and the page plan. The `build` package owns the build pipeline. The `convert` package owns the parser-neutral conversion layers. `corrections/data` holds the versioned correction files that section 13 defines.

Scratch and cache layout:

```text
.scratch/
  specmirror/
    opentype/
      toc/
        toc.json
      pages/
        <slug>.html
      images/
        <local-name>
      staging/
        page-plan.json
      manifest.json
    truetype/
      toc/
        nav.json
      pages/
        <slug>.html
      images/
        <local-name>
      staging/
        page-plan.json
      manifest.json
    reports/
      fetch-opentype-pages.json
      fetch-opentype-images.json
      fetch-truetype-pages.json
      fetch-truetype-images.json
      build-opentype.json
      build-truetype.json
```

Committed output:

```text
docs/
  references/
    opentype/
      README.md
      index.md
      <slug>.md
      images/
        <local-name>
    truetype/
      README.md
      index.md
      <slug>.md
      images/
        <local-name>
  specmirror/
    design.md
```

Git ignores `.scratch/`. The repository commits the generated artifacts under `docs/references/opentype/` and `docs/references/truetype/`.

The build owns the complete `docs/references/<source>/` directory, including the generated `README.md`. It renders into a staging directory and replaces that directory only after the complete build passes validation. Manual edits under those directories are therefore overwritten. Corrections belong in the versioned correction data described in section 13.

The raw discovery artifact under each source's `toc/` directory is audit material. It's not read by `build`. The page plan under `staging/` is fetch state, and `build` never reads it. The manifest is the only authoritative snapshot inventory.

## 4. Sources and discovery

Source adapters are responsible only for discovery, URL scope, slug rules, content extraction, and source-specific link or image behavior. They don't implement HTTP, caching, rendering, or tables.

### 4.1 Microsoft source

Discovery entry point:

```text
https://learn.microsoft.com/en-us/typography/toc.json
```

The adapter stores the raw response as `opentype/toc/toc.json`. It walks the JSON tree recursively. Nodes use `toc_title`, `href`, and `children`. It resolves relative `href` values against the TOC URL's directory, which is:

```text
https://learn.microsoft.com/en-us/typography/
```

The adapter retains a node only when its resolved path is inside the current specification prefix:

```text
/en-us/typography/opentype/spec/
```

The adapter also explicitly rejects the archived-versions subtree by title and by URL path. In the current TOC, the archived subtree is outside the retained prefix, so this guard is defensive.

The page list includes the specification landing page. Page order is the depth-first TOC order, with one supplemental insertion. Duplicate resolved URLs keep the first occurrence. Each retained page records a navigation title from `toc_title` and a section path from its ancestor titles.

The TOC omits the `featurelist` page. When the TOC contains a Feature tags node, the adapter inserts `featurelist` immediately after the last Feature tags child, using the Feature tags section path and the navigation title `Registered features`.

After downloading a page, the adapter requires its `<meta name="source_path">` value. The slug is the final path component without the `.md` suffix. A source path ending in `index.md` maps to the slug `index`, which the build renders as `index.md`. Slugs must be unique case-insensitively across the source. A collision aborts the pages stage.

In the observed pages, the OpenType article spans two `div.content` elements: one contains the page H1 and the other contains the article body. The adapter extracts the H1-bearing content block and the article-body content block, merges them in that order, and removes site chrome.

The adapter accepts a page with a single content block only when that block contains the H1 and the article body. Any other structure aborts the running stage. The article body must not silently fall back to the entire page.

Page images are the resolved URLs of `<img src>` elements in the article. SpecMirror mirrors only `src`. It ignores and reports `srcset` and CSS background images if encountered.

### 4.2 Apple source

Discovery entry point:

```text
https://developer.apple.com/fonts/TrueType-Reference-Manual/RM06/Chap6.html
```

The index page is also a mirrored page. The adapter parses the left `#navBar` navigation links and retains only pages whose last path component matches:

```text
Chap6*.html
```

The adapter excludes other chapters. The index page isn't self-linked in the navigation, so the adapter adds it explicitly as the first page. Duplicate links keep the first occurrence.

Slug mapping:

- `Chap6.html` maps to `index`.
- `Chap6<slug>.html` maps to `<slug>`.
- The slug preserves case, producing values such as `head`, `OS2`, `AATIntro`, and `Tables`.
- The adapter accepts only a filename matching the `Chap6` rule.
- Slugs must be unique case-insensitively. A collision aborts the pages stage.

The adapter stores the raw navigation extraction as `truetype/toc/nav.json` for audit. It records the index URL, index hash, and the ordered raw links. `build` doesn't read this file. The manifest's ordered page list is authoritative.

The adapter extracts article content from `#chapterContent` and discards site chrome outside that element. Page images are the resolved URLs of `<img src>` elements in that content root.

### 4.3 Canonical page inventory

The manifest orders the page array. OpenType uses TOC traversal order. TrueType uses navigation order with the index first.

The images stage preserves it in the manifest, so snapshot hashing is deterministic. Image copying follows the sorted image inventory, not page order. The build never sorts pages by slug unless a specific operation, such as a set comparison, requires sorting internally.

## 5. Fetch pipeline

Fetch has two stages. The pages stage prepares a complete page snapshot, and the images stage completes it into a publishable manifest.

The manifest stays transactional: only the images stage publishes it, and it does so only after every required page and image succeeds. Either stage may add or replace cache files before a later failure. The build verifies every referenced hash and refuses a mixed snapshot.

### 5.1 Stage model

- `fetch pages` refreshes discovery, downloads and validates pages, derives slugs, extracts image candidates, and atomically writes `staging/page-plan.json`. It downloads no images and doesn't change `manifest.json`.
- `fetch images` requires a valid page plan. It verifies every page file and hash before any image network I/O, re-derives image candidates from the verified pages, downloads images, assembles the manifest, and atomically publishes it.
- `fetch all` runs the pages stage and then the images stage in one process. If the images stage fails, the page plan remains available for a retry.
- `fetch images` never refreshes discovery and never downloads or changes pages. Run `fetch pages` before it.
- The page plan is fetch staging state. `build` never reads it.

The pages stage replaces the page plan only after it completes. A failed pages stage leaves the previous plan in place. That plan may no longer match the cache, and the images stage rejects such a mismatch instead of repairing it silently.

The two stages may run minutes or hours apart. The page plan pins the page inventory and page bytes. The images stage fetches image bytes for that pinned inventory. The resulting manifest describes the bytes that each stage fetched, not a server-side atomic revision, and no local time enters the snapshot.

### 5.2 Pages stage

1. Resolve command-line options and validate paths.
2. Refresh discovery:
   - OpenType downloads `toc.json`.
   - TrueType downloads `Chap6.html`.
3. Parse discovery into an ordered candidate page list.
4. Plan page work:
   - reuse a page when its cache file matches the previous manifest or the existing page plan for the same URL
   - download a page when it's new, missing, corrupt, or the command sets `--refresh`.
5. Download and validate pages. Strictly decode each body as UTF-8 before accepting it. The stage tolerates a leading UTF-8 BOM and leaves cache bytes unchanged.
6. Derive OpenType slugs from `source_path` and validate slug uniqueness. For TrueType, validate the filename-derived slug. Validate every slug before moving any downloaded page into the cache, then move the validated page files into place.
7. For every effective page, parse the HTML and discover `<img src>` URLs. Resolution uses the page's absolute requested URL. Drop data URLs, `srcset` variants, and CSS background images from the candidate set, and report them.
8. Record the HTTP `Last-Modified` value for each downloaded page. A reused page carries the value from the source manifest or page plan that supplied its hash.
9. Write `staging/page-plan.json` atomically after every page validates, every slug is unique, and the image candidate set is complete.
10. Write the pages report.

Discovery refresh belongs to the pages stage. The cache reuses pages based on hashes, not modification times.

### 5.3 Page plan

The page plan is a staging artifact with this schema:

```json
{
  "schema_version": 1,
  "source": "opentype",
  "discovery": {
    "requested_url": "https://learn.microsoft.com/en-us/typography/toc.json",
    "raw_file": "toc/toc.json",
    "sha256": "..."
  },
  "pages": [
    {
      "title": "OpenType font file",
      "section": ["OpenType spec"],
      "requested_url": "https://learn.microsoft.com/en-us/typography/opentype/spec/otff",
      "source_path": "typographydocs/opentype/spec/otff.md",
      "slug": "otff",
      "file": "pages/otff.html",
      "sha256": "...",
      "content_type": "text/html",
      "last_modified": "2026-09-17T18:19:04Z"
    }
  ],
  "image_urls": [
    "https://learn.microsoft.com/en-us/typography/opentype/spec/images/otvo_fig1.png"
  ]
}
```

Page entries use exactly the manifest page schema. `pages` preserves discovery order. `image_urls` is the sorted, de-duplicated set of absolute image URLs with no fragment. The plan has no snapshot hash because it isn't a published snapshot. The pages stage serializes it as canonical JSON, writes it atomically, and leaves the previous plan in place on failure.

The images stage validates the plan schema and source, then verifies every page file and hash. It reparses the verified pages, derives the image URL set again, and requires an exact match with `image_urls`. The images stage treats a mismatch as a fetch failure. This check prevents a corrupted or stale plan from producing an incomplete manifest.

### 5.4 Page downloads

A page request follows redirects according to the HTTP client. The pages report may record redirect chains for diagnosis, but the manifest doesn't store a final URL. The resolved absolute requested URL is the page's identity.

Each page's media type must be HTML. The body must be non-empty and valid UTF-8. A page that doesn't meet these conditions aborts the pages stage. The stage downloads page files to temporary files on the same filesystem and moves them into place with an atomic rename after validation.

Because the pages stage reuses pages by default, it doesn't revalidate a page against upstream unless the command uses `--refresh`. This is a deliberate consequence of not using conditional requests.

### 5.5 Images stage

1. Load `staging/page-plan.json` and validate its schema and source.
2. Verify the discovery raw file and hash, then verify every page file and hash in the plan. Stop before any network I/O on a mismatch, and instruct the operator to rerun `fetch pages`.
3. Reparse every verified page, derive the image URL set, and require equality with `image_urls`.
4. Plan image work:
   - reuse an image when its cache file matches the previous manifest
   - download an image when it's new, missing, corrupt, or the command sets `--refresh`.
5. Compute local names for the complete candidate set, including deterministic collision suffixes.
6. Download and validate images. Strictly accept only a non-empty `image/*` resource. The stage writes cache files through temporary files and atomic renames.
7. Assemble the manifest from the page plan and the verified image cache. Pages retain plan order. The manifest sorts images by normalized absolute URL.
8. Write the complete manifest atomically. This step publishes the snapshot.
9. Write the images report.

### 5.6 Image downloads

SpecMirror mirrors only `<img src>` in the effective article content. The images stage resolves image URLs against the page URL and removes fragments. It doesn't mirror data URLs, and it reports them. CSS background images and `srcset` variants are out of scope.

An image response must be a non-empty `image/*` resource. The manifest records the base media type, not response parameters. The cache stores images by normalized URL.

Local image names use the percent-decoded URL basename after replacing characters outside `[A-Za-z0-9._-]` with `_`. The images stage replaces empty, `.` and `..` names with `image`.

If distinct URLs would produce the same local name, every colliding URL receives a deterministic `-<sha256-prefix>` suffix before the extension. The manifest maps each URL to its local name. Rendering never guesses names from URLs.

### 5.7 Failure behavior

The images stage assembles and publishes the manifest only after every required page and image has succeeded. It writes the manifest to a temporary file and atomically replaces `manifest.json`.

If the pages stage fails:

- the previous page plan and manifest remain in place
- the stage publishes no new page plan
- it removes temporary files
- it exits non-zero and records the failure in a pages report when persistent reporting is available.

If the images stage fails:

- the previous manifest remains in place
- the stage publishes no new manifest
- the page plan remains valid for a retry
- it removes temporary files
- it exits non-zero and records the failure in an images report when persistent reporting is available.

A pages stage may replace page files that the previous manifest references. Until the images stage publishes a new manifest, a build may fail snapshot verification. The committed output remains untouched.

A successful pages stage followed by a successful images stage repairs the snapshot. A build must never proceed from a manifest whose referenced hash set doesn't match the files on disk.

Pages removed from discovery disappear from the next page plan and the next manifest. Unreferenced cache files aren't deleted automatically. The stages report them as orphans. The build's whole-directory replacement cleans the committed output, so stale pages don't survive there.

### 5.8 Last-modified

When the pages stage downloads a page, the adapter captures the HTTP `Last-Modified` header. If present, it parses the value and normalizes it to an RFC 3339 UTC string such as:

```text
2026-09-17T18:19:04Z
```

If the header is absent or invalid, the page plan stores `null`. A reused page retains the value from the previous manifest or page plan. Local fetch time never substitutes for this value. The images stage copies the value into the manifest and doesn't contact the page.

For OpenType, the HTTP header is effectively a site-level last-modified value. In the observed snapshot, different specification pages share the same value. The per-page `<meta name="updated_at">` value is different metadata, and front matter exposes it separately as `updated_at`.

## 6. Manifest

The manifest is the single authoritative description of a fetched snapshot. The images stage writes it and copies discovery and page entries from the verified page plan. The pages stage writes only `staging/page-plan.json`, which the images stage consumes and `build` never reads. Raw discovery files are audit inputs and aren't build inputs.

```json
{
  "schema_version": 1,
  "source": "opentype",
  "discovery": {
    "requested_url": "https://learn.microsoft.com/en-us/typography/toc.json",
    "raw_file": "toc/toc.json",
    "sha256": "..."
  },
  "pages": [
    {
      "title": "OpenType font file",
      "section": ["OpenType spec"],
      "requested_url": "https://learn.microsoft.com/en-us/typography/opentype/spec/otff",
      "source_path": "typographydocs/opentype/spec/otff.md",
      "slug": "otff",
      "file": "pages/otff.html",
      "sha256": "...",
      "content_type": "text/html",
      "last_modified": "2026-09-17T18:19:04Z"
    }
  ],
  "images": [
    {
      "requested_url": "https://learn.microsoft.com/en-us/typography/opentype/spec/images/otvo_fig1.png",
      "file": "images/otvo_fig1.png",
      "sha256": "...",
      "content_type": "image/png"
    }
  ],
  "snapshot_sha256": "..."
}
```

Field rules:

- `schema_version` is the manifest schema version.
- `source` is `opentype` or `truetype`.
- `discovery.requested_url` identifies the discovery resource. `discovery.raw_file` is relative to the source cache root.
- `pages` preserves order and contains exactly the retained pages.
- `title` is the navigation title from the TOC or Apple navigation. It's not necessarily the document H1 used in front matter.
- `section` is the ancestor title path for OpenType and a flat path such as `["Chapter 6"]` for TrueType.
- `requested_url` is an absolute URL with no fragment.
- OpenType pages require `source_path`. TrueType pages omit it.
- `file` and image `file` are POSIX-style paths relative to the source cache root.
- `sha256` is the lowercase SHA-256 of the cached file bytes.
- `content_type` is a bare media type such as `text/html` or `image/png`, never a parameterized header value.
- `last_modified` is an RFC 3339 UTC string or `null`.
- The manifest sorts `images` by normalized absolute `requested_url` and includes each URL once. This makes the snapshot hash independent of image-discovery order.
- `final_url` is intentionally absent. Redirects are diagnostic data only.
- `charset` is intentionally absent. UTF-8 is a fetch contract.

For TrueType, `discovery.raw_file` is `pages/index.html`. The extracted `toc/nav.json` is audit-only.

`snapshot_sha256` is the SHA-256 of canonical JSON serialization of the manifest object with the `snapshot_sha256` field removed. Canonical JSON means UTF-8 encoding, sorted object keys, compact separators, and preserved array order. The hashed bytes omit a trailing newline.

A build rejects the snapshot when:

- the manifest is missing or has an unknown schema version
- `snapshot_sha256` doesn't match
- any page or image file is missing
- any page or image hash doesn't match
- a page or source path isn't in the expected scope
- slugs collide case-insensitively
- a required source path or media type is missing.

## 7. Build pipeline

`build` performs no network I/O. The conversion runs in the parser-independent layers that section 7.1 defines, and the build assembles the output only after every page succeeds. The build proceeds in three phases:

Snapshot phase:

1. Load and validate the manifest and `snapshot_sha256`.
2. Verify every referenced page and image file and hash.
3. Decode each page as UTF-8, tolerating a leading BOM.

Per-page phase, in manifest page order:

4. Parse the decoded text into the parser-neutral DOM document.
5. Extract front-matter metadata from the parsed document, following section 8.
6. Extract the source-specific content roots and form the DOM-neutral subtree, following section 7.2.
7. Normalize the subtree, following section 10.1.
8. Convert the normalized subtree into the semantic AST through the element registry and the page builder, following sections 7.3 and 9.
9. Apply page-specific correction rules against the AST, following section 13.
10. Re-merge anchor groups that corrections left on emptied paragraphs, following section 13.5.
11. Table: lower nested tables, following section 12.7.
12. Table: expand row and column spans, following section 12.5.
13. Table: normalize headers, following sections 12.3 and 12.4.
14. Map links, images, and fragments, following section 11.
15. Table: flatten cell blocks into inline content, following section 12.6.
16. Render deterministic Markdown, following section 10.2.

Assembly phase:

17. Generate `README.md`, following section 7.4.
18. Validate the complete output, following section 17.
19. Write to a staging directory and replace `docs/references/<source>/`, following section 7.5.
20. Write the deterministic build report, following section 14.

The steps with the `Table:` prefix form the table sub-pipeline. Their order is strict, including their order relative to the corrections in step 9.

Corrections run before nested-table lowering, so that they see source row and cell positions. Lowering precedes span expansion, span expansion precedes header normalization, and the header line-break rule of section 12.3 runs before multi-row flattening. Cell flattening runs last, because it reduces the flattened cells to inline content for rendering.

The build never reads `toc/toc.json`, `toc/nav.json`, or `staging/page-plan.json`. It never reads raw HTML from a network location, never consults a clock, and never reads generated Markdown as an input.

### 7.1 Conversion layers

The conversion separates parser-independent layers, and data flows through them in one direction:

- `dom.py` owns parsing and the parser-neutral DOM contract. It's the only module that imports BeautifulSoup, and it produces the `DomDocument`, `DomElement`, `DomText`, and `DomComment` nodes that section 16.1 defines.
- `convert/ast.py` owns the AST vocabulary and its tree infrastructure: node classes, identity-based page state, traversal, text extraction, canonical fingerprints, anchor groups, and the fragment map.
- `convert/normalize.py` owns character and text normalization over the neutral subtree: line endings, preformatted whitespace, prose whitespace with quoted-literal preservation, comments, list repair, definition-term spacing, and the effective inline `font-style` state.
- `convert/html_model.py` owns the HTML5 element registry: the accepted element subset, each element's content categories and content model, its legacy aliases, and its conversion intent.
- `convert/markdown_model.py` owns the Markdown construct registry: each CommonMark or GFM construct's level and content model, its canonical marks, the raw HTML subset the renderer may emit, and construct validation.
- `convert/build_page_ast.py` orchestrates conversion from the normalized subtree into the page AST. It dispatches over the element registry's conversion intents, places anchors and style-derived emphasis, handles lists, definition lists, code, tables, and figures, and consumes adapter nodes only.
- `convert/patch.py` owns the AST editing engine: correction rule loading, strict target resolution, the repair primitives, correction node decoding, and the post-correction anchor remerge and attachment check.
- `convert/table.py` owns the table governance sub-pipeline: source-fact capture, nested lowering, span expansion, header normalization, cell flattening, diagnostics, and the table inventory.
- `convert/render.py` serializes the AST to deterministic Markdown through the Markdown construct registry.
- `convert/__init__.py` exposes the pipeline entry points and page-level types as the package facade.

No stage manipulates a BeautifulSoup object, serializes the neutral DOM back to HTML, or reads generated Markdown as an input. The layers confine a parser replacement to `dom.py` and its fixtures, and they define the output contract in exactly one place.

The conversion between the layers is the only place where HTML semantics become Markdown semantics, and no second, string-based path exists.

### 7.2 The DOM neutral subtree

The source adapter selects the content roots of a page, following section 4. The build treats these roots, in extraction order, as the children of one synthetic container. That container and its descendants are the DOM-neutral subtree.

Every later per-page stage traverses only this subtree, and site chrome outside the content roots never re-enters the pipeline. The build extracts front matter from the parsed document before it forms the subtree, because metadata lives outside the content roots.

The subtree obeys the following invariants:

- Node identity is stable. Stages compare nodes by identity, never by value.
- Parent links stay valid. Every repair that moves a node updates its parent link.
- Text extraction has one definition, equivalent to `get_text(" ", strip=True)`. It serves metadata, fingerprints, and diagnostics. It isn't the AST whitespace policy of section 10.1, which preserves significant whitespace.
- The build collects comments as diagnostics, and the conversion ignores them, as section 10.1 specifies.
- The subtree is never serialized back to HTML.
- A missing, duplicated, or malformed content root aborts the build. The article body never falls back to the whole page, as section 4.1 requires.

The subtree is a conversion input, not an HTML5 tree builder and not a general DOM library:

- It doesn't implement foster parenting, formatting-element reconstruction, implicit element closing beyond the documented list repair, or duplicate-attribute precedence.
- Its API is the minimal query surface plus the documented repairs. There are no selectors and no arbitrary mutation.
- Markup it can't represent reaches the AST through the registry or fails the build. It never silently drops content.

### 7.3 Registry-driven conversion

The element registry covers exactly the element subset the build accepts. Each entry declares the element's HTML5 content categories, its content model, its legacy aliases, its conversion intent, and its child mode. The conversion intent names the AST side of the conversion and uses Markdown vocabulary.

HTML5 content categories use different words, and a category never determines an intent by itself: `p` and `div` are both flow content, but `p` maps to a paragraph and `div` is transparent. The strategies are:

- The `block` strategy maps an element to an AST block, such as `p`, the heading elements, `ul`, `ol`, `blockquote`, `pre`, `table`, `dl`, `hr`, and `figure`.
- The `inline` strategy maps an element to AST inlines, such as `em`, `strong`, `code`, `a`, `img`, `br`, `sup`, and `sub`. Section 10.3 defines the mappings.
- The `transparent` strategy contributes the element's children unchanged, for `div`, `span`, and similar wrappers. The children inherit the element's context.
- The `context-only` strategy applies to elements that are valid only inside a specific parent context, such as `li`, `dt`, `dd`, `thead`, `tbody`, `tfoot`, `tr`, `td`, `th`, `caption`, and `figcaption`. The page builder tracks the element context. `html.parser` enforces no context, so a context-only element outside its context is a build failure.
- The `narrowed` strategy restricts the children's mode. The children of `pre` become literal code text. The children of `a` remain inline. The content of `sup` and `sub` follows the digit rule in section 10.3.

A paragraph whose children include a block-level element converts each surrounding inline run into a paragraph and converts the nested block at the same level. This matches HTML rendering for malformed paragraph nesting while preserving every content fragment.

Inline code accepts a nested link as a link whose content is inline code. The page builder flattens any other markup nested inside inline code to literal code text, and still collects every anchor target.

The Markdown construct registry declares, for each construct, its level, the AST content model it accepts, its emphasis marks, and the raw HTML subset it may emit. The registry covers exactly the CommonMark constructs and the GFM extensions the design uses, which are tables, strikethrough, and the raw HTML subset.

The renderer and the output validator both read this registry, so the constructs the renderer may emit and the constructs the validator accepts can't drift apart.

A name missing from the element registry is an unknown tag and fails the build. The registry doesn't model elements outside the accepted subset.

### 7.4 Generated `README`

Each mirror root contains a generated `README.md`. This file provides orientation and complete local navigation for the mirror directory, and it isn't a mirror of an upstream page. A fixed template produces these elements in order:

- a level-one heading naming the mirrored specification
- a paragraph identifying the upstream publication and the retained scope
- the upstream landing URL as a link
- a `Regeneration` section with the source-specific fetch and build commands
- a warning that the build replaces generated files and that corrections belong in correction data.
- a `Pages` section listing every mirrored page

The page list covers every mirrored page exactly once. It follows manifest order and uses the manifest navigation title as link text.

OpenType groups entries under nested bullet labels derived from the manifest section path. When a section path names a page, that page link is the parent bullet. TrueType uses a flat bullet list.

The list includes `index.md` and uses the same local page address mapping as mirrored pages. Section labels are plain text, not links.

The build generates README because it owns the output directory and the page list must stay synchronized with the manifest. The page list provides complete local navigation because the upstream landing pages don't link every mirrored page.

The build fills the template from the source adapter and the manifest. Discovery order puts the specification landing page or manual index first, so the README uses the first page's `requested_url` as the upstream landing URL.

The build uses no local time, environment data, or filesystem order. `README.md` carries no front matter, no HTML, and no comments. Both sources use the same structure. Only the adapter-provided name, scope, landing URL, and source key vary.

### 7.5 Output replacement

The build stages a complete `docs/references/<source>/` tree. This tree includes `README.md`, every Markdown file, and every referenced image. Only after validation does it replace the existing directory. This removes stale pages and images that are no longer in the manifest.

SpecMirror owns generated output files. The build doesn't preserve manual edits. All persistent customizations must live in correction rules.

## 8. Front matter

Every mirrored Markdown page, including `index.md`, begins with YAML front matter. The generated `README.md` is orientation content, not a mirrored page, and carries no front matter. OpenType pages use this fixed field order:

```yaml
---
title: "The OpenType Font File"
description: "OpenType font file specification (OpenType 1.9.1)"
author: "PeterCon"
ms.date: "2024-05-29T00:00:00Z"
updated_at: "2025-03-19T23:08:00Z"
upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/9fd3f7b24062807b6359a7d0b9b8c9ebef16677c/typographydocs/opentype/spec/otff.md"
last-modified: "2026-09-17T18:19:04Z"
---
```

TrueType pages use this fixed field order:

```yaml
---
title: "Glyph Outline Table"
author: "Apple Inc."
last-modified: "2026-01-30T23:10:21Z"
---
```

OpenType mapping:

| Field | Source | Rule |
| --- | --- | --- |
| `title` | Article H1 | Fallback to `og:title`, then `<title>`. |
| `description` | `<meta name="description">` | Omit when missing. |
| `author` | `<meta name="author">` | Omit when missing. |
| `ms.date` | `<meta name="ms.date">` | Normalize to RFC 3339 UTC. Omit when missing. |
| `updated_at` | `<meta name="updated_at">` | Normalize to RFC 3339 UTC. Omit when missing. |
| `upstream_gitcommit` | `<meta name="gitcommit">` | Store the full URL. Omit when missing. |
| `last-modified` | Manifest HTTP value | Emit `null` when missing. |

TrueType mapping:

| Field | Source | Rule |
| --- | --- | --- |
| `title` | Article H1 | Fallback to `omni_page`, then `<title>`. |
| `author` | `<meta name="Author">` | Omit when missing. |
| `last-modified` | Manifest HTTP value | Emit `null` when missing. |

Rules:

- `title` and `last-modified` are always present. The build omits every other field when its source is absent.
- The H1 is the semantic document title. The build uses it directly because meta titles carry site suffixes such as `" - Typography"` and `" - TrueType Reference Manual - Apple Developer"`.
- For OpenType, the H1 lives in a separate title `div.content`. The adapter extracts it before article-body extraction.
- `upstream_gitcommit` holds the full GitHub URL from `<meta name="gitcommit">`. The URL contains the commit ID and the source path. The build doesn't extract the commit ID and doesn't rewrite the URL. It validates the value as `https://github.com/<owner>/<repo>/blob/<commit>/<path>` and fails when the meta tag is present but malformed.
- All three timestamps normalize to RFC 3339 UTC form `YYYY-MM-DDTHH:MM:SSZ`. The build drops fractional seconds and converts offsets to UTC. Invalid values fail the build.
- `ms.date`, `updated_at`, and `last-modified` carry different meanings and never substitute for one another. `ms.date` is the Microsoft Learn content date. `updated_at` is the page update timestamp. `last-modified` is the HTTP protocol value.
- The build emits every present scalar value as a quoted YAML string. Dates remain strings and don't become YAML date objects. A missing `last-modified` renders as `null`.
- Values undergo trimming, whitespace collapsing, entity decoding, and control-character rejection.
- Front matter carries no source URL, charset, final URL, generator name, local fetch time, or build time.
- Front matter comes from metadata elements in the parsed document and never from corrections. A correction can't rewrite front matter.

The manifest navigation title and the front-matter title intentionally have different roles. The former drives manifest ordering and README page list labels. The latter describes the document itself.

## 9. Document tree

The converter operates on a semantic AST, not through string replacement on HTML or Markdown. The page builder produces the AST from the DOM-neutral subtree through the element registry, and the renderer consumes it through the Markdown construct registry that section 7.3 defines. Corrections and table lowering operate on the same tree.

```text
Document
  meta: {
    slug,
    source_url
  }
  blocks: [Block]

Block =
  Heading(level, inlines)
  Paragraph(inlines)
  BlockQuote(blocks)
  List(ordered, start, tight, items: [ListItem])
  ListItem(blocks)
  CodeBlock(info?, text)
  ThematicBreak
  Table(caption?, header, rows)

Inline =
  Text
  Emphasis
  Strong
  Strikethrough(inlines)
  Code(text)
  Link(href, inlines)
  Image(src, alt, title?)
  LineBreak
  RawHtml(element, inlines?)

Table
  caption?: [Inline]
  header: {
    source: "declared" | "none",
    rows: [Row],
    repair_id?: string
  }
  rows: [Row]

Row
  cells: [Cell]

Cell
  role: "th" | "td"
  row_span: int
  col_span: int
  blocks: [Block]
```

Notes:

- Every `Block` and `Inline` node is a CommonMark construct, a GFM extension, or the limited `RawHtml` node. The AST has no source-specific node types. HTML structures without a CommonMark or GFM counterpart, such as figures and definition lists, lower into CommonMark blocks during conversion, following section 10.2.
- `RawHtml` is the only node that carries raw HTML. Its `element` must be `sup`, `sub`, or an anchor-form `a`. It carries no attributes except the `id` of an anchor-form `a`. Its `inlines` are the children the renderer emits inside the element, and an anchor-form `a` has none. `br` isn't raw HTML, because it's the semantic `LineBreak` with a canonical `<br>` rendering. The builder creates `RawHtml` nodes only through registry strategies, and corrections can't construct them. Anchor-form `RawHtml` nodes occur only as the leading inline content of flattened table cells, where they carry the cell's anchor group.
- `List.tight` records whether the renderer separates items without blank lines. The build marks a list loose when an item contains more than one block.
- `Table.header.source` records what the source markup declared. `header.rows` records the effective header after corrections.
- `Table.rows` data rows and header rows are separate. A header repair may move rows between them.
- `Cell.blocks` may temporarily contain a nested `Table`. The build lowers nested tables before rendering.
- `th` cells in the table body remain data cells. They're never promoted automatically to a GFM column header.
- Unsupported structural markup either lowers into CommonMark blocks or causes a build error.
- Source HTML comments aren't AST nodes. The build collects them as diagnostics so that every hidden comment appears in the report.
- The build derives AST node paths from stable positions such as section heading, table ordinal within a section, row index, and cell index. It computes fingerprints over normalized node content and structure.
- The AST never contains presentation-only attributes such as `class`, `style`, `width`, `height`, `border`, `align`, or `valign`. The normalizer records the inline `font-style` state and the page builder emits `Emphasis`, so no style attribute reaches the AST. The loss of all other presentation attributes is intentional.
- Front matter isn't an AST node. The build extracts it from the parsed document before conversion, following section 8, and renders it from the build's own record.

## 10. Normalization and Markdown rendering

### 10.1 Source normalization

Normalization runs on the DOM-neutral subtree before AST construction:

- The page builder traverses `<thead>`, `<tbody>`, and `<tfoot>` in document order and doesn't assume table rows are direct children of `<table>`. This matters because `html.parser` doesn't insert an implicit `tbody`.
- The normalizer flattens list items that the parser nested instead of closing the previous item, updates parent links as it moves them, and reports the repair.
- The normalizer rewrites CRLF and CR line endings as LF in a `<pre>` block and removes exactly one leading newline, matching HTML5 rendering semantics. The build preserves the remaining whitespace.
- The normalizer collapses whitespace runs to single spaces and removes insignificant leading and trailing whitespace.
- Space runs inside straight-quoted spans survive when the run contains only spaces, so padded tag literals such as the four-byte language tag `'WA  '` keep their content. A quoted run that contains a tab or line break collapses to one space.
- Quoted-literal detection is local to one text node. An apostrophe preceded by a letter is a contraction, not a quote delimiter.
- No-break space runs survive so table cells can keep source indentation. Table cells render those runs as `&nbsp;`, while prose renders them as ordinary spaces.
- The normalizer inserts a separating space after a `dfn` element when the source has no whitespace there and both adjacent characters are word characters.
- The parser decodes HTML entities and represents them as Unicode text.
- `<br>` becomes a `LineBreak`.
- During DOM normalization, inline `font-style` is the only CSS declaration with semantic meaning. The normalizer combines the element's inline declaration with the effective style state inherited from its ancestors and records that state for every element. `italic` and `oblique` activate emphasis, `normal` cancels it, and the normalizer ignores and reports other values. Property and value matching is case-insensitive and whitespace-trimmed.
- The page builder emits `Emphasis` around each affected inline run inside the styled element's subtree, including a literal inline code run, and starts a new run when `normal` cancels inherited emphasis. This covers `span`, `p`, `td`, `tr`, and any other content element.
- Style-derived emphasis merges with existing `em` or `i` emphasis rather than nesting duplicates. Nested same-marker emphasis from the source, such as `<i>n<i> ]</i></i>`, merges the same way, because a browser renders one italic run.
- The normalizer reads inline declarations only and doesn't resolve classes or stylesheets. It discards and reports all other CSS declarations.
- The build removes source comments from the AST and logs them.
- The page builder accepts only semantic tags with defined mappings inside the content root. Unknown tags cause a build failure rather than silent loss.

### 10.2 Deterministic output format

Output is UTF-8, uses LF line endings, and ends with a final newline. The renderer follows fixed rules:

- Headings use ATX syntax and preserve source heading levels.
- The renderer separates paragraphs with one blank line.
- Unordered lists use `-`. Ordered lists preserve the source start number. A list renders tight. The build marks a list loose when an item contains more than one block.
- Block quotes use `>` prefixes.
- Code blocks use fenced code. The fence is longer than the longest backtick run in the content. The renderer emits a language info string only when it comes from a recognized source language class.
- Inline code uses backticks, with a delimiter longer than any backtick run in the content.
- A figure lowers to a single paragraph: its images separated by single spaces, followed by the caption in emphasis.
- A definition list lowers during conversion: each term becomes a paragraph in strong emphasis, followed by its definition paragraph, or blocks.
- Thematic breaks render as `---`.
- Section 12 defines table formatting.
- Inline emphasis, strong text, links, images, anchors, and line breaks have canonical renderings declared in the Markdown construct registry.
- The renderer escapes Markdown metacharacters in text where required. The renderer also escapes pipes in table cell text and inline code so they can't split a GFM row. The escaping rules are deterministic and don't depend on a downstream Markdown renderer.

### 10.3 Inline markup policy

| Source | AST / output |
| --- | --- |
| `strong`, `b` | Strong emphasis |
| `del`, `s`, `strike` | GFM strikethrough |
| `em`, `i`, `dfn`, `var` | Emphasis |
| Inline `font-style: italic` or `oblique` | Emphasis around affected inline runs |
| `code`, `tt` | Inline code when outside a code block |
| `a` with `href` | Markdown link, possibly rewritten to a local page |
| `a` with `id` or `name`, no meaningful link | Anchor-form `RawHtml` node |
| `img` | Markdown image with normalized alt text |
| `br` | Literal `<br>` |
| `sup` | Digit-and-space Unicode conversion, otherwise a `RawHtml` node |
| `sub` | Digit-and-space Unicode conversion, otherwise a `RawHtml` node |
| `u` | Plain text, with underline discarded |

The converter maps digits in a text-only `sup` or `sub` node through fixed Unicode tables. For example, `<sup>2</sup>` becomes `²` and `<sub>2</sub>` becomes `₂`. Ordinary spaces remain spaces. Any other node becomes a `RawHtml` node with element `sup` or `sub`, and renders as that element with its content intact. That covers a node with no digit, a character other than a digit or an ordinary space, or an inline element.

`font-style: normal` cancels a style-derived italic context inherited from an ancestor. It doesn't remove emphasis from `em` or `i`.

Unicode conversion preserves visual position but not markup semantics. Copied text contains Unicode superscript or subscript code points, not a `<sup>` or `<sub>` element. Other content keeps its HTML element and inline structure. The build report records each occurrence with its source tag, text, and mode, either `unicode` or `html`.

`u` has no representation within the permitted output HTML subset and no standard GFM equivalent. The build preserves its text and discards its styling, then records the occurrence in the build report. This is an explicit lossy normalization, not a silent conversion.

### 10.4 Allowed HTML and comments

Outside fenced code blocks and inline code, the output validator permits only:

- `<a>` elements with link or anchor attributes required by this design
- `<br>`
- `<sup>` and `<sub>` elements without attributes
- the exact comments `<!-- colspan -->`, `<!-- rowspan -->`, and `<!-- rowspan colspan -->`.

All other tags and comments are validation errors. The permitted subset is the raw HTML subset declared in the Markdown construct registry that section 7.3 defines, and the validator reads the registry rather than a second list.

Source comments never survive. The validator parses the generated Markdown while ignoring fenced and inline code, so code samples may legitimately contain angle brackets and HTML-like text.

### 10.5 Lossy normalizations

The following losses are intentional and reported:

- Site chrome, navigation, scripts, stylesheets, tracking attributes, classes, and inline CSS other than recognized `font-style` values.
- Presentational table attributes and alignment.
- Source HTML comments.
- Underline styling.
- Superscript and subscript markup when digit-and-space Unicode conversion succeeds.
- `srcset` variants and CSS background images.
- Lexical details such as entity spelling, attribute order, and attribute quoting.

The build report records dropped comments, superscript and subscript conversion outcomes, style-derived emphasis mappings, ignored CSS declarations, unsupported underline occurrences, ignored `srcset` attributes, and unresolved links. The build never drops semantic body content without a report entry or a build failure.

## 11. Links, images, and anchors

### 11.1 Page address mapping

The build constructs a lookup from normalized absolute page URLs to manifest pages. Normalization:

- lowercases scheme and host
- removes default ports
- removes the fragment
- resolves dot segments in the path
- preserves query strings and trailing slashes for the primary lookup.

If a link doesn't match the primary key but matches the same path with the opposite trailing-slash convention, the build uses that page. It records the alias in the build report. This handles the OpenType specification landing page without relying on a redirect final URL.

### 11.2 Link rewriting

- A link to a page in the snapshot becomes a relative link to `<slug>.md`.
- A same-page link becomes a fragment-only link after anchor mapping.
- A link to an excluded page, another Apple manual page outside the retained set, an archived OpenType version, or an external site remains an absolute URL.
- The build resolves a relative URL against the source page URL before classification.
- The build externalizes a link to an in-scope URL missing from the manifest to its absolute URL and reports it.
- A fragment that the build can't map to a local anchor produces a page link without the fragment and a warning. The build doesn't emit a knowingly broken local anchor.

### 11.3 Explicit anchors

The build doesn't depend on a Markdown renderer's heading-slug algorithm. It assigns explicit local anchor IDs derived from source names:

```text
anchor-<page-slug>-<sanitized-source>
anchor-<page-slug>-part-<n>
```

The build collects every source anchor target in document order: an `id` attribute on any accepted element, and a `name` attribute on an `a` element. Collection treats anchors as pending positions, not as blocks:

- Pending anchors attach to the next block that renders content. A paragraph that contains only anchor targets produces no block, so its anchors land immediately before the following block, matching the source position.
- An anchor recorded after the paragraph's last rendered content is trailing: it attaches to the next block, not to the start of its own paragraph. Anchors still trailing at the end of a composite subtree stay with the subtree's last block, which keeps a cell's trailing anchor inside that cell.
- The build records a block element's own anchors after flushing the preceding inline run, so an intervening image or phrase can't detach an anchor from its block.
- A composite block such as a table, list, block quote, definition list, or figure converts its subtree under a fresh pending state. Anchors that precede the block attach to the block itself, and anchors recorded inside the subtree belong to their inner positions. This keeps a table's preceding anchors from drifting into its first cell.
- A table row has no block of its own. A `<tr id>` anchor renders at the start of the first cell's content.
- A table cell is a hard position boundary. Anchors inside a cell render as inline anchor-form `RawHtml` at the start of the flattened cell content, and an anchor that outlives the cell's block content stays inside that cell.
- Anchors still pending at the end of the page attach to the last block.

The build merges all anchor targets at one position into one anchor group and renders exactly one `<a id="..."></a>` for it. Consecutive source anchors, including anchors separated by markup that renders nothing, therefore produce one line. Duplicate source names are an upstream fact: the first occurrence in document order wins the fragment mapping, and the build report records every duplicate. The heading id is the preferred canonical source. Otherwise, the group uses the first source name. Every heading carries an anchor group. When the source provides no anchor name for a heading, its group uses the `part` fallback.

The sanitized source keeps basic Latin letters, digits, `.`, `_`, and `-`, collapses other characters to `-`, and falls back to `anchor` when empty. The build truncates long values with a SHA-256 suffix.

Source-name collisions receive a deterministic SHA-256 suffix. Every source fragment in a group maps to the canonical local ID. A per-page map translates upstream fragments to local IDs. Internal fragment links are rewritten through that map.

This policy prevents duplicate IDs that can occur when an explicit anchor and a renderer-generated heading ID use the same source value, and it makes links stable across renderers. The build report retains the source fragment map, every anchor group, and every duplicate source anchor for traceability.

Corrections run after anchor collection, so they can't change group membership. Section 13.5 defines the remerge pass that repairs group placement when a correction empties an anchored paragraph.

Nested tables use a separate generated namespace:

```text
nested-<page-slug>-<n>
```

The build reserves both namespaces and checks all final anchors for uniqueness in the same page. Source-name collisions receive deterministic suffixes. A generated-namespace collision is a build failure.

### 11.4 Images

The build resolves image URLs to manifest image entries. A rendered image points to:

```text
images/<local-name>
```

The local name comes from the manifest, never from ad hoc URL parsing at render time. A missing manifest image entry or missing cache file is a build failure. The build normalizes alt text but otherwise preserves it. It preserves the optional source image title, if present and meaningful, as the Markdown image title.

Images referenced from code blocks aren't rewritten, because code content is literal.

### 11.5 `README` page list

The README page list links to every mirrored page through the same page address mapping as mirrored pages. Entries follow manifest order. OpenType groups them under nested bullet labels from the manifest, and TrueType uses a flat list. Section labels are plain text, not links. No mirrored page, including `index.md`, carries generated navigation.

## 12. Tables

### 12.1 Header detection

The build derives header state only from source structure:

- If `<thead>` is present, the build treats its rows as declared header rows.
- If there is no `<thead>` and every cell in the first row is `<th>`, the first row is a declared header row.
- Otherwise the table is headerless.

The build uses no content-based heuristics. It never treats a bold row, a first row with a particular appearance, or an all-uppercase row as a header. The build preserves `th` cells in the table body as data and reports them. They aren't automatically column headers.

### 12.2 True headerless tables

GFM requires a header row. A table with no effective header renders a synthetic empty header:

```markdown
|  |  |
| --- | --- |
| ... | ... |
```

All source rows remain data rows. The build invents no placeholder labels. The build report records `declared_header: "none"` and `rendered_header: "synthetic-empty"`.

### 12.3 Mis-marked first rows

A source may declare a header row that's semantically data, or omit a header that should exist. This is page-specific semantic repair, not automatic detection. It's expressed with the `set_table_header` correction primitive:

- `mode: "none"` demotes the declared header rows into data rows and makes the table headerless.
- `mode: "rows"` promotes the listed source rows to the header and demotes all other rows to data.

Source row indices refer to the pre-repair table row sequence, including any declared header rows. The build rejects multiple header rules for one table. Each rule requires an expected header fingerprint, row count, and column count. A mismatch is a build failure.

Promoted header rows lose strong emphasis. GFM renders header cells in bold, so a source `<strong>` used to simulate a header would otherwise add redundant `**` markers.

Header normalization removes source line breaks from header cells and removes whitespace at fragment edges. A boundary next to punctuation or an underscore joins without a space, so identifier and punctuated-compound fragments stay intact. All other boundaries collapse to one space. This runs before multi-row flattening, so separators introduced between header rows remain.

This supports both real headerless tables and tables whose first data row was mistakenly marked as a header, without making either decision heuristically.

### 12.4 Multi-row headers

GFM permits only one header row. After span expansion, the build flattens multiple effective header rows column by column. It joins non-empty fragments for a column top to bottom with `<br>`. Empty columns produce empty header cells. The build report records every flattening.

The build fails and requires a correction when a header cell contains block content that it can't reduce to inline content without ambiguity. It doesn't silently discard the block structure.

### 12.5 Row and column spans

The AST retains `row_span` and `col_span`. Before rendering, the build expands spans into a rectangular grid. The complete content remains in the primary cell, which occupies the top-left position of the span. Every covered cell contains exactly one placeholder comment:

| Coverage | Placeholder |
| --- | --- |
| Covered horizontally | `<!-- colspan -->` |
| Covered vertically | `<!-- rowspan -->` |
| Covered in both directions | `<!-- rowspan colspan -->` |

The primary content is never duplicated. Span values must be positive integers and must fit within the table. A covered cell that contains source content is a build failure, because placing the content in both the primary and covered positions would duplicate or reinterpret it. The build report records span counts.

### 12.6 Cell block content

GFM table cells are inline containers. The build flattens block content in a data cell deterministically:

- The build renders inline content in order.
- Paragraph and list boundaries become `<br>`.
- The build lifts nested tables before this step, following section 12.7, so no nested table remains inside a cell.
- A code block in a table cell isn't representable without ambiguity, so it causes a build failure and requires a correction.
- Content that the build can't represent without ambiguity causes a build failure and requires a correction.

This policy is deliberately fail-closed. It prevents a table cell from silently losing a list, code block, or nested structure.

### 12.7 Nested tables

Nested tables remain inside their parent cell until after the correction engine applies all rules. Lowering then proceeds in document order:

1. Assign the nested table an anchor ID of the form `nested-<page-slug>-<n>`.
2. Replace the nested table in the parent cell with an in-place Markdown link to that anchor.
3. After the main table, emit the anchor, a fixed description, and the lifted table.
4. Repeat recursively for nested tables inside lifted tables.

The fixed description identifies the source position, for example:

```text
The following table was originally nested in row 4, cell 2 of the table above.
```

The build uses fixed in-place link text. The source row and cell numbers are one-based and refer to the source table before span expansion.

Anchor groups attached to the lifted table move onto the in-place link, so anchors that preceded the nested table in the source cell keep their rendered position. The build emits lifted tables in document order. The build report records the anchor, source location, nesting depth, dimensions, and fingerprint of each lifted table.

No nested table remains in the rendered output. A generated anchor collision is a build failure.

### 12.8 Table inventory

The build report contains an inventory entry for every table:

- page and section path
- table ordinal within the section
- source row and column counts
- declared header state and header fingerprint
- first data-row fingerprint
- effective header after repairs
- span counts
- nested table count and lifted anchors
- rendered header strategy, `declared` or `synthetic-empty`
- applied correction IDs.

This inventory is the authoring surface for page-specific header and text repairs. It contains structural facts, not automatic judgments that a table is wrong.

### 12.9 Captions and presentation

If a table has a caption, it's rendered as an emphasized paragraph separated from the table by one blank line, and recorded in the report. The caption keeps its inline content, including code, emphasis, and links. Table alignment, `valign`, borders, widths, and cell styling aren't preserved. Their loss is part of the documented presentation loss.

### 12.10 Table governance

Tables undergo the most structural change in the build, so the design governs that change explicitly. The governance rules are:

- The build changes table structure through exactly two mechanisms: a shared normalizer that applies to every table, or a page-specific correction rule with a reported rule ID. There is no third mechanism and no heuristic.
- Every table passes through three states: the source structure, the effective structure after corrections, and the rendered structure after lowering, span expansion, and cell flattening. The inventory records structural facts for all three states.
- The inventory contains exactly one entry per rendered table, and the build fails when a rendered table has no inventory entry.
- Cell content exists exactly once. Span expansion inserts placeholder comments, nested lifting moves content, and cell flattening reduces blocks. No step duplicates or drops cell content silently.
- Every semantic repair is traceable. The `set_table_header` rule records its rule ID as the table's `repair_id` that section 9 defines, and the inventory lists every applied correction ID.
- The inventory is the authoring surface for repairs. An author reads the header state, fingerprints, and dimensions from the build report, writes a correction rule, and rebuilds. Stale rules fail the build loudly through their expected fingerprints and match counts.
- Governance never judges that a table is wrong. Only the source audit makes that decision, and it expresses the decision as correction data.

## 13. Corrections and repair primitives

Corrections form versioned data that the build applies to the AST before structural lowering and rendering. They aren't edits to generated Markdown and never patch raw HTML strings.

Correction files live under:

```text
scripts/specmirror/corrections/data/<source>/<page-slug>.json
```

The build loads each file deterministically by page slug and applies rules within a file in array order. Rules may not reference another page. The source audit adds page entries as it identifies them.

### 13.1 Rule schema

A rule contains:

```json
{
  "id": "otff-0001",
  "op": "replace_text",
  "target": {
    "section_heading": ["The OpenType font file", "Font tables"],
    "table": 2,
    "row": 3,
    "cell": 1
  },
  "find": "exact source text",
  "replace": "corrected text",
  "expect": {
    "count": 1
  },
  "note": "Source of the erratum and reason for the correction."
}
```

Required properties:

- `id` is unique within the source and stable over time.
- `op` is one of the repair primitives.
- `target` is a structural selector. It may address a section heading path, block ordinal within a section, table ordinal, row, cell, or inline position. Table and block ordinals are one-based. A block ordinal numbers the top-level blocks of a section, so a rule reaches content inside a table with `table`, `row`, and `cell` instead.

Additional properties:

- `expect` contains strict expectations. Text replacements require an exact match count. Structural repairs require a content or structure fingerprint.
- `note` records the reason for the correction.

The target must resolve unambiguously. The build fails and reports the rule ID when a section heading path no longer exists, a table ordinal points to a different table, a fingerprint differs, or the expected match count isn't met. Corrections are never applied approximately.

### 13.2 Primitives

| Primitive | AST effect |
| --- | --- |
| `replace_text` | Replaces an exact substring inside one text node at the target. The match count must equal the expected count. |
| `replace_inline` | Replaces a matched inline node sequence with new inline nodes. |
| `replace_block` | Replaces one block node with a new block subtree. |
| `insert_block` | Inserts blocks before or after a target block. |
| `remove_node` | Removes a targeted block or inline node. |
| `retarget_link` | Changes a link target after verifying the expected old target. |
| `retarget_image` | Changes an image source or alt text after verifying the expected old source. |
| `set_table_header` | Changes the effective header rows or removes the header entirely. |

Corrections construct CommonMark and GFM AST nodes only. They can't inject raw HTML, raw Markdown, scripts, or comments, can't construct `RawHtml` nodes, and never operate on the DOM-neutral subtree or on generated Markdown.

Every node a rule constructs must satisfy the Markdown construct registry's content model, so a rule that builds an unrenderable AST fails the build. This preserves the output contract and prevents page rules from becoming a second converter.

`replace_text` intentionally operates within a single text node. If source text spans multiple inline nodes, the correction must use `replace_inline`. This avoids ambiguous matching across formatting boundaries.

### 13.3 Order of correction rules

Per page:

1. Parse and normalize the source.
2. Build the AST.
3. Apply correction rules in file order.
4. Re-merge anchor groups left on emptied paragraphs, following section 13.5.
5. Lower nested tables.
6. Expand spans.
7. Normalize headers.
8. Map links, images, and anchors.
9. Flatten table cell blocks.
10. Render Markdown.

Header corrections therefore see the source table structure before span expansion and can move header rows unambiguously. Nested-table lifting happens after corrections so a correction can target a table inside a cell by its source position.

A correction that no longer matches due to an upstream change fails the build. This is intentional. While upstream bytes remain unchanged, the correction remains effective across rebuilds.

A parser or renderer upgrade that changes conversion output can also invalidate correction expectations. The build fails, and the source audit updates the correction data as part of the migration that section 15 defines.

### 13.4 Normalizers versus corrections

Shared normalizers handle mechanical behavior:

- `tbody` handling
- preformatted whitespace
- entity decoding
- URL resolution
- headerless table synthesis
- table header line-break removal and spacing
- span expansion
- nested-table lifting
- link and image mapping.

Corrections handle page-specific semantic judgments:

- correcting source text
- choosing a real header for a mis-marked table
- removing a declaration that's an error
- retargeting a broken link.

A behavior that applies to all pages belongs in a normalizer, not in repeated correction entries.

### 13.5 Anchor remerge after corrections

A correction can empty a paragraph that carried an anchor group, leaving a lone anchor line before the following block. After corrections, the build moves such a group onto the next top-level block, merging it into that block's group when one exists.

The surviving group keeps its canonical id, the merged group's names are the emptied paragraph's names followed by the surviving names, and the build recomputes the fragment map and the duplicate list from the merged groups.

The pass considers only top-level paragraphs. A table cell's anchor-holding paragraph is a hard boundary and never moves. A group whose target block is the page's last block stays put.

The remerge is traceable. The page report records every moved group's names and the canonical id it merged into, or a null target when it became the next block's only group.

After the remerge, the build verifies that every anchor group's block still exists in the document and fails loudly otherwise. Without this check, a correction that replaces or removes an anchored block would silently produce a fragment that maps to an anchor no output renders.

## 14. Reports

The build writes reports under `.scratch/specmirror/reports/`. They're diagnostics and aren't inputs to a build.

### 14.1 Fetch reports

Each fetch stage writes a separate report. The pages report at `reports/fetch-<source>-pages.json` records:

- source and stage
- discovery URL, raw file, and hash
- counts of added, removed, reused, and downloaded pages
- image candidate count
- page-plan file hash
- orphan page cache files
- download failures and HTTP status codes
- redirect chains
- warnings.

The images report at `reports/fetch-<source>-images.json` records:

- source and stage
- page-plan file hash and page verification summary
- counts of reused, downloaded, pending, and failed images
- orphan image cache files
- old and new manifest hashes
- manifest `snapshot_sha256`
- download failures and HTTP status codes
- redirect chains
- warnings.

`fetch all` writes both reports. Fetch reports may contain run-specific information. They're never consulted by `build`.

### 14.2 Build report

The build report is deterministic and contains no local timestamps, durations, absolute paths, or random identifiers. It records:

- source and manifest `snapshot_sha256`
- ordered page list and page output hashes, including `index.md`
- generated `README.md` hash
- front-matter fields and provenance: `h1`, `og:title`, `title`, `meta:description`, `meta:author`, `meta:ms.date`, `meta:updated_at`, `meta:gitcommit`, `http:last-modified`
- applied correction IDs
- anchor groups re-merged after corrections, with names and the canonical id each merged into
- inline style mappings, including style-derived emphasis and ignored CSS declarations
- dropped source comments with page, path, text, and fingerprint
- DOM tree repairs applied before conversion, such as flattened list items
- superscript and subscript conversion outcomes, including source tag, text, and rendered mode
- underline occurrences
- ignored `srcset` attributes
- generated anchors, anchor groups, duplicate source anchors, and the upstream-fragment map
- table inventory from section 12.8
- lifted nested tables and their anchors
- internal links externalized or missing fragments
- link records for every external, unsupported, or unresolved link target
- output validation summary
- warnings and failures.

Authors can use the build report to write corrections without re-parsing HTML manually. The report stays uncommitted unless someone intentionally copies it.

## 15. Reproducibility

A build is reproducible when the same input closure produces byte-identical output. The input closure is:

- the manifest
- every page and image file referenced by the manifest, at the recorded hashes
- correction files
- all SpecMirror source code, including the source adapters, converter, renderer, and validators
- configuration
- pinned Python and dependency versions, including the HTML parser.

Network state isn't part of the build closure. The snapshot manifest pins the fetched bytes. The build doesn't use wall-clock time, random values, locale-dependent formatting, environment-dependent path separators, filesystem enumeration order, or file modification times.

The following are deterministic:

- page order from the manifest
- heading and anchor order from document order
- section order from source structure
- sorted manifest image order and image copying order, neither of which depends on filesystem enumeration
- JSON report serialization with sorted keys
- YAML front-matter field order
- Markdown line endings and final newline
- `README.md` content, including its page list, from the fixed template, which depends only on the source adapter and manifest
- escaping and table layout.

`last-modified` is upstream data stored in the manifest. It doesn't change during a local rebuild.

`build --check` builds a complete candidate tree in a temporary directory and compares it with the committed `docs/references/<source>/` tree. It compares the exact file set and file hashes, including `README.md`. Any difference is a non-zero exit. This is the reproducibility gate for CI and for parser or renderer upgrades.

A parser upgrade, Python upgrade, or dependency upgrade may legitimately change output. It's treated as a migration: rebuild everything, inspect the diff, update fixtures, and commit the new output intentionally. Parser versions are therefore part of the reproducibility contract, not an implementation detail.

## 16. Parser

### 16.1 Approved choice

The runtime parser is BeautifulSoup 4 with Python's standard-library `html.parser` backend. The project approves this dependency. Implementation adds pinned BeautifulSoup and soupsieve versions to `pyproject.toml` and `uv.lock`.

The parser sits behind `dom.py`, which owns parsing, text extraction, and the parser-independent DOM contract. `dom.py` converts BeautifulSoup nodes into `DomDocument`, `DomElement`, `DomText`, and `DomComment` nodes. Every other module traverses only these adapter types, and only `dom.py` imports BeautifulSoup.

The HTML5 content categories and content models live in `convert/html_model.py`, the Markdown constructs live in `convert/markdown_model.py`, and the conversion between them lives in `convert/build_page_ast.py`, which consumes adapter nodes only.

A parser replacement therefore changes `dom.py` and the parser fixtures, not the page builder, table normalization, source adapters, or renderer. Parser semantics can still change the resulting tree and output, so a replacement remains a Section 15 migration.

The build passes decoded `str` input to the parser. It never allows encoding sniffing from bytes, because the manifest intentionally omits charset and encoding sniffing would introduce an unnecessary nondeterministic input.

### 16.2 Evaluation

The evaluation covered ten representative pages: five OpenType pages and five Apple pages, including table-heavy pages and the image-heavy variations overview. The comparison reference was `html5lib`, which served only for evaluation. The tested versions were BeautifulSoup 4.15.0, soupsieve 3.0.3, and Python 3.13.15.

Results on the extracted content roots:

| Check | Result |
| --- | --- |
| Normalized content text | Identical on 10/10 pages |
| Tags and attributes after removing structural `tbody` wrappers | Identical on 10/10 pages |
| Links, images, row and cell counts, `colspan`, `rowspan` | Preserved |
| Canonical tree after documented normalizations | Identical on 10/10 pages |
| Malformed `tr`/`td` parentage in content | None observed |
| Duplicate attributes in content | None observed |

Observed differences:

- `html.parser` leaves rows directly under `<table>` where HTML5 inserts `<tbody>`. The source adapter must not assume `tbody` exists on either source.
- `html.parser` preserves one leading newline after `<pre>` and preserves CRLF, while HTML5 drops the first newline and normalizes line endings. The build normalizes both cases explicitly.
- The parser discards empty text nodes.
- Two hidden content comments exist in the sampled pages. The AST doesn't render them. The build report records them.

Behavior outside the current corpus is the real risk. `html.parser` isn't an HTML5 tree builder. It doesn't implement implicit paragraph closing, foster parenting, formatting-element reconstruction, or HTML5 duplicate-attribute precedence.

Small malformed fragments can therefore produce a different tree than a browser. The source adapter must fail closed on structural invariants, unknown content tags, and invalid table nesting rather than accepting whatever tree the parser recovered.

### 16.3 Required parser safeguards

- Parse decoded text, not bytes.
- Pin BeautifulSoup, soupsieve, and Python versions through the lockfile.
- Confine BeautifulSoup imports to `dom.py`.
- Preserve adapter node identity and parent links across tree repair.
- Keep adapter text extraction equivalent to `get_text(" ", strip=True)`.
- Normalize table section wrappers and `<pre>` whitespace before AST assertions.
- Fail when the expected content root is missing or duplicated.
- Fail on unknown content tags.
- Fail on invalid table parentage, invalid spans, or covered cells with content.
- Never serialize the DOM back to HTML as part of output generation.
- Include stored source fixtures and parser-regression tests.
- Record parser and runtime versions in build diagnostics.

## 17. Validation and failure behavior

Fetch stages and builds fail closed. They publish no partial page plan or manifest.

Fetch validation:

- page-plan schema and source
- discovery raw file and hash
- page file and hash coverage before image network I/O
- image URL set equality after reparse of the verified pages
- image media types and non-empty bodies.

Build input validation:

- manifest schema and `snapshot_sha256`
- page/image files and hashes
- UTF-8 page decoding
- scoped URLs and source paths
- slug uniqueness
- expected source metadata for OpenType
- expected content roots for both sources.

AST and correction validation:

- every correction target resolves
- every expected match count is exact
- fingerprints and dimensions match
- no conflicting header repairs
- every recognized inline `font-style` maps to `Emphasis` and no style attribute enters the AST
- table spans are valid
- covered cells don't contain content
- nested table anchors don't collide
- the table inventory covers every rendered table.

Output validation:

- `README.md` and `index.md` exist
- `README.md` contains the required orientation elements, complete page list, and no front matter
- the README page list covers every mirrored page exactly once in manifest order
- front matter parses and has a non-empty title
- every mirrored page has the required front matter
- no nested tables remain
- every table is rectangular
- every image link resolves to a copied image
- every internal page link resolves
- no raw HTML tags except `<a>`, `<br>`, `<sup>`, and `<sub>` outside code
- no HTML comments except the three exact span placeholders
- no source comments survive
- row/column span placeholders are exact
- Markdown is valid UTF-8 with LF endings and a final newline.

Any validation failure aborts the current fetch stage or build. Fetch stages never write committed output. A build writes to a staging directory first, so a failed build leaves the previous committed output untouched. The applicable report describes the failed rule, page, and reason.

## 18. Testing strategy

The implementation must include:

- source discovery tests using saved TOC and navigation fixtures
- scope, exclusion, ordering, slug, and collision tests
- manifest schema, canonical hash, and incomplete-snapshot tests
- page-plan schema, canonical serialization, and stale-plan rejection tests
- staged-fetch tests proving that `fetch pages` writes a page plan without changing the manifest
- staged-fetch tests proving that `fetch images` requires a valid page plan, verifies page hashes before image I/O, and compares the reparsed image URL set with the plan
- staged-fetch equivalence tests proving that `fetch pages` followed by `fetch images` produces the same manifest as `fetch all`
- cache reuse tests across stages and `--refresh` scope tests for each stage
- tests proving that the images stage never refreshes discovery or downloads pages
- strict UTF-8 and malformed-page tests
- front-matter extraction tests for both sources, including all OpenType fields, missing optional fields, timestamp normalization, and malformed `gitcommit` URLs
- parser fixture tests for content roots, implicit `tbody`, `<pre>` whitespace, comments, and unknown tags
- DOM adapter contract tests for node identity, text extraction, attributes, queries, parent links, and list repair
- HTML5 element registry contract tests for content categories, content models, and legacy elements
- conversion strategy registry tests for element coverage, the accepted subset, and the derived child modes
- Markdown construct registry tests for levels, content models, emphasis marks, and the raw HTML subset
- page-builder dispatch tests for context-only, table-only, and narrowed elements
- inline `font-style` tests for `italic` and `oblique` on `span`, paragraph, cell, and row scopes, including inheritance and `normal` cancellation
- tests proving that style-derived emphasis merges with `em` and `i` without duplicate emphasis nodes
- tests proving that no `style` attribute reaches the AST or output and that the report records ignored CSS declarations
- a fixture test based on the Chap6Zapf italic examples
- superscript and subscript tests for digit-and-space Unicode conversion, `RawHtml` preservation of other content, and report entries
- tests for GFM strikethrough rendering of `del`, `s`, and `strike`
- table cell tests for no-break space indentation rendered as `&nbsp;`
- AST and renderer golden tests
- AST alignment tests proving that every AST node is a CommonMark construct, a GFM extension, or the limited `RawHtml` node, and that corrections can't construct `RawHtml` nodes
- link, image, fragment, and anchor mapping tests, including source sanitization, heading-priority merging, and deterministic collision suffixes
- table tests for declared headers, true headerless tables, mis-marked headers, table header line-break removal and spacing, multi-row headers, spans, cell block content, and nested lifting
- table governance tests proving that every rendered table has exactly one inventory entry and that `set_table_header` records its rule ID as `repair_id`
- correction tests for exact matches, stale targets, conflicting rules, and report output
- output validator tests that assert disallowed tags and comments fail while code blocks stay exempt
- output layout tests for both `docs/references/<source>/` roots, including the required `README.md` and `index.md`
- README page list tests proving complete coverage, manifest order, OpenType section grouping, TrueType flat layout, and resolvable local links
- README golden tests for required elements, absent front matter, and deterministic bytes for both sources
- index rendering tests proving that `index.md` uses the normal page pipeline and receives no generated navigation
- reproducibility tests that build twice and compare bytes, including `README.md`
- dry-run network matrix tests proving that `fetch pages --dry-run` always requests discovery, makes no image requests, skips pages with a trusted cached hash, and requests every page under `--refresh`
- tests proving that `fetch images --dry-run` makes no network requests
- `fetch pages --dry-run`, `fetch images --dry-run`, `build --dry-run`, and `build --check` tests that assert no persistent writes
- failure tests that assert a failed pages stage preserves the previous page plan and manifest, a failed images stage preserves the previous manifest, and the previous committed output survives
- module-boundary tests that reject imports from `fetch` to `build`, from `build` to `fetch`, from pure layers to main lines or reports, network imports outside `fetch/http.py`, and BeautifulSoup imports outside `dom.py`

No implementation or test code is part of this design change.

### 18.1 Quality gates

The repository enforces these gates:

- `ruff check` and `ruff format --check` pass for Python code.
- `pyright` passes in strict mode.
- `pytest` passes.
- `vale` passes for `docs/specmirror/design.md`, implementation documentation, and the generated `docs/references/*/README.md` files with zero alerts, including suggestions. Vale skips the rest of the mirror content because it reproduces upstream text.
- `build --check` passes.

## 19. Deferred work

No design decisions remain open. The following work is intentionally deferred:

1. **Concrete correction entries.** The design specifies the framework, and the source audit has added initial entries for the baseline table, the features_uz page, the TrueType index page, the glyf page, the kerx page, the morx page, the name page, the OS/2 page, the post page, and the Zapf page. The audit adds further page-specific entries as it proceeds.

## Appendix: end-to-end invariants

The following statements should remain true after every implementation change:

- The pages and images fetch stages are the only network stages.
- The manifest is the only authoritative snapshot inventory. The page plan is staging state, and `build` never reads it.
- Every mirror root contains a generated `README.md`.
- The README page list covers every mirrored page exactly once.
- `index.md` uses the same page pipeline as every other mirrored page and carries no generated navigation.
- Build is offline and deterministic from the manifest, cached bytes, corrections, and code.
- No generated output depends on local time, locale, filesystem order, or modification times.
- The build applies no page-specific semantic repair without a strict rule and a reported rule ID.
- The conversion either maps inline `font-style` to `Emphasis` or reports it as unsupported. No style attribute survives.
- No raw HTML survives outside the allowed anchors, line breaks, superscript and subscript elements, and exact span comments.
- Every converted element resolves through the element registry, and an unknown tag fails the build.
- The build limits `RawHtml` nodes to `sup`, `sub`, and anchor-form `a`, and corrections can't construct them.
- No table is silently flattened, truncated, or duplicated.
- Every rendered table has one inventory entry, and every semantic table repair carries a rule ID.
- Every intentional information loss is either reported or is a documented rendering consequence.
