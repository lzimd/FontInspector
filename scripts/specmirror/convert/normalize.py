"""Character and text normalization over the neutral DOM subtree.

Normalization happens once, before AST construction. It removes source
comments, repairs parser artifacts, resolves the one semantic CSS property,
and applies the whitespace policy. The policy keeps significant spaces,
including padded literals inside straight-quoted spans and no-break space
runs that table cells later render as entities.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from ..dom import (
    DomComment,
    DomContainer,
    DomDocument,
    DomElement,
    DomNode,
    DomText,
    attribute_text,
    find_all,
    iter_nodes,
    normalize_list_items,
)
from ..errors import BuildError

_WORD_CHARACTER = re.compile(r"[A-Za-z0-9]")
_IDENTIFIER_DISALLOWED = re.compile(r"[^A-Za-z0-9._-]+")
_IDENTIFIER_HYPHENS = re.compile(r"-{2,}")
_MAX_IDENTIFIER = 64

SUPERSCRIPT_DIGITS: dict[str, str] = {
    "0": "\u2070",
    "1": "\u00b9",
    "2": "\u00b2",
    "3": "\u00b3",
    "4": "\u2074",
    "5": "\u2075",
    "6": "\u2076",
    "7": "\u2077",
    "8": "\u2078",
    "9": "\u2079",
}

SUBSCRIPT_DIGITS: dict[str, str] = {
    "0": "\u2080",
    "1": "\u2081",
    "2": "\u2082",
    "3": "\u2083",
    "4": "\u2084",
    "5": "\u2085",
    "6": "\u2086",
    "7": "\u2087",
    "8": "\u2088",
    "9": "\u2089",
}


@dataclass(slots=True)
class DroppedComment:
    text: str
    fingerprint: str


@dataclass(slots=True)
class ListRepair:
    description: str


@dataclass(slots=True)
class IgnoredCss:
    property: str
    value: str


@dataclass(slots=True)
class StyleEmphasis:
    element: str
    value: str


def _new_italic() -> dict[DomElement, bool]:
    return {}


def _new_comments() -> list[DroppedComment]:
    return []


def _new_repairs() -> list[ListRepair]:
    return []


def _new_ignored_css() -> list[IgnoredCss]:
    return []


def _new_style_emphasis() -> list[StyleEmphasis]:
    return []


@dataclass(slots=True)
class NormalizationResult:
    """The facts normalization learned about one page's subtree."""

    italic: dict[DomElement, bool] = field(default_factory=_new_italic)
    comments: list[DroppedComment] = field(default_factory=_new_comments)
    repairs: list[ListRepair] = field(default_factory=_new_repairs)
    ignored_css: list[IgnoredCss] = field(default_factory=_new_ignored_css)
    style_emphasis: list[StyleEmphasis] = field(default_factory=_new_style_emphasis)


def normalize_roots(
    roots: tuple[DomElement, ...],
    *,
    page: str,
    result: NormalizationResult,
) -> None:
    """Normalize every content root in place."""
    for root in roots:
        _collect_comments(root, result)
        _merge_adjacent_text(root)
        _normalize_preformatted(root)
        _repair_lists(root, page, result)
        root_italic = _resolve_element_font_style(root, False, result)
        _resolve_descendant_font_styles(root, root_italic, result)
        _collapse_prose_whitespace(root)
        _separate_definition_terms(root, page)


# ------------------------------------------------------------- character text


def normalize_line_endings(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def normalize_label(text: str) -> str:
    """Collapse every whitespace class for labels such as alt and captions."""
    return " ".join(text.split())


def normalize_code_span(text: str) -> str:
    """CommonMark rewrites line endings in a code span to spaces."""
    return normalize_line_endings(text).replace("\n", " ")


def is_ascii_digit_text(text: str) -> bool:
    if not text:
        return False
    seen_digit = False
    for character in text:
        if character == " ":
            continue
        if not (character.isascii() and character.isdigit()):
            return False
        seen_digit = True
    return seen_digit


def to_superscript(text: str) -> str:
    return "".join(SUPERSCRIPT_DIGITS.get(character, character) for character in text)


def to_subscript(text: str) -> str:
    return "".join(SUBSCRIPT_DIGITS.get(character, character) for character in text)


def sanitize_identifier(source: str) -> str:
    """A stable local-id fragment for a source anchor name."""
    cleaned = _IDENTIFIER_DISALLOWED.sub("-", source)
    cleaned = _IDENTIFIER_HYPHENS.sub("-", cleaned).strip("-._")
    if not cleaned:
        return "anchor"
    if len(cleaned) > _MAX_IDENTIFIER:
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:8]
        cleaned = f"{cleaned[: _MAX_IDENTIFIER - 9].rstrip('-._')}-{digest}"
    return cleaned


