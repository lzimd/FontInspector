"""The AST editing engine for versioned correction rules.

Corrections are data, not patches to generated Markdown. The engine resolves
a structural target, verifies strict expectations, and applies one primitive
to the AST. The engine constructs only CommonMark and GFM nodes here. A rule
can't inject raw HTML, comments, spans, or tables. The engine also owns the
post-correction anchor remerge and the attachment check that keeps fragment
maps honest.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from ..errors import BuildError, SchemaError
from ..schema import (
    is_json_array,
    require_object,
    require_positive_int,
    require_text,
)
from .ast import (
    AnchorGroup,
    AnchorRemerge,
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
    Strikethrough,
    Strong,
    Table,
    TableCell,
    TableHeader,
    TableRow,
    Text,
    ThematicBreak,
    block_fingerprint,
    build_fragment_map,
    inlines_text,
    iter_block_inlines,
    iter_blocks,
    iter_tables,
    rows_fingerprint,
)
from .markdown_model import (
    MAX_HEADING_LEVEL,
    MAX_LIST_START,
    require_construct,
    require_construct_document,
)

OPS: frozenset[str] = frozenset(
    {
        "replace_text",
        "replace_inline",
        "replace_block",
        "insert_block",
        "remove_node",
        "retarget_link",
        "retarget_image",
        "set_table_header",
    }
)


@dataclass(frozen=True, slots=True)
class Rule:
    id: str
    op: str
    target: dict[str, object]
    payload: dict[str, object]
    expect: dict[str, object]
    note: str

    @classmethod
    def from_dict(cls, value: object, *, where: str) -> Rule:
        data = require_object(value, where)
        _check_keys(
            data,
            required={"id", "op", "target"},
            optional={
                "find",
                "replace",
                "inlines",
                "blocks",
                "mode",
                "rows",
                "position",
                "expect",
                "note",
            },
            where=where,
        )
        rule_id = require_text(data["id"], f"{where}.id")
        op = require_text(data["op"], f"{where}.op")
        if op not in OPS:
            raise SchemaError(f"{where}.op is unknown: {op!r}")
        target = require_object(data["target"], f"{where}.target")
        expect = require_object(data.get("expect", {}), f"{where}.expect")
        note = require_text(data.get("note", ""), f"{where}.note", allow_empty=True)
        payload = {
            key: data[key]
            for key in (
                "find",
                "replace",
                "inlines",
                "blocks",
                "mode",
                "rows",
                "position",
            )
            if key in data
        }
        return cls(
            id=rule_id,
            op=op,
            target=target,
            payload=payload,
            expect=expect,
            note=note,
        )


@dataclass(slots=True)
class AppliedRule:
    id: str
    op: str
    note: str


def _check_keys(
    data: dict[str, object],
    *,
    required: set[str],
    optional: set[str],
    where: str,
) -> None:
    missing = sorted(required - data.keys())
    unknown = sorted(data.keys() - required - optional)
    if missing:
        raise SchemaError(f"{where} is missing keys: {', '.join(missing)}")
    if unknown:
        raise SchemaError(f"{where} has unknown keys: {', '.join(unknown)}")


def _text(value: object, where: str, *, allow_empty: bool = False) -> str:
    return require_text(value, where, allow_empty=allow_empty)


def load_rules(corrections_root: Path, *, source: str, slug: str) -> list[Rule]:
    path = corrections_root / source / f"{slug}.json"
    if not path.is_file():
        return []
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SchemaError(f"corrections {path} is not valid JSON: {error}") from error
    if not is_json_array(value):
        raise SchemaError(f"corrections {path} must be an array of rules")
    return [
        Rule.from_dict(item, where=f"corrections {path}[{index}]")
        for index, item in enumerate(value)
    ]


def _new_applied() -> list[AppliedRule]:
    return []


def _new_table_repairs() -> dict[int, list[str]]:
    return {}


class PatchEngine:
    """Applies one page's rules in file order and fails loudly on drift."""

    def __init__(self, *, page: str, slug: str) -> None:
        self.page = page
        self.slug = slug
        self.applied: list[AppliedRule] = _new_applied()
        self.table_repairs: dict[int, list[str]] = _new_table_repairs()

    def apply(self, document: Document, rules: list[Rule]) -> None:
        for rule in rules:
            target = self._apply_rule(document, rule)
            self.applied.append(AppliedRule(id=rule.id, op=rule.op, note=rule.note))
            if target.table is not None:
                self.table_repairs.setdefault(id(target.table), []).append(rule.id)
        try:
            require_construct_document(document, where=f"page {self.page}")
        except ValueError as error:
            raise BuildError(str(error)) from error

    # -------------------------------------------------------------- dispatch

    def _apply_rule(self, document: Document, rule: Rule) -> _Target:
        target = _Target.resolve(document, rule.target, rule=self._where(rule))
        match rule.op:
            case "replace_text":
                self._replace_text(target, rule)
            case "replace_inline":
                self._replace_inline(target, rule)
            case "replace_block":
                self._replace_block(target, rule)
            case "insert_block":
                self._insert_block(target, rule)
            case "remove_node":
                self._remove_node(target, rule)
            case "retarget_link":
                self._retarget_link(target, rule)
            case "retarget_image":
                self._retarget_image(target, rule)
            case "set_table_header":
                self._set_table_header(target, rule)
            case _:
                raise BuildError(f"{self._where(rule)}: unknown op {rule.op!r}")
        return target

    def _where(self, rule: Rule) -> str:
        return f"correction {rule.id!r} on page {self.page}"

    # ------------------------------------------------------------ primitives

    def _replace_text(self, target: _Target, rule: Rule) -> None:
        find = self._require_text_payload(rule, "find")
        if not find:
            raise BuildError(f"{self._where(rule)}: find must not be empty")
        replace = self._require_text_payload(rule, "replace")
        expected = self._expected_count(rule)
        nodes = _text_nodes(target, where=self._where(rule))
        total = sum(node.text.count(find) for node in nodes)
        if total != expected:
            raise BuildError(
                f"{self._where(rule)}: expected {expected} matches of {find!r}, "
                f"found {total}"
            )
        for node in nodes:
            node.text = node.text.replace(find, replace)

    def _replace_inline(self, target: _Target, rule: Rule) -> None:
        inlines = _inline_list(target, where=self._where(rule))
        patterns = _inline_patterns(rule.payload.get("find"), self._where(rule))
        expected = self._expected_count(rule)
        matches = _find_sequence(inlines, patterns)
        if len(matches) != expected:
            raise BuildError(
                f"{self._where(rule)}: expected {expected} inline matches, "
                f"found {len(matches)}"
            )
        replacement = decode_inlines(
            rule.payload.get("inlines"), where=self._where(rule)
        )
        for index in reversed(matches):
            inlines[index : index + len(patterns)] = [
                _clone_inline(inline) for inline in replacement
            ]

    def _replace_block(self, target: _Target, rule: Rule) -> None:
        block = _require_block(target, self._where(rule))
        self._check_fingerprint(rule, block)
        blocks = decode_blocks(rule.payload.get("blocks"), where=self._where(rule))
        parent = target.block_parent
        if parent is None or target.block_index is None:
            raise BuildError(f"{self._where(rule)}: block target is not replaceable")
        parent[target.block_index : target.block_index + 1] = blocks

    def _insert_block(self, target: _Target, rule: Rule) -> None:
        block = _require_block(target, self._where(rule))
        self._check_fingerprint(rule, block)
        blocks = decode_blocks(rule.payload.get("blocks"), where=self._where(rule))
        position = self._payload_text(rule, "position", default="before")
        if position not in {"before", "after"}:
            raise BuildError(
                f"{self._where(rule)}: position must be 'before' or 'after'"
            )
        parent = target.block_parent
        if parent is None or target.block_index is None:
            raise BuildError(f"{self._where(rule)}: block target is not insertable")
        index = target.block_index if position == "before" else target.block_index + 1
        parent[index:index] = blocks

    def _remove_node(self, target: _Target, rule: Rule) -> None:
        if target.block is not None:
            self._check_fingerprint(rule, target.block)
            parent = target.block_parent
            if parent is None or target.block_index is None:
                raise BuildError(f"{self._where(rule)}: block target is not removable")
            del parent[target.block_index]
            return
        if target.inline_index is None:
            raise BuildError(f"{self._where(rule)}: inline target did not resolve")
        inlines = _inline_list(target, where=self._where(rule))
        if target.inline_index >= len(inlines):
            raise BuildError(f"{self._where(rule)}: inline target did not resolve")
        del inlines[target.inline_index]

    def _retarget_link(self, target: _Target, rule: Rule) -> None:
        link = _require_link(target, where=self._where(rule))
        expected = self._require_text_payload(rule, "find")
        if link.href != expected:
            raise BuildError(
                f"{self._where(rule)}: link target is {link.href!r}, "
                f"expected {expected!r}"
            )
        link.href = self._require_text_payload(rule, "replace")

    def _retarget_image(self, target: _Target, rule: Rule) -> None:
        image = _require_image(target, where=self._where(rule))
        expected = self._require_text_payload(rule, "find")
        if image.src != expected:
            raise BuildError(
                f"{self._where(rule)}: image src is {image.src!r}, "
                f"expected {expected!r}"
            )
        replacement = rule.payload.get("replace")
        if isinstance(replacement, str):
            image.src = require_text(replacement, f"{self._where(rule)}.replace")
            return
        fields = require_object(replacement, f"{self._where(rule)}.replace")
        _check_keys(
            fields,
            required=set(),
            optional={"src", "alt"},
            where=f"{self._where(rule)}.replace",
        )
        if not fields:
            raise BuildError(f"{self._where(rule)}: replace must set src or alt")
        if "src" in fields:
            image.src = _text(fields["src"], f"{self._where(rule)}.replace.src")
        if "alt" in fields:
            image.alt = _text(
                fields["alt"],
                f"{self._where(rule)}.replace.alt",
                allow_empty=True,
            )

    def _set_table_header(self, target: _Target, rule: Rule) -> None:
        table = _require_table(target, self._where(rule))
        self._check_table_expectations(rule, table)
        mode = self._payload_text(rule, "mode", default="")
        if mode == "none":
            if table.header.source != "declared" or not table.header.rows:
                raise BuildError(
                    f"{self._where(rule)}: table has no declared header to demote"
                )
            table.rows[:0] = table.header.rows
            table.header = TableHeader(
                source="none",
                rows=[],
                repair_id=rule.id,
            )
            return
        if mode == "rows":
            rows_value = rule.payload.get("rows")
            if not is_json_array(rows_value) or not rows_value:
                raise BuildError(
                    f"{self._where(rule)}: mode 'rows' requires a non-empty rows array"
                )
            indices = [
                require_positive_int(item, f"{self._where(rule)}.rows[{index}]")
                for index, item in enumerate(rows_value)
            ]
            if len(set(indices)) != len(indices):
                raise BuildError(f"{self._where(rule)}: rows contains a duplicate")
            all_rows = [*table.header.rows, *table.rows]
            for index in indices:
                if index > len(all_rows):
                    raise BuildError(
                        f"{self._where(rule)}: row {index} is outside the table"
                    )
            promoted = [all_rows[index - 1] for index in indices]
            promoted_ids = {id(row) for row in promoted}
            remaining = [row for row in all_rows if id(row) not in promoted_ids]
            for row in promoted:
                for cell in row.cells:
                    _strip_strong_in_cell(cell)
            table.header = TableHeader(
                source="declared",
                rows=promoted,
                repair_id=rule.id,
            )
            table.rows = remaining
            return
        raise BuildError(f"{self._where(rule)}: mode must be 'none' or 'rows'")

    # ----------------------------------------------------------- expectations

    def _expected_count(self, rule: Rule) -> int:
        value = rule.expect.get("count")
        if value is None:
            raise BuildError(f"{self._where(rule)}: expect.count is required")
        return require_positive_int(value, f"{self._where(rule)}.expect.count")

    def _check_fingerprint(self, rule: Rule, block: Block) -> None:
        expected = rule.expect.get("fingerprint")
        if expected is None:
            raise BuildError(f"{self._where(rule)}: expect.fingerprint is required")
        actual = block_fingerprint(block)
        if actual != _text(expected, f"{self._where(rule)}.expect.fingerprint"):
            raise BuildError(
                f"{self._where(rule)}: block fingerprint does not match; "
                "the upstream content changed"
            )

    def _check_table_expectations(self, rule: Rule, table: Table) -> None:
        where = self._where(rule)
        expected_fingerprint = rule.expect.get("header_fingerprint")
        if expected_fingerprint is None:
            raise BuildError(f"{where}: expect.header_fingerprint is required")
        if rows_fingerprint(table.header.rows) != _text(
            expected_fingerprint, f"{where}.expect.header_fingerprint"
        ):
            raise BuildError(
                f"{where}: header fingerprint does not match; the table changed"
            )
        row_count = rule.expect.get("row_count")
        if row_count is not None:
            actual_rows = len(table.header.rows) + len(table.rows)
            if actual_rows != require_positive_int(
                row_count, f"{where}.expect.row_count"
            ):
                raise BuildError(f"{where}: row count does not match")
        column_count = rule.expect.get("column_count")
        if column_count is not None:
            expected = require_positive_int(
                column_count, f"{where}.expect.column_count"
            )
            rows = [*table.header.rows, *table.rows]
            if any(len(row.cells) != expected for row in rows):
                raise BuildError(f"{where}: column count does not match")

    def _require_text_payload(self, rule: Rule, key: str) -> str:
        value = rule.payload.get(key)
        if not isinstance(value, str):
            raise BuildError(f"{self._where(rule)}: {key} is required")
        return value

    def _payload_text(self, rule: Rule, key: str, *, default: str) -> str:
        value = rule.payload.get(key, default)
        if not isinstance(value, str):
            raise BuildError(f"{self._where(rule)}: {key} must be a string")
        return value


