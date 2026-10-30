"""The conversion layers: neutral DOM to AST to Markdown.

The package facade exposes the pipeline entry points and the page-level
types that the build and reports consume. The layers are independent of the
source adapters and of the fetch stage.
"""

from __future__ import annotations

from .ast import (
    AnchorGroup,
    Block,
    Document,
    Inline,
    PageAst,
    block_fingerprint,
    inline_text,
    iter_blocks,
    rows_fingerprint,
)
from .build_page_ast import build_page_ast
from .normalize import NormalizationResult, normalize_roots
from .patch import (
    PatchEngine,
    Rule,
    check_anchor_groups_attached,
    load_rules,
    remerge_anchor_groups,
)
from .render import Renderer, render_page
from .table import (
    TableDiagnostics,
    TableInventoryEntry,
    TableLedger,
    expand_table_spans_in_blocks,
    flatten_cells,
    inventory,
    iter_tables,
    lower_nested_tables,
    normalize_headers,
)

__all__ = [
    "AnchorGroup",
    "Block",
    "Document",
    "Inline",
    "NormalizationResult",
    "PageAst",
    "PatchEngine",
    "Renderer",
    "Rule",
    "TableDiagnostics",
    "TableInventoryEntry",
    "TableLedger",
    "block_fingerprint",
    "build_page_ast",
    "check_anchor_groups_attached",
    "expand_table_spans_in_blocks",
    "flatten_cells",
    "inline_text",
    "inventory",
    "iter_blocks",
    "iter_tables",
    "load_rules",
    "lower_nested_tables",
    "normalize_headers",
    "normalize_roots",
    "remerge_anchor_groups",
    "render_page",
    "rows_fingerprint",
]
