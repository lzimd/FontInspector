"""Shared storage helpers: hashing, atomic writes, JSON, and safe paths."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path, PurePosixPath

from .errors import ValidationError

# -------------------------------------------------------------------- hashing

_CHUNK_SIZE = 1024 * 1024


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(_CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def file_matches_hash(path: Path, expected_sha256: str) -> bool:
    try:
        return path.is_file() and sha256_file(path) == expected_sha256
    except OSError:
        return False


# --------------------------------------------------------------- atomic write


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def write_bytes_if_changed(path: Path, data: bytes) -> bool:
    """Write bytes atomically unless the file already carries them."""
    if path.is_file():
        try:
            if sha256_file(path) == sha256_bytes(data):
                return False
        except OSError:
            pass
    atomic_write_bytes(path, data)
    return True


def atomic_copy(source: Path, destination: Path) -> None:
    if source == destination:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        temporary.replace(destination)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


# ---------------------------------------------------------- write JSON object


def canonical_json_bytes(value: object) -> bytes:
    """Serialize a value as canonical JSON bytes."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def canonical_document_bytes(value: object) -> bytes:
    """Serialize a value as a canonical JSON document."""
    return canonical_json_bytes(value) + b"\n"


def pretty_json_text(value: object) -> str:
    """Serialize a value as indented JSON text."""
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)


def pretty_json_bytes(value: object) -> bytes:
    """Serialize a value as an indented JSON document."""
    return (pretty_json_text(value) + "\n").encode("utf-8")


def write_json_document(path: Path, document: object) -> None:
    """Write an indented JSON document atomically."""
    atomic_write_bytes(path, pretty_json_bytes(document))


# ---------------------------------------------------------------------------


def list_tree_files(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    files = [path for path in root.rglob("*") if path.is_file()]
    return sorted(path.relative_to(root).as_posix() for path in files)


def safe_relative_path(relative: str, *, where: str) -> PurePosixPath:
    if not relative:
        raise ValidationError(f"{where} is empty")
    if "\\" in relative:
        raise ValidationError(f"{where} must use POSIX separators: {relative!r}")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or not pure.parts:
        raise ValidationError(f"{where} is not a safe relative path: {relative!r}")
    if any(part in {".", ".."} for part in pure.parts):
        raise ValidationError(f"{where} is not a safe relative path: {relative!r}")
    if pure.as_posix() != relative:
        raise ValidationError(
            f"{where} is not a normalized relative path: {relative!r}"
        )
    return pure