# --------------------------------------------------------------------- targets


@dataclass(slots=True)
class _Target:
    blocks: list[Block]
    block: Block | None = None
    block_parent: list[Block] | None = None
    block_index: int | None = None
    table: Table | None = None
    row: TableRow | None = None
    cell: TableCell | None = None
    inlines: list[Inline] | None = None
    inline_index: int | None = None

    @classmethod
    def resolve(
        cls,
        document: Document,
        target: dict[str, object],
        *,
        rule: str,
    ) -> _Target:
        _check_keys(
            target,
            required=set(),
            optional={
                "section_heading",
                "block",
                "table",
                "row",
                "cell",
                "inline",
            },
            where=f"{rule} target",
        )
        blocks = document.blocks
        start, end = 0, len(blocks)
        heading_path = target.get("section_heading")
        if heading_path is not None:
            if not is_json_array(heading_path):
                raise SchemaError(f"{rule} target.section_heading must be an array")
            start, end = _resolve_section(document.blocks, heading_path, rule)
        section_blocks = blocks[start:end]
        result = cls(blocks=section_blocks)
        if "block" in target:
            index = require_positive_int(target["block"], f"{rule} target.block")
            if index > len(section_blocks):
                raise BuildError(f"{rule}: block {index} is outside the section")
            result.block_index = start + index - 1
            result.block = blocks[result.block_index]
            result.block_parent = blocks
        if "table" in target:
            ordinal = require_positive_int(target["table"], f"{rule} target.table")
            tables = list(iter_tables(section_blocks))
            if ordinal > len(tables):
                raise BuildError(f"{rule}: table {ordinal} does not exist")
            result.table = tables[ordinal - 1]
        if "row" in target:
            if result.table is None:
                raise BuildError(f"{rule}: target.row requires target.table")
            index = require_positive_int(target["row"], f"{rule} target.row")
            rows = [*result.table.header.rows, *result.table.rows]
            if index > len(rows):
                raise BuildError(f"{rule}: row {index} is outside the table")
            result.row = rows[index - 1]
        if "cell" in target:
            if result.row is None:
                raise BuildError(f"{rule}: target.cell requires target.row")
            index = require_positive_int(target["cell"], f"{rule} target.cell")
            if index > len(result.row.cells):
                raise BuildError(f"{rule}: cell {index} is outside the row")
            result.cell = result.row.cells[index - 1]
        if "inline" in target:
            inlines = _inline_list(result, where=rule)
            index = require_positive_int(target["inline"], f"{rule} target.inline")
            if index > len(inlines):
                raise BuildError(f"{rule}: inline {index} is outside the target")
            result.inline_index = index - 1
            result.inlines = inlines
        return result


