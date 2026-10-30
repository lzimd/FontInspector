"""Deterministic serialization of the page AST to Markdown.

The renderer emits only constructs declared in the Markdown language model.
It escapes every text run the same way for the same context, so output
doesn't depend on ambient Markdown state or on a Markdown renderer's slug
algorithm. The renderer limits raw HTML to anchor elements, line breaks,
superscript and subscript elements, and the three exact table span placeholder
comments.
"""

from __future__ import annotations

import re
from urllib.parse import quote

from ..errors import BuildError
from .ast import (
    AnchorGroup,
    AnchorMark,
    Block,
    BlockQuote,
    Code,
    CodeBlock,
    Emphasis,
    Heading,
    Image,
    Inline,
    LineBreak,
    Link,
    List,
    PageAst,
    Paragraph,
    RawHtml,
    SpanPlaceholder,
    Strikethrough,
    Strong,
    Table,
    TableCell,
    Text,
    ThematicBreak,
)
from .markdown_model import (
    EMPHASIS_MARKS,
    HEADING_MARKER,
    MAX_HEADING_LEVEL,
    ORDERED_MARKER,
    SPAN_COMMENTS,
    THEMATIC_BREAK,
    ConstructKind,
)
from .normalize import normalize_code_span

_LINES_STARTING_BLOCKS = ("#", ">", "-", "+", "=")
_ORDERED_MARKER = re.compile(r"^(\d{1,9})([.)])( |$)")
_BACKTICK_RUN = re.compile(r"`+")
_SPACE_OR_NBSP_RUN = re.compile(r"[ \xa0]+")


