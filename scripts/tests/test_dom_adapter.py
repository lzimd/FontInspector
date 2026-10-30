"""Parser-independent DOM adapter contract tests."""

from __future__ import annotations

from specmirror.dom import (
    DomComment,
    DomElement,
    DomText,
    attribute_text,
    class_names,
    find,
    find_all,
    find_all_by_id,
    find_all_with_attribute,
    find_all_with_class,
    has_attribute,
    is_descendant,
    iter_comments,
    next_sibling,
    normalize_list_items,
    parse_html,
    text_content,
)


def test_parse_html_builds_parented_nodes() -> None:
    document = parse_html(
        "<div id='root'>before<span class='x y'>inside</span><!--note-->after</div>"
    )
    root = find_all_by_id(document, "root")[0]
    assert isinstance(root, DomElement)
    assert root.parent is not None
    assert all(child.parent is root for child in root.children)
    assert [type(child) for child in root.children] == [
        DomText,
        DomElement,
        DomComment,
        DomText,
    ]
    span = root.children[1]
    assert isinstance(span, DomElement)
    assert span.name == "span"
    assert class_names(span) == ("x", "y")


def test_text_content_matches_get_text_semantics() -> None:
    document = parse_html("<div>a<!--hidden--> b<span> c </span><br>d</div>")
    div = find(document, "div")
    assert div is not None
    assert text_content(div) == "a b c d"
    assert "hidden" not in text_content(div)

    nbsp = parse_html("<div>a&nbsp;b</div>")
    nbsp_div = find(nbsp, "div")
    assert nbsp_div is not None
    assert text_content(nbsp_div) == "a\u00a0b"


def test_attribute_access_and_presence() -> None:
    document = parse_html("<div id='x' class='a b' data-empty='' hidden></div>")
    element = find(document, "div")
    assert element is not None
    assert attribute_text(element, "id") == "x"
    assert attribute_text(element, "class") is None
    assert class_names(element) == ("a", "b")
    assert has_attribute(element, "data-empty")
    assert has_attribute(element, "hidden")
    assert not has_attribute(element, "missing")


def test_queries_walk_descendants_in_document_order() -> None:
    document = parse_html(
        "<div class='content' id='outer'>"
        "<h1>Title</h1>"
        "<div class='content inner' id='inner'><p>Body</p></div>"
        "<img src='x'>"
        "</div>"
    )
    assert [element.name for element in find_all(document, "div")] == [
        "div",
        "div",
    ]
    assert [
        element.attributes["id"]
        for element in find_all_with_class(document, "div", "content")
    ] == ["outer", "inner"]
    assert find_all_by_id(document, "inner")[0].name == "div"
    assert find_all_with_attribute(document, "src")[0].name == "img"

    outer = find_all_by_id(document, "outer")[0]
    assert find(outer, "h1") is not None
    assert [element.attributes["id"] for element in find_all(outer, "div")] == ["inner"]


def test_comments_keep_stable_identity() -> None:
    document = parse_html("<div><!--a--><!--b--></div>")
    first = list(iter_comments(document))
    second = list(iter_comments(document))
    assert [comment.text for comment in first] == ["a", "b"]
    assert first[0] is second[0]
    assert first[0] is not first[1]


def test_next_sibling_skips_nothing() -> None:
    document = parse_html("<p><dfn>x</dfn><!--c-->word</p>")
    dfn = find(document, "dfn")
    assert dfn is not None
    comment = next_sibling(dfn)
    assert isinstance(comment, DomComment)
    text = next_sibling(comment)
    assert isinstance(text, DomText)
    assert text.text == "word"


def test_normalize_list_items_flattens_nested_items() -> None:
    document = parse_html("<ul><li>a<li>b</ul>")
    ul = find(document, "ul")
    assert ul is not None
    normalize_list_items(ul)
    items = [child for child in ul.children if isinstance(child, DomElement)]
    assert [text_content(item) for item in items] == ["a", "b"]
    assert all(item.parent is ul for item in items)


def test_is_descendant() -> None:
    document = parse_html("<div><p><em>x</em></p></div>")
    div = find(document, "div")
    em = find(document, "em")
    assert div is not None
    assert em is not None
    assert is_descendant(em, div)
    assert not is_descendant(div, em)
