"""Tests for the build pipeline and its conversion layers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import pytest
from helpers import FakeClient, add_opentype_pages, add_truetype_pages
from specmirror.build.pipeline import CORRECTIONS_ROOT, run_build
from specmirror.build.validate import ValidationSummary, validate_output
from specmirror.convert import (
    PageAst,
    build_page_ast,
    check_anchor_groups_attached,
    remerge_anchor_groups,
)
from specmirror.convert import table as tables
from specmirror.convert.ast import Paragraph, Table, Text, rows_fingerprint
from specmirror.convert.render import Renderer, escape_text, render_code_span
from specmirror.dom import DomElement, parse_html
from specmirror.errors import BuildError
from specmirror.fetch import run_fetch
from specmirror.paths import SourcePaths

LANDING = "https://learn.microsoft.com/en-us/typography/opentype/spec/"
IMAGE_URL = f"{LANDING}images/fig.png"


def fetch_opentype(paths: SourcePaths, client: FakeClient) -> None:
    run_fetch(
        "opentype",
        "all",
        dry_run=False,
        refresh=False,
        paths=paths,
        client=client,
    )


def fetch_truetype(paths: SourcePaths, client: FakeClient) -> None:
    run_fetch(
        "truetype",
        "all",
        dry_run=False,
        refresh=False,
        paths=paths,
        client=client,
    )


# --------------------------------------------------------------------- layout


def test_build_writes_the_committed_tree(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    client.add(IMAGE_URL, b"png", content_type="image/png")
    add_opentype_pages(client, otff_images=[IMAGE_URL])
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    assert outcome.page_count == 3
    output = opentype_paths.output_root
    assert (output / "README.md").is_file()
    assert (output / "index.md").is_file()
    assert (output / "otff.md").is_file()
    assert (output / "head.md").is_file()
    assert (output / "images" / "fig.png").is_file()


def test_truetype_build_uses_a_flat_readme_list(
    truetype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_truetype_pages(client)
    fetch_truetype(truetype_paths, client)
    run_build("truetype", dry_run=False, check=False, paths=truetype_paths)
    readme = (truetype_paths.output_root / "README.md").read_text()
    assert "- [About AAT](AATIntro.md)" in readme
    assert "Chapter 6\n" not in readme.split("## Pages")[1]
    index = (truetype_paths.output_root / "index.md").read_text()
    assert index.startswith('---\ntitle: "Font Tables"\n')


# ---------------------------------------------------------------- front matter


def test_opentype_front_matter_fields_and_timestamps(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    html = (
        b"<!DOCTYPE html><html><head>"
        b'<meta name="source_path" content="typographydocs/opentype/spec/otff.md">'
        b'<meta name="description" content="A font file.">'
        b'<meta name="author" content="PeterCon">'
        b'<meta name="ms.date" content="2024-05-29T00:00:00.0000000Z">'
        b'<meta name="updated_at" content="2025-03-19T16:08:00-07:00">'
        b'<meta name="gitcommit" content="https://github.com/MicrosoftDocs/'
        b"typography/blob/9fd3f7b24062807b6359a7d0b9b8c9ebef16677c/"
        b'typographydocs/opentype/spec/otff.md">'
        b"</head><body>"
        b'<div class="content"><h1>The OpenType Font File</h1></div>'
        b'<div class="content"><p>Body text.</p></div>'
        b"</body></html>"
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(LANDING, _landing_page())
    client.add(f"{LANDING}otff", html)
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    otff = (opentype_paths.output_root / "otff.md").read_text()
    assert (
        'ms.date: "2024-05-29T00:00:00Z"' in otff
        and 'updated_at: "2025-03-19T23:08:00Z"' in otff
        and 'upstream_gitcommit: "https://github.com/MicrosoftDocs/typography/blob/'
        in otff
        and 'author: "PeterCon"' in otff
        and "description: null" not in otff
    )


def test_malformed_gitcommit_fails_the_build(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    html = (
        b"<!DOCTYPE html><html><head>"
        b'<meta name="source_path" content="typographydocs/opentype/spec/index.md">'
        b'<meta name="gitcommit" content="not-a-url">'
        b"</head><body>"
        b'<div class="content"><h1>OpenType</h1></div>'
        b'<div class="content"><p>Body text.</p></div>'
        b"</body></html>"
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(LANDING, html)
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    with pytest.raises(BuildError, match="malformed gitcommit"):
        run_build("opentype", dry_run=False, check=False, paths=opentype_paths)


# -------------------------------------------------------------- reproducibility


def test_build_is_deterministic_and_check_passes(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client, otff_images=[IMAGE_URL])
    client.add(IMAGE_URL, b"png", content_type="image/png")
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    first = _read_tree(opentype_paths.output_root)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    second = _read_tree(opentype_paths.output_root)
    assert first == second
    check = run_build("opentype", dry_run=False, check=True, paths=opentype_paths)
    assert check.changed is False


def test_anchor_only_paragraph_keeps_its_anchor_line(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = '<p><a id="avarTable"></a></p><p>content</p>'
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert '<a id="anchor-index-avarTable"></a>\n\ncontent' in index


def test_anchor_paragraph_before_heading_yields_one_anchor_line(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = (
        '<p><a id="avarTable"></a></p>'
        '<p><a id="other"></a></p>'
        '<h2 id="t">T</h2>'
        "<p>text</p>"
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert len(_source_anchor_lines(index)) == 1
    assert '<a id="anchor-index-t"></a>\n\n## T' in index
    page_report = _page_reports(outcome.report)[0]
    assert page_report["fragment_map"] == {
        "avarTable": "anchor-index-t",
        "other": "anchor-index-t",
        "t": "anchor-index-t",
    }


def test_consecutive_upstream_anchors_render_one_anchor(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = (
        '<a name="intro"></a><b></b>'
        '<h2 id="introduction">Title</h2>'
        "<p>text</p>"
        '<p><a href="#introduction">jump</a></p>'
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert len(_source_anchor_lines(index)) == 1
    assert '<a id="anchor-index-introduction"></a>' in index
    page_report = _page_reports(outcome.report)[0]
    assert page_report["fragment_map"] == {
        "intro": "anchor-index-introduction",
        "introduction": "anchor-index-introduction",
    }


def test_anchor_on_an_empty_blockquote_merges_into_the_next_group(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = (
        '<blockquote><a name="intro"></a></blockquote>'
        '<a name="introduction"></a>'
        "<p>text</p>"
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert len(_source_anchor_lines(index)) == 1
    assert '<a id="anchor-index-intro"></a>' in index


def test_escaped_lt_et_is_not_a_disallowed_tag(opentype_paths: SourcePaths) -> None:
    client = FakeClient()
    body = "<p>the sequence &lt;et&gt; is literal text</p>"
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert "\\<et\\>" in index


def test_pre_trailing_newline_does_not_become_a_blank_line() -> None:
    from specmirror.convert.normalize import NormalizationResult, normalize_roots
    from specmirror.convert.render import render_page

    html = "<div><pre>line one\nline two\n</pre></div>"
    document = parse_html(html)
    html_root = document.children[0]
    assert isinstance(html_root, DomElement)
    result = NormalizationResult()
    normalize_roots((html_root,), page="p", result=result)
    ast = build_page_ast(
        (html_root,), page="p", slug="p", page_url="https://x/", italic=result.italic
    )
    assert render_page(ast) == "```\nline one\nline two\n```"


def test_anchor_before_table_attaches_to_the_table(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = '<p><a id="Table1"></a></p><table><tr><td>Data block</td></tr></table>'
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert '<a id="anchor-index-Table1"></a>' in index
    # the anchor precedes the table, not its first cell
    cell_line = next(line for line in index.split("\n") if "Data block" in line)
    assert "<a id=" not in cell_line
    page_report = _page_reports(outcome.report)[0]
    fragment_map = cast("dict[str, str]", page_report["fragment_map"])
    assert fragment_map["Table1"] == "anchor-index-Table1"


def _build_fragment(html: str) -> str:
    document = parse_html(html)
    root = document.children[0]
    assert isinstance(root, DomElement)
    ast = build_page_ast((root,), page="t", slug="t", page_url="https://x/", italic={})
    return Renderer(ast.anchor_groups).render_blocks(ast.document.blocks)


def test_trailing_anchor_in_a_paragraph_attaches_to_the_next_block() -> None:
    html = (
        "<div><p>Format 4 uses an array of records.\n"
        '<a id="codeOffsetPair"></a></p>'
        "<p><em>GlyphIdOffsetPair record</em></p></div>"
    )
    markdown = _build_fragment(html)
    assert '<a id="anchor-t-codeOffsetPair"></a>\n\n*GlyphIdOffsetPair record*' in (
        markdown
    )


def test_trailing_anchor_at_the_page_end_stays_with_the_last_block() -> None:
    html = '<div><p>last paragraph <a id="tail"></a></p></div>'
    markdown = _build_fragment(html)
    assert '<a id="anchor-t-tail"></a>\n\nlast paragraph' in markdown


def test_trailing_anchor_in_a_cell_stays_inside_the_cell() -> None:
    html = (
        "<div><table><tr><td>head</td></tr>"
        '<tr><td><p>tail <a id="celltail"></a></p></td></tr></table></div>'
    )
    document = parse_html(html)
    root = document.children[0]
    assert isinstance(root, DomElement)
    ast = build_page_ast((root,), page="t", slug="t", page_url="https://x/", italic={})
    table = ast.document.blocks[0]
    assert isinstance(table, Table)
    cell = table.rows[1].cells[0]
    group = ast.anchor_groups[0]
    assert group.names == ("celltail",)
    assert group.block is cell.blocks[-1]


def test_style_emphasis_respects_normal_cancellation() -> None:
    from specmirror.convert.normalize import NormalizationResult, normalize_roots
    from specmirror.convert.render import render_page

    html = (
        "<div><p style='font-style: italic'>outer "
        "<span style='font-style: normal'>normal</span> text</p></div>"
    )
    document = parse_html(html)
    root = document.children[0]
    assert isinstance(root, DomElement)
    result = NormalizationResult()
    normalize_roots((root,), page="p", result=result)
    ast = build_page_ast(
        (root,),
        page="p",
        slug="p",
        page_url="https://x/",
        italic=result.italic,
    )
    assert "*outer* normal *text*" in render_page(ast)


def test_inline_code_link_keeps_the_link_and_the_code() -> None:
    markdown = _build_fragment(
        "<div><p>see <code><a href='https://example.com/x'>'bloc'</a></code></p></div>"
    )
    assert "[`'bloc'`](https://example.com/x)" in markdown


def test_link_and_image_titles_stay_inside_the_destination() -> None:
    markdown = _build_fragment(
        "<div><p><a href='https://example.com/x' title='Link'>link</a> "
        "<img src='https://example.com/i.png' alt='i' title='Image'></p></div>"
    )
    assert '[link](https://example.com/x "Link")' in markdown
    assert '![i](https://example.com/i.png "Image")' in markdown


def test_table_caption_is_separated_from_the_table_by_a_blank_line() -> None:
    markdown = _build_fragment(
        "<div><table><caption>Cap</caption>"
        "<tr><th>A</th></tr><tr><td>B</td></tr></table></div>"
    )
    assert "*Cap*\n\n| A |" in markdown


def test_table_caption_preserves_inline_markup() -> None:
    markdown = _build_fragment(
        "<div><table><caption>The <code>'ankr'</code> table header</caption>"
        "<tr><th>A</th></tr><tr><td>B</td></tr></table></div>"
    )
    assert "*The `'ankr'` table header*" in markdown


def test_header_fragments_trim_edges_and_join_compounds() -> None:
    from specmirror.convert import table as table_module
    from specmirror.convert.ast import (
        LineBreak,
        Paragraph,
        Table,
        TableCell,
        TableHeader,
        TableRow,
        Text,
        inline_text,
    )

    header = TableRow(
        cells=[
            TableCell(
                role="th",
                blocks=[
                    Paragraph(
                        inlines=[
                            Text("Offset/"),
                            LineBreak(),
                            Text(" length"),
                            LineBreak(),
                            Text("Language"),
                            LineBreak(),
                            Text(" ID"),
                        ]
                    )
                ],
            )
        ]
    )
    table = Table(
        caption=None,
        header=TableHeader(source="declared", rows=[header]),
        rows=[TableRow(cells=[TableCell(role="td", blocks=[])])],
    )
    ledger = table_module.TableLedger()
    table_module.normalize_headers([table], ledger=ledger, anchor_groups_by_block={})
    cell = table.header.rows[0].cells[0]
    block = cell.blocks[0]
    assert isinstance(block, Paragraph)
    text = "".join(inline_text(inline) for inline in block.inlines)
    assert text == "Offset/length Language ID"


def test_whitespace_in_quoted_literals_and_code_spans() -> None:
    from specmirror.convert.normalize import NormalizationResult, normalize_roots
    from specmirror.convert.render import render_page

    for html, expected in (
        ("<div><p>'WA  ' keeps its padding.</p></div>", "'WA  ' keeps its padding."),
        ("<div><p><code>'jpg\n        '</code></p></div>", "`'jpg '`"),
    ):
        document = parse_html(html)
        root = document.children[0]
        assert isinstance(root, DomElement)
        result = NormalizationResult()
        normalize_roots((root,), page="p", result=result)
        ast = build_page_ast(
            (root,),
            page="p",
            slug="p",
            page_url="https://x/",
            italic=result.italic,
        )
        assert render_page(ast) == expected


# ------------------------------------------------------------------- remerge


def _build_ast(html: str) -> object:
    document = parse_html(html)
    root = document.children[0]
    assert isinstance(root, DomElement)
    return build_page_ast((root,), page="t", slug="t", page_url="https://x/", italic={})


def test_remerge_moves_group_off_emptied_paragraph_to_ungrouped_block() -> None:
    ast = _build_ast('<div><p><a id="x">&gt;</a></p><p>text</p></div>')
    assert isinstance(ast, PageAst)
    paragraph = ast.document.blocks[0]
    assert isinstance(paragraph, Paragraph)
    paragraph.inlines.clear()
    remerges = remerge_anchor_groups(ast)
    assert len(ast.document.blocks) == 1
    assert len(ast.anchor_groups) == 1
    group = ast.anchor_groups[0]
    assert group.names == ("x",)
    assert group.canonical_id == "anchor-t-x"
    assert group.block is ast.document.blocks[0]
    assert ast.fragment_map == {"x": "anchor-t-x"}
    assert [(item.names, item.merged_into) for item in remerges] == [(("x",), None)]


def test_remerge_merges_group_into_the_following_heading_group() -> None:
    ast = _build_ast('<div><p><a id="x">&gt;</a></p><h2 id="h">H</h2></div>')
    assert isinstance(ast, PageAst)
    paragraph = ast.document.blocks[0]
    assert isinstance(paragraph, Paragraph)
    paragraph.inlines.clear()
    remerges = remerge_anchor_groups(ast)
    assert len(ast.document.blocks) == 1
    group = ast.anchor_groups[0]
    assert group.names == ("x", "h")
    assert group.canonical_id == "anchor-t-h"
    assert ast.fragment_map == {"x": "anchor-t-h", "h": "anchor-t-h"}
    assert [(item.names, item.merged_into) for item in remerges] == [
        (("x",), "anchor-t-h")
    ]


def test_remerge_chains_through_consecutive_emptied_paragraphs() -> None:
    ast = _build_ast(
        '<div><p><a id="x">&gt;</a></p><p><a id="y">&gt;</a></p><p>text</p></div>'
    )
    assert isinstance(ast, PageAst)
    for block in list(ast.document.blocks[:2]):
        assert isinstance(block, Paragraph)
        block.inlines.clear()
    remerges = remerge_anchor_groups(ast)
    assert len(ast.document.blocks) == 1
    group = ast.anchor_groups[0]
    assert group.names == ("x", "y")
    assert group.canonical_id == "anchor-t-y"
    assert ast.fragment_map == {"x": "anchor-t-y", "y": "anchor-t-y"}
    assert len(remerges) == 2


def test_remerge_leaves_an_emptied_last_paragraph_alone() -> None:
    ast = _build_ast('<div><p>text</p><p><a id="x">&gt;</a></p></div>')
    assert isinstance(ast, PageAst)
    paragraph = ast.document.blocks[1]
    assert isinstance(paragraph, Paragraph)
    paragraph.inlines.clear()
    assert remerge_anchor_groups(ast) == []
    assert len(ast.document.blocks) == 2
    assert ast.anchor_groups[0].block is ast.document.blocks[1]


def test_remerge_does_not_move_cell_anchor_holders() -> None:
    ast = _build_ast('<div><table><tr><td><a id="x"></a></td></tr></table></div>')
    assert isinstance(ast, PageAst)
    table = ast.document.blocks[0]
    assert isinstance(table, Table)
    holder = table.rows[0].cells[0].blocks[0]
    assert isinstance(holder, Paragraph)
    assert holder.inlines == []
    assert remerge_anchor_groups(ast) == []
    assert ast.anchor_groups[0].block is holder


def test_anchor_groups_attached_fails_for_orphaned_groups() -> None:
    ast = _build_ast('<div><p><a id="x">&gt;</a></p><p>text</p></div>')
    assert isinstance(ast, PageAst)
    del ast.document.blocks[0]
    with pytest.raises(BuildError, match="anchor-t-x"):
        check_anchor_groups_attached(ast, page="t")


def test_emptied_anchor_paragraph_remerges_into_the_next_group(
    opentype_paths: SourcePaths,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rules: list[dict[str, object]] = [
        {
            "id": "index-0001",
            "op": "replace_inline",
            "target": {"block": 2},
            "find": [{"type": "text", "text": ">"}],
            "inlines": [],
            "expect": {"count": 1},
            "note": "test",
        }
    ]
    root = tmp_path / "corrections"
    (root / "opentype").mkdir(parents=True)
    (root / "opentype" / "index.json").write_text(json.dumps(rules))
    monkeypatch.setattr("specmirror.build.pipeline.CORRECTIONS_ROOT", root)
    client = FakeClient()
    body = '<p><a id="x">&gt;</a></p><h2 id="h">H</h2>'
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert len(_source_anchor_lines(index)) == 1
    assert '<a id="anchor-index-h"></a>\n\n## H' in index
    page_report = _page_reports(outcome.report)[0]
    fragment_map = cast("dict[str, str]", page_report["fragment_map"])
    assert fragment_map == {"x": "anchor-index-h", "h": "anchor-index-h"}
    assert page_report["remerged_anchor_groups"] == [
        {"names": ["x"], "merged_into": "anchor-index-h"}
    ]


def test_cell_anchors_before_nested_table_move_to_the_in_place_link(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = (
        "<table><tr><td>"
        "Indicates licensing rights."
        '<p><a id="fst_0"></a><a id="fst_bit0"></a></p>'
        "<table><tr><td>Bits</td></tr></table>"
        "</td></tr></table>"
        "<p>after</p>"
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    cell_line = next(
        line for line in index.split("\n") if "Indicates licensing rights" in line
    )
    assert '<a id="anchor-index-fst_0"></a>' in cell_line
    assert "[See table]" in cell_line
    page_report = _page_reports(outcome.report)[0]
    fragment_map = cast("dict[str, str]", page_report["fragment_map"])
    assert fragment_map["fst_0"] == "anchor-index-fst_0"
    assert fragment_map["fst_bit0"] == "anchor-index-fst_0"


def test_nested_same_marker_emphasis_merges() -> None:
    from specmirror.convert.normalize import NormalizationResult, normalize_roots
    from specmirror.convert.render import render_page

    html = "<div><p>values <i>n<i> ]</i></i> remain</p></div>"
    document = parse_html(html)
    html_root = document.children[0]
    assert isinstance(html_root, DomElement)
    result = NormalizationResult()
    normalize_roots((html_root,), page="p", result=result)
    ast = build_page_ast(
        (html_root,), page="p", slug="p", page_url="https://x/", italic=result.italic
    )
    body = render_page(ast)
    assert "values *n \\]* remain" in body
    assert body.count("*") == 2


def test_figcaption_emphasis_merges_into_one_marker() -> None:
    from specmirror.convert.normalize import NormalizationResult, normalize_roots
    from specmirror.convert.render import render_page

    for figcaption in (
        "<figcaption><i>NOTE: read the diagram.</i></figcaption>",
        "<figcaption><i>NOTE: read the diagram. </i></figcaption>",
    ):
        html = (
            "<div><figure>"
            '<img src="https://x/fig.png" alt="diagram">'
            f"{figcaption}"
            "</figure></div>"
        )
        document = parse_html(html)
        html_root = document.children[0]
        assert isinstance(html_root, DomElement)
        result = NormalizationResult()
        normalize_roots((html_root,), page="p", result=result)
        ast = build_page_ast(
            (html_root,),
            page="p",
            slug="p",
            page_url="https://x/",
            italic=result.italic,
        )
        body = render_page(ast)
        caption = next(line for line in body.split("\n") if "NOTE" in line)
        assert not caption.endswith(" ")
        assert "*NOTE: read the diagram.*" in body
        assert "**NOTE" not in body


def test_no_break_space_in_table_cells_renders_as_entity(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = "<table><tr><td>\u00a0\u00a0indented</td><td>b</td></tr></table>"
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert "| &nbsp;&nbsp;indented | b |" in index


def test_anchors_inside_table_cells_are_rendered(opentype_paths: SourcePaths) -> None:
    client = FakeClient()
    body = (
        "<table>"
        '<tr><td><a id="x"></a>left</td><td>right</td></tr>'
        '<tr><td>only</td><td><a id="y"></a></td></tr>'
        "</table>"
        "<p>after</p>"
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert '<a id="anchor-index-x"></a>left' in index
    assert '<a id="anchor-index-y"></a>' in index
    # the last-cell anchor stays inside the table; nothing drifts to "after"
    after = index.split("after", 1)[1]
    assert "<a id=" not in after
    page_report = _page_reports(outcome.report)[0]
    fragment_map = cast("dict[str, str]", page_report["fragment_map"])
    assert fragment_map["x"] == "anchor-index-x"
    assert fragment_map["y"] == "anchor-index-y"


def test_pipes_in_table_cells_do_not_break_rectangularity(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = "<table><tr><td>a|b</td><td>c</td></tr></table>"
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>h</p>"),
    )
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert "| a\\|b | c |" in index


def test_binary_images_are_not_subject_to_text_validation(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    add_opentype_pages(client, otff_images=[IMAGE_URL])
    client.add(IMAGE_URL, b"\x89PNG\r\n\x00binary", content_type="image/png")
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    image = (opentype_paths.output_root / "images" / "fig.png").read_bytes()
    assert image == b"\x89PNG\r\n\x00binary"
    assert outcome.changed is not None


def test_check_detects_committed_changes(opentype_paths: SourcePaths) -> None:
    client = FakeClient()
    add_opentype_pages(client)
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = opentype_paths.output_root / "index.md"
    index.write_text(index.read_text() + "\nedited\n")
    check = run_build("opentype", dry_run=False, check=True, paths=opentype_paths)
    assert check.changed is True


def _source_anchor_lines(text: str) -> list[str]:
    return [
        line for line in text.splitlines() if "<a id=" in line and "-part-" not in line
    ]


def _page_reports(report: dict[str, object]) -> list[dict[str, object]]:
    pages = report["pages"]
    if not isinstance(pages, list):
        pytest.fail("pages report is missing")
    return cast("list[dict[str, object]]", pages)


def _read_tree(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


# ------------------------------------------------------------------- renderer


def test_escape_text_is_deterministic() -> None:
    assert escape_text("a*b_c") == "a\\*b\\_c"
    assert escape_text("foo_bar") == "foo\\_bar"
    assert escape_text("[x] <y> `z`") == "\\[x\\] \\<y\\> \\`z\\`"
    assert escape_text("a | b", in_table=True) == "a \\| b"
    assert escape_text("- item", line_start=True) == "\\- item"
    assert escape_text("1. one", line_start=True) == "1\\. one"


def test_code_span_delimiter_grows_with_runs() -> None:
    assert render_code_span("x", in_table=False) == "`x`"
    assert render_code_span("a``b", in_table=False) == "```a``b```"
    assert render_code_span("`x`", in_table=False) == "`` `x` ``"
    content = "2" + "`" * 25 + "d"
    assert render_code_span(content, in_table=False) == ("`" * 26 + content + "`" * 26)


# --------------------------------------------------------------------- tables


def test_headerless_table_renders_a_synthetic_header() -> None:
    from specmirror.convert.ast import (
        Paragraph,
        Table,
        TableCell,
        TableHeader,
        TableRow,
        Text,
    )

    table = Table(
        caption=None,
        header=TableHeader(source="none", rows=[]),
        rows=[
            TableRow(cells=[TableCell(role="td", blocks=[Paragraph([Text("a")])])]),
            TableRow(cells=[TableCell(role="td", blocks=[Paragraph([Text("b")])])]),
        ],
    )
    from specmirror.convert.render import Renderer

    rendered = Renderer([]).render_table(table)
    assert rendered == "|  |\n| --- |\n| a |\n| b |"


def test_span_expansion_inserts_exact_placeholders() -> None:
    from specmirror.convert.ast import (
        Paragraph,
        SpanPlaceholder,
        Table,
        TableCell,
        TableHeader,
        TableRow,
    )

    table = Table(
        caption=None,
        header=TableHeader(source="none", rows=[]),
        rows=[
            TableRow(
                cells=[
                    TableCell(role="td", row_span=2, col_span=2, blocks=[]),
                    TableCell(role="td", blocks=[Paragraph([Text("x")])]),
                ]
            ),
            TableRow(cells=[TableCell(role="td", blocks=[Paragraph([Text("y")])])]),
        ],
    )
    diagnostics = tables.TableDiagnostics()
    tables.expand_span_grid(table, diagnostics)
    kinds = [
        inline.kind
        for row in table.rows
        for cell in row.cells
        for block in cell.blocks
        if isinstance(block, Paragraph)
        for inline in block.inlines
        if isinstance(inline, SpanPlaceholder)
    ]
    assert kinds == ["colspan", "rowspan", "rowspan colspan"]
    assert diagnostics.covered_cells == {
        "rowspan colspan": 1,
        "colspan": 1,
        "rowspan": 1,
    }


def test_overlapping_spans_fail() -> None:
    from specmirror.convert.ast import Table, TableCell, TableHeader, TableRow

    table = Table(
        caption=None,
        header=TableHeader(source="none", rows=[]),
        rows=[
            TableRow(
                cells=[
                    TableCell(role="td", row_span=2, blocks=[]),
                    TableCell(role="td", blocks=[]),
                    TableCell(role="td", row_span=2, blocks=[]),
                ]
            ),
            TableRow(cells=[TableCell(role="td", col_span=2, blocks=[])]),
            TableRow(cells=[TableCell(role="td", blocks=[])]),
        ],
    )
    with pytest.raises(BuildError, match="overlapping"):
        tables.expand_span_grid(table, tables.TableDiagnostics())


# ------------------------------------------------------------- conversion end


def test_links_images_and_anchors_are_mapped(opentype_paths: SourcePaths) -> None:
    client = FakeClient()
    body = (
        "<p>"
        '<a href="otff">The file</a> and '
        '<a href="#section">this section</a> and '
        '<a href="https://example.com/x">external</a>'
        "</p>"
        '<h2 id="section">head</h2>'
        '<p><img src="images/fig.png" alt="Figure"></p>'
        '<table><caption>See <a href="otff">the caption</a></caption>'
        "<tr><th>A</th></tr><tr><td>B</td></tr></table>"
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>Head.</p>"),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(IMAGE_URL, b"png", content_type="image/png")
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert "[The file](otff.md)" in index
    assert "](#anchor-index-section)" in index
    assert "](https://example.com/x)" in index
    assert "![Figure](images/fig.png)" in index
    assert "*See [the caption](otff.md)*" in index
    assert '<a id="anchor-index-section"></a>' in index


def test_duplicate_source_anchors_map_to_the_first_occurrence(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = (
        '<h2 id="section">first</h2>'
        "<p>text</p>"
        '<h2 id="section">second</h2>'
        "<p>more</p>"
        '<p><a href="#section">jump</a></p>'
    )
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>Head.</p>"),
    )
    fetch_opentype(opentype_paths, client)
    outcome = run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert index.count('<a id="anchor-index-section') == 2
    assert '<a id="anchor-index-section-3fb45623"></a>' in index
    assert "](#anchor-index-section)" in index
    page_report = _page_reports(outcome.report)[0]
    assert page_report["duplicate_anchors"] == ["section"]
    assert page_report["fragment_map"] == {"section": "anchor-index-section"}


def test_missing_manifest_image_fails_the_build(
    opentype_paths: SourcePaths,
) -> None:
    client = FakeClient()
    body = '<p><img src="images/other.png" alt="x"></p>'
    client.add("https://learn.microsoft.com/en-us/typography/toc.json", _toc())
    client.add(
        LANDING,
        _opentype_page("typographydocs/opentype/spec/index.md", "OpenType", body),
    )
    client.add(
        f"{LANDING}otff",
        _opentype_page(
            "typographydocs/opentype/spec/otff.md", "The OpenType Font File", "<p>b</p>"
        ),
    )
    client.add(
        f"{LANDING}head",
        _opentype_page("typographydocs/opentype/spec/head.md", "head", "<p>Head.</p>"),
    )
    client.add(f"{LANDING}images/other.png", b"png", content_type="image/png")
    fetch_opentype(opentype_paths, client)
    _drop_image_from_manifest(opentype_paths, f"{LANDING}images/other.png")
    with pytest.raises(BuildError, match="missing from the manifest"):
        run_build("opentype", dry_run=False, check=False, paths=opentype_paths)


def _drop_image_from_manifest(paths: SourcePaths, url: str) -> None:
    data = json.loads(paths.manifest_path.read_text())
    data["images"] = [
        image for image in data["images"] if image["requested_url"] != url
    ]
    without = {key: value for key, value in data.items() if key != "snapshot_sha256"}
    canonical = json.dumps(without, sort_keys=True, separators=(",", ":"))
    data["snapshot_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    paths.manifest_path.write_text(json.dumps(data))


def test_markup_inside_pre_is_ignored_with_literal_text_kept() -> None:
    from specmirror.convert.normalize import NormalizationResult, normalize_roots
    from specmirror.convert.render import render_page

    html = "<div><pre><b>bold</b> code\nline two</pre></div>"
    document = parse_html(html)
    html_root = document.children[0]
    assert isinstance(html_root, DomElement)
    result = NormalizationResult()
    normalize_roots((html_root,), page="p", result=result)
    ast = build_page_ast(
        (html_root,), page="p", slug="p", page_url="https://x/", italic=result.italic
    )
    body = render_page(ast)
    assert "```\nbold code\nline two\n```" in body
    assert ast.pre_markup_ignored == ["b"]


def test_sup_sub_digit_conversion_and_html_fallback() -> None:
    from specmirror.convert import build_page_ast
    from specmirror.convert.normalize import NormalizationResult, normalize_roots
    from specmirror.convert.render import render_page

    html = "<p>x<sup>2</sup> y<sub>n+1</sub></p>"
    document = parse_html(html)
    html_root = document.children[0]
    assert isinstance(html_root, DomElement)
    result = NormalizationResult()
    normalize_roots((html_root,), page="p", result=result)
    ast = build_page_ast(
        (html_root,), page="p", slug="p", page_url="https://x/", italic=result.italic
    )
    body = render_page(ast)
    assert "x\u00b2" in body
    assert "<sub>n+1</sub>" in body
    assert [outcome.mode for outcome in ast.sup_sub_outcomes] == ["unicode", "html"]


# ---------------------------------------------------------------- corrections


def test_replace_text_correction_is_applied(
    opentype_paths: SourcePaths,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rules: list[dict[str, object]] = [
        {
            "id": "index-0001",
            "op": "replace_text",
            "target": {"block": 2},
            "find": "Body",
            "replace": "Corrected",
            "expect": {"count": 1},
            "note": "test",
        }
    ]
    root = tmp_path / "corrections"
    (root / "opentype").mkdir(parents=True)
    (root / "opentype" / "index.json").write_text(json.dumps(rules))
    monkeypatch.setattr("specmirror.build.pipeline.CORRECTIONS_ROOT", root)
    client = FakeClient()
    add_opentype_pages(client)
    fetch_opentype(opentype_paths, client)
    run_build("opentype", dry_run=False, check=False, paths=opentype_paths)
    index = (opentype_paths.output_root / "index.md").read_text()
    assert "Corrected text." in index
    assert "Body text." not in index
    assert CORRECTIONS_ROOT.is_dir()


def test_stale_correction_fails_the_build(
    opentype_paths: SourcePaths,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rules: list[dict[str, object]] = [
        {
            "id": "index-0001",
            "op": "replace_text",
            "target": {"block": 2},
            "find": "Absent text",
            "replace": "x",
            "expect": {"count": 1},
            "note": "test",
        }
    ]
    root = tmp_path / "corrections"
    (root / "opentype").mkdir(parents=True)
    (root / "opentype" / "index.json").write_text(json.dumps(rules))
    monkeypatch.setattr("specmirror.build.pipeline.CORRECTIONS_ROOT", root)
    client = FakeClient()
    add_opentype_pages(client)
    fetch_opentype(opentype_paths, client)
    with pytest.raises(BuildError, match="index-0001"):
        run_build("opentype", dry_run=False, check=False, paths=opentype_paths)


def test_set_table_header_correction_promotes_rows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:

    html = (
        "<div><table>"
        "<tr><td>h1</td><td>h2</td></tr>"
        "<tr><td>a</td><td>b</td></tr>"
        "</table></div>"
    )
    document = parse_html(html)
    root = document.children[0]
    assert isinstance(root, DomElement)
    ast = build_page_ast((root,), page="t", slug="t", page_url="https://x/", italic={})
    block = ast.document.blocks[0]
    assert isinstance(block, Table)
    table = block
    header_fingerprint = rows_fingerprint(list(table.header.rows))
    rules: list[dict[str, object]] = [
        {
            "id": "t-0001",
            "op": "set_table_header",
            "target": {"table": 1},
            "mode": "rows",
            "rows": [1],
            "expect": {
                "header_fingerprint": header_fingerprint,
                "row_count": 2,
                "column_count": 2,
            },
            "note": "test",
        }
    ]
    root_dir = tmp_path / "corrections"
    (root_dir / "opentype").mkdir(parents=True)
    (root_dir / "opentype" / "t.json").write_text(json.dumps(rules))
    monkeypatch.setattr("specmirror.build.pipeline.CORRECTIONS_ROOT", root_dir)
    from specmirror.convert.patch import PatchEngine, load_rules

    engine = PatchEngine(page="t", slug="t")
    engine.apply(ast.document, load_rules(root_dir, source="opentype", slug="t"))
    assert table.header.source == "declared"
    assert table.header.repair_id == "t-0001"
    assert len(table.header.rows) == 1
    assert len(table.rows) == 1


def test_promoted_header_strips_strong_inside_link(tmp_path: Path) -> None:
    from specmirror.convert.ast import (
        Link,
        Paragraph,
        Strong,
        inlines_text,
        iter_inlines,
    )
    from specmirror.convert.patch import PatchEngine, load_rules

    html = (
        "<div><table>"
        '<tr><td><a href="https://example.com/x"><strong>head</strong></a></td>'
        "<td>h2</td></tr>"
        "<tr><td>a</td><td>b</td></tr>"
        "</table></div>"
    )
    document = parse_html(html)
    root = document.children[0]
    assert isinstance(root, DomElement)
    ast = build_page_ast((root,), page="t", slug="t", page_url="https://x/", italic={})
    table = ast.document.blocks[0]
    assert isinstance(table, Table)
    rules: list[dict[str, object]] = [
        {
            "id": "t-0001",
            "op": "set_table_header",
            "target": {"table": 1},
            "mode": "rows",
            "rows": [1],
            "expect": {
                "header_fingerprint": rows_fingerprint(list(table.header.rows)),
                "row_count": 2,
                "column_count": 2,
            },
            "note": "test",
        }
    ]
    root_dir = tmp_path / "corrections"
    (root_dir / "opentype").mkdir(parents=True)
    (root_dir / "opentype" / "t.json").write_text(json.dumps(rules))
    engine = PatchEngine(page="t", slug="t")
    engine.apply(ast.document, load_rules(root_dir, source="opentype", slug="t"))
    cell = table.header.rows[0].cells[0]
    block = cell.blocks[0]
    assert isinstance(block, Paragraph)
    nodes = list(iter_inlines(block.inlines))
    links = [node for node in nodes if isinstance(node, Link)]
    assert len(links) == 1
    assert links[0].href == "https://example.com/x"
    assert inlines_text(links[0].inlines) == "head"
    assert not any(isinstance(node, Strong) for node in nodes)


def test_section_targeted_structural_corrections_edit_the_document(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from specmirror.convert.ast import block_fingerprint, inlines_text

    html = "<div><h2>Section</h2><p>first</p><p>second</p></div>"
    document = parse_html(html)
    root = document.children[0]
    assert isinstance(root, DomElement)
    ast = build_page_ast((root,), page="t", slug="t", page_url="https://x/", italic={})
    first, second = ast.document.blocks[1], ast.document.blocks[2]
    assert isinstance(first, Paragraph)
    assert isinstance(second, Paragraph)
    rules: list[dict[str, object]] = [
        {
            "id": "t-0001",
            "op": "remove_node",
            "target": {"section_heading": ["Section"], "block": 2},
            "expect": {"fingerprint": block_fingerprint(second)},
            "note": "test",
        },
        {
            "id": "t-0002",
            "op": "insert_block",
            "target": {"section_heading": ["Section"], "block": 1},
            "position": "after",
            "expect": {"fingerprint": block_fingerprint(first)},
            "blocks": [
                {
                    "type": "paragraph",
                    "inlines": [{"type": "text", "text": "inserted"}],
                }
            ],
            "note": "test",
        },
    ]
    root_dir = tmp_path / "corrections"
    (root_dir / "opentype").mkdir(parents=True)
    (root_dir / "opentype" / "t.json").write_text(json.dumps(rules))
    monkeypatch.setattr("specmirror.build.pipeline.CORRECTIONS_ROOT", root_dir)
    from specmirror.convert.patch import PatchEngine, load_rules

    engine = PatchEngine(page="t", slug="t")
    engine.apply(ast.document, load_rules(root_dir, source="opentype", slug="t"))
    paragraphs = [
        inlines_text(block.inlines)
        for block in ast.document.blocks
        if isinstance(block, Paragraph)
    ]
    assert paragraphs == ["first", "inserted"]


def test_correction_list_tightness_follows_item_blocks() -> None:
    from specmirror.convert.ast import List
    from specmirror.convert.patch import decode_blocks

    payload: list[dict[str, object]] = [
        {
            "type": "list",
            "ordered": False,
            "start": 1,
            "items": [
                {
                    "blocks": [
                        {
                            "type": "paragraph",
                            "inlines": [{"type": "text", "text": "one"}],
                        }
                    ]
                },
                {
                    "blocks": [
                        {
                            "type": "paragraph",
                            "inlines": [{"type": "text", "text": "two"}],
                        },
                        {
                            "type": "paragraph",
                            "inlines": [{"type": "text", "text": "detail"}],
                        },
                    ]
                },
            ],
        }
    ]
    blocks = decode_blocks(payload, where="t")
    assert isinstance(blocks[0], List)
    assert not blocks[0].tight


# ------------------------------------------------------------------ validator


def test_validator_rejects_disallowed_tags_and_comments() -> None:
    from specmirror.schema import Manifest

    manifest = Manifest.from_dict(_minimal_manifest_dict())
    files = {
        "README.md": b"# Readme\n\n## Regeneration\n\n## Pages\n\n- [t](index.md)\n",
        "index.md": (b'---\ntitle: "T"\n---\n\n<p>bad</p>\n\n<!-- custom -->\n'),
    }
    summary = ValidationSummary()
    validate_output(files, manifest, summary)
    assert any("disallowed HTML tag" in failure for failure in summary.failures)
    assert any("disallowed HTML comment" in failure for failure in summary.failures)


def test_validator_accepts_the_permitted_subset() -> None:
    from specmirror.schema import Manifest

    manifest = Manifest.from_dict(_minimal_manifest_dict())
    files = {
        "README.md": b"# Readme\n\n## Regeneration\n\n## Pages\n\n- [t](index.md)\n",
        "index.md": (
            b'---\ntitle: "T"\n---\n\n'
            b'<a id="anchor-index-a"></a>\n\n'
            b"x <br> <sup>1</sup> <sub>2</sub>\n\n"
            b'[t](index.md "T")\n\n'
            b"| a |\n| --- |\n| <!-- colspan --> |\n"
        ),
    }
    summary = ValidationSummary()
    validate_output(files, manifest, summary)
    assert summary.failures == []


def _minimal_manifest_dict() -> dict[str, object]:
    import hashlib

    def entry(slug: str) -> dict[str, object]:
        return {
            "title": "t",
            "section": [],
            "requested_url": f"{LANDING}{slug}",
            "source_path": f"typographydocs/opentype/spec/{slug}.md",
            "slug": slug,
            "file": f"pages/{slug}.html",
            "sha256": "0" * 64,
            "content_type": "text/html",
            "last_modified": None,
        }

    manifest: dict[str, object] = {
        "schema_version": 1,
        "source": "opentype",
        "discovery": {
            "requested_url": "https://learn.microsoft.com/en-us/typography/toc.json",
            "raw_file": "toc/toc.json",
            "sha256": "0" * 64,
        },
        "pages": [entry("index")],
        "images": [],
    }

    def canonical(value: dict[str, object]) -> str:
        return json.dumps(value, sort_keys=True, separators=(",", ":"))

    manifest["snapshot_sha256"] = hashlib.sha256(
        canonical(manifest).encode()
    ).hexdigest()
    return manifest


# ----------------------------------------------------------------- fixtures


def _toc() -> bytes:
    return json.dumps(
        {
            "items": [
                {
                    "toc_title": "OpenType spec",
                    "href": "opentype/spec/",
                    "children": [
                        {
                            "toc_title": "The OpenType font file",
                            "href": "opentype/spec/otff",
                        },
                        {"toc_title": "head", "href": "opentype/spec/head"},
                    ],
                }
            ]
        }
    ).encode()


def _landing_page() -> bytes:
    return _opentype_page(
        "typographydocs/opentype/spec/index.md", "OpenType", "<p>Body text.</p>"
    )


def _opentype_page(source_path: str, title: str, body: str) -> bytes:
    return (
        "<!DOCTYPE html><html><head>"
        f'<meta name="source_path" content="{source_path}">'
        "</head><body>"
        f'<div class="content"><h1>{title}</h1></div>'
        f'<div class="content">{body}</div>'
        "</body></html>"
    ).encode()
