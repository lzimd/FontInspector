"""Deterministic local names for mirrored images."""

from __future__ import annotations

import re
from collections import defaultdict
from urllib.parse import unquote, urlsplit

from ..errors import FetchError
from ..storage import sha256_bytes


def assign_image_names(urls: tuple[str, ...]) -> dict[str, str]:
    ordered = list(urls)
    base = {url: _image_base_name(url) for url in ordered}
    names = dict(base)
    suffix_length = 8
    while True:
        groups: dict[str, list[str]] = defaultdict(list)
        for url in ordered:
            groups[names[url]].append(url)
        colliding = {
            url for group in groups.values() if len(group) > 1 for url in group
        }
        if not colliding:
            return names
        if suffix_length > 64:
            raise FetchError("could not assign unique local image names")
        for url in colliding:
            names[url] = _with_suffix(
                base[url],
                sha256_bytes(url.encode("utf-8"))[:suffix_length],
            )
        suffix_length += 8


def _image_base_name(url: str) -> str:
    basename = unquote(urlsplit(url).path.rsplit("/", 1)[-1])
    name = re.sub(r"[^A-Za-z0-9._-]", "_", basename)
    if name in {"", ".", ".."}:
        return "image"
    return name


def _with_suffix(name: str, suffix: str) -> str:
    dot = name.rfind(".")
    if dot > 0:
        return f"{name[:dot]}-{suffix}{name[dot:]}"
    return f"{name}-{suffix}"