# ------------------------------------------------------------------- comments


def _collect_comments(container: DomContainer, result: NormalizationResult) -> None:
    for node in list(iter_nodes(container)):
        if not isinstance(node, DomComment):
            continue
        text = node.text.strip()
        fingerprint = hashlib.sha256(text.encode("utf-8")).hexdigest()
        result.comments.append(DroppedComment(text=text, fingerprint=fingerprint))
        _detach(node)


def _merge_adjacent_text(container: DomContainer) -> None:
    merged: list[DomNode] = []
    for child in container.children:
        if isinstance(child, DomText) and merged and isinstance(merged[-1], DomText):
            merged[-1].text += child.text
            child.parent = None
            continue
        merged.append(child)
    container.children = merged
    for child in container.children:
        if isinstance(child, DomElement):
            _merge_adjacent_text(child)


# --------------------------------------------------------------- preformatted


def _normalize_preformatted(container: DomContainer) -> None:
    for pre in find_all(container, "pre"):
        texts = [node for node in iter_nodes(pre) if isinstance(node, DomText)]
        for text in texts:
            text.text = normalize_line_endings(text.text)
        if texts and texts[0].text.startswith("\n"):
            texts[0].text = texts[0].text[1:]


# --------------------------------------------------------------------- lists


def _repair_lists(
    container: DomContainer, page: str, result: NormalizationResult
) -> None:
    """Flatten list items that the parser nested inside another item.

    ``html.parser`` doesn't close an open ``li`` implicitly. The DOM helper
    moves nested items to the parent list and updates their parent links.
    Each changed list adds a ``ListRepair`` entry.
    """
    for name in ("ul", "ol"):
        for list_tag in find_all(container, name):
            before = _list_layout(list_tag)
            normalize_list_items(list_tag)
            if before != _list_layout(list_tag):
                result.repairs.append(
                    ListRepair(
                        description=(
                            f"flattened nested list items in a <{name}> on page {page}"
                        )
                    )
                )


def _list_layout(element: DomElement) -> tuple[tuple[str, object], ...]:
    return tuple(
        (child.name, _list_layout(child))
        for child in element.children
        if isinstance(child, DomElement)
    )


# ---------------------------------------------------------------- font styles


def _resolve_descendant_font_styles(
    container: DomContainer,
    inherited: bool,
    result: NormalizationResult,
) -> None:
    for child in container.children:
        if not isinstance(child, DomElement):
            continue
        state = _resolve_element_font_style(child, inherited, result)
        _resolve_descendant_font_styles(child, state, result)


def _resolve_element_font_style(
    element: DomElement,
    inherited: bool,
    result: NormalizationResult,
) -> bool:
    state = inherited
    style = attribute_text(element, "style")
    if style is not None:
        state = _apply_inline_style(element, style, state, result)
    result.italic[element] = state
    return state


def _apply_inline_style(
    element: DomElement,
    style: str,
    state: bool,
    result: NormalizationResult,
) -> bool:
    active = state
    for declaration in style.split(";"):
        stripped = declaration.strip()
        if not stripped:
            continue
        property_name, separator, raw_value = stripped.partition(":")
        if not separator:
            result.ignored_css.append(IgnoredCss(property="?", value=stripped))
            continue
        name = property_name.strip().casefold()
        value = raw_value.strip()
        if value.casefold().endswith("!important"):
            value = value[: -len("!important")].rstrip()
        if name != "font-style":
            result.ignored_css.append(IgnoredCss(property=name, value=value))
            continue
        folded = value.casefold()
        if folded in {"italic", "oblique"}:
            if not active:
                result.style_emphasis.append(
                    StyleEmphasis(element=element.name, value=folded)
                )
            active = True
            continue
        if folded == "normal":
            active = False
            continue
        result.ignored_css.append(IgnoredCss(property=name, value=value))
    return active