class Renderer:
    """Renders one page AST into Markdown text."""

    def __init__(self, anchor_groups: list[AnchorGroup]) -> None:
        self._anchor_groups_by_block: dict[int, AnchorGroup] = {
            id(group.block): group
            for group in anchor_groups
            if group.canonical_id is not None
        }

    def render_page(self, page: PageAst) -> str:
        return self.render_blocks(page.document.blocks)

    def render_blocks(self, blocks: list[Block]) -> str:
        parts: list[str] = []
        for block in blocks:
            group = self._anchor_groups_by_block.get(id(block))
            if group is not None and group.canonical_id is not None:
                parts.append(_anchor_element(group.canonical_id))
            rendered = self.render_block(block)
            if rendered:
                parts.append(rendered)
        return "\n\n".join(parts)

    def render_block(self, block: Block) -> str:
        match block:
            case Heading():
                return self._render_heading(block)
            case Paragraph():
                text = self.render_inlines(block.inlines, line_start=True).strip()
                return _escape_line_start(text) if text else ""
            case BlockQuote():
                return self._render_block_quote(block)
            case List():
                return self._render_list(block)
            case CodeBlock():
                return self._render_code_block(block)
            case ThematicBreak():
                return THEMATIC_BREAK
            case Table():
                return self.render_table(block)
        raise BuildError(f"cannot render {type(block).__name__}")

    def _render_heading(self, heading: Heading) -> str:
        if not 1 <= heading.level <= MAX_HEADING_LEVEL:
            raise BuildError(f"heading level {heading.level} is invalid")
        marker = HEADING_MARKER * heading.level
        text = self.render_inlines(heading.inlines).strip()
        return f"{marker} {text}".rstrip() if text else marker

    def _render_block_quote(self, quote: BlockQuote) -> str:
        inner = self.render_blocks(quote.blocks)
        if not inner:
            return ">"
        return "\n".join(f"> {line}" if line else ">" for line in inner.split("\n"))

    def _render_list(self, block: List) -> str:
        items: list[str] = []
        number = block.start
        for item in block.items:
            marker = ORDERED_MARKER if block.ordered else "-"
            prefix = f"{number}{marker}" if block.ordered else marker
            number += 1
            indent = " " * (len(prefix) + 1)
            rendered = self.render_blocks(item.blocks)
            lines = rendered.split("\n") if rendered else [""]
            first, *rest = lines
            first_line = f"{prefix} {first}".rstrip() if first else prefix
            continuation = [f"{indent}{line}".rstrip() if line else "" for line in rest]
            items.append("\n".join([first_line, *continuation]))
        separator = "\n" if block.tight else "\n\n"
        return separator.join(items)

    def _render_code_block(self, block: CodeBlock) -> str:
        """Render a code block as a CommonMark fenced code block.

        A content line with enough leading backticks could act as a closing
        fence, so the renderer uses the longest backtick run plus one, at
        least three, as a conservative guard against early closure.
        """
        runs = _BACKTICK_RUN.findall(block.text)
        longest = max((len(run) for run in runs), default=0)
        fence = "`" * max(3, longest + 1)
        info = block.info or ""
        if "`" in info:
            raise BuildError("code block info string contains a backtick")
        return f"{fence}{info}\n{block.text}\n{fence}"

    # ----------------------------------------------------------------- tables

    def render_table(self, table: Table) -> str:
        parts: list[str] = []
        width = _table_width(table)
        if width == 0:
            raise BuildError("table has no columns")
        if len(table.header.rows) > 1:
            raise BuildError("table header was not flattened before rendering")
        header = table.header.rows[0] if table.header.rows else None
        header_cells = (
            [self._render_cell(cell) for cell in header.cells]
            if header is not None
            else []
        )
        header_cells.extend([""] * (width - len(header_cells)))
        parts.append("| " + " | ".join(header_cells) + " |")
        parts.append("| " + " | ".join(["---"] * width) + " |")
        for row in table.rows:
            cells = [self._render_cell(cell) for cell in row.cells]
            cells.extend([""] * (width - len(cells)))
            parts.append("| " + " | ".join(cells) + " |")
        text = "\n".join(parts)
        if table.caption:
            caption = self._render_marked_inlines(
                table.caption, ConstructKind.EMPHASIS, False
            )
            text = f"{caption}\n\n{text}"
        for nested in table.nested_tables:
            text = (
                f"{text}\n\n"
                f"{_anchor_element(nested.anchor_id)}\n\n"
                f"{escape_text(nested.description)}\n\n"
                f"{self.render_table(nested.table)}"
            )
        return text

    def _render_cell(self, cell: TableCell) -> str:
        if not cell.blocks:
            return ""
        if len(cell.blocks) != 1 or not isinstance(cell.blocks[0], Paragraph):
            raise BuildError("table cell was not flattened before rendering")
        return self.render_inlines(cell.blocks[0].inlines, in_table=True)

    # ---------------------------------------------------------------- inlines

    def render_inlines(
        self,
        inlines: list[Inline],
        *,
        in_table: bool = False,
        line_start: bool = False,
    ) -> str:
        parts: list[str] = []
        at_start = line_start
        for inline in inlines:
            if isinstance(inline, Text):
                parts.append(
                    escape_text(
                        inline.text,
                        in_table=in_table,
                        line_start=at_start,
                    )
                )
            else:
                parts.append(self.render_inline(inline, in_table=in_table))
            at_start = False
        return "".join(parts)

    def render_inline(self, inline: Inline, *, in_table: bool = False) -> str:
        match inline:
            case Text():
                return escape_text(inline.text, in_table=in_table)
            case Code():
                return render_code_span(inline.text, in_table=in_table)
            case Emphasis():
                return self._render_marked_inlines(
                    inline.inlines, ConstructKind.EMPHASIS, in_table
                )
            case Strong():
                return self._render_marked_inlines(
                    inline.inlines, ConstructKind.STRONG, in_table
                )
            case Strikethrough():
                return self._render_marked_inlines(
                    inline.inlines, ConstructKind.STRIKETHROUGH, in_table
                )
            case Link():
                return self._render_link(inline, in_table=in_table)
            case Image():
                return self._render_image(inline, in_table=in_table)
            case LineBreak():
                return "<br>"
            case RawHtml():
                return self._render_raw_html(inline, in_table=in_table)
            case SpanPlaceholder():
                try:
                    return SPAN_COMMENTS[inline.kind]
                except KeyError as error:
                    raise BuildError(
                        f"unknown span placeholder {inline.kind!r}"
                    ) from error
            case AnchorMark():
                raise BuildError("an anchor mark reached the renderer")
        raise BuildError(f"cannot render {type(inline).__name__}")

    def _render_marked_inlines(
        self,
        inlines: list[Inline],
        kind: ConstructKind,
        in_table: bool,
    ) -> str:
        mark = EMPHASIS_MARKS.get(kind)
        if mark is None:
            raise BuildError(f"{kind} has no emphasis mark")
        inner = self.render_inlines(inlines, in_table=in_table)
        stripped = inner.strip(" ")
        if not stripped:
            return inner
        leading = " " if inner.startswith(" ") else ""
        trailing = " " if inner.endswith(" ") else ""
        return f"{leading}{mark}{stripped}{mark}{trailing}"

    def _render_link(self, link: Link, *, in_table: bool) -> str:
        text = self.render_inlines(link.inlines, in_table=in_table)
        if not text:
            text = escape_text(link.href, in_table=in_table)
        return f"[{text}]({_escape_href(link.href)}{_title(link.title)})"

    def _render_image(self, image: Image, *, in_table: bool) -> str:
        alt = escape_text(image.alt, in_table=in_table)
        return f"![{alt}]({_escape_href(image.src)}{_title(image.title)})"

    def _render_raw_html(self, node: RawHtml, *, in_table: bool) -> str:
        if node.element == "a":
            if node.anchor_id is None:
                raise BuildError("raw anchor has no id")
            return _anchor_element(node.anchor_id)
        if node.element in {"sup", "sub"}:
            inner = self.render_inlines(node.inlines, in_table=in_table)
            return f"<{node.element}>{inner}</{node.element}>"
        raise BuildError(f"raw HTML <{node.element}> is outside the subset")


