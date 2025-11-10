from typing import Protocol

from .config import BaseConfig
from .http import HTTPClient
from .logger import Logger

class ClientLike(Protocol):
    """Exposes a common interface for [`Client`][scurrypy.client.Client]."""

    token: str
    """Bot's token."""

    application_id: int
    """Bot's application ID."""

    intents: int
    """Bot intents for listening to events."""

    config: BaseConfig
    """User-defined config."""

    _http: HTTPClient
    """HTTP session for requests."""

    _logger: Logger
    """Logger instance to log events."""
