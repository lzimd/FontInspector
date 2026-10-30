"""The table governance subpipeline.

Tables pass through three recorded states: the source structure captured before
corrections, the effective structure after corrections, and the rendered
structure after nested lowering, span expansion, header normalization, and cell
flattening. The ledger is the authoring surface for page-specific repairs; it
records structural facts rather than judgments.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..errors import BuildError
from .ast import (
    AnchorGroup,
    Block,
    BlockQuote,
    Heading,
    Inline,
    LineBreak,
    Link,
    List,
    NestedTable,
    Paragraph,
    RawHtml,
    SpanPlaceholder,
    SpanPlaceholderKind,
    Table,
    TableCell,
    TableRow,
    Text,
    inline_text,
    inlines_text,
    iter_rows,
    iter_tables,
    rows_fingerprint,
    table_fingerprint,
)

COLSPAN: SpanPlaceholderKind = "colspan"
ROWSPAN: SpanPlaceholderKind = "rowspan"
ROWSPAN_COLSPAN: SpanPlaceholderKind = "rowspan colspan"
NESTED_LINK_TEXT = "See table"


@dataclass(frozen=True, slots=True)
class TableFacts:
    """Structural facts about a table before corrections run."""

    source_rows: int
    source_columns: int
    declared_header: str
    header_fingerprint: str
    first_data_row_fingerprint: str


@dataclass(frozen=True, slots=True)
class LiftedTable:
    anchor: str
    row: int
    cell: int
    depth: int
    rows: int
    columns: int
    fingerprint: str


def _new_lifted() -> list[LiftedTable]:
    return []


def _new_flattened() -> list[str]:
    return []


def _new_covered() -> dict[str, int]:
    return {}


@dataclass(slots=True)
class TableDiagnostics:
    """What the table pipeline changed and why."""

    lifted: list[LiftedTable] = field(default_factory=_new_lifted)
    flattened_headers: list[str] = field(default_factory=_new_flattened)
    covered_cells: dict[str, int] = field(default_factory=_new_covered)


def _new_facts() -> dict[int, TableFacts]:
    return {}


def _new_spans() -> dict[int, dict[str, int]]:
    return {}


def _new_repairs() -> dict[int, list[str]]:
    return {}


@dataclass(slots=True)
class TableLedger:
    """The source, effective, and rendered facts of a page's tables."""

    facts: dict[int, TableFacts] = field(default_factory=_new_facts)
    spans: dict[int, dict[str, int]] = field(default_factory=_new_spans)
    repairs: dict[int, list[str]] = field(default_factory=_new_repairs)
    diagnostics: TableDiagnostics = field(default_factory=TableDiagnostics)

    def capture_sources(self, blocks: list[Block]) -> None:
        """Record every table's source structure before corrections."""
        for table in iter_tables(blocks):
            self.facts[id(table)] = _table_facts(table)

    def record_repair(self, table: Table, rule_id: str) -> None:
        self.repairs.setdefault(id(table), []).append(rule_id)

    def record_spans(self, table: Table, counts: dict[str, int]) -> None:
        self.spans[id(table)] = counts


@dataclass(frozen=True, slots=True)
class TableInventoryEntry:
    """One rendered table's structural record for the build report."""

    section: tuple[str, ...]
    ordinal: int
    source_rows: int | None
    source_columns: int | None
    declared_header: str | None
    header_fingerprint: str | None
    first_data_row_fingerprint: str | None
    effective_header_rows: int
    effective_header_source: str
    repair_id: str | None
    spans: dict[str, int]
    nested_tables: int
    nested_anchors: tuple[str, ...]
    rendered_header: str
    corrections: tuple[str, ...]


def _table_facts(table: Table) -> TableFacts:
    rows = [*table.header.rows, *table.rows]
    return TableFacts(
        source_rows=len(rows),
        source_columns=max((len(row.cells) for row in rows), default=0),
        declared_header=table.header.source,
        header_fingerprint=rows_fingerprint(table.header.rows),
        first_data_row_fingerprint=rows_fingerprint(table.rows[:1]),
    )


def _outer_tables(blocks: list[Block]) -> list[Table]:
    result: list[Table] = []
    for block in blocks:
        if isinstance(block, Table):
            result.append(block)
            continue
        if isinstance(block, BlockQuote):
            result.extend(_outer_tables(block.blocks))
            continue
        if isinstance(block, List):
            for item in block.items:
                result.extend(_outer_tables(item.blocks))
    return result


def nested_table_anchor_id(slug: str, number: int) -> str:
    return f"nested-{slug}-{number}"


