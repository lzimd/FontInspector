"""The semantic AST vocabulary and its tree infrastructure.

The AST models CommonMark and GFM constructs plus the narrow raw HTML
subset. Corrections, the table pipeline, and the renderer all operate on
these nodes. Node identity is significant: bookkeeping such as anchor
groups and table ledgers keys nodes by identity, so every node class uses
identity equality.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from typing import Literal

type SpanPlaceholderKind = Literal["colspan", "rowspan", "rowspan colspan"]


def _new_inlines() -> list[Inline]:
    return []


def _new_blocks() -> list[Block]:
    return []


def _new_cells() -> list[TableCell]:
    return []


def _new_rows() -> list[TableRow]:
    return []


def _new_items() -> list[ListItem]:
    return []


def _new_nested() -> list[NestedTable]:
    return []


def _new_groups() -> list[AnchorGroup]:
    return []


def _new_outcomes() -> list[SupSubOutcome]:
    return []


def _new_underlines() -> list[UnderlineOccurrence]:
    return []


def _new_fragment_map() -> dict[str, str]:
    return {}


def _new_names() -> list[str]:
    return []


@dataclass(slots=True, eq=False)
class Text:
    text: str


@dataclass(slots=True, eq=False)
class Emphasis:
    inlines: list[Inline] = field(default_factory=_new_inlines)


@dataclass(slots=True, eq=False)
class Strong:
    inlines: list[Inline] = field(default_factory=_new_inlines)


@dataclass(slots=True, eq=False)
class Strikethrough:
    inlines: list[Inline] = field(default_factory=_new_inlines)


@dataclass(slots=True, eq=False)
class Code:
    text: str


@dataclass(slots=True, eq=False)
class Link:
    href: str
    inlines: list[Inline] = field(default_factory=_new_inlines)
    title: str | None = None


@dataclass(slots=True, eq=False)
class Image:
    src: str
    alt: str
    title: str | None = None


@dataclass(slots=True, eq=False)
class LineBreak:
    pass


@dataclass(slots=True, eq=False)
class RawHtml:
    """An anchor-form ``a`` or an attribute-free ``sup``/``sub`` element."""

    element: str
    inlines: list[Inline] = field(default_factory=_new_inlines)
    anchor_id: str | None = None


@dataclass(slots=True, eq=False)
class SpanPlaceholder:
    """One exact span placeholder comment inserted by span expansion."""

    kind: SpanPlaceholderKind


@dataclass(slots=True, eq=False)
class AnchorMark:
    """A conversion-internal anchor position.

    The builder records source anchors as marks while it assembles inline runs,
    then converts them into page-level anchor groups. No mark survives into the
    page AST; the Markdown construct registry rejects one.
    """

    names: tuple[str, ...]
    preferred: str | None = None


type Inline = (
    Text
    | Emphasis
    | Strong
    | Strikethrough
    | Code
    | Link
    | Image
    | LineBreak
    | RawHtml
    | SpanPlaceholder
    | AnchorMark
)


@dataclass(slots=True, eq=False)
class TableCell:
    role: str
    row_span: int = 1
    col_span: int = 1
    blocks: list[Block] = field(default_factory=_new_blocks)


@dataclass(slots=True, eq=False)
class TableRow:
    cells: list[TableCell] = field(default_factory=_new_cells)


@dataclass(slots=True, eq=False)
class TableHeader:
    source: str
    rows: list[TableRow] = field(default_factory=_new_rows)
    repair_id: str | None = None


@dataclass(slots=True, eq=False)
class NestedTable:
    """A nested table that lowering moved out of its parent cell."""

    anchor_id: str
    description: str
    table: Table


@dataclass(slots=True, eq=False)
class Table:
    caption: list[Inline] | None
    header: TableHeader
    rows: list[TableRow] = field(default_factory=_new_rows)
    nested_tables: list[NestedTable] = field(default_factory=_new_nested)


@dataclass(slots=True, eq=False)
class Heading:
    level: int
    inlines: list[Inline] = field(default_factory=_new_inlines)


@dataclass(slots=True, eq=False)
class Paragraph:
    inlines: list[Inline] = field(default_factory=_new_inlines)


@dataclass(slots=True, eq=False)
class BlockQuote:
    blocks: list[Block] = field(default_factory=_new_blocks)


@dataclass(slots=True, eq=False)
class ListItem:
    blocks: list[Block] = field(default_factory=_new_blocks)


@dataclass(slots=True, eq=False)
class List:
    ordered: bool
    start: int
    tight: bool = True
    items: list[ListItem] = field(default_factory=_new_items)


@dataclass(slots=True, eq=False)
class CodeBlock:
    info: str | None
    text: str


@dataclass(slots=True, eq=False)
class ThematicBreak:
    pass


type Block = Heading | Paragraph | BlockQuote | List | CodeBlock | ThematicBreak | Table


@dataclass(slots=True, eq=False)
class Document:
    slug: str
    source_url: str
    blocks: list[Block] = field(default_factory=_new_blocks)


@dataclass(slots=True, eq=False)
class AnchorGroup:
    """Consecutive source anchors that render at one block position."""

    block: Block
    names: tuple[str, ...]
    preferred: str | None = None
    canonical_id: str | None = None


@dataclass(slots=True)
class AnchorRemerge:
    """An anchor group that a correction's emptied paragraph released."""

    names: tuple[str, ...]
    merged_into: str | None


