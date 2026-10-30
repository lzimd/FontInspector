"""Orchestration from the normalized neutral subtree to the page AST.

The builder dispatches over the HTML registry's conversion intents, applies
the style-derived emphasis facts that normalization recorded, and turns
source anchors into page-level anchor groups. It consumes adapter nodes only
and never serializes the DOM back to HTML.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

from ..dom import (
    DomElement,
    DomText,
    attribute_text,
    class_names,
    text_content,
)
from ..errors import BuildError, ValidationError
from ..urls import resolve_link_reference, resolve_url
from .ast import (
    AnchorGroup,
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
    Strikethrough,
    Strong,
    SupSubOutcome,
    Table,
    TableCell,
    TableHeader,
    TableRow,
    Text,
    ThematicBreak,
    UnderlineOccurrence,
    build_fragment_map,
    iter_block_inlines,
    iter_blocks,
)
from .html_model import (
    BlockIntent,
    ElementSpec,
    InlineIntent,
    Strategy,
    accepts_parent,
    is_heading,
    resolve_element,
)
from .markdown_model import MAX_LIST_START
from .normalize import (
    is_ascii_digit_text,
    normalize_label,
    sanitize_identifier,
    to_subscript,
    to_superscript,
)

_LANGUAGE_CLASS = re.compile(r"^(?:language|lang)-(?P<language>.+)$")
_SAFE_LANGUAGE = re.compile(r"^[A-Za-z0-9_+.#-]+$")


@dataclass(frozen=True, slots=True)
class _AnchorName:
    name: str
    preferred: bool = False


@dataclass(slots=True)
class _ConversionState:
    page: str
    slug: str
    page_url: str
    italic: dict[DomElement, bool]
    pending_anchor_names: list[_AnchorName]
    anchor_groups: list[AnchorGroup]
    anchor_groups_by_block: dict[int, AnchorGroup]
    sup_sub_outcomes: list[SupSubOutcome]
    underline_occurrences: list[UnderlineOccurrence]
    pre_markup_ignored: list[str]


def _new_pending_anchor_names() -> list[_AnchorName]:
    return []


def _new_anchor_groups() -> list[AnchorGroup]:
    return []


def _new_anchor_groups_by_block() -> dict[int, AnchorGroup]:
    return {}


def _new_outcomes() -> list[SupSubOutcome]:
    return []


def _new_underlines() -> list[UnderlineOccurrence]:
    return []


def _new_names() -> list[str]:
    return []


class _Builder:
    def __init__(
        self,
        *,
        page: str,
        slug: str,
        page_url: str,
        italic: dict[DomElement, bool],
    ) -> None:
        self.state = _ConversionState(
            page=page,
            slug=slug,
            page_url=page_url,
            italic=italic,
            pending_anchor_names=_new_pending_anchor_names(),
            anchor_groups=_new_anchor_groups(),
            anchor_groups_by_block=_new_anchor_groups_by_block(),
            sup_sub_outcomes=_new_outcomes(),
            underline_occurrences=_new_underlines(),
            pre_markup_ignored=_new_names(),
        )

    # ------------------------------------------------------------------ entry

    def build(self, roots: tuple[DomElement, ...]) -> PageAst:
        blocks: list[Block] = []
        for root in roots:
            self._record_pending_anchors(root, preferred=False)
            blocks.extend(self._convert_blocks(root, parent=None))
        self._flush_pending_anchors(blocks)
        self._order_anchor_groups(blocks)
        self._assign_anchor_group_ids()
        fragment_map, duplicates = build_fragment_map(self.state.anchor_groups)
        self._assert_no_marks(blocks)
        return PageAst(
            document=Document(
                slug=self.state.slug,
                source_url=self.state.page_url,
                blocks=blocks,
            ),
            anchor_groups=self.state.anchor_groups,
            fragment_map=fragment_map,
            duplicate_anchors=duplicates,
            sup_sub_outcomes=self.state.sup_sub_outcomes,
            underline_occurrences=self.state.underline_occurrences,
            pre_markup_ignored=self.state.pre_markup_ignored,
        )

    # --------------------------------------------------------------- anchoring

    def _flush_pending_anchors(self, blocks: list[Block]) -> None:
        if not self.state.pending_anchor_names:
            return
        names = self._take_pending_anchors()
        if blocks:
            self._attach_anchor_group(blocks[-1], names, prepend=False)
            return
        paragraph = Paragraph(inlines=[])
        self._attach_anchor_group(paragraph, names, prepend=False)
        blocks.append(paragraph)

    def _record_pending_anchors(self, element: DomElement, *, preferred: bool) -> None:
        for name in _source_anchor_names(element):
            self.state.pending_anchor_names.append(
                _AnchorName(name=name, preferred=preferred)
            )

    def _anchor_marks(self, element: DomElement) -> list[Inline]:
        names = _source_anchor_names(element)
        if not names:
            return []
        return [AnchorMark(names=tuple(names))]

    def _take_pending_anchors(self) -> list[_AnchorName]:
        taken = self.state.pending_anchor_names
        self.state.pending_anchor_names = _new_pending_anchor_names()
        return taken

    def _attach_anchor_group(
        self, block: Block, names: list[_AnchorName], *, prepend: bool
    ) -> None:
        if not names:
            return
        unique = _unique_anchor_names(names)
        existing = self.state.anchor_groups_by_block.get(id(block))
        preferred = existing.preferred if existing is not None else None
        if preferred is None:
            preferred = next((name.name for name in unique if name.preferred), None)
        new_names = tuple(name.name for name in unique)
        if existing is None:
            group = AnchorGroup(block=block, names=new_names, preferred=preferred)
            self.state.anchor_groups.append(group)
            self.state.anchor_groups_by_block[id(block)] = group
            return
        # else: existing anchor_group
        if prepend:
            merged_names = (*new_names, *existing.names)
        else:
            merged_names = (*existing.names, *new_names)
        existing.names = tuple(_dedupe_names(merged_names))
        existing.preferred = preferred or existing.preferred

    def _order_anchor_groups(self, blocks: list[Block]) -> None:
        order = {id(block): index for index, block in enumerate(iter_blocks(blocks))}
        self.state.anchor_groups.sort(
            key=lambda group: order.get(id(group.block), len(order))
        )

    def _assign_anchor_group_ids(self) -> None:
        used: set[str] = set()
        part = 0
        for group in self.state.anchor_groups:
            source = group.preferred or (group.names[0] if group.names else None)
            if source is None:
                part += 1
                base = f"anchor-{self.state.slug}-part-{part}"
            else:
                base = f"anchor-{self.state.slug}-{sanitize_identifier(source)}"
            group.canonical_id = _unique_local_id(base, source, used)

    def _assert_no_marks(self, blocks: list[Block]) -> None:
        for block in iter_blocks(blocks):
            for inline in iter_block_inlines(block):
                if isinstance(inline, AnchorMark):
                    raise BuildError(
                        f"anchor mark survived conversion on page {self.state.page}"
                    )

    # -------------------------------------------------------- block dispatch

    def _convert_blocks(
        self,
        container: DomElement,
        *,
        parent: ElementSpec | None,
    ) -> list[Block]:
        parent_name = parent.name if parent is not None else None
        blocks: list[Block] = []
        run: list[Inline] = []
        for child in container.children:
            if isinstance(child, DomText):
                self._append_text(run, container, child.text)
                continue
            if not isinstance(child, DomElement):
                continue
            spec = self._resolve(child)
            if spec.required_parents and not accepts_parent(spec, parent_name):
                raise BuildError(
                    f"<{child.name}> is outside its required context on page "
                    f"{self.state.page}"
                )
            block_producing = self._produces_blocks(spec, child)
            if not block_producing:
                run.extend(self._anchor_marks(child))
                run.extend(self._convert_run_element(child, spec))
                continue
            # else: block_producing == True
            self._flush_run(blocks, run)
            self._record_pending_anchors(child, preferred=is_heading(spec))
            if spec.strategy is Strategy.TRANSPARENT:
                blocks.extend(self._convert_blocks(child, parent=spec))
                continue
            carried = self._take_pending_anchors()
            converted = self._convert_block_element(child, spec)
            leftover = self._take_pending_anchors()
            if converted:
                self._attach_anchor_group(converted[0], carried, prepend=True)
                self.state.pending_anchor_names = leftover
            else:
                self.state.pending_anchor_names = [*carried, *leftover]
            blocks.extend(converted)
        self._flush_run(blocks, run)
        return blocks

    def _produces_blocks(self, spec: ElementSpec, element: DomElement) -> bool:
        if spec.block is not None:
            return True
        if spec.strategy is not Strategy.TRANSPARENT:
            return False
        for child in element.children:
            if not isinstance(child, DomElement):
                continue
            if self._produces_blocks(self._resolve(child), child):
                return True
        return False

    def _convert_block_element(
        self,
        element: DomElement,
        spec: ElementSpec,
    ) -> list[Block]:
        match spec.block:
            case BlockIntent.BLOCK_QUOTE:
                return self._convert_blockquote(element, spec)
            case BlockIntent.LIST:
                return [self._convert_list(element, spec)]
            case BlockIntent.THEMATIC_BREAK:
                return [ThematicBreak()]
            case BlockIntent.HEADING:
                return [self._convert_heading(element)]
            case BlockIntent.CODE_BLOCK:
                return [self._convert_code_block(element)]
            case BlockIntent.PARAGRAPH:
                return self._convert_blocks(element, parent=spec)
            case BlockIntent.TABLE:
                return [self._convert_table(element)]
            case BlockIntent.DEFINITION_LIST:
                return self._convert_definition_list(element)
            case BlockIntent.FIGURE:
                return [self._convert_figure(element)]
            case _:
                pass
        raise BuildError(
            f"<{element.name}> is outside its required context on page "
            f"{self.state.page}"
        )

    def _flush_run(
        self,
        blocks: list[Block],
        run: list[Inline],
    ) -> None:
        inlines = _assemble(run)
        run.clear()
        if not inlines:
            return
        nontrailing_marks, kept_inlines, trailing_marks = _split_anchor_marks(inlines)
        if not kept_inlines:
            self.state.pending_anchor_names.extend(nontrailing_marks)
            self.state.pending_anchor_names.extend(trailing_marks)
            return
        self.state.pending_anchor_names.extend(nontrailing_marks)
        paragraph = Paragraph(inlines=kept_inlines)
        self._attach_anchor_group(
            paragraph,
            self._take_pending_anchors(),
            prepend=False,
        )
        self.state.pending_anchor_names = trailing_marks
        blocks.append(paragraph)

    def _convert_heading(self, element: DomElement) -> Heading:
        inlines = self._inlines(element)
        kept_inlines, heading_marks = _extract_content_inlines_with_marks(inlines)
        if heading_marks and not _source_anchor_names(element):
            heading_marks[0] = _AnchorName(
                name=heading_marks[0].name,
                preferred=True,
            )
        self.state.pending_anchor_names.extend(heading_marks)
        heading = Heading(level=int(element.name[1]), inlines=kept_inlines)
        self._attach_anchor_group(
            heading,
            self._take_pending_anchors(),
            prepend=False,
        )
        self._ensure_heading_anchor_group(heading)
        return heading

    def _ensure_heading_anchor_group(self, heading: Heading) -> None:
        if id(heading) in self.state.anchor_groups_by_block:
            return
        group = AnchorGroup(block=heading, names=())
        self.state.anchor_groups.append(group)
        self.state.anchor_groups_by_block[id(heading)] = group

    # ------------------------------------------------------- inline dispatch

    def _inlines(self, element: DomElement, *, trim: bool = True) -> list[Inline]:
        run: list[Inline] = []
        for child in element.children:
            if isinstance(child, DomText):
                self._append_text(run, element, child.text)
                continue
            if not isinstance(child, DomElement):
                continue
            spec = self._resolve(child)
            run.extend(self._anchor_marks(child))
            run.extend(self._convert_run_element(child, spec))
        return _assemble(run, trim=trim)

    def _convert_run_element(
        self,
        element: DomElement,
        spec: ElementSpec,
    ) -> list[Inline]:
        produced = self._convert_inline_element(element, spec)
        if spec.inline is InlineIntent.CODE and self.state.italic.get(element, False):
            return _wrap_style_emphasis(produced)
        return produced

    def _append_text(
        self,
        run: list[Inline],
        element: DomElement,
        text: str,
    ) -> None:
        if text.strip() and self.state.italic.get(element, False):
            run.append(Emphasis(inlines=[Text(text=text)]))
            return
        run.append(Text(text=text))

    def _convert_inline_element(
        self,
        element: DomElement,
        spec: ElementSpec,
    ) -> list[Inline]:
        match spec.strategy:
            case Strategy.CONTEXT_ONLY:
                raise BuildError(
                    f"<{element.name}> is outside its required context on page "
                    f"{self.state.page}"
                )
            case Strategy.BLOCK:
                raise BuildError(
                    f"block element <{element.name}> in inline content on page "
                    f"{self.state.page}"
                )
            case Strategy.TRANSPARENT:
                return self._inlines(element)
            case _:
                pass

        match spec.inline:
            case InlineIntent.EMPHASIS:
                return [
                    Emphasis(
                        inlines=_merge_emphasis(self._inlines(element, trim=False))
                    )
                ]
            case InlineIntent.STRONG:
                return [
                    Strong(inlines=_merge_strong(self._inlines(element, trim=False)))
                ]
            case InlineIntent.STRIKETHROUGH:
                return [Strikethrough(inlines=self._inlines(element))]
            case InlineIntent.CODE:
                return self._convert_inline_code(element)
            case InlineIntent.LINK:
                return self._convert_link(element)
            case InlineIntent.IMAGE:
                return [self._convert_image(element)]
            case InlineIntent.LINE_BREAK:
                return [LineBreak()]
            case InlineIntent.SUPERSCRIPT:
                return self._convert_sup_sub(element, InlineIntent.SUPERSCRIPT)
            case InlineIntent.SUBSCRIPT:
                return self._convert_sup_sub(element, InlineIntent.SUBSCRIPT)
            case InlineIntent.UNDERLINE:
                self.state.underline_occurrences.append(
                    UnderlineOccurrence(text=text_content(element))
                )
                return self._inlines(element)
            case InlineIntent.WRAPPER:
                return self._inlines(element)
            case _:
                pass
        raise BuildError(
            f"unhandled inline element <{element.name}> on page {self.state.page}"
        )

    def _convert_link(self, element: DomElement) -> list[Inline]:
        href = attribute_text(element, "href")
        if href is None or not href.strip():
            return self._inlines(element)
        title = attribute_text(element, "title")
        normalized_title = _label_or_none(title)
        try:
            target = resolve_link_reference(self.state.page_url, href.strip())
        except ValidationError as error:
            raise BuildError(
                f"link target is invalid on page {self.state.page}: {error}"
            ) from error
        return [
            Link(href=target, inlines=self._inlines(element), title=normalized_title)
        ]

    def _convert_image(self, element: DomElement) -> Image:
        src = attribute_text(element, "src")
        if src is None or not src.strip():
            raise BuildError(f"img without src on page {self.state.page}")
        try:
            target = resolve_url(self.state.page_url, src.strip())
        except ValidationError as error:
            raise BuildError(
                f"image source is invalid on page {self.state.page}: {error}"
            ) from error
        alt = attribute_text(element, "alt")
        title = attribute_text(element, "title")
        return Image(
            src=target,
            alt=normalize_label(alt) if alt else "",
            title=_label_or_none(title),
        )

    def _convert_sup_sub(
        self,
        element: DomElement,
        intent: InlineIntent,
    ) -> list[Inline]:
        tag = "sup" if intent is InlineIntent.SUPERSCRIPT else "sub"
        has_element_child = any(
            isinstance(child, DomElement) for child in element.children
        )
        text = "".join(
            child.text for child in element.children if isinstance(child, DomText)
        )
        if not has_element_child and is_ascii_digit_text(text):
            converted = to_superscript(text) if tag == "sup" else to_subscript(text)
            self.state.sup_sub_outcomes.append(
                SupSubOutcome(tag=tag, text=text, mode="unicode")
            )
            return [Text(text=converted)]
        self.state.sup_sub_outcomes.append(
            SupSubOutcome(tag=tag, text=text_content(element), mode="html")
        )
        return [RawHtml(element=tag, inlines=self._inlines(element))]

    def _convert_inline_code(self, element: DomElement) -> list[Inline]:
        result: list[Inline] = []
        self._collect_inline_code(element, result)
        return _merge_adjacent_code(result)

    def _collect_inline_code(
        self,
        element: DomElement,
        result: list[Inline],
    ) -> None:
        for child in element.children:
            if isinstance(child, DomText):
                if child.text:
                    result.append(Code(text=child.text))
                continue
            if not isinstance(child, DomElement):
                continue
            result.extend(self._anchor_marks(child))
            if child.name == "a" and _has_link_target(child):
                result.append(self._code_link(child))
                continue
            self._collect_inline_code(child, result)

    def _code_link(self, element: DomElement) -> Link:
        href = attribute_text(element, "href")
        assert href is not None
        title = attribute_text(element, "title")
        try:
            target = resolve_link_reference(self.state.page_url, href.strip())
        except ValidationError as error:
            raise BuildError(
                f"link target is invalid on page {self.state.page}: {error}"
            ) from error
        text = _literal_text_deep(element)
        inlines: list[Inline] = [Code(text=text)] if text else []
        return Link(href=target, inlines=inlines, title=_label_or_none(title))

    # ------------------------------------------------------- element handlers

    def _convert_list(self, element: DomElement, spec: ElementSpec) -> List:
        ordered = spec.name == "ol"
        start = self._list_start(element) if ordered else 1
        items: list[ListItem] = []
        for child in element.children:
            if isinstance(child, DomText):
                if child.text.strip():
                    raise BuildError(
                        "unexpected text directly inside "
                        f"<{element.name}> on page {self.state.page}"
                    )
                continue
            if not isinstance(child, DomElement):
                continue
            item_spec = self._resolve(child)
            if item_spec.name != "li" or not accepts_parent(item_spec, spec.name):
                raise BuildError(
                    f"<{child.name}> inside <{element.name}> on page {self.state.page}"
                )
            self._record_pending_anchors(child, preferred=False)
            blocks = self._convert_blocks(child, parent=item_spec)
            self._flush_pending_anchors(blocks)
            items.append(ListItem(blocks=blocks))
        if not items:
            raise BuildError(f"empty list on page {self.state.page}")
        return List(
            ordered=ordered,
            start=start,
            tight=all(len(item.blocks) <= 1 for item in items),
            items=items,
        )

    def _list_start(self, element: DomElement) -> int:
        raw = attribute_text(element, "start")
        if raw is None:
            return 1
        try:
            start = int(raw.strip())
        except ValueError as error:
            raise BuildError(
                f"ol start is not an integer: {raw!r} on page {self.state.page}"
            ) from error
        if not 0 <= start <= MAX_LIST_START:
            raise BuildError(
                f"ol start is outside CommonMark: {start} on page {self.state.page}"
            )
        return start

    def _convert_blockquote(
        self,
        element: DomElement,
        spec: ElementSpec,
    ) -> list[Block]:
        blocks = self._convert_blocks(element, parent=spec)
        if not blocks:
            return []
        self._flush_pending_anchors(blocks)
        return [BlockQuote(blocks=blocks)]

    def _convert_code_block(self, element: DomElement) -> CodeBlock:
        info = self._pre_language(element)
        text = self._collect_pre_text(element, inside_code=False)
        if text.endswith("\n"):
            text = text[:-1]
        return CodeBlock(info=info, text=text)

    def _collect_pre_text(self, element: DomElement, *, inside_code: bool) -> str:
        parts: list[str] = []
        for child in element.children:
            if isinstance(child, DomText):
                parts.append(child.text)
                continue
            if not isinstance(child, DomElement):
                continue
            is_code_wrapper = not inside_code and child.name == "code"
            if not is_code_wrapper:
                self.state.pre_markup_ignored.append(child.name)
            parts.append(
                self._collect_pre_text(
                    child,
                    inside_code=inside_code or is_code_wrapper,
                )
            )
        return "".join(parts)

    def _pre_language(self, element: DomElement) -> str | None:
        for child in element.children:
            if isinstance(child, DomElement) and child.name == "code":
                language = _language_from_classes(child)
                if language is not None:
                    return language
        return _language_from_classes(element)

    def _convert_table(self, element: DomElement) -> Table:
        caption: list[Inline] | None = None
        has_caption = False
        header_rows: list[TableRow] = []
        body_rows: list[TableRow] = []
        footer_rows: list[TableRow] = []
        declared = False
        extra_anchors: list[_AnchorName] = []
        for child in element.children:
            if isinstance(child, DomText):
                if child.text.strip():
                    raise BuildError(
                        f"unexpected text directly inside <table> on page "
                        f"{self.state.page}"
                    )
                continue
            if not isinstance(child, DomElement):
                continue
            spec = self._resolve(child)
            if not accepts_parent(spec, "table"):
                raise BuildError(
                    f"<{child.name}> is outside its required context on page "
                    f"{self.state.page}"
                )
            if spec.name == "caption":
                if has_caption:
                    raise BuildError(f"duplicate <caption> on page {self.state.page}")
                has_caption = True
                extra_anchors.extend(
                    _AnchorName(name) for name in _source_anchor_names(child)
                )
                inlines = self._inlines(child)
                kept_inlines, caption_marks = _extract_content_inlines_with_marks(
                    inlines
                )
                extra_anchors.extend(caption_marks)
                caption = (
                    _trim_edges(_merge_emphasis(kept_inlines)) if kept_inlines else None
                )
                continue
            if spec.name in {"thead", "tbody", "tfoot"}:
                extra_anchors.extend(
                    _AnchorName(name) for name in _source_anchor_names(child)
                )
                rows = self._convert_rows(child, spec)
                if spec.name == "thead":
                    declared = True
                    header_rows.extend(rows)
                elif spec.name == "tfoot":
                    footer_rows.extend(rows)
                else:
                    body_rows.extend(rows)
                continue
            if spec.name == "tr":
                body_rows.append(self._convert_row(child))
                continue
            raise BuildError(f"<{child.name}> inside <table> on page {self.state.page}")
        body_rows.extend(footer_rows)
        if not declared and body_rows:
            first = body_rows[0]
            if first.cells and all(cell.role == "th" for cell in first.cells):
                declared = True
                header_rows.append(body_rows.pop(0))
        if not header_rows and not body_rows:
            raise BuildError(f"table without rows on page {self.state.page}")
        table = Table(
            caption=caption,
            header=TableHeader(
                source="declared" if declared else "none",
                rows=header_rows,
            ),
            rows=body_rows,
        )
        self._attach_anchor_group(table, extra_anchors, prepend=False)
        return table

    def _convert_rows(
        self,
        container: DomElement,
        section: ElementSpec,
    ) -> list[TableRow]:
        rows: list[TableRow] = []
        for child in container.children:
            if isinstance(child, DomText):
                if child.text.strip():
                    raise BuildError(
                        f"unexpected text directly inside <{container.name}> "
                        f"on page {self.state.page}"
                    )
                continue
            if not isinstance(child, DomElement):
                continue
            spec = self._resolve(child)
            if spec.name != "tr" or not accepts_parent(spec, section.name):
                raise BuildError(
                    f"<{child.name}> inside <{container.name}> on page "
                    f"{self.state.page}"
                )
            rows.append(self._convert_row(child))
        return rows

    def _convert_row(self, element: DomElement) -> TableRow:
        self._record_pending_anchors(element, preferred=False)
        cells: list[TableCell] = []
        for child in element.children:
            if isinstance(child, DomText):
                if child.text.strip():
                    raise BuildError(
                        f"unexpected text directly inside <tr> on page "
                        f"{self.state.page}"
                    )
                continue
            if not isinstance(child, DomElement):
                continue
            cell_spec = self._resolve(child)
            if cell_spec.name not in {"td", "th"} or not accepts_parent(
                cell_spec, "tr"
            ):
                raise BuildError(
                    f"<{child.name}> inside <tr> on page {self.state.page}"
                )
            self._record_pending_anchors(child, preferred=False)
            blocks = self._convert_blocks(child, parent=cell_spec)
            self._flush_pending_anchors(blocks)
            cells.append(
                TableCell(
                    role=child.name,
                    row_span=_table_span_attribute(
                        child, "rowspan", page=self.state.page
                    ),
                    col_span=_table_span_attribute(
                        child, "colspan", page=self.state.page
                    ),
                    blocks=blocks,
                )
            )
        if not cells:
            raise BuildError(f"table row without cells on page {self.state.page}")
        return TableRow(cells=cells)

    def _convert_definition_list(self, element: DomElement) -> list[Block]:
        blocks: list[Block] = []
        for child in element.children:
            if isinstance(child, DomText):
                if child.text.strip():
                    raise BuildError(
                        f"unexpected text directly inside <dl> on page "
                        f"{self.state.page}"
                    )
                continue
            if not isinstance(child, DomElement):
                continue
            spec = self._resolve(child)
            if spec.name not in {"dt", "dd"} or not accepts_parent(spec, "dl"):
                raise BuildError(
                    f"<{child.name}> inside <dl> on page {self.state.page}"
                )
            self._record_pending_anchors(child, preferred=False)
            if spec.name == "dt":
                inlines = self._inlines(child)
                nontrailing_marks, kept_inlines, trailing_marks = _split_anchor_marks(
                    inlines
                )
                self.state.pending_anchor_names.extend(nontrailing_marks)
                if not kept_inlines:
                    self.state.pending_anchor_names.extend(trailing_marks)
                    continue
                term = Paragraph(inlines=[Strong(inlines=_merge_strong(kept_inlines))])
                self._attach_anchor_group(
                    term, self._take_pending_anchors(), prepend=False
                )
                self.state.pending_anchor_names = trailing_marks
                blocks.append(term)
                continue
            if spec.name == "dd":
                inner = self._convert_blocks(child, parent=spec)
                self._flush_pending_anchors(inner)
                blocks.extend(inner)
                continue
        if blocks:
            self._flush_pending_anchors(blocks)
        return blocks

    def _convert_figure(self, element: DomElement) -> Paragraph:
        images: list[Image] = []
        caption: list[Inline] | None = None
        has_caption = False
        marks: list[_AnchorName] = []
        for child in element.children:
            if isinstance(child, DomText):
                if child.text.strip():
                    raise BuildError(
                        f"unexpected text directly inside <figure> on page "
                        f"{self.state.page}"
                    )
                continue
            if not isinstance(child, DomElement):
                continue
            spec = self._resolve(child)
            if spec.name == "img":
                marks.extend(_AnchorName(name) for name in _source_anchor_names(child))
                images.append(self._convert_image(child))
                continue
            if spec.name == "figcaption" and accepts_parent(spec, "figure"):
                if has_caption:
                    raise BuildError(
                        f"duplicate <figcaption> on page {self.state.page}"
                    )
                has_caption = True
                marks.extend(_AnchorName(name) for name in _source_anchor_names(child))
                inlines = self._inlines(child)
                kept_inlines, caption_marks = _extract_content_inlines_with_marks(
                    inlines
                )
                marks.extend(caption_marks)
                caption = (
                    _trim_edges(_merge_emphasis(kept_inlines)) if kept_inlines else None
                )
                continue
            raise BuildError(
                f"<{child.name}> inside <figure> on page {self.state.page}"
            )
        if not images:
            raise BuildError(f"figure without images on page {self.state.page}")
        inlines: list[Inline] = []
        for index, image in enumerate(images):
            if index:
                inlines.append(Text(text=" "))
            inlines.append(image)
        if caption:
            inlines.append(LineBreak())
            inlines.append(Emphasis(inlines=caption))
        paragraph = Paragraph(inlines=inlines)
        self._attach_anchor_group(paragraph, marks, prepend=False)
        return paragraph

    # ---------------------------------------------------------------- helpers

    def _resolve(self, element: DomElement) -> ElementSpec:
        try:
            return resolve_element(element.name)
        except BuildError as error:
            raise BuildError(f"{error} on page {self.state.page}") from error


def build_page_ast(
    roots: tuple[DomElement, ...],
    *,
    page: str,
    slug: str,
    page_url: str,
    italic: dict[DomElement, bool],
) -> PageAst:
    return _Builder(
        page=page,
        slug=slug,
        page_url=page_url,
        italic=italic,
    ).build(roots)


# --------------------------------------------------------------- inline assembly


def _extract_content_inlines_with_marks(
    inlines: list[Inline],
) -> tuple[list[Inline], list[_AnchorName]]:
    """Extract every anchor mark plus the inline content that survives them.

    Single-block contexts such as headings and captions attach all marks to
    the same block, so they don't need the trailing boundary split.
    """
    events: list[tuple[bool, _AnchorName | None]] = []
    kept_inlines = _extract_content_inlines(inlines, events)
    marks = [name for _, name in events if name is not None]
    return kept_inlines, marks


def _split_anchor_marks(
    inlines: list[Inline],
) -> tuple[list[_AnchorName], list[Inline], list[_AnchorName]]:
    events: list[tuple[bool, _AnchorName | None]] = []
    kept_inlines = _extract_content_inlines(inlines, events)
    content_positions = [
        index for index, (is_content, _) in enumerate(events) if is_content
    ]
    if not content_positions:
        marks = [name for _, name in events if name is not None]
        return [], [], marks
    last_content = content_positions[-1]
    nontrailing_marks = [
        name
        for index, (_, name) in enumerate(events)
        if name is not None and index < last_content
    ]
    trailing_marks = [
        name
        for index, (_, name) in enumerate(events)
        if name is not None and index > last_content
    ]
    return nontrailing_marks, kept_inlines, trailing_marks


def _extract_content_inlines(
    inlines: list[Inline],
    events: list[tuple[bool, _AnchorName | None]],
) -> list[Inline]:
    kept_inlines: list[Inline] = []
    for inline in inlines:
        match inline:
            case AnchorMark():
                events.extend(
                    (
                        False,
                        _AnchorName(name=name, preferred=name == inline.preferred),
                    )
                    for name in inline.names
                )
            case Text():
                if inline.text.strip():
                    events.append((True, None))
                kept_inlines.append(inline)
            case Code():
                if inline.text:
                    events.append((True, None))
                kept_inlines.append(inline)
            case Image() | LineBreak() | SpanPlaceholder():
                events.append((True, None))
                kept_inlines.append(inline)
            case Emphasis() | Strong() | Strikethrough():
                start = len(events)
                inner = _extract_content_inlines(inline.inlines, events)
                if any(is_content for is_content, _ in events[start:]):
                    kept_inlines.append(type(inline)(inlines=inner))
            case Link():
                start = len(events)
                inner = _extract_content_inlines(inline.inlines, events)
                kept_inlines.append(
                    Link(
                        href=inline.href,
                        inlines=inner,
                        title=inline.title,
                    )
                )
                if not any(is_content for is_content, _ in events[start:]):
                    events.append((True, None))
            case RawHtml():
                start = len(events)
                inner = _extract_content_inlines(inline.inlines, events)
                kept_inlines.append(
                    RawHtml(
                        element=inline.element,
                        inlines=inner,
                        anchor_id=inline.anchor_id,
                    )
                )
                if not any(is_content for is_content, _ in events[start:]):
                    events.append((True, None))
            case _:
                raise BuildError(f"unexpected inline node {type(inline).__name__}")
    return _collapse_adjacent_spaces(_coalesce_containers(kept_inlines))


def _assemble(run: list[Inline], *, trim: bool = True) -> list[Inline]:
    merged: list[Inline] = []
    for inline in run:
        if isinstance(inline, Text) and merged and isinstance(merged[-1], Text):
            merged[-1].text += inline.text
            continue
        merged.append(inline)
    merged = _coalesce_containers(merged)
    merged = _collapse_adjacent_spaces(merged)
    if trim:
        merged = _trim_run(merged)
    return merged


def _wrap_style_emphasis(inlines: list[Inline]) -> list[Inline]:
    """Wrap inlines in Emphasis representing style-derived italic.

    This routine achieves a low hit rate in the corpus.
    """
    if not inlines:
        return inlines
    merged = _merge_emphasis(inlines)
    if len(merged) == 1 and isinstance(merged[0], Emphasis):
        return merged
    return [Emphasis(inlines=merged)]


def _collapse_adjacent_spaces(inlines: list[Inline]) -> list[Inline]:
    """Remove duplicate spaces at boundaries between adjacent inlines.

    When one inline ends with a space and the next begins with one, the next
    loses its leading space. The helper ignores anchor marks and leaves code
    or raw HTML content unchanged.

    This routine achieves a low hit rate in the corpus.

    Typical scenario: gvar - an italic definition term with spaces on both
    sides, such as a ``dfn`` wrapping an ``em``, creates this boundary before
    the following prose.
    """
    for index in range(len(inlines) - 1):
        if _ends_with_space(inlines[index]) and _starts_with_space(inlines[index + 1]):
            _strip_leading_space(inlines[index + 1])
    return inlines


def _starts_with_space(inline: Inline) -> bool:
    if isinstance(inline, Text):
        return inline.text.startswith(" ")
    if isinstance(inline, (Emphasis, Strong, Strikethrough, Link)):
        for inner in inline.inlines:
            if isinstance(inner, AnchorMark):
                continue
            return _starts_with_space(inner)
    return False


def _ends_with_space(inline: Inline) -> bool:
    if isinstance(inline, Text):
        return inline.text.endswith(" ")
    if isinstance(inline, (Emphasis, Strong, Strikethrough, Link)):
        for inner in reversed(inline.inlines):
            if isinstance(inner, AnchorMark):
                continue
            return _ends_with_space(inner)
    return False


def _strip_leading_space(inline: Inline) -> bool:
    if isinstance(inline, Text):
        if not inline.text.startswith(" "):
            return False
        inline.text = inline.text[1:]
        return True
    if isinstance(inline, (Emphasis, Strong, Strikethrough, Link)):
        for inner in inline.inlines:
            if isinstance(inner, AnchorMark):
                continue
            return _strip_leading_space(inner)
    return False


def _coalesce_containers(inlines: list[Inline]) -> list[Inline]:
    """Merge adjacent emphasis containers of the same type.

    Source splitting and generated style runs can produce adjacent
    ``Emphasis``, ``Strong``, or ``Strikethrough`` nodes. Combining them
    avoids adjacent Markdown delimiters; other inlines pass through.

    This routine achieves a low hit rate in the corpus.

    Typical scenario: Zapf - a table cell with ``font-style: italic`` around
    text and an inline code span yields adjacent ``Emphasis`` nodes, and merging
    keeps a single pair of emphasis markers.
    """
    merged: list[Inline] = []
    for inline in inlines:
        if (
            merged
            and type(inline) is type(merged[-1])
            and isinstance(inline, (Emphasis, Strong, Strikethrough))
        ):
            previous = merged[-1]
            if isinstance(previous, (Emphasis, Strong, Strikethrough)):
                previous.inlines.extend(inline.inlines)
                continue
        merged.append(inline)
    return merged


def _trim_run(inlines: list[Inline]) -> list[Inline]:
    content_positions = [
        index for index, inline in enumerate(inlines) if _inline_has_content(inline)
    ]
    if not content_positions:
        return [
            inline
            for inline in inlines
            if isinstance(inline, AnchorMark) or _contains_anchor_marks(inline)
        ]
    first = content_positions[0]
    last = content_positions[-1]
    kept: list[Inline] = []
    for index, inline in enumerate(inlines):
        if first <= index <= last:
            kept.append(inline)
            continue
        if isinstance(inline, AnchorMark) or _contains_anchor_marks(inline):
            kept.append(inline)
    for inline in kept:
        if _inline_has_content(inline):
            if isinstance(inline, Text):
                inline.text = inline.text.lstrip(" ")
            break  # first text
    for inline in reversed(kept):
        if _inline_has_content(inline):
            if isinstance(inline, Text):
                inline.text = inline.text.rstrip(" ")
            break  # last text
    return kept


def _inline_has_content(inline: Inline) -> bool:
    if isinstance(inline, Text):
        return bool(inline.text.strip())
    if isinstance(inline, Code):
        return bool(inline.text)
    if isinstance(inline, AnchorMark):
        return False
    if isinstance(inline, (Image, LineBreak, SpanPlaceholder, RawHtml)):
        return True
    if isinstance(inline, Link):
        return True
    return any(_inline_has_content(inner) for inner in inline.inlines)


def _contains_anchor_marks(inline: Inline) -> bool:
    if isinstance(inline, AnchorMark):
        return True
    if isinstance(inline, (Emphasis, Strong, Strikethrough, Link, RawHtml)):
        return any(_contains_anchor_marks(inner) for inner in inline.inlines)
    return False


def _merge_emphasis(inlines: list[Inline]) -> list[Inline]:
    merged: list[Inline] = []
    for inline in inlines:
        if isinstance(inline, Emphasis):
            merged.extend(_merge_emphasis(inline.inlines))
        else:
            merged.append(inline)
    return merged


def _merge_strong(inlines: list[Inline]) -> list[Inline]:
    merged: list[Inline] = []
    for inline in inlines:
        if isinstance(inline, Strong):
            merged.extend(_merge_strong(inline.inlines))
        else:
            merged.append(inline)
    return merged


def _merge_adjacent_code(inlines: list[Inline]) -> list[Inline]:
    merged: list[Inline] = []
    for inline in inlines:
        if isinstance(inline, Code) and merged and isinstance(merged[-1], Code):
            merged[-1].text += inline.text
            continue
        merged.append(inline)
    return merged


def _has_link_target(element: DomElement) -> bool:
    href = attribute_text(element, "href")
    return href is not None and bool(href.strip())


def _literal_text_deep(element: DomElement) -> str:
    parts: list[str] = []
    for child in element.children:
        if isinstance(child, DomText):
            parts.append(child.text)
        elif isinstance(child, DomElement):
            parts.append(_literal_text_deep(child))
    return "".join(parts)


def _trim_edges(merged: list[Inline]) -> list[Inline]:
    while merged and isinstance(merged[0], Text) and not merged[0].text.strip():
        merged.pop(0)
    while merged and isinstance(merged[-1], Text) and not merged[-1].text.strip():
        merged.pop()
    if merged and isinstance(merged[0], Text):
        merged[0].text = merged[0].text.lstrip(" ")
    if merged and isinstance(merged[-1], Text):
        merged[-1].text = merged[-1].text.rstrip(" ")
    return merged


# ------------------------------------------------------------------- anchors


def _source_anchor_names(element: DomElement) -> list[str]:
    names: list[str] = []
    identifier = attribute_text(element, "id")
    if identifier is not None and identifier.strip():
        names.append(identifier.strip())
    if element.name == "a":
        name = attribute_text(element, "name")
        if name is not None and name.strip():
            names.append(name.strip())
    return _dedupe_names(names)


def _unique_anchor_names(names: list[_AnchorName]) -> list[_AnchorName]:
    seen: set[str] = set()
    unique: list[_AnchorName] = []
    for name in names:
        if name.name in seen:
            continue
        seen.add(name.name)
        unique.append(name)
    return unique


def _dedupe_names(names: tuple[str, ...] | list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for name in names:
        if name in seen:
            continue
        seen.add(name)
        unique.append(name)
    return unique


def _unique_local_id(base: str, source: str | None, used: set[str]) -> str:
    if base not in used:
        used.add(base)
        return base
    digest = hashlib.sha256((source or base).encode("utf-8")).hexdigest()[:8]
    candidate = f"{base}-{digest}"
    counter = 1
    while candidate in used:
        candidate = f"{base}-{digest}-{counter}"
        counter += 1
    used.add(candidate)
    return candidate


# -------------------------------------------------------------------- parsing


def _table_span_attribute(element: DomElement, name: str, *, page: str) -> int:
    raw = attribute_text(element, name)
    if raw is None:
        return 1
    try:
        value = int(raw.strip())
    except ValueError as error:
        raise BuildError(f"{name} is not an integer: {raw!r} on page {page}") from error
    if value < 1:
        raise BuildError(f"{name} must be a positive integer: {value} on page {page}")
    return value


def _label_or_none(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = normalize_label(value)
    return normalized or None


def _language_from_classes(element: DomElement) -> str | None:
    for name in class_names(element):
        match = _LANGUAGE_CLASS.fullmatch(name)
        if match is None:
            continue
        language = match.group("language").strip()
        if _SAFE_LANGUAGE.fullmatch(language):
            return language
    return None
