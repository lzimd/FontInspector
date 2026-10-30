"""Command-line interface."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .build import run_build
from .errors import SpecMirrorError, UsageError
from .fetch import FetchOutcome, run_fetch
from .fetch.http import UrllibHttpClient
from .paths import SourcePaths, repository_root
from .sources import source_keys
from .storage import pretty_json_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="specmirror",
        description="Build deterministic Markdown mirrors of font specifications.",
    )
    parser.add_argument(
        "source",
        choices=source_keys(),
        help="documentation source to mirror",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    fetch = commands.add_parser("fetch", help="fetch a source snapshot")
    fetch.add_argument(
        "stage",
        nargs="?",
        choices=("pages", "images", "all"),
        default="all",
        help="fetch stage to run; defaults to all",
    )
    fetch.add_argument(
        "--dry-run",
        action="store_true",
        help="validate and print the fetch plan without persistent writes",
    )
    fetch.add_argument(
        "--refresh",
        action="store_true",
        help="redownload every page or image for the selected stage",
    )
    fetch.add_argument(
        "--verbose",
        action="store_true",
        help="emit detailed progress and diagnostics to standard error",
    )

    build = commands.add_parser(
        "build",
        help="build a Markdown mirror from the fetched snapshot",
    )
    build_mode = build.add_mutually_exclusive_group()
    build_mode.add_argument(
        "--dry-run",
        action="store_true",
        help="build and validate in a temporary location without writing output",
    )
    build_mode.add_argument(
        "--check",
        action="store_true",
        help="compare a fresh build with the committed output and fail on differences",
    )
    build.add_argument(
        "--verbose",
        action="store_true",
        help="emit detailed progress and diagnostics to standard error",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    source = str(arguments.source)
    command = str(arguments.command)
    verbose = bool(arguments.verbose)

    def log(message: str) -> None:
        print(f"specmirror: {message}", file=sys.stderr)

    try:
        paths = SourcePaths(root=repository_root(), source=source)
        if command == "fetch":
            dry_run = bool(arguments.dry_run)
            outcome = run_fetch(
                source,
                str(arguments.stage),
                dry_run=dry_run,
                refresh=bool(arguments.refresh),
                paths=paths,
                client=UrllibHttpClient(),
                log=log if verbose else None,
            )
            if dry_run:
                print(pretty_json_text(_dry_run_fetch_payload(outcome)))
            else:
                _print_fetch_summary(outcome)
            return 0
        if command == "build":
            dry_run = bool(arguments.dry_run)
            check = bool(arguments.check)
            outcome = run_build(
                source,
                dry_run=dry_run,
                check=check,
                paths=paths,
                log=log if verbose else None,
            )
            if dry_run or check:
                print(pretty_json_text(_dry_run_build_payload(outcome)))
                if check and outcome.changed:
                    print(
                        "specmirror: error: the committed mirror differs from "
                        "the build; rerun the build and commit the output",
                        file=sys.stderr,
                    )
                    return 1
                return 0
            _print_build_summary(outcome)
            return 0
        raise UsageError(f"unknown command: {command}")
    except SpecMirrorError as error:
        print(f"specmirror: error: {error}", file=sys.stderr)
        return 1


def _dry_run_fetch_payload(outcome: FetchOutcome) -> dict[str, object]:
    payload: dict[str, object] = {
        "source": outcome.source,
        "dry_run": True,
    }
    if outcome.pages is not None:
        payload["pages"] = outcome.pages.plan.to_dict()
    if outcome.images is not None:
        payload["images"] = {
            "page_plan_sha256": outcome.images.plan_sha256,
            "work": [action.to_json() for action in outcome.images.actions],
        }
    return payload


def _print_fetch_summary(outcome: FetchOutcome) -> None:
    if outcome.pages is not None:
        counts = outcome.pages.counts
        print(
            f"{outcome.source} pages: {counts.total} pages, "
            f"{counts.downloaded} downloaded, {counts.reused} reused; "
            f"plan {outcome.pages.plan_sha256[:12]}"
        )
    if outcome.images is not None:
        counts = outcome.images.counts
        snapshot = outcome.images.snapshot_sha256 or "unpublished"
        print(
            f"{outcome.source} images: {counts.total} images, "
            f"{counts.downloaded} downloaded, {counts.reused} reused; "
            f"snapshot {snapshot[:12]}"
        )


def _dry_run_build_payload(outcome: object) -> dict[str, object]:
    from .build.pipeline import BuildOutcome

    assert isinstance(outcome, BuildOutcome)
    payload: dict[str, object] = {
        "source": outcome.source,
        "dry_run": outcome.dry_run,
        "check": outcome.check,
        "pages": outcome.page_count,
        "snapshot_sha256": outcome.snapshot_sha256,
        "changed": outcome.changed,
    }
    if not outcome.check:
        payload["page_hashes"] = outcome.page_hashes
        payload["readme_sha256"] = outcome.readme_sha256
    return payload


def _print_build_summary(outcome: object) -> None:
    from .build.pipeline import BuildOutcome

    assert isinstance(outcome, BuildOutcome)
    state = "unchanged" if outcome.changed is False else "updated"
    print(
        f"{outcome.source} build: {outcome.page_count} pages; "
        f"snapshot {outcome.snapshot_sha256[:12]}; {state}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
