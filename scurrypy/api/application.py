from dataclasses import dataclass

from ..core.model import DataModel
from ..core.snowflake import Snowflake

from ..enums.application import ApplicationFlags

from .guilds.guild import GuildModel

from .user import UserModel

@dataclass
class ApplicationModel(DataModel):
    """Represents a Discord application."""

    id: Snowflake
    """ID of the application."""

    name: str
    """Name of the application."""

    icon: str | None
    """Icon hash of the application."""

    description: str | None
    """Description of the application."""

    bot_public: bool | None
    """If the application is public."""

    bot_require_code_grant: bool | None
    """If full OAuth2 code grant is required."""

    bot: UserModel | None
    """Partial bot user object of the application."""

    terms_of_service_url: str | None
    """Terms of Service URL of the application"""

    privacy_policy: str | None
    """Privacy Policy URL of the application."""

    owner: UserModel | None
    """Partial user object of the owner of the application."""

    guild_id: Snowflake | None
    """Guild ID associated with the application."""

    guild: GuildModel | None
    """Partial guild object of the associated guild."""

    cover_image: str | None
    """Image hash of rich presence invite cover."""

    flags: ApplicationFlags | None
    """Public flags of the application."""

    approximate_guild_count: int | None
    """Approximate guild count of the guilds that installed the application."""
