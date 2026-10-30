"""Command-line interface tests."""

from __future__ import annotations

import json

import pytest
from specmirror import cli
from specmirror.errors import UsageError
from specmirror.fetch import FetchOutcome


def test_parser_rejects_an_unknown_source() -> None:
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["unknown", "fetch"])


def test_parser_rejects_dry_run_with_check() -> None:
    with pytest.raises(SystemExit):
        cli.build_parser().parse_args(["opentype", "build", "--dry-run", "--check"])


def test_main_rejects_an_unknown_source() -> None:
    with pytest.raises(SystemExit):
        cli.main(["unknown", "fetch"])


def test_main_prints_a_fetch_dry_run_payload(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run_fetch(source: str, stage: str, **options: object) -> FetchOutcome:
        del stage, options
        return FetchOutcome(source=source, pages=None, images=None)

    monkeypatch.setattr(cli, "run_fetch", fake_run_fetch)
    assert cli.main(["opentype", "fetch", "--dry-run"]) == 0
    assert json.loads(capsys.readouterr().out) == {
        "source": "opentype",
        "dry_run": True,
    }


def test_main_prints_a_build_dry_run_payload(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    from specmirror.build.pipeline import BuildOutcome

    def fake_run_build(source: str, **options: object) -> BuildOutcome:
        del options
        return BuildOutcome(
            source=source,
            dry_run=True,
            check=False,
            page_count=2,
            snapshot_sha256="a" * 64,
            page_hashes={"index.md": "b" * 64},
            readme_sha256="c" * 64,
            changed=None,
            report={},
        )

    monkeypatch.setattr(cli, "run_build", fake_run_build)
    assert cli.main(["opentype", "build", "--dry-run"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["source"] == "opentype"
    assert payload["pages"] == 2
    assert payload["dry_run"] is True


def test_main_check_mode_exits_non_zero_on_difference(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    from specmirror.build.pipeline import BuildOutcome

    def fake_run_build(source: str, **options: object) -> BuildOutcome:
        del options
        return BuildOutcome(
            source=source,
            dry_run=False,
            check=True,
            page_count=1,
            snapshot_sha256="a" * 64,
            page_hashes={},
            readme_sha256="c" * 64,
            changed=True,
            report={},
        )

    monkeypatch.setattr(cli, "run_build", fake_run_build)
    assert cli.main(["opentype", "build", "--check"]) == 1
    assert "differs from the build" in capsys.readouterr().err


def test_main_check_mode_exits_zero_when_identical(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    from specmirror.build.pipeline import BuildOutcome

    def fake_run_build(source: str, **options: object) -> BuildOutcome:
        del options
        return BuildOutcome(
            source=source,
            dry_run=False,
            check=True,
            page_count=1,
            snapshot_sha256="a" * 64,
            page_hashes={},
            readme_sha256="c" * 64,
            changed=False,
            report={},
        )

    monkeypatch.setattr(cli, "run_build", fake_run_build)
    assert cli.main(["opentype", "build", "--check"]) == 0
    assert json.loads(capsys.readouterr().out)["changed"] is False


def test_main_prints_a_build_summary(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    from specmirror.build.pipeline import BuildOutcome

    def fake_run_build(source: str, **options: object) -> BuildOutcome:
        del options
        return BuildOutcome(
            source=source,
            dry_run=False,
            check=False,
            page_count=2,
            snapshot_sha256="a" * 64,
            page_hashes={},
            readme_sha256="c" * 64,
            changed=False,
            report={},
        )

    monkeypatch.setattr(cli, "run_build", fake_run_build)
    assert cli.main(["opentype", "build"]) == 0
    assert "2 pages" in capsys.readouterr().out


def test_main_prints_a_controlled_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def fake_run_fetch(source: str, stage: str, **options: object) -> FetchOutcome:
        del source, stage, options
        raise UsageError("boom")

    monkeypatch.setattr(cli, "run_fetch", fake_run_fetch)
    assert cli.main(["opentype", "fetch"]) == 1
    assert "specmirror: error: boom" in capsys.readouterr().err