def _resolve_section(
    blocks: list[Block], path: list[object], rule: str
) -> tuple[int, int]:
    start, end = 0, len(blocks)
    for depth, raw in enumerate(path):
        if not isinstance(raw, str) or not raw:
            raise SchemaError(f"{rule} target.section_heading[{depth}] must be text")
        match = _find_heading(blocks, start, end, raw)
        if match is None:
            raise BuildError(f"{rule}: section heading {raw!r} no longer exists")
        heading_index, section_end = match
        start, end = heading_index + 1, section_end
    return start, end


def _find_heading(
    blocks: list[Block],
    start: int,
    end: int,
    title: str,
) -> tuple[int, int] | None:
    for index in range(start, end):
        block = blocks[index]
        if not isinstance(block, Heading):
            continue
        if inlines_text(block.inlines).strip() != title:
            continue
        for following_index in range(index + 1, end):
            following = blocks[following_index]
            if isinstance(following, Heading) and following.level <= block.level:
                return index, following_index
        return index, end
    return None


def _text_nodes(target: _Target, *, where: str) -> list[Text]:
    if target.inline_index is not None:
        inlines = _inline_list(target, where=where)
        inline = inlines[target.inline_index]
        if not isinstance(inline, Text):
            raise BuildError(f"{where}: inline target is not a text node")
        return [inline]
    if target.cell is not None:
        blocks = target.cell.blocks
    elif target.block is not None:
        blocks = [target.block]
    else:
        blocks = target.blocks
    nodes: list[Text] = []
    for block in iter_blocks(blocks):
        nodes.extend(
            inline for inline in iter_block_inlines(block) if isinstance(inline, Text)
        )
    return nodes


