"""Shared parser adapter and parser-independent DOM model."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import TypeGuard

from bs4 import BeautifulSoup, Tag
from bs4.element import Comment, NavigableString, PageElement

from .errors import PageValidationError
from .text import normalize_whitespace


@dataclass(slots=True, eq=False, kw_only=True)
class DomNode:
    """Shared parent link for parser-independent nodes."""

    parent: DomDocument | DomElement | None = field(
        default=None, repr=False, compare=False
    )


def _new_nodes() -> list[DomNode]:
    return []


@dataclass(slots=True, eq=False, kw_only=True)
class DomElement(DomNode):
    """A parser-independent element node."""

    name: str
    attributes: dict[str, str | tuple[str, ...]]
    children: list[DomNode] = field(default_factory=_new_nodes)


@dataclass(slots=True, eq=False, kw_only=True)
class DomText(DomNode):
    """A parser-independent text node."""

    text: str


@dataclass(slots=True, eq=False, kw_only=True)
class DomComment(DomNode):
    """A parser-independent comment node."""

    text: str


@dataclass(slots=True, eq=False)
class DomDocument:
    """The parser-independent document root."""

    children: list[DomNode] = field(default_factory=_new_nodes)


DomContainer = DomDocument | DomElement


def decode_utf8(body: bytes, *, what: str) -> str:
    try:
        return body.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise PageValidationError(f"{what} is not valid UTF-8: {error}") from error


def parse_html(text: str) -> DomDocument:
    """Parse decoded HTML into the parser-independent DOM model."""
    soup = BeautifulSoup(text, "html.parser")
    document = DomDocument()
    for child in soup.children:
        node = _convert_node(child)
        if node is None:
            continue
        node.parent = document
        document.children.append(node)
    return document


def _convert_node(node: PageElement) -> DomNode | None:
    if isinstance(node, Comment):
        return DomComment(text=str(node))
    if isinstance(node, NavigableString):
        return DomText(text=str(node))
    if not isinstance(node, Tag):
        return None
    element = DomElement(
        name=_element_name(node),
        attributes=_element_attributes(node),
    )
    for child in node.children:
        converted = _convert_node(child)
        if converted is None:
            continue
        converted.parent = element
        element.children.append(converted)
    return element


def _element_name(tag: Tag) -> str:
    return tag.name.casefold()


def _element_attributes(tag: Tag) -> dict[str, str | tuple[str, ...]]:
    attributes: dict[str, str | tuple[str, ...]] = {}
    for raw_name, raw_value in tag.attrs.items():
        name = str(raw_name).casefold()
        if isinstance(raw_value, str):
            attributes[name] = raw_value
        else:
            attributes[name] = tuple(str(value) for value in raw_value)
    return attributes


def iter_nodes(container: DomContainer) -> Iterator[DomNode]:
    """Yield every descendant node depth-first in document order."""
    for child in container.children:
        yield child
        if isinstance(child, DomElement):
            yield from iter_nodes(child)


def iter_elements(container: DomContainer) -> Iterator[DomElement]:
    """Yield every descendant element depth-first in document order."""
    for node in iter_nodes(container):
        if isinstance(node, DomElement):
            yield node


def iter_comments(container: DomContainer) -> Iterator[DomComment]:
    """Yield every descendant comment depth-first in document order."""
    for node in iter_nodes(container):
        if isinstance(node, DomComment):
            yield node


def next_sibling(node: DomNode) -> DomNode | None:
    """Return the node that immediately follows another sibling."""
    parent = node.parent
    if parent is None:
        return None
    found = False
    for child in parent.children:
        if found:
            return child
        if child is node:
            found = True
    return None


def find_all(container: DomContainer, name: str) -> list[DomElement]:
    """Return every descendant element with the given tag name."""
    folded = name.casefold()
    return [element for element in iter_elements(container) if element.name == folded]


def find(container: DomContainer, name: str) -> DomElement | None:
    """Return the first descendant element with the given tag name."""
    folded = name.casefold()
    for element in iter_elements(container):
        if element.name == folded:
            return element
    return None


def find_all_with_class(
    container: DomContainer,
    name: str,
    class_name: str,
) -> list[DomElement]:
    """Return descendant elements with the given tag name and class."""
    return [
        element
        for element in find_all(container, name)
        if class_name in class_names(element)
    ]


def find_all_with_attribute(
    container: DomContainer,
    attribute: str,
    *,
    name: str | None = None,
) -> list[DomElement]:
    """Return descendant elements that carry the given attribute."""
    folded = name.casefold() if name is not None else None
    return [
        element
        for element in iter_elements(container)
        if attribute in element.attributes
        and (folded is None or element.name == folded)
    ]


def find_all_by_id(container: DomContainer, element_id: str) -> list[DomElement]:
    """Return descendant elements whose id attribute equals the given value."""
    return [
        element
        for element in iter_elements(container)
        if attribute_text(element, "id") == element_id
    ]


def class_names(element: DomElement) -> tuple[str, ...]:
    """The class attribute tokens of an element."""
    value = element.attributes.get("class")
    if isinstance(value, tuple):
        return value
    if isinstance(value, str):
        return tuple(value.split())
    return ()


def text_content(container: DomContainer) -> str:
    """The descendant text joined with spaces after stripping each text node."""
    parts: list[str] = []
    for node in iter_nodes(container):
        if not isinstance(node, DomText):
            continue
        text = node.text.strip()
        if text:
            parts.append(text)
    return " ".join(parts)


def _tag_text(tag: DomElement) -> str:
    """The visible text of an element with the whitespace collapsed."""
    return normalize_whitespace(text_content(tag))


def meta_content(document: DomContainer, key: str) -> str | None:
    """The content of the meta tag that carries the given key."""
    folded_key = key.casefold()
    for element in find_all(document, "meta"):
        for attribute in ("name", "property"):
            candidate = attribute_text(element, attribute)
            if candidate is not None and candidate.casefold() == folded_key:
                content = attribute_text(element, "content")
                if content is not None:
                    normalized = normalize_whitespace(content)
                    if normalized:
                        return normalized
    return None


def h1_text(document: DomContainer) -> str | None:
    """The text of the first heading of a page."""
    element = find(document, "h1")
    if element is None:
        return None
    text = _tag_text(element)
    return text or None


def html_title(document: DomContainer) -> str | None:
    """The text of the title element of a page."""
    element = find(document, "title")
    if element is None:
        return None
    text = _tag_text(element)
    return text or None


def require_single_tag_by_id(
    document: DomContainer,
    element_id: str,
    *,
    what: str,
) -> DomElement:
    matches = find_all_by_id(document, element_id)
    if not matches:
        raise PageValidationError(f"{what} is missing: #{element_id}")
    if len(matches) > 1:
        raise PageValidationError(f"{what} is duplicated: #{element_id}")
    return matches[0]


def has_content_beyond_h1(block: DomElement) -> bool:
    heading = find(block, "h1")
    if heading is None:
        return False
    heading_text = normalize_whitespace(text_content(heading))
    total_text = normalize_whitespace(text_content(block))
    if total_text and total_text != heading_text:
        return True
    for name in ("p", "table", "pre", "ul", "ol", "blockquote", "img", "hr", "figure"):
        for candidate in find_all(block, name):
            if candidate is heading or is_descendant(candidate, heading):
                continue
            return True
    return False


def is_descendant(node: DomNode, ancestor: DomElement) -> bool:
    current = node.parent
    while isinstance(current, DomElement):
        if current is ancestor:
            return True
        current = current.parent
    return False


def is_comment(node: object) -> TypeGuard[DomComment]:
    return isinstance(node, DomComment)


def tag_names(node: DomElement) -> str:
    return node.name.casefold()


def attribute_text(element: DomElement, name: str) -> str | None:
    value = element.attributes.get(name)
    if isinstance(value, str):
        return value
    return None


def has_attribute(element: DomElement, name: str) -> bool:
    return name in element.attributes


def anchor_names(tag: DomElement) -> list[str]:
    names: list[str] = []
    identifier = attribute_text(tag, "id")
    if identifier:
        names.append(identifier)
    if tag_names(tag) == "a":
        name = attribute_text(tag, "name")
        if name:
            names.append(name)
    return names


def _direct_child_elements(tag: DomElement) -> list[DomElement]:
    return [child for child in tag.children if isinstance(child, DomElement)]


def normalize_list_items(tag: DomElement) -> None:
    """Flatten list items that html.parser nested instead of closing."""
    for child in _direct_child_elements(tag):
        if tag_names(child) == "li":
            _flatten_nested_list_items(child)


def _flatten_nested_list_items(item: DomElement) -> DomElement:
    cursor = item
    for child in list(item.children):
        if isinstance(child, DomElement) and tag_names(child) == "li":
            _detach(child)
            _insert_after(cursor, child)
            cursor = _flatten_nested_list_items(child)
    return cursor


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
        raise PageValidationError("cannot insert a node without a parent")
    if node.parent is not None:
        _detach(node)
    for index, child in enumerate(parent.children):
        if child is reference:
            node.parent = parent
            parent.children.insert(index + 1, node)
            return
    raise PageValidationError("cannot find the insertion reference")