# ----------------------------------------------------------------- whitespace


@dataclass(slots=True)
class _QuoteState:
    in_quote: bool = False
    previous: str | None = None


def _collapse_prose_whitespace(container: DomContainer) -> None:
    _collapse_scope(container)


def _collapse_scope(container: DomContainer) -> None:
    for child in container.children:
        if isinstance(child, DomText):
            child.text = _collapse_text(child.text)
            continue
        if not isinstance(child, DomElement):
            continue
        if child.name == "pre":
            continue
        _collapse_scope(child)


def _collapse_text(text: str) -> str:
    state = _QuoteState()
    output: list[str] = []
    run_active = False
    run_spaces = 0
    run_in_quote = False
    run_has_non_space = False

    def flush_run() -> None:
        nonlocal run_active, run_spaces, run_in_quote, run_has_non_space
        if not run_active:
            return
        if run_in_quote and not run_has_non_space:
            output.append(" " * run_spaces)
        else:
            output.append(" ")
        run_active = False
        run_spaces = 0
        run_in_quote = False
        run_has_non_space = False

    for character in text:
        if character in " \t\r\n\f":
            if not run_active:
                run_active = True
                run_in_quote = state.in_quote
            if character == " " and run_in_quote and not run_has_non_space:
                run_spaces += 1
            elif character != " " or not run_in_quote:
                run_has_non_space = True
            state.previous = character
            continue
        flush_run()
        is_apostrophe = character == "'" and (
            state.previous is None or not state.previous.isalpha()
        )
        if is_apostrophe:
            state.in_quote = not state.in_quote
        output.append(character)
        state.previous = character
    flush_run()
    return "".join(output)


def _separate_definition_terms(container: DomContainer, page: str) -> None:
    for dfn in find_all(container, "dfn"):
        text = _element_text(dfn).strip()
        following = _following_text(dfn)
        if not text or following is None:
            continue
        if not _WORD_CHARACTER.fullmatch(text[-1]):
            continue
        if not _WORD_CHARACTER.fullmatch(following[0]):
            continue
        parent = dfn.parent
        if parent is None:
            raise BuildError(f"<dfn> without a parent on page {page}")
        _insert_after(dfn, DomText(text=" "))


def _element_text(element: DomElement) -> str:
    return "".join(
        node.text for node in iter_nodes(element) if isinstance(node, DomText)
    )


def _following_text(element: DomElement) -> str | None:
    current: DomContainer = element
    while True:
        parent = current.parent
        if parent is None:
            return None
        index = _child_index(parent, current)
        for sibling in parent.children[index + 1 :]:
            if isinstance(sibling, DomText):
                if sibling.text.strip():
                    return sibling.text
                continue
            if isinstance(sibling, DomElement):
                text = _element_text(sibling)
                if text.strip():
                    return text
        if isinstance(parent, DomDocument):
            return None
        current = parent


def _child_index(container: DomContainer, node: DomNode) -> int:
    for index, child in enumerate(container.children):
        if child is node:
            return index
    raise BuildError("normalization lost a child link")


# -------------------------------------------------------------------- mutation


def _detach(node: DomNode) -> None:
    parent = node.parent
    if parent is None:
        return
    for index, child in enumerate(parent.children):
        if child is node:
            del parent.children[index]
            break
    node.parent = None


def _insert_after(reference: DomNode, node: DomNode) -> None:
    parent = reference.parent
    if parent is None:
        raise BuildError("cannot insert a node without a parent")
    index = _child_index(parent, reference)
    node.parent = parent
    parent.children.insert(index + 1, node)


__all__ = [
    "SUBSCRIPT_DIGITS",
    "SUPERSCRIPT_DIGITS",
    "DroppedComment",
    "IgnoredCss",
    "ListRepair",
    "NormalizationResult",
    "StyleEmphasis",
    "is_ascii_digit_text",
    "normalize_code_span",
    "normalize_label",
    "normalize_line_endings",
    "normalize_roots",
    "sanitize_identifier",
    "to_subscript",
    "to_superscript",
]