def _inline_list(target: _Target, *, where: str) -> list[Inline]:
    if target.inline_index is not None:
        if target.inlines is None:
            raise BuildError(f"{where}: inline target did not resolve")
        return target.inlines
    if target.cell is not None:
        return _cell_inline_list(target.cell, where=where)
    if target.block is not None:
        if isinstance(target.block, (Paragraph, Heading)):
            return target.block.inlines
        raise BuildError(f"{where}: block target does not carry inline content")
    raise BuildError(f"{where}: inline target did not resolve")


def _cell_inline_list(cell: TableCell, *, where: str) -> list[Inline]:
    candidates = [
        block for block in cell.blocks if isinstance(block, (Paragraph, Heading))
    ]
    if len(candidates) != 1:
        raise BuildError(
            f"{where}: cell inline target is ambiguous; the cell must contain "
            "exactly one paragraph or heading"
        )
    return candidates[0].inlines


def _require_block(target: _Target, where: str) -> Block:
    if target.block is None:
        raise BuildError(f"{where}: the target does not address a block")
    return target.block


def _require_table(target: _Target, where: str) -> Table:
    if target.table is None:
        raise BuildError(f"{where}: the target does not address a table")
    return target.table


def _require_inline_at(target: _Target, where: str) -> Inline:
    inlines = _inline_list(target, where=where)
    index = target.inline_index
    if index is None or index >= len(inlines):
        raise BuildError(f"{where}: inline target did not resolve")
    return inlines[index]