def lower_nested_tables(
    blocks: list[Block],
    *,
    slug: str,
    ledger: TableLedger,
    anchor_groups_by_block: dict[int, AnchorGroup],
) -> None:
    """Lift nested tables out of their parent cells in document order."""
    lifter = _NestedLifter(
        slug=slug,
        ledger=ledger,
        anchor_groups_by_block=anchor_groups_by_block,
        number=0,
    )
    for table in _outer_tables(blocks):
        lifter.lower(table, depth=0)


class _NestedLifter:
    def __init__(
        self,
        *,
        slug: str,
        ledger: TableLedger,
        anchor_groups_by_block: dict[int, AnchorGroup],
        number: int,
    ) -> None:
        self.slug = slug
        self.ledger = ledger
        self.anchor_groups_by_block = anchor_groups_by_block
        self.number = number

    def lower(self, table: Table, *, depth: int) -> None:
        for row_index, row in enumerate(iter_rows(table)):
            for cell_index, cell in enumerate(row.cells):
                for position, block in enumerate(cell.blocks):
                    if not isinstance(block, Table):
                        continue
                    self.number += 1
                    anchor = nested_table_anchor_id(self.slug, self.number)
                    description = (
                        "The following table was originally nested in "
                        f"row {row_index + 1}, cell {cell_index + 1} "
                        "of the table above."
                    )
                    self.ledger.diagnostics.lifted.append(
                        LiftedTable(
                            anchor=anchor,
                            row=row_index + 1,
                            cell=cell_index + 1,
                            depth=depth,
                            rows=len(block.header.rows) + len(block.rows),
                            columns=column_count(block),
                            fingerprint=table_fingerprint(block),
                        )
                    )
                    link = Paragraph(
                        inlines=[
                            Link(
                                href=f"#{anchor}",
                                inlines=[Text(text=NESTED_LINK_TEXT)],
                            )
                        ]
                    )
                    cell.blocks[position] = link
                    group = self.anchor_groups_by_block.pop(id(block), None)
                    if group is not None:
                        group.block = link
                        self.anchor_groups_by_block[id(link)] = group
                    table.nested_tables.append(
                        NestedTable(
                            anchor_id=anchor,
                            description=description,
                            table=block,
                        )
                    )
                    self.lower(block, depth=depth + 1)


def expand_table_spans_in_blocks(blocks: list[Block], *, ledger: TableLedger) -> None:
    """Expand every table's spans and record per-table span counts."""
    for table in iter_tables(blocks):
        ledger.record_spans(table, expand_span_grid(table, ledger.diagnostics))


def expand_span_grid(table: Table, diagnostics: TableDiagnostics) -> dict[str, int]:
    """Expand row and column spans into a rectangular grid with placeholders."""
    counts: dict[str, int] = {"row_span": 0, "col_span": 0}
    all_rows = [*table.header.rows, *table.rows]
    if not all_rows:
        raise BuildError("table without rows")
    occupied: list[dict[int, TableCell | SpanPlaceholderKind]] = [{} for _ in all_rows]
    for row_index, row in enumerate(all_rows):
        column = 0
        for cell in row.cells:
            while column in occupied[row_index]:
                column += 1
            if cell.row_span > 1:
                counts["row_span"] += 1
            if cell.col_span > 1:
                counts["col_span"] += 1
            if row_index + cell.row_span > len(all_rows):
                raise BuildError(
                    f"rowspan {cell.row_span} exceeds the table bottom in row "
                    f"{row_index + 1}"
                )
            for row_offset in range(cell.row_span):
                target_row = occupied[row_index + row_offset]
                for column_offset in range(cell.col_span):
                    target_column = column + column_offset
                    if target_column in target_row:
                        raise BuildError(
                            "overlapping table spans at row "
                            f"{row_index + row_offset + 1}, "
                            f"column {target_column + 1}"
                        )
                    if row_offset == 0 and column_offset == 0:
                        target_row[target_column] = cell
                        continue
                    kind = _covered_kind(row_offset, column_offset)
                    target_row[target_column] = kind
                    diagnostics.covered_cells[kind] = (
                        diagnostics.covered_cells.get(kind, 0) + 1
                    )
            column += cell.col_span
    width = max((len(row_map) for row_map in occupied), default=0)
    header_count = len(table.header.rows)
    expanded: list[TableRow] = []
    for row_map in occupied:
        cells: list[TableCell] = []
        for column in range(width):
            entry = row_map.get(column)
            if entry is None:
                cells.append(TableCell(role="td", blocks=[]))
            elif isinstance(entry, str):
                placeholders: list[Inline] = [SpanPlaceholder(kind=entry)]
                cells.append(
                    TableCell(role="td", blocks=[Paragraph(inlines=placeholders)])
                )
            else:
                cells.append(entry)
        expanded.append(TableRow(cells=cells))
    table.header.rows = expanded[:header_count]
    table.rows = expanded[header_count:]
    return counts


