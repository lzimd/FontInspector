"""Generation of the mirror README.md."""

from __future__ import annotations

from dataclasses import dataclass

from ..schema import Manifest, PageEntry
from ..sources.base import SourceAdapter


@dataclass(frozen=True, slots=True)
class ReadmeInput:
    manifest: Manifest
    adapter: SourceAdapter


def render_readme(input: ReadmeInput) -> str:
    manifest = input.manifest
    adapter = input.adapter
    landing = manifest.pages[0].requested_url
    lines: list[str] = []
    lines.append(f"# {adapter.display_name}")
    lines.append("")
    lines.append(
        f"This directory is a generated mirror of {adapter.readme_publication}. "
        f"The mirror covers {adapter.readme_scope}"
    )
    lines.append("")
    lines.append(f"Upstream landing page: [{landing}]({landing}).")
    lines.append("")
    lines.append("## Regeneration")
    lines.append("")
    lines.append("Run the following commands from the repository root:")
    lines.append("")
    lines.append("```sh")
    lines.append(f"uv run -m specmirror {adapter.key} fetch")
    lines.append(f"uv run -m specmirror {adapter.key} build")
    lines.append("```")
    lines.append("")
    lines.append(
        "The build replaces generated files in this directory. "
        "Don't edit them by hand. Corrections belong in the versioned "
        "correction data under "
        f"`scripts/specmirror/corrections/data/{manifest.source}/`."
    )
    lines.append("")
    lines.append("## Pages")
    lines.append("")
    if adapter.readme_nested_sections:
        lines.extend(_nested_page_list(manifest))
    else:
        lines.extend(_flat_page_list(manifest))
    return "\n".join(lines).rstrip("\n") + "\n"


def _flat_page_list(manifest: Manifest) -> list[str]:
    return [f"- [{page.title}]({page.slug}.md)" for page in manifest.pages]


def _nested_page_list(manifest: Manifest) -> list[str]:
    pages_by_label: dict[tuple[str, ...], PageEntry] = {}
    for page in manifest.pages:
        pages_by_label[(*page.section, page.title)] = page
    lines: list[str] = []
    emitted_slugs: set[str] = set()
    emitted_labels: set[tuple[str, ...]] = set()
    for page in manifest.pages:
        section = page.section
        for depth in range(len(section)):
            path = section[: depth + 1]
            if path in emitted_labels:
                continue
            label = path[-1]
            label_page = pages_by_label.get(path)
            known = isinstance(label_page, PageEntry)
            if known and label_page.slug not in emitted_slugs:
                lines.append(
                    f"{'  ' * depth}- [{label_page.title}]({label_page.slug}.md)"
                )
                emitted_slugs.add(label_page.slug)
            elif label_page is None:
                lines.append(f"{'  ' * depth}- {label}")
            emitted_labels.add(path)
        if page.slug not in emitted_slugs:
            lines.append(f"{'  ' * len(section)}- [{page.title}]({page.slug}.md)")
            emitted_slugs.add(page.slug)
    return lines