def _require_link(target: _Target, *, where: str) -> Link:
    inline = _require_inline_at(target, where)
    if not isinstance(inline, Link):
        raise BuildError(f"{where}: target is not a link")
    return inline


def _require_image(target: _Target, *, where: str) -> Image:
    inline = _require_inline_at(target, where)
    if not isinstance(inline, Image):
        raise BuildError(f"{where}: target is not an image")
    return inline


# --------------------------------------------------------------- expectations


class _InlinePattern:
    def __init__(self, kind: str, text: str) -> None:
        self.kind = kind
        self.text = text

    def matches(self, inline: Inline) -> bool:
        if isinstance(inline, (Emphasis, Strong, Strikethrough)):
            return (
                self.kind == "emphasis-container"
                and inlines_text(inline.inlines) == self.text
            )
        if isinstance(inline, Text):
            return self.kind == "text" and inline.text == self.text
        if isinstance(inline, Code):
            return self.kind == "code" and inline.text == self.text
        if isinstance(inline, Image):
            return self.kind == "image" and inline.alt == self.text
        if isinstance(inline, LineBreak):
            return self.kind == "line-break"
        if isinstance(inline, Link):
            return self.kind == "link" and inlines_text(inline.inlines) == self.text
        return False


def _find_sequence(inlines: list[Inline], patterns: list[_InlinePattern]) -> list[int]:
    return [
        start
        for start in range(len(inlines) - len(patterns) + 1)
        if all(
            pattern.matches(inlines[start + offset])
            for offset, pattern in enumerate(patterns)
        )
    ]


