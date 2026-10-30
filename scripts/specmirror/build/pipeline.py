"""The build pipeline: snapshot verification, conversion, and output assembly."""

from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from ..convert import patch, table
from ..convert.ast import AnchorGroup, PageAst
from ..convert.build_page_ast import build_page_ast
from ..convert.markdown_model import validate_page_ast
from ..convert.normalize import NormalizationResult, normalize_roots
from ..convert.render import render_page
from ..dom import (
    DomDocument,
    DomElement,
    decode_utf8,
    find_all,
    has_attribute,
    parse_html,
)
from ..errors import BuildError
from ..manifest import load_manifest
from ..notice import NoticeJson, NoticeKind
from ..paths import SourcePaths
from ..progress import Log, noop_log
from ..schema import Manifest, PageEntry
from ..sources import get_source
from ..sources.base import SourceAdapter
from ..storage import file_matches_hash, list_tree_files, sha256_bytes
from .front_matter import FrontMatter, extract_front_matter
from .links import PageMaps, build_page_maps, check_anchor_uniqueness, map_page_links
from .readme import ReadmeInput, render_readme
from .validate import ValidationSummary, require_no_failures, validate_output

CORRECTIONS_ROOT = Path(__file__).resolve().parent.parent / "corrections" / "data"


def _new_anchor_groups_by_block() -> dict[int, AnchorGroup]:
    return {}


def _new_anchor_remerges() -> list[patch.AnchorRemerge]:
    return []


@dataclass(slots=True)
class PageWork:
    entry: PageEntry
    document: DomDocument
    roots: tuple[DomElement, ...]
    ast: PageAst
    normalization: NormalizationResult
    corrections: list[str]
    table_ledger: table.TableLedger = field(default_factory=table.TableLedger)
    anchor_groups_by_block: dict[int, AnchorGroup] = field(
        default_factory=_new_anchor_groups_by_block
    )
    anchor_remerges: list[patch.AnchorRemerge] = field(
        default_factory=_new_anchor_remerges
    )


@dataclass(slots=True)
class BuildOutcome:
    source: str
    dry_run: bool
    check: bool
    page_count: int
    snapshot_sha256: str
    page_hashes: dict[str, str]
    readme_sha256: str | None
    changed: bool | None
    report: dict[str, object]


def run_build(
    source: str,
    *,
    dry_run: bool,
    check: bool,
    paths: SourcePaths,
    log: Log | None = None,
) -> BuildOutcome:
    logger = log or noop_log
    adapter = get_source(source)
    if source != paths.source:
        raise BuildError("source does not match the configured paths")
    loaded = load_manifest(paths.manifest_path, expected_source=source, required=True)
    if loaded is None:
        raise BuildError(f"manifest is missing: {paths.manifest_path}")
    manifest = loaded.manifest
    _verify_snapshot(manifest, paths)

    works = _convert_pages(adapter, manifest, paths, logger)
    maps = build_page_maps(manifest, {work.entry.slug: work.ast for work in works})
    page_files: dict[str, bytes] = {}
    page_records: list[dict[str, object]] = []
    for work in works:
        body = _finish_page(work, adapter, maps, logger)
        front = extract_front_matter(
            work.document,
            spec=adapter.front_matter,
            slug=work.entry.slug,
            last_modified=work.entry.last_modified,
        )
        data = f"{front.to_yaml()}\n\n{body}\n".encode()
        page_files[f"{work.entry.slug}.md"] = data
        page_records.append(_page_record(work, front, data))

    readme = render_readme(ReadmeInput(manifest=manifest, adapter=adapter))
    files: dict[str, bytes] = {"README.md": readme.encode("utf-8"), **page_files}
    _copy_images(manifest, paths, files)

    summary = ValidationSummary()
    validate_output(files, manifest, summary)
    require_no_failures(summary, what=f"build for {source}")

    report = _build_report(
        source, manifest, works, maps, page_records, readme, summary, check=check
    )
    if check:
        return BuildOutcome(
            source=source,
            dry_run=False,
            check=True,
            page_count=len(works),
            snapshot_sha256=manifest.snapshot_sha256(),
            page_hashes={name: sha256_bytes(data) for name, data in page_files.items()},
            readme_sha256=sha256_bytes(readme.encode("utf-8")),
            changed=_compare_with_committed(files, paths),
            report=report,
        )
    if dry_run:
        return BuildOutcome(
            source=source,
            dry_run=True,
            check=False,
            page_count=len(works),
            snapshot_sha256=manifest.snapshot_sha256(),
            page_hashes={name: sha256_bytes(data) for name, data in page_files.items()},
            readme_sha256=sha256_bytes(readme.encode("utf-8")),
            changed=None,
            report=report,
        )
    changed = _compare_with_committed(files, paths)
    _write_output(files, paths, logger)
    from ..reports.build import write_build_report

    write_build_report(paths, report, dry_run=False, log=logger)
    return BuildOutcome(
        source=source,
        dry_run=False,
        check=False,
        page_count=len(works),
        snapshot_sha256=manifest.snapshot_sha256(),
        page_hashes={name: sha256_bytes(data) for name, data in page_files.items()},
        readme_sha256=sha256_bytes(readme.encode("utf-8")),
        changed=changed,
        report=report,
    )