@dataclass(slots=True)
class SupSubOutcome:
    tag: str
    text: str
    mode: str


@dataclass(slots=True)
class UnderlineOccurrence:
    text: str


@dataclass(slots=True)
class PageAst:
    """One page's AST plus the facts gathered while converting it."""

    document: Document
    anchor_groups: list[AnchorGroup] = field(default_factory=_new_groups)
    fragment_map: dict[str, str] = field(default_factory=_new_fragment_map)
    duplicate_anchors: list[str] = field(default_factory=_new_names)
    sup_sub_outcomes: list[SupSubOutcome] = field(default_factory=_new_outcomes)
    underline_occurrences: list[UnderlineOccurrence] = field(
        default_factory=_new_underlines
    )
    pre_markup_ignored: list[str] = field(default_factory=_new_names)

    @property
    def anchor_ids(self) -> set[str]:
        return {
            group.canonical_id
            for group in self.anchor_groups
            if group.canonical_id is not None
        }

    @property
    def anchor_groups_by_block(self) -> dict[int, AnchorGroup]:
        return {
            id(group.block): group
            for group in self.anchor_groups
            if group.canonical_id is not None
        }

    @property
    def blocks(self) -> list[Block]:
        return self.document.blocks

    def iter_blocks(self) -> Iterator[Block]:
        return iter_blocks(self.blocks)

    def iter_inlines(self) -> Iterator[Inline]:
        for block in iter_blocks(self.blocks):
            yield from iter_block_inlines(block)


# ---------------------------------------------------------------- traversal


def iter_child_blocks(block: Block) -> Iterator[Block]:
    """Yield the blocks directly contained by a block."""
    if isinstance(block, BlockQuote):
        yield from block.blocks
    elif isinstance(block, List):
        for item in block.items:
            yield from item.blocks
    elif isinstance(block, Table):
        for row in iter_rows(block):
            for cell in row.cells:
                yield from cell.blocks
        for nested in block.nested_tables:
            yield nested.table


def iter_blocks(blocks: Sequence[Block]) -> Iterator[Block]:
    """Every block depth-first in document order, including table cells."""
    for block in blocks:
        yield block
        yield from iter_blocks(list(iter_child_blocks(block)))


def iter_rows(table: Table) -> Iterator[TableRow]:
    yield from table.header.rows
    yield from table.rows


def iter_cells(table: Table) -> Iterator[TableCell]:
    for row in iter_rows(table):
        yield from row.cells
    for nested in table.nested_tables:
        yield from iter_cells(nested.table)


def iter_tables(blocks: Sequence[Block]) -> Iterator[Table]:
    """Every table depth-first in document order, including nested tables."""
    for block in blocks:
        if isinstance(block, Table):
            yield block
            for row in iter_rows(block):
                for cell in row.cells:
                    yield from iter_tables(cell.blocks)
            for nested in block.nested_tables:
                yield from iter_tables([nested.table])
            continue
        yield from iter_tables(list(iter_child_blocks(block)))