def _inline_patterns(value: object, where: str) -> list[_InlinePattern]:
    if not is_json_array(value) or not value:
        raise BuildError(f"{where}: find must be a non-empty array of inline patterns")
    patterns: list[_InlinePattern] = []
    for index, item in enumerate(value):
        data = require_object(item, f"{where}.find[{index}]")
        _check_keys(
            data,
            required={"type", "text"},
            optional=set(),
            where=f"{where}.find[{index}]",
        )
        kind = _text(data["type"], f"{where}.find[{index}].type")
        if kind not in {
            "text",
            "code",
            "image",
            "line-break",
            "link",
            "emphasis-container",
        }:
            raise BuildError(f"{where}.find[{index}]: unknown type {kind!r}")
        text = _text(
            data["text"],
            f"{where}.find[{index}].text",
            allow_empty=True,
        )
        patterns.append(_InlinePattern(kind, text))
    return patterns


# -------------------------------------------------------------------- anchors


def remerge_anchor_groups(ast: PageAst) -> list[AnchorRemerge]:
    """Move anchor groups off top-level paragraphs emptied by corrections."""
    blocks = ast.document.blocks
    groups_by_block = {id(group.block): group for group in ast.anchor_groups}
    remerges: list[AnchorRemerge] = []
    index = 0
    while index < len(blocks) - 1:
        block = blocks[index]
        group = groups_by_block.get(id(block))
        if not isinstance(block, Paragraph) or block.inlines or group is None:
            index += 1
            continue
        target = blocks[index + 1]
        existing = groups_by_block.get(id(target))
        if existing is not None:
            merged = AnchorGroup(
                block=target,
                names=(*group.names, *existing.names),
                preferred=existing.preferred or group.preferred,
                canonical_id=existing.canonical_id,
            )
            ast.anchor_groups = [
                merged if candidate is existing else candidate
                for candidate in ast.anchor_groups
                if candidate is not group
            ]
            del groups_by_block[id(block)]
            groups_by_block[id(target)] = merged
            remerges.append(
                AnchorRemerge(names=group.names, merged_into=existing.canonical_id)
            )
        else:
            group.block = target
            del groups_by_block[id(block)]
            groups_by_block[id(target)] = group
            remerges.append(AnchorRemerge(names=group.names, merged_into=None))
        del blocks[index]
    if remerges:
        ast.fragment_map, ast.duplicate_anchors = build_fragment_map(ast.anchor_groups)
    return remerges


