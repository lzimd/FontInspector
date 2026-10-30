"""Manifest loading, publication, and snapshot file verification."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .errors import FetchError, SchemaError
from .paths import SourcePaths
from .schema import Manifest, parse_json_bytes
from .storage import atomic_write_bytes, file_matches_hash, sha256_bytes


@dataclass(frozen=True, slots=True)
class LoadedManifest:
    manifest: Manifest
    data: bytes
    file_sha256: str
    path: Path


def load_manifest(
    path: Path,
    *,
    expected_source: str,
    required: bool,
) -> LoadedManifest | None:
    if not path.is_file():
        if required:
            raise FetchError(f"manifest is missing: {path}")
        return None
    data = path.read_bytes()
    value = parse_json_bytes(data, what=f"manifest {path}")
    manifest = Manifest.from_dict(value, expected_source=expected_source)
    return LoadedManifest(
        manifest=manifest,
        data=data,
        file_sha256=sha256_bytes(data),
        path=path,
    )


def write_manifest(paths: SourcePaths, manifest: Manifest) -> LoadedManifest:
    data = manifest.to_bytes()
    if manifest.source != paths.source:
        raise SchemaError("manifest source does not match the target paths")
    atomic_write_bytes(paths.manifest_path, data)
    return LoadedManifest(
        manifest=manifest,
        data=data,
        file_sha256=sha256_bytes(data),
        path=paths.manifest_path,
    )


def verify_manifest_files(manifest: Manifest, paths: SourcePaths) -> None:
    for page in manifest.pages:
        path = paths.cache_path(page.file)
        if not file_matches_hash(path, page.sha256):
            raise FetchError(
                f"page cache does not match the manifest: {page.file}; "
                f"rerun 'fetch pages' for {paths.source}"
            )
    for image in manifest.images:
        path = paths.cache_path(image.file)
        if not file_matches_hash(path, image.sha256):
            raise FetchError(
                f"image cache does not match the manifest: {image.file}; "
                f"rerun 'fetch images' for {paths.source}"
            )