# ------------------------------------------------------------------ snapshot


def _verify_snapshot(manifest: Manifest, paths: SourcePaths) -> None:
    for page in manifest.pages:
        if not file_matches_hash(paths.cache_path(page.file), page.sha256):
            raise BuildError(
                f"page cache does not match the manifest: {page.file}; "
                f"rerun 'fetch pages' for {paths.source}"
            )
    for image in manifest.images:
        if not file_matches_hash(paths.cache_path(image.file), image.sha256):
            raise BuildError(
                f"image cache does not match the manifest: {image.file}; "
                f"rerun 'fetch images' for {paths.source}"
            )


# ---------------------------------------------------------------- conversion


def _convert_pages(
    adapter: SourceAdapter,
    manifest: Manifest,
    paths: SourcePaths,
    log: Log,
) -> list[PageWork]:
    works: list[PageWork] = []
    for page in manifest.pages:
        log(f"{adapter.key} build: converting {page.slug}")
        body = paths.cache_path(page.file).read_bytes()
        text = decode_utf8(body, what=f"page {page.requested_url}")
        document = parse_html(text)
        roots = adapter.article_roots(document)
        normalization = NormalizationResult()
        normalize_roots(roots, page=page.slug, result=normalization)
        ast = build_page_ast(
            roots,
            page=page.slug,
            slug=page.slug,
            page_url=page.requested_url,
            italic=normalization.italic,
        )
        ledger = table.TableLedger()
        ledger.capture_sources(ast.document.blocks)
        engine = patch.PatchEngine(page=page.slug, slug=page.slug)
        rules = patch.load_rules(CORRECTIONS_ROOT, source=adapter.key, slug=page.slug)
        engine.apply(ast.document, rules)
        for table_id, rule_ids in engine.table_repairs.items():
            ledger.repairs[table_id] = list(rule_ids)
        corrections = [rule.id for rule in engine.applied]
        anchor_remerges = patch.remerge_anchor_groups(ast)
        patch.check_anchor_groups_attached(ast, page=page.slug)
        anchor_groups_by_block = ast.anchor_groups_by_block
        table.lower_nested_tables(
            ast.document.blocks,
            slug=page.slug,
            ledger=ledger,
            anchor_groups_by_block=anchor_groups_by_block,
        )
        table.expand_table_spans_in_blocks(ast.document.blocks, ledger=ledger)
        table.normalize_headers(
            ast.document.blocks,
            ledger=ledger,
            anchor_groups_by_block=anchor_groups_by_block,
        )
        works.append(
            PageWork(
                entry=page,
                document=document,
                roots=roots,
                ast=ast,
                normalization=normalization,
                corrections=corrections,
                table_ledger=ledger,
                anchor_groups_by_block=anchor_groups_by_block,
                anchor_remerges=anchor_remerges,
            )
        )
    return works


