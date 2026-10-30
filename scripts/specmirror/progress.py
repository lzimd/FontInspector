"""Progress callbacks shared by the fetch and build stages."""

from __future__ import annotations

from collections.abc import Callable

Log = Callable[[str], None]


def noop_log(_message: str) -> None:
    """Discard a progress message."""
