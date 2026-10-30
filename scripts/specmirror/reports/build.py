"""The deterministic build report artifact."""

from __future__ import annotations

from ..paths import SourcePaths
from ..progress import Log, noop_log
from ..storage import atomic_write_bytes, pretty_json_bytes


def write_build_report(
    paths: SourcePaths,
    report: dict[str, object],
    *,
    dry_run: bool,
    log: Log = noop_log,
) -> None:
    if dry_run:
        return
    data = pretty_json_bytes(report)
    atomic_write_bytes(paths.build_report_path, data)
    log(f"wrote build report {paths.build_report_path}")
