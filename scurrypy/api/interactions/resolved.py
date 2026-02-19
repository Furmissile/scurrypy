from dataclasses import dataclass

from ...core.model import DataModel
from ...core.snowflake import Snowflake

from ..guilds.role import GuildRoleModel
from ..channels.channel import ChannelModel
from ..messages.message import MessageModel
from ..messages.attachment import AttachmentModel

from ..user import UserModel, GuildMemberModel

@dataclass
class ResolvedDataModel(DataModel):
    """Represents the resolved data object."""

    users: dict[Snowflake, UserModel] | None
    """Map of user snowflakes to user objects."""

    members: dict[Snowflake, GuildMemberModel] | None
    """Map of member snowflakes to partial guild member objects.

    !!! note "Missing Fields"
        `user`, `deaf`, and `mute`.
    """

    roles: dict[Snowflake, GuildRoleModel] | None
    """Map of role snowflakes to role objects."""

    channels: dict[Snowflake, ChannelModel] | None
    """Map of channel snowflakes to partial channel objects."""

    messages: dict[Snowflake, MessageModel] | None
    """Map of message snowflakes to partial message objects."""

    attachments: dict[Snowflake, AttachmentModel] | None
    """Map of attachment snowflakes to attachment objects."""
