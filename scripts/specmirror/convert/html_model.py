"""HTML facts and the conversion intent for the accepted element subset.

Each registry entry records the element's HTML5 content categories and content
model, following the WHATWG HTML standard index, together with the conversion
intent that the page builder applies. Categories describe the source language;
the conversion intent names the Markdown-side construct. The registry therefore
separates facts about HTML from decisions about Markdown.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ..errors import BuildError


class Strategy(StrEnum):
    """How the page builder treats an element."""

    BLOCK = "block"  # produces one or more AST blocks
    INLINE = "inline"  # produces AST inlines
    TRANSPARENT = "transparent"  # no node; children stay in the current context
    CONTEXT_ONLY = "context-only"  # valid only inside a required parent
    NARROWED = "narrowed"  # produces a node; children use a dedicated mode


class ChildMode(StrEnum):
    """How the page builder converts an element's children."""

    BLOCKS = "blocks"  # children become blocks
    INLINES = "inlines"  # children become inlines
    MIXED = "mixed"  # children keep their own block or inline nature
    LITERAL = "literal"  # verbatim text; skip nested markup
    DIGITS_OR_RAW = "digits-or-raw"  # digit-only Unicode, otherwise RawHtml
    NONE = "none"  # element has no children
    STRUCTURE = "structure"  # parent handler consumes structural children


class Category(StrEnum):
    """WHATWG HTML content categories that the accepted subset uses."""

    FLOW = "flow"
    SECTIONING = "sectioning"
    HEADING = "heading"
    PHRASING = "phrasing"
    EMBEDDED = "embedded"
    FORM_ASSOCIATED = "form-associated"
    INTERACTIVE = "interactive"
    PALPABLE = "palpable"


class ContentModel(StrEnum):
    """The WHATWG content model of an element's children."""

    EMPTY = "empty"
    PHRASING = "phrasing"
    FLOW = "flow"
    TRANSPARENT = "transparent"
    LIST_ITEM_SEQUENCE = "li elements"
    DEFINITION_SEQUENCE = "dt and dd elements"
    TABLE = "caption, table sections, and rows"
    TABLE_ROW_SEQUENCE = "tr elements"
    TABLE_CELL_SEQUENCE = "td and th elements"
    FIGURE = "figcaption and flow content"


class BlockIntent(StrEnum):
    """The block or structural role an element fills.

    Some members describe roles that have no standalone AST `Block`: list
    items, table parts, definition items, and figure captions. Their parent
    handlers consume them while building the enclosing block.
    """

    BLOCK_QUOTE = "block-quote"  # AST BlockQuote
    LIST = "list"  # AST List
    LIST_ITEM = "list-item"  # role only; becomes List.items
    THEMATIC_BREAK = "thematic-break"  # AST ThematicBreak
    HEADING = "heading"  # AST Heading
    CODE_BLOCK = "code-block"  # AST CodeBlock
    PARAGRAPH = "paragraph"  # AST Paragraph
    TABLE = "table"  # AST Table
    TABLE_SECTION = "table-section"  # role only; contributes rows to Table
    TABLE_ROW = "table-row"  # role only; becomes Row
    TABLE_CELL = "table-cell"  # role only; becomes Cell
    TABLE_CAPTION = "table-caption"  # role only; becomes Table.caption
    DEFINITION_LIST = "definition-list"  # lowers to term/definition blocks
    DEFINITION_TERM = "definition-term"  # role only; lowers to a term paragraph
    DEFINITION_DESCRIPTION = "definition-description"  # role only; contributes blocks
    FIGURE = "figure"  # lowers to one image/caption paragraph
    FIGURE_CAPTION = "figure-caption"  # role only; becomes caption inlines


