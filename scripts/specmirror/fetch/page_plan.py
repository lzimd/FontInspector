"""Page-plan loading, canonical serialization, and publication."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..errors import FetchError, SchemaError
from ..paths import SourcePaths
from ..schema import PagePlan, parse_json_bytes
from ..storage import atomic_write_bytes, sha256_bytes


@dataclass(frozen=True, slots=True)
class LoadedPagePlan:
    plan: PagePlan
    data: bytes
    file_sha256: str
    path: Path


def load_page_plan(
    path: Path,
    *,
    expected_source: str,
    required: bool,
) -> LoadedPagePlan | None:
    if not path.is_file():
        if required:
            raise FetchError(
                f"page plan is missing: {path}; "
                f"run 'fetch pages' for {expected_source} first"
            )
        return None
    data = path.read_bytes()
    value = parse_json_bytes(data, what=f"page plan {path}")
    plan = PagePlan.from_dict(value, expected_source=expected_source)
    if data != plan.to_bytes():
        raise SchemaError(
            f"page plan is not in canonical form: {path}; "
            f"rerun 'fetch pages' for {expected_source}"
        )
    return LoadedPagePlan(
        plan=plan,
        data=data,
        file_sha256=sha256_bytes(data),
        path=path,
    )


def write_page_plan(paths: SourcePaths, plan: PagePlan) -> LoadedPagePlan:
    data = plan.to_bytes()
    if plan.source != paths.source:
        raise SchemaError("page plan source does not match the target paths")
    atomic_write_bytes(paths.plan_path, data)
    return LoadedPagePlan(
        plan=plan,
        data=data,
        file_sha256=sha256_bytes(data),
        path=paths.plan_path,
    )