def _covered_kind(row_offset: int, column_offset: int) -> SpanPlaceholderKind:
    match (bool(row_offset), bool(column_offset)):
        case (True, True):
            return ROWSPAN_COLSPAN
        case (True, False):
            return ROWSPAN
        case (False, True):
            return COLSPAN
        case _:
            raise AssertionError("unreachable")


def normalize_headers(
    blocks: list[Block],
    *,
    ledger: TableLedger,
    anchor_groups_by_block: dict[int, AnchorGroup],
) -> None:
    """Remove header line breaks and flatten multi-row headers."""
    for table in iter_tables(blocks):
        _normalize_table_headers(
            table,
            diagnostics=ledger.diagnostics,
            anchor_groups_by_block=anchor_groups_by_block,
        )


def _normalize_table_headers(
    table: Table,
    *,
    diagnostics: TableDiagnostics,
    anchor_groups_by_block: dict[int, AnchorGroup],
) -> None:
    for row in table.header.rows:
        for cell in row.cells:
            _join_header_cell(cell, anchor_groups_by_block)
    if len(table.header.rows) > 1:
        table.header.rows = [_flatten_header_rows(table.header.rows, diagnostics)]


def _join_header_cell(
    cell: TableCell,
    anchor_groups_by_block: dict[int, AnchorGroup],
) -> None:
    fragments: list[list[Inline]] = []
    for block in cell.blocks:
        if not isinstance(block, Paragraph):
            raise BuildError(
                "header cell contains block content that cannot be reduced to "
                "inline content; a correction is required"
            )
        current: list[Inline] = []
        group = anchor_groups_by_block.get(id(block))
        if group is not None and group.canonical_id is not None:
            current.append(RawHtml(element="a", anchor_id=group.canonical_id))
        for inline in block.inlines:
            if isinstance(inline, LineBreak):
                fragments.append(current)
                current = []
                continue
            current.append(inline)
        fragments.append(current)
    joined = _join_fragments(fragments)
    cell.blocks = _paragraph_blocks(joined)


def _join_fragments(fragments: list[list[Inline]]) -> list[Inline]:
    parts = [trimmed for fragment in fragments if (trimmed := _trim_fragment(fragment))]
    joined: list[Inline] = []
    for index, part in enumerate(parts):
        if index and _needs_space(joined, part):
            joined.append(Text(text=" "))
        joined.extend(part)
    return joined


def _trim_fragment(fragment: list[Inline]) -> list[Inline]:
    while fragment and isinstance(fragment[0], Text) and not fragment[0].text.strip():
        fragment.pop(0)
    while fragment and isinstance(fragment[-1], Text) and not fragment[-1].text.strip():
        fragment.pop()
    if fragment and isinstance(fragment[0], Text):
        fragment[0].text = fragment[0].text.lstrip(" ")
    if fragment and isinstance(fragment[-1], Text):
        fragment[-1].text = fragment[-1].text.rstrip(" ")
    return fragment


def _needs_space(previous: list[Inline], following: list[Inline]) -> bool:
    """Return whether two header fragments need a separating space.

    Only alphanumeric boundaries get a space. Punctuation boundaries,
    including an opening parenthesis, join directly. A label word followed
    by a parenthetical therefore joins without a space.
    """
    previous_text = "".join(inline_text(inline) for inline in previous)
    following_text = "".join(inline_text(inline) for inline in following)
    if not previous_text or not following_text:
        return False
    return previous_text[-1].isalnum() and following_text[0].isalnum()


def _paragraph_blocks(inlines: list[Inline]) -> list[Block]:
    if not inlines:
        return []
    block: Block = Paragraph(inlines=inlines)
    return [block]


def _flatten_header_rows(
    rows: list[TableRow],
    diagnostics: TableDiagnostics,
) -> TableRow:
    width = max((len(row.cells) for row in rows), default=0)
    cells: list[TableCell] = []
    for column in range(width):
        pieces: list[list[Inline]] = []
        for row in rows:
            content = _cell_inlines(row.cells[column])
            if content:
                pieces.append(content)
        joined: list[Inline] = []
        for index, piece in enumerate(pieces):
            if index:
                joined.append(LineBreak())
            joined.extend(piece)
        if len(pieces) > 1:
            diagnostics.flattened_headers.append(
                f"column {column + 1}: joined {len(pieces)} header rows"
            )
        blocks = _paragraph_blocks(joined)
        cells.append(TableCell(role="th", blocks=blocks))
    return TableRow(cells=cells)