class InlineIntent(StrEnum):
    """The inline construct or inline role an element fills.

    Some members produce no node or choose between nodes based on content.
    """

    WRAPPER = "wrapper"  # no node; children stay inline
    EMPHASIS = "emphasis"  # AST Emphasis
    STRONG = "strong"  # AST Strong
    STRIKETHROUGH = "strikethrough"  # AST Strikethrough
    CODE = "code"  # AST Code; literal text
    LINK = "link"  # Link with href, otherwise inline children
    IMAGE = "image"  # AST Image
    LINE_BREAK = "line-break"  # AST LineBreak, rendered <br>
    SUPERSCRIPT = "superscript"  # Unicode digits or RawHtml sup
    SUBSCRIPT = "subscript"  # Unicode digits or RawHtml sub
    UNDERLINE = "underline"  # no construct; text kept, style discarded


@dataclass(frozen=True, slots=True)
class ElementSpec:
    """One accepted element with its HTML facts and conversion intent."""

    name: str
    categories: frozenset[Category]
    content_model: ContentModel
    strategy: Strategy
    child_mode: ChildMode
    block: BlockIntent | None = None
    inline: InlineIntent | None = None
    required_parents: frozenset[str] = frozenset()
    aliases: tuple[str, ...] = ()


_FLOW = frozenset({Category.FLOW})
_FLOW_PALPABLE = frozenset({Category.FLOW, Category.PALPABLE})
_FLOW_PHRASING = frozenset({Category.FLOW, Category.PHRASING})
_FLOW_PHRASING_PALPABLE = frozenset(
    {Category.FLOW, Category.PHRASING, Category.PALPABLE}
)
_PHRASING = frozenset({Category.PHRASING})
_IMG_CATEGORIES = frozenset(
    {
        Category.FLOW,
        Category.PHRASING,
        Category.EMBEDDED,
        Category.FORM_ASSOCIATED,
        Category.INTERACTIVE,
        Category.PALPABLE,
    }
)


