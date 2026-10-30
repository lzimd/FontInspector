"""Text helpers shared by the metadata, and source layers."""

from __future__ import annotations

import html


def normalize_whitespace(value: str) -> str:
    """Collapse every run of whitespace into a single space."""
    return " ".join(value.split())


def normalize_title(value: str) -> str:
    """Collapse the whitespace of a title that an HTML parser already decoded."""
    return normalize_whitespace(value)


def normalize_escaped_title(value: str) -> str:
    """Collapse the whitespace of a title that still carries HTML entities."""
    return normalize_whitespace(html.unescape(value))
