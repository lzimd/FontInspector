"""Controlled failures that the command-line interface reports without a traceback."""

from __future__ import annotations


class SpecMirrorError(Exception):
    """Base class for expected SpecMirror failures."""


class UsageError(SpecMirrorError):
    """Invalid command-line usage."""


class ValidationError(SpecMirrorError):
    """An input artifact violates the SpecMirror contract."""


class SchemaError(ValidationError):
    """A JSON artifact doesn't match its schema."""


class DiscoveryError(ValidationError):
    """The adapter can't interpret a discovery response."""


class PageValidationError(ValidationError):
    """A page doesn't satisfy the source adapter contract."""


class FetchError(SpecMirrorError):
    """A fetch stage can't complete."""


class BuildError(SpecMirrorError):
    """The build stage can't produce a valid mirror."""


class HttpError(SpecMirrorError):
    """A network request failed."""

    def __init__(self, url: str, message: str, redirects: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.url = url
        self.redirects = redirects


class HttpStatusError(HttpError):
    """The server answered with a non-success status."""

    def __init__(
        self,
        url: str,
        status: int,
        message: str,
        redirects: tuple[str, ...] = (),
    ) -> None:
        super().__init__(url, message, redirects)
        self.status = status


class HttpTransportError(HttpError):
    """The request failed before an HTTP response was available."""
