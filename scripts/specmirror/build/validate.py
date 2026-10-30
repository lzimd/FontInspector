"""Output validation over the staged build tree."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..convert.markdown_model import RAW_HTML_COMMENTS, RAW_HTML_ELEMENTS
from ..errors import BuildError
from ..schema import Manifest

_FRONT_MATTER_LINE = re.compile(r'^([A-Za-z0-9._-]+): (?:"(.*)"|null)$')
_TAG_PATTERN = re.compile(r"</?([a-zA-Z][a-zA-Z0-9]*)((?:\s+[^<>]*?)?)/?>")
_COMMENT_PATTERN = re.compile(r"<!--(.*?)-->", re.DOTALL)
_LINK_PATTERN = re.compile(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"(?:\\.|[^"\\])*")?\)')
_CODE_FENCE = re.compile(r"^(`{3,})")
_ESCAPE_MASK = re.compile(r"\\([!-/:-@[-`{-~])")


def _mask_escapes(text: str) -> str:
    """Replace backslash-escaped punctuation so structural scans ignore it.

    CommonMark treats ``\\<`` as a literal ``<``, so the raw file text of an
    escaped character must not look like markup to the validator.
    """
    return _ESCAPE_MASK.sub("\x00", text)


def _new_failures() -> list[str]:
    return []


@dataclass(slots=True)
class ValidationSummary:
    checks: int = 0
    failures: list[str] = field(default_factory=_new_failures)

    def check(self, condition: object, message: str) -> bool:
        self.checks += 1
        if condition:
            return True
        self.failures.append(message)
        return False


def validate_output(
    files: dict[str, bytes],
    manifest: Manifest,
    summary: ValidationSummary,
) -> None:
    """Validate the complete staged output; collect failures."""
    _validate_layout(files, manifest, summary)
    _validate_readme(files, manifest, summary)
    for slug in (page.slug for page in manifest.pages):
        name = f"{slug}.md"
        if name not in files:
            continue
        _validate_page(files[name], slug, files, summary)


def _validate_layout(
    files: dict[str, bytes], manifest: Manifest, summary: ValidationSummary
) -> None:
    summary.check("README.md" in files, "README.md is missing")
    summary.check("index.md" in files, "index.md is missing")
    expected = {"README.md", *(f"{page.slug}.md" for page in manifest.pages)}
    expected |= {image.file for image in manifest.images}
    actual = set(files)
    unexpected = sorted(actual - expected)
    summary.check(not unexpected, f"unexpected files in output: {unexpected}")
    for name, data in files.items():
        if not name.endswith(".md"):
            continue
        text = data.decode("utf-8", errors="replace")
        summary.check("\r" not in text, f"{name} contains CR characters")
        summary.check(
            data.endswith(b"\n") or not data,
            f"{name} does not end with a newline",
        )


def _validate_readme(
    files: dict[str, bytes], manifest: Manifest, summary: ValidationSummary
) -> None:
    data = files.get("README.md")
    if data is None:
        return
    text = data.decode("utf-8")
    summary.check(not text.startswith("---"), "README.md must not carry front matter")
    summary.check(
        "## Regeneration" in text and "## Pages" in text,
        "README.md is missing required sections",
    )
    pages_section = text.split("## Pages", 1)
    if len(pages_section) != 2:
        summary.check(False, "README.md has no Pages section")
        return
    links = [
        match.group(1)
        for match in _LINK_PATTERN.finditer(pages_section[1])
        if match.group(1).endswith(".md")
    ]
    expected = [f"{page.slug}.md" for page in manifest.pages]
    summary.check(
        sorted(links) == sorted(expected),
        f"README.md page list does not cover every page exactly once: {links}",
    )
    summary.check(
        [link for link in links if link in set(expected)] == expected,
        "README.md page list does not follow manifest order",
    )


def _validate_page(
    data: bytes,
    slug: str,
    files: dict[str, bytes],
    summary: ValidationSummary,
) -> None:
    text = data.decode("utf-8")
    front = _parse_front_matter(text)
    summary.check(front is not None, f"{slug}.md has no front matter")
    if front is None:
        return
    title = front.get("title")
    summary.check(bool(title), f"{slug}.md front matter has no non-empty title")
    body = text.split("---", 2)[2] if text.startswith("---") else text
    _validate_raw_html(body, slug, summary)
    _validate_links(body, slug, files, summary)
    _validate_tables(body, slug, summary)


def _parse_front_matter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None
    result: dict[str, str] = {}
    for line in parts[0][4:].split("\n"):
        match = _FRONT_MATTER_LINE.fullmatch(line)
        if match is None:
            return None
        result[match.group(1)] = match.group(2) or ""
    return result


def _strip_code(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.split("\n"):
        match = _CODE_FENCE.match(line)
        if match is not None:
            if not in_fence:
                in_fence = True
                fence_marker = match.group(1)
                continue
            if len(match.group(1)) >= len(fence_marker):
                in_fence = False
                fence_marker = ""
                continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def _validate_raw_html(body: str, slug: str, summary: ValidationSummary) -> None:
    stripped = _mask_escapes(_strip_inline_code(_strip_code(body)))
    for match in _COMMENT_PATTERN.finditer(stripped):
        normalized = f"<!-- {match.group(1).strip()} -->"
        summary.check(
            normalized in RAW_HTML_COMMENTS,
            f"{slug}.md contains a disallowed HTML comment: {normalized!r}",
        )
    without_comments = _COMMENT_PATTERN.sub("", stripped)
    for match in _TAG_PATTERN.finditer(without_comments):
        if match.group(0).startswith("</"):
            continue
        name = match.group(1).casefold()
        element = RAW_HTML_ELEMENTS.get(name)
        if element is None:
            summary.check(
                False, f"{slug}.md contains a disallowed HTML tag: <{match.group(1)}>"
            )
            continue
        raw_tag = match.group(0)
        attributes = re.findall(r"([a-zA-Z-]+)\s*=", match.group(2) or "")
        unexpected = sorted(set(attributes) - set(element.attributes))
        summary.check(
            not unexpected,
            f"{slug}.md has <{name}> with disallowed attributes: {unexpected}",
        )
        if name == "a":
            summary.check(
                "id" in attributes,
                f"{slug}.md has <a> without an id: {raw_tag!r}",
            )


def _strip_inline_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", text)


def _validate_links(
    body: str, slug: str, files: dict[str, bytes], summary: ValidationSummary
) -> None:
    stripped = _mask_escapes(_strip_inline_code(_strip_code(body)))
    for match in _LINK_PATTERN.finditer(stripped):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        page = target.split("#", 1)[0]
        if page.startswith("images/"):
            summary.check(
                page in files, f"{slug}.md links to a missing image: {target}"
            )
            continue
        summary.check(page in files, f"{slug}.md links to a missing page: {target}")


def _validate_tables(body: str, slug: str, summary: ValidationSummary) -> None:
    lines = _strip_code(body).split("\n")
    in_table = False
    columns = 0
    for line in lines:
        masked = _mask_escapes(line)
        is_row = masked.strip().startswith("|") and masked.strip().endswith("|")
        if not is_row:
            if in_table:
                in_table = False
            continue
        count = masked.count("|") - 1
        if not in_table:
            in_table = True
            columns = count
            continue
        summary.check(
            count == columns,
            f"{slug}.md has a table row with {count} columns, expected {columns}",
        )


def require_no_failures(summary: ValidationSummary, *, what: str) -> None:
    if summary.failures:
        details = "\n".join(f"  - {failure}" for failure in summary.failures)
        raise BuildError(
            f"{what} failed {len(summary.failures)} validation check(s):\n{details}"
        )