def check_anchor_groups_attached(ast: PageAst, *, page: str) -> None:
    """Fail when an anchor group references a block that no longer exists."""
    attached = {id(block) for block in iter_blocks(ast.document.blocks)}
    orphans = [
        group.canonical_id or (group.names[0] if group.names else "<unnamed>")
        for group in ast.anchor_groups
        if id(group.block) not in attached
    ]
    if orphans:
        raise BuildError(
            "anchor groups reference blocks that no longer exist on page "
            f"{page}: {', '.join(orphans)}"
        )


# ---------------------------------------------------- correction node decoding


def decode_blocks(value: object, *, where: str) -> list[Block]:
    if not is_json_array(value) or not value:
        raise BuildError(f"{where}: blocks must be a non-empty array")
    return [
        _decode_block(item, where=f"{where}.blocks[{index}]")
        for index, item in enumerate(value)
    ]


def decode_inlines(value: object, *, where: str) -> list[Inline]:
    if not is_json_array(value):
        raise BuildError(f"{where}: inlines must be an array")
    return [
        _decode_inline(item, where=f"{where}.inlines[{index}]")
        for index, item in enumerate(value)
    ]


def _decode_block(value: object, *, where: str) -> Block:
    data = require_object(value, where)
    _check_keys(
        data,
        required={"type"},
        optional={
            "level",
            "inlines",
            "blocks",
            "items",
            "ordered",
            "start",
            "info",
            "text",
        },
        where=where,
    )
    kind = _text(data["type"], f"{where}.type")
    if kind == "paragraph":
        block: Block = Paragraph(
            inlines=decode_inlines(data.get("inlines", []), where=where)
        )
    elif kind == "heading":
        level = require_positive_int(data.get("level"), f"{where}.level")
        if level > MAX_HEADING_LEVEL:
            raise BuildError(f"{where}: heading level {level} is invalid")
        block = Heading(
            level=level,
            inlines=decode_inlines(data.get("inlines", []), where=where),
        )
    elif kind == "block_quote":
        block = BlockQuote(blocks=decode_blocks(data.get("blocks"), where=where))
    elif kind == "code_block":
        info = data.get("info")
        block = CodeBlock(
            info=info if isinstance(info, str) else None,
            text=_text(data.get("text", ""), f"{where}.text", allow_empty=True),
        )
    elif kind == "thematic_break":
        block = ThematicBreak()
    elif kind == "list":
        block = _decode_list(data, where=where)
    else:
        raise BuildError(f"{where}: block type {kind!r} is not a correction construct")
    _require_construct_node(block, where=where)
    return block


def _decode_list(data: dict[str, object], *, where: str) -> List:
    ordered = bool(data.get("ordered", False))
    start = require_positive_int(data.get("start", 1), f"{where}.start")
    if start > MAX_LIST_START:
        raise BuildError(f"{where}: list start is outside CommonMark")
    items_value = data.get("items")
    if not is_json_array(items_value) or not items_value:
        raise BuildError(f"{where}: list requires items")
    items: list[ListItem] = []
    for index, item in enumerate(items_value):
        item_data = require_object(item, f"{where}.items[{index}]")
        _check_keys(
            item_data,
            required={"blocks"},
            optional=set(),
            where=f"{where}.items[{index}]",
        )
        items.append(
            ListItem(
                blocks=decode_blocks(
                    item_data["blocks"], where=f"{where}.items[{index}]"
                )
            )
        )
    return List(
        ordered=ordered,
        start=start,
        tight=all(len(item.blocks) <= 1 for item in items),
        items=items,
    )


