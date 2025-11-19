from dataclasses import dataclass
from typing import Optional

from ..core.http import HTTPClient
from ..core.model import DataModel

from ..models import UserModel, GuildModel

class ApplicationFlags:
    """Application flags (bitwise constants)."""

    GATEWAY_PRESENCE = 1 << 12
    """Privileged intent to receive presence_update events."""

    GATEWAY_PRESENCE_LIMITED = 1 << 13
    """Intent to receive presence_update events."""

    GATEWAY_GUILD_MEMBERS = 1 << 14
    """Privileged intent to receive member-related events."""

    GATEWAY_GUILD_MEMBERS_LIMITED = 1 << 15
    """Intent to receive member-related events."""

    VERIFICATION_PENDING_GUILD_LIMIT = 1 << 16
    """Indicates unusual growth of an app that prevents verification."""

    GATEWAY_MESSAGE_CONTENT = 1 << 18
    """Privileged intent to receive message content."""

    GATEWAY_MESSAGE_CONTENT_LIMITED = 1 << 19
    """Intent to receive message content."""

@dataclass
class Application(DataModel):
    """Represents a Discord application."""

    id: int
    """ID of the application."""

    _http: HTTPClient
    """HTTP session for requests."""

    name: str = None
    """Name of the application."""

    icon: Optional[str] = None
    """Icon hash of the application."""

    description: Optional[str] = None
    """Description of the application."""

    bot_public: Optional[bool] = None
    """If the application is public."""

    bot_require_code_grant: Optional[bool] = None
    """If full OAuth2 code grant is required."""

    bot: Optional[UserModel] = None
    """Partial bot user object of the application."""

    terms_of_service_url: Optional[str] = None
    """Terms of Service URL of the application"""

    privacy_policy: Optional[str] = None
    """Privacy Policy URL of the application."""

    owner: Optional[UserModel] = None
    """Partial user object of the owner of the application."""

    guild_id: Optional[int] = None
    """Guild ID associated with the application."""

    guild: Optional[GuildModel] = None
    """Partial guild object of the associated guild."""

    cover_image: Optional[str] = None
    """Image hash of rich presence invite cover."""

    flags: Optional[int] = None
    """Public flags of the application."""

    approximate_guild_count: Optional[int] = None
    """Approximate guild count of the guilds that installed the application."""
    
    def fetch(self):
        """Fetch this application's data.

        Returns:
            (Application): the Application data
        """
        data = self._http.request('GET', '/applications/@me')

        return Application.from_dict(data, self._http)
