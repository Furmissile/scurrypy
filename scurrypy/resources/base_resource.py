from dataclasses import dataclass

from ..core.http import HTTPClientProtocol

@dataclass
class BaseResource:
    """Represents a Discord Resource object."""

    http: HTTPClientProtocol
    """HTTP session for requests."""
