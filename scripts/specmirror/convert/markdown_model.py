"""The Markdown language model: constructs, content models, and raw HTML.

The model follows CommonMark 0.31.2 and the GFM extensions the build uses, which
are tables, strikethrough, and task-free list items. It declares the constructs
the renderer may emit, the marks and fences it uses, and the exact raw HTML
subset that may appear outside code. The renderer and the output validator both
read this model, so emission and acceptance can't drift apart.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .ast import (
    AnchorMark,
    Block,
    BlockQuote,
    Code,
    CodeBlock,
    Document,
    Emphasis,
    Heading,
    Image,
    Inline,
    LineBreak,
    Link,
    List,
    ListItem,
    PageAst,
    Paragraph,
    RawHtml,
    SpanPlaceholder,
    SpanPlaceholderKind,
    Strikethrough,
    Strong,
    Table,
    TableCell,
    TableRow,
    Text,
    ThematicBreak,
    iter_rows,
)


class Level(StrEnum):
    BLOCK = "block"
    INLINE = "inline"


class ContentModel(StrEnum):
    """The child content a construct accepts."""

    EMPTY = "empty"
    LITERAL = "literal"
    INLINES = "inlines"
    BLOCKS = "blocks"
    LIST_ITEMS = "list-items"
    TABLE_ROWS = "table-rows"


class ConstructKind(StrEnum):
    # container blocks
    BLOCK_QUOTE = "block-quote"
    LIST = "list"
    LIST_ITEM = "list-item"
    # leaf blocks
    THEMATIC_BREAK = "thematic-break"
    HEADING = "heading"
    CODE_BLOCK = "code-block"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    # Inlines
    CODE = "code"
    EMPHASIS = "emphasis"
    STRONG = "strong"
    STRIKETHROUGH = "strikethrough"
    LINK = "link"
    IMAGE = "image"
    LINE_BREAK = "line-break"
    TEXT = "text"
    # specific
    ANCHOR = "anchor"
    SUPERSCRIPT = "superscript"
    SUBSCRIPT = "subscript"
    SPAN_PLACEHOLDER = "span-placeholder"


@dataclass(frozen=True, slots=True)
class RawHtmlElement:
    """One raw HTML element form the renderer may emit outside code."""

    element: str
    attributes: frozenset[str] = frozenset()


@dataclass(frozen=True, slots=True)
class RawHtmlComment:
    """One exact raw HTML comment the renderer may emit outside code."""

    text: str


@dataclass(frozen=True, slots=True)
class ConstructSpec:
    """One CommonMark or GFM construct.

    ``markup`` names the canonical delimiter or line marker.
     ``raw_html`` lists the forms this construct may emit outside code.
    """

    kind: ConstructKind
    level: Level
    content: ContentModel
    markup: str | None = None
    raw_html: tuple[RawHtmlElement | RawHtmlComment, ...] = ()


RAW_HTML_A = RawHtmlElement("a", frozenset({"id"}))
RAW_HTML_BR = RawHtmlElement("br")
RAW_HTML_SUP = RawHtmlElement("sup")
RAW_HTML_SUB = RawHtmlElement("sub")
COMMENT_COLSPAN = RawHtmlComment("<!-- colspan -->")
COMMENT_ROWSPAN = RawHtmlComment("<!-- rowspan -->")
COMMENT_ROWSPAN_COLSPAN = RawHtmlComment("<!-- rowspan colspan -->")

SPAN_COMMENTS: dict[SpanPlaceholderKind, str] = {
    "colspan": COMMENT_COLSPAN.text,
    "rowspan": COMMENT_ROWSPAN.text,
    "rowspan colspan": COMMENT_ROWSPAN_COLSPAN.text,
}

_CONSTRUCTS: tuple[ConstructSpec, ...] = (
    ConstructSpec(
        ConstructKind.BLOCK_QUOTE, Level.BLOCK, ContentModel.BLOCKS, markup=">"
    ),
    ConstructSpec(ConstructKind.LIST, Level.BLOCK, ContentModel.LIST_ITEMS),
    ConstructSpec(ConstructKind.LIST_ITEM, Level.BLOCK, ContentModel.BLOCKS),
    ConstructSpec(
        ConstructKind.THEMATIC_BREAK, Level.BLOCK, ContentModel.EMPTY, markup="---"
    ),
    ConstructSpec(ConstructKind.HEADING, Level.BLOCK, ContentModel.INLINES, markup="#"),
    ConstructSpec(
        ConstructKind.CODE_BLOCK, Level.BLOCK, ContentModel.LITERAL, markup="```"
    ),
    ConstructSpec(ConstructKind.PARAGRAPH, Level.BLOCK, ContentModel.INLINES),
    ConstructSpec(ConstructKind.TABLE, Level.BLOCK, ContentModel.TABLE_ROWS),
    ConstructSpec(ConstructKind.CODE, Level.INLINE, ContentModel.LITERAL, markup="`"),
    ConstructSpec(
        ConstructKind.EMPHASIS, Level.INLINE, ContentModel.INLINES, markup="*"
    ),
    ConstructSpec(
        ConstructKind.STRONG, Level.INLINE, ContentModel.INLINES, markup="**"
    ),
    ConstructSpec(
        ConstructKind.STRIKETHROUGH, Level.INLINE, ContentModel.INLINES, markup="~~"
    ),
    ConstructSpec(ConstructKind.LINK, Level.INLINE, ContentModel.INLINES),
    ConstructSpec(ConstructKind.IMAGE, Level.INLINE, ContentModel.LITERAL),
    ConstructSpec(
        ConstructKind.LINE_BREAK,
        Level.INLINE,
        ContentModel.EMPTY,
        raw_html=(RAW_HTML_BR,),
    ),
    ConstructSpec(ConstructKind.TEXT, Level.INLINE, ContentModel.LITERAL),
    ConstructSpec(
        ConstructKind.ANCHOR,
        Level.INLINE,
        ContentModel.EMPTY,
        raw_html=(RAW_HTML_A,),
    ),
    ConstructSpec(
        ConstructKind.SUPERSCRIPT,
        Level.INLINE,
        ContentModel.INLINES,
        raw_html=(RAW_HTML_SUP,),
    ),
    ConstructSpec(
        ConstructKind.SUBSCRIPT,
        Level.INLINE,
        ContentModel.INLINES,
        raw_html=(RAW_HTML_SUB,),
    ),
    ConstructSpec(
        ConstructKind.SPAN_PLACEHOLDER,
        Level.INLINE,
        ContentModel.EMPTY,
        raw_html=(COMMENT_COLSPAN, COMMENT_ROWSPAN, COMMENT_ROWSPAN_COLSPAN),
    ),
)

CONSTRUCTS: dict[ConstructKind, ConstructSpec] = {
    construct.kind: construct for construct in _CONSTRUCTS
}

RAW_HTML_ELEMENTS: dict[str, RawHtmlElement] = {
    element.element: element
    for construct in _CONSTRUCTS
    for element in construct.raw_html
    if isinstance(element, RawHtmlElement)
}

RAW_HTML_COMMENTS: frozenset[str] = frozenset(
    comment.text
    for construct in _CONSTRUCTS
    for comment in construct.raw_html
    if isinstance(comment, RawHtmlComment)
)

EMPHASIS_MARKS: dict[ConstructKind, str] = {
    construct.kind: construct.markup
    for construct in _CONSTRUCTS
    if construct.markup is not None
}

LIST_MARKER = "-"
ORDERED_MARKER = "."
THEMATIC_BREAK = "---"
HEADING_MARKER = "#"
MAX_HEADING_LEVEL = 6
MAX_LIST_START = 999_999_999
CODE_FENCE = "```"
CODE_FENCE_CHARACTER = "`"
MIN_CODE_FENCE = 3

_NODE_CONSTRUCTS: dict[type[object], ConstructKind] = {
    BlockQuote: ConstructKind.BLOCK_QUOTE,
    List: ConstructKind.LIST,
    ListItem: ConstructKind.LIST_ITEM,
    ThematicBreak: ConstructKind.THEMATIC_BREAK,
    Heading: ConstructKind.HEADING,
    CodeBlock: ConstructKind.CODE_BLOCK,
    Paragraph: ConstructKind.PARAGRAPH,
    Table: ConstructKind.TABLE,
    Code: ConstructKind.CODE,
    Emphasis: ConstructKind.EMPHASIS,
    Strong: ConstructKind.STRONG,
    Strikethrough: ConstructKind.STRIKETHROUGH,
    Link: ConstructKind.LINK,
    Image: ConstructKind.IMAGE,
    LineBreak: ConstructKind.LINE_BREAK,
    Text: ConstructKind.TEXT,
    SpanPlaceholder: ConstructKind.SPAN_PLACEHOLDER,
}


def construct_for(node: object) -> ConstructSpec:
    """The construct of an AST node, or a failure for internal markers."""
    if isinstance(node, AnchorMark):
        raise ValueError("an anchor mark is conversion-internal")
    if isinstance(node, RawHtml):
        if node.element == "a":
            return CONSTRUCTS[ConstructKind.ANCHOR]
        if node.element == "sup":
            return CONSTRUCTS[ConstructKind.SUPERSCRIPT]
        if node.element == "sub":
            return CONSTRUCTS[ConstructKind.SUBSCRIPT]
        raise ValueError(f"raw HTML <{node.element}> is outside the subset")
    kind = _NODE_CONSTRUCTS.get(type(node))
    if kind is None:
        raise ValueError(f"{type(node).__name__} is not a Markdown construct")
    return CONSTRUCTS[kind]


def require_construct(node: Inline | Block | ListItem, *, where: str) -> None:
    """Validate one AST node and its descendants against the model."""
    if isinstance(node, AnchorMark):
        raise ValueError(f"{where}: an anchor mark must not reach the AST")
    try:
        construct_for(node)
    except ValueError as error:
        raise ValueError(f"{where}: {error}") from error
    if isinstance(node, Heading):
        if not 1 <= node.level <= MAX_HEADING_LEVEL:
            raise ValueError(f"{where}: heading level {node.level} is invalid")
        _require_inlines(node.inlines, where=where)
        return
    if isinstance(node, Paragraph):
        _require_inlines(node.inlines, where=where)
        return
    if isinstance(node, BlockQuote):
        for index, block in enumerate(node.blocks):
            require_construct(block, where=f"{where}.blocks[{index}]")
        return
    if isinstance(node, List):
        if not node.items:
            raise ValueError(f"{where}: list has no items")
        if not 0 <= node.start <= MAX_LIST_START:
            raise ValueError(f"{where}: list start is outside CommonMark")
        for index, item in enumerate(node.items):
            require_construct(item, where=f"{where}.items[{index}]")
        return
    if isinstance(node, ListItem):
        for index, block in enumerate(node.blocks):
            require_construct(block, where=f"{where}.blocks[{index}]")
        return
    if isinstance(node, CodeBlock):
        if node.info is not None and CODE_FENCE_CHARACTER in node.info:
            raise ValueError(f"{where}: code fence info contains a backtick")
        return
    if isinstance(node, Table):
        _require_table(node, where=where)
        return
    if isinstance(node, (Emphasis, Strong, Strikethrough)):
        _require_inlines(node.inlines, where=where)
        return
    if isinstance(node, Link):
        if not node.href:
            raise ValueError(f"{where}: link href is empty")
        _require_inlines(node.inlines, where=where)
        return
    if isinstance(node, Image):
        if not node.src:
            raise ValueError(f"{where}: image src is empty")
        return
    if isinstance(node, RawHtml):
        _require_raw_html(node, where=where)
        return
    if isinstance(node, SpanPlaceholder) and node.kind not in SPAN_COMMENTS:
        raise ValueError(f"{where}: unknown span placeholder {node.kind!r}")


def _require_inlines(inlines: list[Inline], *, where: str) -> None:
    for index, inline in enumerate(inlines):
        require_construct(inline, where=f"{where}.inlines[{index}]")


def _require_table(table: Table, *, where: str) -> None:
    if table.caption is not None:
        _require_inlines(table.caption, where=f"{where}.caption")
    for index, row in enumerate(iter_rows(table)):
        _require_row(row, where=f"{where}.rows[{index}]")
    for index, nested in enumerate(table.nested_tables):
        _require_table(nested.table, where=f"{where}.nested_tables[{index}]")


def _require_row(row: TableRow, *, where: str) -> None:
    for index, cell in enumerate(row.cells):
        _require_cell(cell, where=f"{where}.cells[{index}]")


def _require_cell(cell: TableCell, *, where: str) -> None:
    if cell.role not in {"td", "th"}:
        raise ValueError(f"{where}: cell role {cell.role!r} is invalid")
    if cell.row_span < 1 or cell.col_span < 1:
        raise ValueError(f"{where}: cell span must be positive")
    for index, block in enumerate(cell.blocks):
        require_construct(block, where=f"{where}.blocks[{index}]")


def _require_raw_html(node: RawHtml, *, where: str) -> None:
    element = RAW_HTML_ELEMENTS.get(node.element)
    if element is None:
        raise ValueError(f"{where}: raw HTML <{node.element}> is not allowed")
    if node.element == "a":
        if node.anchor_id is None:
            raise ValueError(f"{where}: raw anchor requires an id")
        if node.inlines:
            raise ValueError(f"{where}: raw anchor must not carry content")
        return
    if node.anchor_id is not None:
        raise ValueError(f"{where}: raw <{node.element}> must not carry an id")
    _require_inlines(node.inlines, where=where)


def validate_page_ast(page: PageAst, *, where: str = "page") -> None:
    """Validate the complete page tree against the construct registry."""
    require_construct_document(page.document, where=where)
    for inline in page.iter_inlines():
        if isinstance(inline, AnchorMark):
            raise ValueError(f"{where}: an anchor mark survived conversion")


def require_construct_document(document: Document, *, where: str) -> None:
    for index, block in enumerate(document.blocks):
        require_construct(block, where=f"{where}.blocks[{index}]")


__all__ = [
    "CODE_FENCE",
    "CODE_FENCE_CHARACTER",
    "COMMENT_COLSPAN",
    "COMMENT_ROWSPAN",
    "COMMENT_ROWSPAN_COLSPAN",
    "CONSTRUCTS",
    "EMPHASIS_MARKS",
    "HEADING_MARKER",
    "LIST_MARKER",
    "MAX_HEADING_LEVEL",
    "MAX_LIST_START",
    "MIN_CODE_FENCE",
    "ORDERED_MARKER",
    "RAW_HTML_A",
    "RAW_HTML_BR",
    "RAW_HTML_COMMENTS",
    "RAW_HTML_ELEMENTS",
    "RAW_HTML_SUB",
    "RAW_HTML_SUP",
    "SPAN_COMMENTS",
    "THEMATIC_BREAK",
    "ConstructKind",
    "ConstructSpec",
    "ContentModel",
    "Level",
    "RawHtmlComment",
    "RawHtmlElement",
    "construct_for",
    "require_construct",
    "require_construct_document",
    "validate_page_ast",
]