def _cell_inlines(cell: TableCell) -> list[Inline]:
    inlines: list[Inline] = []
    for block in cell.blocks:
        if not isinstance(block, Paragraph):
            raise BuildError(
                "header cell contains block content that cannot be reduced to "
                "inline content; a correction is required"
            )
        inlines.extend(block.inlines)
    return inlines


def flatten_cells(
    blocks: list[Block],
    *,
    anchor_groups_by_block: dict[int, AnchorGroup],
) -> None:
    """Reduce every data cell's block content to inline content."""
    for table in iter_tables(blocks):
        for row in table.rows:
            for cell in row.cells:
                _flatten_cell(cell, anchor_groups_by_block)


def _flatten_cell(
    cell: TableCell, anchor_groups_by_block: dict[int, AnchorGroup]
) -> None:
    inlines: list[Inline] = []
    first = True
    for block in cell.blocks:
        group = anchor_groups_by_block.get(id(block))
        if group is not None and group.canonical_id is not None:
            inlines.append(RawHtml(element="a", anchor_id=group.canonical_id))
        if not first:
            inlines.append(LineBreak())
        first = False
        inlines.extend(_flatten_block_to_inlines(block))
    cell.blocks = _paragraph_blocks(inlines)


def _flatten_block_to_inlines(block: Block) -> list[Inline]:
    if isinstance(block, Paragraph):
        return list(block.inlines)
    if isinstance(block, List):
        inlines: list[Inline] = []
        for item_index, item in enumerate(block.items):
            if item_index:
                inlines.append(LineBreak())
            for block_index, inner in enumerate(item.blocks):
                if block_index:
                    inlines.append(LineBreak())
                inlines.extend(_flatten_block_to_inlines(inner))
        return inlines
    raise BuildError(
        "table cell contains block content that cannot be represented inline; "
        "a correction is required"
    )


def column_count(table: Table) -> int:
    rows = [*table.header.rows, *table.rows]
    if not rows:
        return 0
    return max(len(row.cells) for row in rows)


def inventory(blocks: list[Block], ledger: TableLedger) -> list[TableInventoryEntry]:
    """One inventory entry per rendered table, in document order."""
    entries: list[TableInventoryEntry] = []
    counters: dict[tuple[str, ...], int] = {}

    def visit_table(table: Table, section: tuple[str, ...], ordinal: int) -> None:
        entries.append(_inventory_entry(table, section, ordinal, ledger))
        for nested in table.nested_tables:
            visit_table(nested.table, section, ordinal)

    def walk(blocks: list[Block], section: tuple[str, ...]) -> None:
        for block in blocks:
            if isinstance(block, Heading):
                section = (*section, _heading_text(block))
                continue
            if isinstance(block, BlockQuote):
                walk(block.blocks, section)
                continue
            if isinstance(block, List):
                for item in block.items:
                    walk(item.blocks, section)
                continue
            if isinstance(block, Table):
                ordinal = counters.get(section, 0) + 1
                counters[section] = ordinal
                visit_table(block, section, ordinal)

    walk(blocks, ())
    return entries


def _inventory_entry(
    table: Table,
    section: tuple[str, ...],
    ordinal: int,
    ledger: TableLedger,
) -> TableInventoryEntry:
    facts = ledger.facts.get(id(table))
    return TableInventoryEntry(
        section=section,
        ordinal=ordinal,
        source_rows=facts.source_rows if facts else None,
        source_columns=facts.source_columns if facts else None,
        declared_header=facts.declared_header if facts else None,
        header_fingerprint=facts.header_fingerprint if facts else None,
        first_data_row_fingerprint=(
            facts.first_data_row_fingerprint if facts else None
        ),
        effective_header_rows=len(table.header.rows),
        effective_header_source=table.header.source,
        repair_id=table.header.repair_id,
        spans=dict(ledger.spans.get(id(table), {})),
        nested_tables=len(table.nested_tables),
        nested_anchors=tuple(nested.anchor_id for nested in table.nested_tables),
        rendered_header="declared" if table.header.rows else "synthetic-empty",
        corrections=tuple(ledger.repairs.get(id(table), ())),
    )


def _heading_text(heading: Heading) -> str:
    return inlines_text(heading.inlines).strip()


__all__ = [
    "COLSPAN",
    "NESTED_LINK_TEXT",
    "ROWSPAN",
    "ROWSPAN_COLSPAN",
    "LiftedTable",
    "TableDiagnostics",
    "TableFacts",
    "TableInventoryEntry",
    "TableLedger",
    "column_count",
    "expand_span_grid",
    "expand_table_spans_in_blocks",
    "flatten_cells",
    "inventory",
    "iter_tables",
    "lower_nested_tables",
    "nested_table_anchor_id",
    "normalize_headers",
]