_SPECS: tuple[ElementSpec, ...] = (
    # Transparent sectioning and grouping wrappers.
    ElementSpec(
        "div",
        _FLOW_PALPABLE,
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "section",
        frozenset({Category.FLOW, Category.SECTIONING, Category.PALPABLE}),
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "article",
        frozenset({Category.FLOW, Category.SECTIONING, Category.PALPABLE}),
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "main",
        _FLOW_PALPABLE,
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "header",
        _FLOW_PALPABLE,
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "footer",
        _FLOW_PALPABLE,
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "aside",
        frozenset({Category.FLOW, Category.SECTIONING, Category.PALPABLE}),
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "center",  # legacy; inferred block categories
        _FLOW,
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "address",
        _FLOW_PALPABLE,
        ContentModel.FLOW,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "ins",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.TRANSPARENT,
        Strategy.TRANSPARENT,
        ChildMode.MIXED,
    ),
    ElementSpec(
        "span",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.TRANSPARENT,
        ChildMode.INLINES,
        inline=InlineIntent.WRAPPER,
    ),
    ElementSpec(
        "font",
        _PHRASING,  # obsolete; inferred inline categories
        ContentModel.PHRASING,
        Strategy.TRANSPARENT,
        ChildMode.INLINES,
        inline=InlineIntent.WRAPPER,
    ),
    ElementSpec(
        "def",  # nonstandard Apple tag; inferred inline categories
        _PHRASING,
        ContentModel.PHRASING,
        Strategy.TRANSPARENT,
        ChildMode.INLINES,
        inline=InlineIntent.WRAPPER,
    ),
    ElementSpec(
        "abbr",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.TRANSPARENT,
        ChildMode.INLINES,
        inline=InlineIntent.WRAPPER,
    ),
    ElementSpec(
        "small",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.TRANSPARENT,
        ChildMode.INLINES,
        inline=InlineIntent.WRAPPER,
    ),
    ElementSpec(
        "mark",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.TRANSPARENT,
        ChildMode.INLINES,
        inline=InlineIntent.WRAPPER,
    ),
    ElementSpec(
        "wbr",
        _FLOW_PHRASING,
        ContentModel.EMPTY,
        Strategy.TRANSPARENT,
        ChildMode.NONE,
        inline=InlineIntent.WRAPPER,
    ),
    # Headings and paragraphs.
    ElementSpec(
        "h1",
        frozenset({Category.FLOW, Category.HEADING, Category.PALPABLE}),
        ContentModel.PHRASING,
        Strategy.BLOCK,
        ChildMode.INLINES,
        block=BlockIntent.HEADING,
    ),
    ElementSpec(
        "h2",
        frozenset({Category.FLOW, Category.HEADING, Category.PALPABLE}),
        ContentModel.PHRASING,
        Strategy.BLOCK,
        ChildMode.INLINES,
        block=BlockIntent.HEADING,
    ),
    ElementSpec(
        "h3",
        frozenset({Category.FLOW, Category.HEADING, Category.PALPABLE}),
        ContentModel.PHRASING,
        Strategy.BLOCK,
        ChildMode.INLINES,
        block=BlockIntent.HEADING,
    ),
    ElementSpec(
        "h4",
        frozenset({Category.FLOW, Category.HEADING, Category.PALPABLE}),
        ContentModel.PHRASING,
        Strategy.BLOCK,
        ChildMode.INLINES,
        block=BlockIntent.HEADING,
    ),
    ElementSpec(
        "h5",
        frozenset({Category.FLOW, Category.HEADING, Category.PALPABLE}),
        ContentModel.PHRASING,
        Strategy.BLOCK,
        ChildMode.INLINES,
        block=BlockIntent.HEADING,
    ),
    ElementSpec(
        "h6",
        frozenset({Category.FLOW, Category.HEADING, Category.PALPABLE}),
        ContentModel.PHRASING,
        Strategy.BLOCK,
        ChildMode.INLINES,
        block=BlockIntent.HEADING,
    ),
    ElementSpec(
        "p",
        _FLOW_PALPABLE,
        ContentModel.PHRASING,
        Strategy.BLOCK,
        ChildMode.INLINES,
        block=BlockIntent.PARAGRAPH,
    ),
    ElementSpec(
        "blockquote",
        _FLOW_PALPABLE,
        ContentModel.FLOW,
        Strategy.BLOCK,
        ChildMode.BLOCKS,
        block=BlockIntent.BLOCK_QUOTE,
    ),
    ElementSpec(
        "pre",
        _FLOW_PALPABLE,
        ContentModel.PHRASING,
        Strategy.NARROWED,
        ChildMode.LITERAL,
        block=BlockIntent.CODE_BLOCK,
    ),
    ElementSpec(
        "hr",
        _FLOW,
        ContentModel.EMPTY,
        Strategy.BLOCK,
        ChildMode.NONE,
        block=BlockIntent.THEMATIC_BREAK,
    ),
    # Lists.
    ElementSpec(
        "ul",
        _FLOW_PALPABLE,
        ContentModel.LIST_ITEM_SEQUENCE,
        Strategy.BLOCK,
        ChildMode.BLOCKS,
        block=BlockIntent.LIST,
    ),
    ElementSpec(
        "ol",
        _FLOW_PALPABLE,
        ContentModel.LIST_ITEM_SEQUENCE,
        Strategy.BLOCK,
        ChildMode.BLOCKS,
        block=BlockIntent.LIST,
    ),
    ElementSpec(
        "li",
        frozenset(),
        ContentModel.FLOW,
        Strategy.CONTEXT_ONLY,
        ChildMode.BLOCKS,
        block=BlockIntent.LIST_ITEM,
        required_parents=frozenset({"ul", "ol"}),
    ),
    # Definition lists.
    ElementSpec(
        "dl",
        _FLOW_PALPABLE,
        ContentModel.DEFINITION_SEQUENCE,
        Strategy.BLOCK,
        ChildMode.BLOCKS,
        block=BlockIntent.DEFINITION_LIST,
    ),
    ElementSpec(
        "dt",
        frozenset(),
        ContentModel.PHRASING,
        Strategy.CONTEXT_ONLY,
        ChildMode.INLINES,
        block=BlockIntent.DEFINITION_TERM,
        required_parents=frozenset({"dl"}),
    ),
    ElementSpec(
        "dd",
        frozenset(),
        ContentModel.FLOW,
        Strategy.CONTEXT_ONLY,
        ChildMode.BLOCKS,
        block=BlockIntent.DEFINITION_DESCRIPTION,
        required_parents=frozenset({"dl"}),
    ),
    # Tables.
    ElementSpec(
        "table",
        _FLOW_PALPABLE,
        ContentModel.TABLE,
        Strategy.BLOCK,
        ChildMode.STRUCTURE,
        block=BlockIntent.TABLE,
    ),
    ElementSpec(
        "caption",
        frozenset(),
        ContentModel.PHRASING,
        Strategy.CONTEXT_ONLY,
        ChildMode.INLINES,
        block=BlockIntent.TABLE_CAPTION,
        required_parents=frozenset({"table"}),
    ),
    ElementSpec(
        "thead",
        frozenset(),
        ContentModel.TABLE_ROW_SEQUENCE,
        Strategy.CONTEXT_ONLY,
        ChildMode.STRUCTURE,
        block=BlockIntent.TABLE_SECTION,
        required_parents=frozenset({"table"}),
    ),
    ElementSpec(
        "tbody",
        frozenset(),
        ContentModel.TABLE_ROW_SEQUENCE,
        Strategy.CONTEXT_ONLY,
        ChildMode.STRUCTURE,
        block=BlockIntent.TABLE_SECTION,
        required_parents=frozenset({"table"}),
    ),
    ElementSpec(
        "tfoot",
        frozenset(),
        ContentModel.TABLE_ROW_SEQUENCE,
        Strategy.CONTEXT_ONLY,
        ChildMode.STRUCTURE,
        block=BlockIntent.TABLE_SECTION,
        required_parents=frozenset({"table"}),
    ),
    ElementSpec(
        "tr",
        frozenset(),
        ContentModel.TABLE_CELL_SEQUENCE,
        Strategy.CONTEXT_ONLY,
        ChildMode.STRUCTURE,
        block=BlockIntent.TABLE_ROW,
        required_parents=frozenset({"table", "thead", "tbody", "tfoot"}),
    ),
    ElementSpec(
        "td",
        frozenset(),
        ContentModel.FLOW,
        Strategy.CONTEXT_ONLY,
        ChildMode.BLOCKS,
        block=BlockIntent.TABLE_CELL,
        required_parents=frozenset({"tr"}),
    ),
    ElementSpec(
        "th",
        frozenset({Category.INTERACTIVE}),
        ContentModel.FLOW,
        Strategy.CONTEXT_ONLY,
        ChildMode.BLOCKS,
        block=BlockIntent.TABLE_CELL,
        required_parents=frozenset({"tr"}),
    ),
    # Figures.
    ElementSpec(
        "figure",
        _FLOW_PALPABLE,
        ContentModel.FIGURE,
        Strategy.BLOCK,
        ChildMode.STRUCTURE,
        block=BlockIntent.FIGURE,
    ),
    ElementSpec(
        "figcaption",
        frozenset(),
        ContentModel.PHRASING,
        Strategy.CONTEXT_ONLY,
        ChildMode.INLINES,
        block=BlockIntent.FIGURE_CAPTION,
        required_parents=frozenset({"figure"}),
    ),
    # Emphasis and phrase semantics.
    ElementSpec(
        "em",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.INLINE,
        ChildMode.INLINES,
        inline=InlineIntent.EMPHASIS,
        aliases=("i",),
    ),
    ElementSpec(
        "strong",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.INLINE,
        ChildMode.INLINES,
        inline=InlineIntent.STRONG,
        aliases=("b",),
    ),
    ElementSpec(
        "dfn",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.INLINE,
        ChildMode.INLINES,
        inline=InlineIntent.EMPHASIS,
    ),
    ElementSpec(
        "var",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.INLINE,
        ChildMode.INLINES,
        inline=InlineIntent.EMPHASIS,
    ),
    ElementSpec(
        "cite",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.INLINE,
        ChildMode.INLINES,
        inline=InlineIntent.EMPHASIS,
    ),
    ElementSpec(
        "q",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.INLINE,
        ChildMode.INLINES,
        inline=InlineIntent.EMPHASIS,
    ),
    ElementSpec(
        "del",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.INLINE,
        ChildMode.INLINES,
        inline=InlineIntent.STRIKETHROUGH,
        aliases=("s",),
    ),
    # Code, links, and media.
    ElementSpec(
        "code",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.NARROWED,
        ChildMode.LITERAL,
        inline=InlineIntent.CODE,
        aliases=("tt",),
    ),
    ElementSpec(
        "kbd",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.NARROWED,
        ChildMode.LITERAL,
        inline=InlineIntent.CODE,
    ),
    ElementSpec(
        "samp",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.NARROWED,
        ChildMode.LITERAL,
        inline=InlineIntent.CODE,
    ),
    ElementSpec(
        "a",
        frozenset(
            {
                Category.FLOW,
                Category.PHRASING,
                Category.INTERACTIVE,
                Category.PALPABLE,
            }
        ),
        ContentModel.TRANSPARENT,
        Strategy.NARROWED,
        ChildMode.INLINES,
        inline=InlineIntent.LINK,
    ),
    ElementSpec(
        "img",
        _IMG_CATEGORIES,
        ContentModel.EMPTY,
        Strategy.INLINE,
        ChildMode.NONE,
        inline=InlineIntent.IMAGE,
    ),
    ElementSpec(
        "br",
        _FLOW_PHRASING,
        ContentModel.EMPTY,
        Strategy.INLINE,
        ChildMode.NONE,
        inline=InlineIntent.LINE_BREAK,
    ),
    ElementSpec(
        "sup",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.NARROWED,
        ChildMode.DIGITS_OR_RAW,
        inline=InlineIntent.SUPERSCRIPT,
    ),
    ElementSpec(
        "sub",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.NARROWED,
        ChildMode.DIGITS_OR_RAW,
        inline=InlineIntent.SUBSCRIPT,
    ),
    ElementSpec(
        "u",
        _FLOW_PHRASING_PALPABLE,
        ContentModel.PHRASING,
        Strategy.INLINE,
        ChildMode.INLINES,
        inline=InlineIntent.UNDERLINE,
    ),
)