def _decode_inline(value: object, *, where: str) -> Inline:
    data = require_object(value, where)
    _check_keys(
        data,
        required={"type"},
        optional={"text", "inlines", "href", "src", "alt", "title"},
        where=where,
    )
    kind = _text(data["type"], f"{where}.type")
    if kind == "text":
        inline: Inline = Text(
            text=_text(data.get("text", ""), f"{where}.text", allow_empty=True)
        )
    elif kind == "code":
        inline = Code(
            text=_text(data.get("text", ""), f"{where}.text", allow_empty=True)
        )
    elif kind == "emphasis":
        inline = Emphasis(inlines=decode_inlines(data.get("inlines", []), where=where))
    elif kind == "strong":
        inline = Strong(inlines=decode_inlines(data.get("inlines", []), where=where))
    elif kind == "strikethrough":
        inline = Strikethrough(
            inlines=decode_inlines(data.get("inlines", []), where=where)
        )
    elif kind == "line-break":
        inline = LineBreak()
    elif kind == "link":
        title = data.get("title")
        inline = Link(
            href=_text(data.get("href"), f"{where}.href"),
            inlines=decode_inlines(data.get("inlines", []), where=where),
            title=_text(title, f"{where}.title", allow_empty=True) if title else None,
        )
    elif kind == "image":
        title = data.get("title")
        inline = Image(
            src=_text(data.get("src"), f"{where}.src"),
            alt=_text(data.get("alt", ""), f"{where}.alt", allow_empty=True),
            title=_text(title, f"{where}.title", allow_empty=True) if title else None,
        )
    else:
        raise BuildError(f"{where}: inline type {kind!r} is not a correction construct")
    _require_construct_node(inline, where=where)
    return inline


def _require_construct_node(node: Inline | Block, *, where: str) -> None:
    try:
        require_construct(node, where=where)
    except ValueError as error:
        raise BuildError(str(error)) from error


def _clone_inline(inline: Inline) -> Inline:
    if isinstance(inline, Text):
        return Text(text=inline.text)
    if isinstance(inline, Code):
        return Code(text=inline.text)
    if isinstance(inline, Emphasis):
        return Emphasis(inlines=[_clone_inline(inner) for inner in inline.inlines])
    if isinstance(inline, Strong):
        return Strong(inlines=[_clone_inline(inner) for inner in inline.inlines])
    if isinstance(inline, Strikethrough):
        return Strikethrough(inlines=[_clone_inline(inner) for inner in inline.inlines])
    if isinstance(inline, Link):
        return Link(
            href=inline.href,
            inlines=[_clone_inline(inner) for inner in inline.inlines],
            title=inline.title,
        )
    if isinstance(inline, Image):
        return Image(src=inline.src, alt=inline.alt, title=inline.title)
    if isinstance(inline, LineBreak):
        return LineBreak()
    raise BuildError(f"corrections cannot construct {type(inline).__name__} nodes")


# -------------------------------------------------------------------- helpers


def _strip_strong_in_cell(cell: TableCell) -> None:
    for block in iter_blocks(cell.blocks):
        if isinstance(block, (Paragraph, Heading)):
            _strip_strong_inlines(block.inlines)


def _strip_strong_inlines(inlines: list[Inline]) -> None:
    for inline in inlines:
        if isinstance(inline, Strong):
            _strip_strong_inlines(inline.inlines)
            index = inlines.index(inline)
            inlines[index : index + 1] = list(inline.inlines)
            continue
        if isinstance(inline, (Emphasis, Strikethrough, Link)):
            _strip_strong_inlines(inline.inlines)


__all__ = [
    "OPS",
    "AppliedRule",
    "PatchEngine",
    "Rule",
    "check_anchor_groups_attached",
    "decode_blocks",
    "decode_inlines",
    "load_rules",
    "remerge_anchor_groups",
]