def _finish_page(
    work: PageWork, adapter: SourceAdapter, maps: PageMaps, log: Log
) -> str:
    check_anchor_uniqueness(work.ast, work.ast.document.blocks, page=work.entry.slug)
    map_page_links(
        work.ast.document.blocks,
        work.ast,
        page=work.entry.slug,
        scope_contains=adapter.scope_contains,
        maps=maps,
    )
    table.flatten_cells(
        work.ast.document.blocks,
        anchor_groups_by_block=work.anchor_groups_by_block,
    )
    try:
        validate_page_ast(work.ast, where=f"page {work.entry.slug}")
    except ValueError as error:
        raise BuildError(str(error)) from error
    log(f"{adapter.key} build: _finish_page {work.entry.slug}")
    return render_page(work.ast)


# ------------------------------------------------------------------- records


def _page_record(work: PageWork, front: FrontMatter, data: bytes) -> dict[str, object]:
    return {
        "slug": work.entry.slug,
        "sha256": sha256_bytes(data),
        "front_matter": {
            "fields": {entry.key: entry.value for entry in front.fields},
            "provenance": {entry.key: entry.provenance for entry in front.fields},
        },
        "corrections": list(work.corrections),
        "style_emphasis": [
            {"element": item.element, "value": item.value}
            for item in work.normalization.style_emphasis
        ],
        "ignored_css": [
            {"property": item.property, "value": item.value}
            for item in work.normalization.ignored_css
        ],
        "dropped_comments": [
            {"text": item.text, "fingerprint": item.fingerprint}
            for item in work.normalization.comments
        ],
        "dom_repairs": [
            {"description": item.description} for item in work.normalization.repairs
        ],
        "sup_sub": [
            {"tag": item.tag, "text": item.text, "mode": item.mode}
            for item in work.ast.sup_sub_outcomes
        ],
        "underline": [{"text": item.text} for item in work.ast.underline_occurrences],
        "pre_markup_ignored": list(work.ast.pre_markup_ignored),
        "ignored_srcset": _count_srcset(work.roots),
        "ignored_css_declarations": len(work.normalization.ignored_css),
        "anchors": [
            {"id": group.canonical_id, "names": list(group.names)}
            for group in work.ast.anchor_groups
            if group.canonical_id is not None
        ],
        "remerged_anchor_groups": [
            {"names": list(item.names), "merged_into": item.merged_into}
            for item in work.anchor_remerges
        ],
        "duplicate_anchors": list(work.ast.duplicate_anchors),
        "fragment_map": dict(work.ast.fragment_map),
        "header_flattenings": list(work.table_ledger.diagnostics.flattened_headers),
    }


def _count_srcset(roots: tuple[DomElement, ...]) -> int:
    return sum(
        sum(1 for image in find_all(root, "img") if has_attribute(image, "srcset"))
        for root in roots
    )


def _build_report(
    source: str,
    manifest: Manifest,
    works: list[PageWork],
    maps: PageMaps,
    page_records: list[dict[str, object]],
    readme: str,
    summary: ValidationSummary,
    *,
    check: bool,
) -> dict[str, object]:
    inventory: list[dict[str, object]] = []
    lifted: list[dict[str, object]] = []
    for work in works:
        inventory.extend(_table_inventory(work))
        lifted.extend(
            {"page": work.entry.slug, **record} for record in _lifted_records(work)
        )
    return {
        "source": source,
        "check": check,
        "snapshot_sha256": manifest.snapshot_sha256(),
        "pages": page_records,
        "readme_sha256": _sha256_text(readme),
        "table_inventory": inventory,
        "lifted_nested_tables": lifted,
        "links": {
            "alias_hits": sorted(set(maps.alias_hits)),
            "records": [
                {
                    "page": record.page,
                    "href": record.href,
                    "outcome": record.outcome,
                    "detail": record.detail,
                }
                for record in maps.link_records
            ],
        },
        "validation": {
            "checks": summary.checks,
            "failures": list(summary.failures),
        },
        "warnings": _warnings(works),
    }