def iter_inlines(inlines: Sequence[Inline]) -> Iterator[Inline]:
    """Every inline depth-first in document order, including nested inlines."""
    for inline in inlines:
        yield inline
        yield from iter_inlines(_inline_children(inline))


def iter_block_inlines(block: Block) -> Iterator[Inline]:
    """Every inline that belongs directly to a paragraph or heading."""
    if isinstance(block, (Paragraph, Heading)):
        yield from iter_inlines(block.inlines)


def _inline_children(inline: Inline) -> list[Inline]:
    if isinstance(inline, (Emphasis, Strong, Strikethrough, Link, RawHtml)):
        return inline.inlines
    return []


def iter_block_locations(
    blocks: list[Block],
) -> Iterator[tuple[Block, list[Block], int]]:
    """Every block with its parent list and index, depth-first."""
    for index, block in enumerate(blocks):
        yield block, blocks, index
        if isinstance(block, BlockQuote):
            yield from iter_block_locations(block.blocks)
        elif isinstance(block, List):
            for item in block.items:
                yield from iter_block_locations(item.blocks)
        elif isinstance(block, Table):
            for row in iter_rows(block):
                for cell in row.cells:
                    yield from iter_block_locations(cell.blocks)
            for nested in block.nested_tables:
                yield from iter_block_locations([nested.table])


# --------------------------------------------------------------------- text


def inlines_text(inlines: Sequence[Inline]) -> str:
    parts: list[str] = []
    for inline in inlines:
        if isinstance(inline, (Text, Code)):
            parts.append(inline.text)
        elif isinstance(inline, Image):
            parts.append(inline.alt)
        elif isinstance(inline, (Emphasis, Strong, Strikethrough, Link, RawHtml)):
            parts.append(inlines_text(inline.inlines))
        elif isinstance(inline, LineBreak):
            parts.append(" ")
    return "".join(parts)


def inline_text(inline: Inline) -> str:
    return inlines_text([inline])


def block_text(block: Block) -> str:
    if isinstance(block, (Paragraph, Heading)):
        return inlines_text(block.inlines)
    if isinstance(block, CodeBlock):
        return block.text
    if isinstance(block, BlockQuote):
        return "\n".join(block_text(inner) for inner in block.blocks)
    if isinstance(block, List):
        return "\n".join(
            "\n".join(block_text(inner) for inner in item.blocks)
            for item in block.items
        )
    if isinstance(block, Table):
        return "\n".join(
            " | ".join(cell_text(cell) for cell in row.cells)
            for row in iter_rows(block)
        )
    return ""


def cell_text(cell: TableCell) -> str:
    parts = [block_text(block) for block in cell.blocks]
    return " ".join(part for part in parts if part)


# --------------------------------------------------------------- fingerprints


def _fingerprint(payload: object) -> str:
    data = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def inline_payload(inline: Inline) -> object:
    if isinstance(inline, Text):
        return {"type": "text", "text": inline.text}
    if isinstance(inline, Emphasis):
        return {"type": "emphasis", "inlines": _inlines_payload(inline.inlines)}
    if isinstance(inline, Strong):
        return {"type": "strong", "inlines": _inlines_payload(inline.inlines)}
    if isinstance(inline, Strikethrough):
        return {"type": "strikethrough", "inlines": _inlines_payload(inline.inlines)}
    if isinstance(inline, Code):
        return {"type": "code", "text": inline.text}
    if isinstance(inline, Link):
        return {
            "type": "link",
            "href": inline.href,
            "title": inline.title,
            "inlines": _inlines_payload(inline.inlines),
        }
    if isinstance(inline, Image):
        return {
            "type": "image",
            "src": inline.src,
            "alt": inline.alt,
            "title": inline.title,
        }
    if isinstance(inline, LineBreak):
        return {"type": "line-break"}
    if isinstance(inline, RawHtml):
        return {
            "type": "raw-html",
            "element": inline.element,
            "anchor_id": inline.anchor_id,
            "inlines": _inlines_payload(inline.inlines),
        }
    if isinstance(inline, SpanPlaceholder):
        return {"type": "span-placeholder", "kind": inline.kind}
    return {"type": "anchor-mark", "names": list(inline.names)}


