"""Storage helper and path-safety tests."""

from __future__ import annotations

import os
from pathlib import Path, PurePosixPath

import pytest
from specmirror.errors import ValidationError
from specmirror.storage import (
    atomic_copy,
    atomic_write_bytes,
    canonical_json_bytes,
    list_tree_files,
    safe_relative_path,
    sha256_bytes,
    sha256_file,
)


@pytest.mark.parametrize(
    "relative",
    [
        "",
        ".",
        "..",
        "/absolute",
        "../escape",
        "a/../b",
        "a/./b",
        "a//b",
        "a\\b",
        "a/",
    ],
)
def test_safe_relative_path_rejects_unsafe_paths(relative: str) -> None:
    with pytest.raises(ValidationError):
        safe_relative_path(relative, where="path")


@pytest.mark.parametrize(
    "relative",
    ["page.html", "pages/index.html", "images/a-b_c.png"],
)
def test_safe_relative_path_accepts_normalized_paths(relative: str) -> None:
    assert safe_relative_path(relative, where="path") == PurePosixPath(relative)


@pytest.mark.parametrize(
    ("relative", "message"),
    [
        ("", "is empty"),
        ("a\\b", "must use POSIX separators"),
        ("/absolute", "is not a safe relative path"),
        ("../escape", "is not a safe relative path"),
        ("a/./b", "is not a normalized relative path"),
    ],
)
def test_safe_relative_path_explains_the_failure(relative: str, message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        safe_relative_path(relative, where="path")


def test_atomic_write_bytes_leaves_no_temporary_file(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "file.bin"
    atomic_write_bytes(target, b"payload")
    assert target.read_bytes() == b"payload"
    assert sorted(path.name for path in tmp_path.rglob("*")) == ["file.bin", "nested"]


def test_atomic_write_bytes_removes_the_temporary_file_on_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(_descriptor: int) -> None:
        raise OSError("disk failure")

    monkeypatch.setattr(os, "fsync", fail)
    with pytest.raises(OSError, match="disk failure"):
        atomic_write_bytes(tmp_path / "file.bin", b"payload")
    assert list(tmp_path.iterdir()) == []


def test_atomic_copy_replaces_the_destination(tmp_path: Path) -> None:
    source = tmp_path / "source.bin"
    source.write_bytes(b"new")
    destination = tmp_path / "nested" / "destination.bin"
    destination.parent.mkdir()
    destination.write_bytes(b"old")
    atomic_copy(source, destination)
    assert destination.read_bytes() == b"new"


def test_atomic_copy_skips_a_copy_onto_itself(tmp_path: Path) -> None:
    source = tmp_path / "file.bin"
    source.write_bytes(b"payload")
    atomic_copy(source, source)
    assert source.read_bytes() == b"payload"


def test_list_tree_files_returns_sorted_posix_paths(tmp_path: Path) -> None:
    (tmp_path / "b").mkdir()
    (tmp_path / "a.txt").write_bytes(b"a")
    (tmp_path / "b" / "c.txt").write_bytes(b"c")
    assert list_tree_files(tmp_path) == ["a.txt", "b/c.txt"]
    assert list_tree_files(tmp_path / "missing") == []


def test_canonical_json_bytes_are_sorted_and_compact() -> None:
    assert canonical_json_bytes({"b": 1, "a": 2}) == b'{"a":2,"b":1}'


def test_sha256_file_matches_the_bytes(tmp_path: Path) -> None:
    target = tmp_path / "file.bin"
    target.write_bytes(b"payload")
    assert sha256_file(target) == sha256_bytes(b"payload")