def _sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def _notice(kind: NoticeKind, message: str, page: str) -> NoticeJson:
    return {"kind": str(kind), "message": message, "page": page}


def _warnings(works: list[PageWork]) -> list[NoticeJson]:
    warnings: list[NoticeJson] = []
    for work in works:
        page = work.entry.slug
        warnings.extend(
            _notice(
                NoticeKind.STYLE_EMPHASIS_MAPPED,
                "inline font-style:"
                f"{item.value} mapped to emphasis on <{item.element}>",
                page,
            )
            for item in work.normalization.style_emphasis
        )
        warnings.extend(
            _notice(
                NoticeKind.IGNORED_CSS_DECLARATION,
                f"ignored CSS declaration: {item.property}: {item.value}",
                page,
            )
            for item in work.normalization.ignored_css
        )
        warnings.extend(
            _notice(
                NoticeKind.UNDERLINE_DISCARDED,
                "underline styling discarded",
                page,
            )
            for _item in work.ast.underline_occurrences
        )
        warnings.extend(
            _notice(
                NoticeKind.SPAN_PLACEHOLDER_INSERTED,
                f"{count} covered cell(s) of kind {kind}",
                page,
            )
            for kind, count in sorted(
                work.table_ledger.diagnostics.covered_cells.items()
            )
        )
    return warnings


def _table_inventory(work: PageWork) -> list[dict[str, object]]:
    return [
        {
            "page": work.entry.slug,
            "section": list(entry.section),
            "ordinal": entry.ordinal,
            "source_rows": entry.source_rows,
            "source_columns": entry.source_columns,
            "declared_header": entry.declared_header,
            "header_fingerprint": entry.header_fingerprint,
            "first_data_row_fingerprint": entry.first_data_row_fingerprint,
            "effective_header_rows": entry.effective_header_rows,
            "effective_header_source": entry.effective_header_source,
            "repair_id": entry.repair_id,
            "spans": dict(entry.spans),
            "nested_tables": entry.nested_tables,
            "nested_anchors": list(entry.nested_anchors),
            "rendered_header": entry.rendered_header,
            "corrections": list(entry.corrections),
        }
        for entry in table.inventory(work.ast.document.blocks, work.table_ledger)
    ]


def _lifted_records(work: PageWork) -> list[dict[str, object]]:
    return [
        {
            "anchor": item.anchor,
            "row": item.row,
            "cell": item.cell,
            "depth": item.depth,
            "rows": item.rows,
            "columns": item.columns,
            "fingerprint": item.fingerprint,
        }
        for item in work.table_ledger.diagnostics.lifted
    ]


# -------------------------------------------------------------------- output


def _copy_images(
    manifest: Manifest, paths: SourcePaths, files: dict[str, bytes]
) -> None:
    for image in sorted(manifest.images, key=lambda image: image.file):
        source = paths.cache_path(image.file)
        if not file_matches_hash(source, image.sha256):
            raise BuildError(f"image cache is missing or corrupt: {image.file}")
        files[image.file] = source.read_bytes()


def _write_output(files: dict[str, bytes], paths: SourcePaths, log: Log) -> None:
    output = paths.output_root
    staging = Path(tempfile.mkdtemp(prefix="specmirror-build-", dir=paths.scratch_root))
    try:
        for relative in sorted(files):
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[relative])
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.is_dir():
            shutil.rmtree(output)
        staging.rename(output)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    log(f"wrote {len(files)} files to {output}")


def _compare_with_committed(files: dict[str, bytes], paths: SourcePaths) -> bool:
    output = paths.output_root
    committed = {
        relative: (output / relative).read_bytes()
        for relative in list_tree_files(output)
    }
    return committed != files