def _inlines_payload(inlines: Sequence[Inline]) -> list[object]:
    return [inline_payload(inline) for inline in inlines]


def block_payload(block: Block) -> object:
    if isinstance(block, Heading):
        return {
            "type": "heading",
            "level": block.level,
            "inlines": _inlines_payload(block.inlines),
        }
    if isinstance(block, Paragraph):
        return {"type": "paragraph", "inlines": _inlines_payload(block.inlines)}
    if isinstance(block, BlockQuote):
        return {"type": "block-quote", "blocks": _blocks_payload(block.blocks)}
    if isinstance(block, List):
        return {
            "type": "list",
            "ordered": block.ordered,
            "start": block.start,
            "tight": block.tight,
            "items": [{"blocks": _blocks_payload(item.blocks)} for item in block.items],
        }
    if isinstance(block, CodeBlock):
        return {"type": "code-block", "info": block.info, "text": block.text}
    if isinstance(block, ThematicBreak):
        return {"type": "thematic-break"}
    return {
        "type": "table",
        "caption": (None if block.caption is None else _inlines_payload(block.caption)),
        "header": _rows_payload(block.header.rows),
        "rows": _rows_payload(block.rows),
    }


def _blocks_payload(blocks: Sequence[Block]) -> list[object]:
    return [block_payload(block) for block in blocks]


def _rows_payload(rows: Sequence[TableRow]) -> list[object]:
    return [row_payload(row) for row in rows]


def row_payload(row: TableRow) -> object:
    cells: list[object] = [
        {
            "role": cell.role,
            "row_span": cell.row_span,
            "col_span": cell.col_span,
            "blocks": _blocks_payload(cell.blocks),
        }
        for cell in row.cells
    ]
    return {"cells": cells}


def block_fingerprint(block: Block) -> str:
    return _fingerprint(block_payload(block))


def rows_fingerprint(rows: Sequence[TableRow]) -> str:
    return _fingerprint(_rows_payload(rows))


def table_fingerprint(table: Table) -> str:
    return _fingerprint(block_payload(table))


# -------------------------------------------------------------------- anchors


def build_fragment_map(
    groups: Sequence[AnchorGroup],
) -> tuple[dict[str, str], list[str]]:
    """Map each source fragment to its canonical local id.

    The first occurrence in document order wins, and the page record reports
    duplicate source names.
    """

    first: dict[str, str] = {}
    duplicates: list[str] = []
    for group in groups:
        if group.canonical_id is None:
            continue
        for name in group.names:
            previous = first.get(name)
            if previous is None:
                first[name] = group.canonical_id
            elif previous != group.canonical_id:
                duplicates.append(name)
    return first, duplicates


__all__ = [
    "AnchorGroup",
    "AnchorMark",
    "AnchorRemerge",
    "Block",
    "BlockQuote",
    "Code",
    "CodeBlock",
    "Document",
    "Emphasis",
    "Heading",
    "Image",
    "Inline",
    "LineBreak",
    "Link",
    "List",
    "ListItem",
    "NestedTable",
    "PageAst",
    "Paragraph",
    "RawHtml",
    "SpanPlaceholder",
    "SpanPlaceholderKind",
    "Strikethrough",
    "Strong",
    "SupSubOutcome",
    "Table",
    "TableCell",
    "TableHeader",
    "TableRow",
    "Text",
    "ThematicBreak",
    "UnderlineOccurrence",
    "block_fingerprint",
    "block_payload",
    "block_text",
    "build_fragment_map",
    "cell_text",
    "inline_payload",
    "inline_text",
    "inlines_text",
    "iter_block_inlines",
    "iter_block_locations",
    "iter_blocks",
    "iter_cells",
    "iter_child_blocks",
    "iter_inlines",
    "iter_rows",
    "iter_tables",
    "row_payload",
    "rows_fingerprint",
    "table_fingerprint",
]
