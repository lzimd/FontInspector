"""Source adapter registry."""

from __future__ import annotations

from collections.abc import Callable

from ..errors import UsageError
from ..schema import SOURCE_KEYS
from .base import SourceAdapter
from .opentype import OpenTypeSource
from .truetype import TrueTypeSource

__all__ = [
    "SourceAdapter",
    "get_source",
    "source_keys",
]

_ADAPTERS: dict[str, Callable[[], SourceAdapter]] = {
    "opentype": OpenTypeSource,
    "truetype": TrueTypeSource,
}


def _build_registry() -> dict[str, SourceAdapter]:
    """Instantiate one adapter for every source the schema accepts."""
    missing = sorted(set(SOURCE_KEYS) - set(_ADAPTERS))
    unknown = sorted(set(_ADAPTERS) - set(SOURCE_KEYS))
    if missing or unknown:
        raise RuntimeError(
            "the source adapters and the schema source keys disagree: "
            f"missing {missing}, unknown {unknown}"
        )
    return {key: _ADAPTERS[key]() for key in SOURCE_KEYS}


_SOURCES: dict[str, SourceAdapter] = _build_registry()


def get_source(key: str) -> SourceAdapter:
    try:
        return _SOURCES[key]
    except KeyError as error:
        raise UsageError(f"unknown source: {key}") from error


def source_keys() -> tuple[str, ...]:
    return tuple(_SOURCES)