def render_page(page: PageAst) -> str:
    return Renderer(page.anchor_groups).render_page(page)


def _anchor_element(anchor_id: str) -> str:
    escaped = anchor_id.replace("&", "&amp;").replace('"', "&quot;")
    return f'<a id="{escaped}"></a>'


def _table_width(table: Table) -> int:
    rows = [*table.header.rows, *table.rows]
    if not rows:
        return 0
    return max(len(row.cells) for row in rows)


def _title(title: str | None) -> str:
    if not title:
        return ""
    escaped = title.replace("\\", "\\\\").replace('"', '\\"')
    return f' "{escaped}"'


def _escape_href(href: str) -> str:
    value = href.replace("(", "%28").replace(")", "%29")
    value = quote(value, safe="/%#:@&?=+$,;!*'[]~")
    return value.replace(" ", "%20")


def render_code_span(text: str, *, in_table: bool) -> str:
    """Render a code span with a delimiter length absent from its content.

    CommonMark closes a code span at the first backtick run of the same length
    as the opening delimiter, so a matching run would truncate the span. The
    longest-run-plus-one rule is a conservative, deterministic way to satisfy
    that condition. Content that starts or ends with a backtick gets one padding
    space on each side so the CommonMark trim rule keeps the backticks.
    """
    value = normalize_code_span(text)
    if in_table:
        value = value.replace("|", "\\|")
    runs = _BACKTICK_RUN.findall(value)
    longest = max((len(run) for run in runs), default=0)
    delimiter = "`" * (longest + 1)
    if value.startswith("`") or value.endswith("`"):
        return f"{delimiter} {value} {delimiter}"
    return f"{delimiter}{value}{delimiter}"


def escape_text(
    text: str,
    *,
    line_start: bool = False,
    in_table: bool = False,
) -> str:
    """Escape Markdown metacharacters deterministically."""
    if in_table:
        expanded = text.replace("\xa0", "&nbsp;")
    else:
        expanded = _SPACE_OR_NBSP_RUN.sub(
            lambda match: " " if "\xa0" in match.group(0) else match.group(0),
            text,
        )
    characters: list[str] = []
    previous: str | None = None
    for index, character in enumerate(expanded):
        following: str | None = (
            expanded[index + 1] if index + 1 < len(expanded) else None
        )
        match character:
            case "\\":
                characters.append("\\\\")
            case "*":
                characters.append("\\*")
            case "`":
                characters.append("\\`")
            case "[" | "]":
                characters.append(f"\\{character}")
            case "<":
                characters.append("\\<")
            case ">":
                characters.append("\\>")
            case "_":
                characters.append("\\_")
            case "~":
                if following == "~" or previous == "~":
                    characters.append("\\~")
                else:
                    characters.append(character)
            case "|":
                characters.append("\\|" if in_table else character)
            case _:
                characters.append(character)
        previous = character
    result = "".join(characters)
    if line_start:
        result = _escape_line_start(result)
    return result


def _escape_line_start(line: str) -> str:
    if line.startswith(_LINES_STARTING_BLOCKS):
        return f"\\{line}"
    match = _ORDERED_MARKER.match(line)
    if match is not None:
        return f"{match.group(1)}\\{match.group(2)}{line[match.end(2) :]}"
    return line


__all__ = [
    "Renderer",
    "escape_text",
    "render_code_span",
    "render_page",
]
