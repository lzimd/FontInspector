"""Import-boundary tests for the fetch, reports, and pure layers."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "specmirror"


@dataclass(frozen=True, slots=True)
class ImportEdge:
    module: str
    target: str
    line: int


def _module_name(path: Path, *, is_package: bool) -> str:
    parts = ["specmirror", *path.relative_to(PACKAGE_ROOT).with_suffix("").parts]
    if is_package:
        parts.pop()
    return ".".join(parts)


def _resolve_from(module: str, node: ast.ImportFrom, *, is_package: bool) -> str:
    if not node.level:
        return node.module or ""
    parts = module.split(".")
    prefix = parts if is_package else parts[:-1]
    keep = len(prefix) - (node.level - 1)
    prefix = prefix[:keep]
    if node.module:
        prefix = [*prefix, *node.module.split(".")]
    return ".".join(prefix)


def _import_edges() -> list[ImportEdge]:
    edges: list[ImportEdge] = []
    for path in sorted(PACKAGE_ROOT.rglob("*.py")):
        is_package = path.name == "__init__.py"
        module = _module_name(path, is_package=is_package)
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                edges.extend(
                    ImportEdge(module, alias.name, node.lineno) for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom):
                edges.append(
                    ImportEdge(
                        module,
                        _resolve_from(module, node, is_package=is_package),
                        node.lineno,
                    )
                )
    return edges


def _is_under(module: str, prefix: str) -> bool:
    return module == prefix or module.startswith(prefix + ".")


def _forbidden(
    module_prefixes: tuple[str, ...],
    target_prefixes: tuple[str, ...],
) -> list[ImportEdge]:
    return [
        edge
        for edge in _import_edges()
        if any(_is_under(edge.module, prefix) for prefix in module_prefixes)
        and any(_is_under(edge.target, prefix) for prefix in target_prefixes)
    ]


def _format(edges: list[ImportEdge]) -> str:
    return "\n".join(
        f"{edge.module}:{edge.line} imports {edge.target}" for edge in edges
    )


def test_pure_layers_do_not_import_main_lines_or_reports() -> None:
    edges = _forbidden(
        ("specmirror.sources",),
        (
            "specmirror.fetch",
            "specmirror.reports",
            "specmirror.cli",
        ),
    )
    assert not edges, _format(edges)


def test_reports_do_not_import_main_lines() -> None:
    edges = _forbidden(
        ("specmirror.reports",),
        ("specmirror.fetch", "specmirror.cli"),
    )
    assert not edges, _format(edges)


def test_errors_has_no_internal_imports() -> None:
    edges = [
        edge
        for edge in _import_edges()
        if edge.module == "specmirror.errors" and _is_under(edge.target, "specmirror")
    ]
    assert not edges, _format(edges)


def test_network_imports_are_confined_to_fetch_http() -> None:
    network_modules = {
        "http.client",
        "urllib.error",
        "urllib.request",
        "email.message",
        "email.utils",
    }
    edges = [
        edge
        for edge in _import_edges()
        if edge.target in network_modules and edge.module != "specmirror.fetch.http"
    ]
    assert not edges, _format(edges)


def test_beautifulsoup_is_confined_to_dom() -> None:
    edges = [
        edge
        for edge in _import_edges()
        if (edge.target == "bs4" or edge.target.startswith("bs4."))
        and edge.module != "specmirror.dom"
    ]
    assert not edges, _format(edges)


def test_only_cli_imports_argparse_and_prints() -> None:
    edges = [edge for edge in _import_edges() if edge.target == "argparse"]
    assert [edge.module for edge in edges] == ["specmirror.cli"], _format(edges)

    offenders: list[str] = []
    for path in sorted(PACKAGE_ROOT.rglob("*.py")):
        if path == PACKAGE_ROOT / "cli.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        offenders.extend(
            f"{path.relative_to(PACKAGE_ROOT)}:{node.lineno}"
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "print"
        )
    assert not offenders, "\n".join(offenders)
