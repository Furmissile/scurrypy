from dataclasses import dataclass
from typing import Optional
from .model import DataModel

from urllib.parse import quote

@dataclass
class EmojiModel(DataModel):
    """Represents a Discord emoji."""
    name: str
    """Name of emoji."""

    id: int = 0
    """ID of the emoji (if custom)."""

    animated: bool = False
    """If the emoji is animated. Defaults to False."""

    @property
    def mention(self) -> str:
        """For use in message content."""
        return f"<a:{self.name}:{self.id}>" if self.animated else f"<:{self.name}:{self.id}>"

    @property
    def api_code(self) -> str:
        """Return the correct API code for this emoji (URL-safe)."""
        if not self.id:
            # unicode emoji
            return quote(self.name)

        # custom emoji
        if self.animated:
            return quote(f"a:{self.name}:{self.id}")
        
        return quote(f"{self.name}:{self.id}")

    @property
    def url(self) -> str:
        """
            Return the full qualifying link for this emoji.

            !!! warning "Important"
                This only works for custom Discord emojis (those with an ID). 
                Unicode emojis will return `None`.
        """
        if not self.id:
            return None
        
        ext = 'gif' if self.animated else 'png'

        return f"https://cdn.discordapp.com/emojis/{self.id}.{ext}"

# Guild Models

@dataclass
class ReadyGuildModel(DataModel):
    """Guild info from Ready event."""
    id: int
    """ID of the associated guild."""

    unavailable: bool
    """If the guild is offline."""

@dataclass
class GuildModel(DataModel):
    """Represents a Discord guild."""

    id: int
    """ID of the guild."""

    name: str
    """Name of the guild."""

    icon: Optional[str] = None
    """Icon hash of the guild."""

    emojis: list[EmojiModel] = None
    """List of emojis reigstered in the guild."""

    approximate_member_count: Optional[int] = None
    """Approximate member count."""

    description: str = None
    """Description of the guild."""

# User Models

@dataclass
class UserModel(DataModel):
    """Describes the User object."""
    id: int
    """ID of the user."""

    username: str
    """Username of the user."""

    avatar: str
    """Avatar hash of the user."""

@dataclass
class ApplicationModel(DataModel):
    """Represents a bot application object."""
    id: int
    """ID of the app."""

    name: str
    """Name of the app."""

    icon: str
    """Icon hash of the app."""

    description: str
    """Description of the app."""

    bot_public: bool
    """If other users can add this app to a guild."""

    bot: UserModel
    """Partial user obhect for the bot user associated with the app."""

    owner: UserModel
    """Partial user object for the owner of the app."""

    guild_id: int
    """Guild ID associated with the app (e.g., a support server)."""

    guild: GuildModel
    """Partial guild object of the associated guild."""

    approximate_guild_count: int
    """Approximate guild member count."""

@dataclass
class IntegrationModel(DataModel):
    """Represents a guild integration."""

    id: int
    """ID of the integration."""

    name: str
    """Name of the integration."""

    type: str
    """Type of integration (e.g., twitch, youtube, discord, or guild_subscription)."""

    enabled: bool
    """If the integration is enabled."""

    application: Optional[ApplicationModel] = None
    """The bot aaplication for Discord integrations."""

@dataclass
class MemberModel(DataModel):
    """Represents a guild member."""

    roles: list[int]
    """List of roles registered to the guild member."""

    user: UserModel
    """User data associated with the guild member."""

    nick: str
    """Server nickname of the guild member."""

    avatar: str
    """Server avatar hash of the guild mmeber."""

    joined_at: str
    """ISO8601 timestamp of when the guild member joined server."""

    deaf: bool
    """If the member is deaf in a VC (input)."""

    mute: bool
    """If the member is muted in VC (output)."""

# Interaction Models

@dataclass
class InteractionCallbackDataModel(DataModel):
    """Represents the interaction callback object."""

    id: int
    """ID of the interaction."""

    type: int
    """Type of interaction."""

    activity_instance_id: str
    """Instance ID of activity if an activity was launched or joined."""

    response_message_id: int
    """ID of the message created by the interaction."""

    response_message_loading: bool
    """If the interaction is in a loading state."""

    response_message_ephemeral: bool
    """If the interaction is ephemeral."""

@dataclass
class InteractionCallbackModel(DataModel):
    """Represents the interaction callback response object."""

    interaction: InteractionCallbackDataModel
    """The interaction object associated with the interaction response."""

# Role Models

@dataclass
class RoleColors(DataModel):
    """Role color data."""

    primary_color: int
    """Primary color of the role."""

    secondary_color: int
    """Secondary color of the role. Creates a gradient."""

    tertiary_color: int
    """Tertiary color of the role. Creates a holographic style."""

@dataclass
class RoleModel(DataModel):
    """Represents a Discord role."""

    id: int
    """ID of the role."""

    name: str
    """Name of the role."""

    colors: RoleColors
    """Colors of the role."""

    hoist: bool
    """If the role is pinned in user listing."""

    position: int
    """Position of the role."""

    permissions: str
    """Permission bit set."""

    managed: bool
    """If the role is managed by an integration."""

    mentionable: bool
    """If the role is mentionable."""

    flags: int
    """Role flags combined as a bitfield."""

    icon: Optional[str] = None
    """Icon hash of the role."""

    unicode_emoji: Optional[str] = None
    """Unicode emoji of the role."""