REGISTRY: dict[str, ElementSpec] = {spec.name: spec for spec in _SPECS}

_ALIASES: dict[str, str] = {
    alias: spec.name for spec in _SPECS for alias in spec.aliases
}


def resolve_element(name: str) -> ElementSpec:
    """The registry entry for a tag name, resolving legacy aliases."""
    folded = name.casefold()
    canonical = _ALIASES.get(folded, folded)
    spec = REGISTRY.get(canonical)
    if spec is None:
        raise BuildError(f"unknown element in content: <{name}>")
    return spec


def is_known_element(name: str) -> bool:
    folded = name.casefold()
    return folded in REGISTRY or folded in _ALIASES


def is_heading(spec: ElementSpec) -> bool:
    return spec.block is BlockIntent.HEADING


def is_transparent(spec: ElementSpec) -> bool:
    return spec.strategy is Strategy.TRANSPARENT


def is_block_scope(spec: ElementSpec) -> bool:
    """Whether an element starts a new text scope for whitespace policy."""
    if spec.name == "pre":
        return True
    if spec.strategy in {Strategy.BLOCK, Strategy.CONTEXT_ONLY}:
        return True
    return (
        spec.strategy is Strategy.TRANSPARENT
        and Category.FLOW in spec.categories
        and Category.PHRASING not in spec.categories
    )


def accepts_parent(spec: ElementSpec, parent_name: str | None) -> bool:
    """Whether the element's required parent context allows it."""
    if not spec.required_parents:
        return True
    return parent_name is not None and parent_name in spec.required_parents


__all__ = [
    "REGISTRY",
    "BlockIntent",
    "Category",
    "ChildMode",
    "ContentModel",
    "ElementSpec",
    "InlineIntent",
    "Strategy",
    "accepts_parent",
    "is_block_scope",
    "is_heading",
    "is_known_element",
    "is_transparent",
    "resolve_element",
]
