from dataclasses import dataclass
from typing import Optional, TypedDict, Unpack

from ..core.http import HTTPClient
from ..core.model import DataModel

from .channel import Channel

from ..parts.channel import GuildChannel
from ..parts.role import Role

from ..models import EmojiModel, MemberModel, RoleModel

class FetchGuildMembersParams(TypedDict, total=False):
    """Params when fetching guild members."""

    limit: int
    """Max number of members to return Range 1 - 1000. Default 1."""

    after: int
    """Highest user ID in previous page."""

class FetchGuildParams(TypedDict, total=False):
    """Params when fetching a guild."""

    with_counts: Optional[bool]
    """If True, return the approximate member and presence counts for the guild."""

@dataclass
class Guild(DataModel):
    """Represents a Discord guild."""
    id: int
    """ID of the guild."""

    _http: HTTPClient
    """HTTP session for requests."""

    name: str = None
    """Name of the guild."""

    icon: str = None
    """Image hash of the guild's icon."""

    splash: str = None
    """Image hash of the guild's splash."""

    owner: Optional[bool] = None
    """If the member is the owner. (Get Current User Guilds)"""

    owner_id: int = None
    """OD of the owner of the guild."""

    roles: list[int] = None
    """List of IDs registered in the guild."""

    emojis: list[EmojiModel] = None
    """List of emojis registered in the guild."""

    mfa_level: int = None
    """Required MFA level of the guild."""

    application_id: int = None
    """ID of the application if the guild is created by a bot."""

    system_channel_id: int = None
    """Channel ID where system messages go (e.g., welcome messages, boost events)."""

    system_channel_flags: int = None
    """System channel flags."""

    rules_channel_id: int = None
    """Channel ID where rules are posted."""

    max_members: Optional[int] = None
    """Maximum member capacity for the guild."""

    description: str = None
    """Description of the guild."""

    banner: str = None
    """Image hash of the guild's banner."""

    preferred_locale: str = None
    """Preferred locale of the guild."""

    public_updates_channel_id: int = None
    """Channel ID of announcement or public updates."""

    approximate_member_count: int = None
    """Approximate number of members in the guild."""

    nsfw_level: int = None
    """NSFW level of the guild."""

    safety_alerts_channel_id: int = None
    """Channel ID for safety alerts."""

    async def fetch(self, **kwargs: Unpack[FetchGuildParams]):
        """Fetch the Guild object by the given ID.

        Args:
            **kwargs: guild fetch params
                !!! note
                    If no kwargs are provided, default to with_counts = False
            
        Returns:
            (Guild): the Guild object
        """
        params = {'with_counts': False, **kwargs}

        data = await self._http.request('GET', f'/guilds/{self.id}', params=params)

        return Guild.from_dict(data, self._http)

    async def fetch_channels(self):
        """Fetch this guild's channels.

        Returns:
            (list[Channel]): list of the guild's channels
        """
        data = await self._http.request('GET', f'guilds/{self.id}/channels')

        return [Channel.from_dict(channel, self._http) for channel in data]

    async def create_channel(self, channel: GuildChannel):
        """Create a channel in this guild.

        Permissions:
            * MANAGE_CHANNELS → required to create a channel

        Args:
            channel (GuildChannel): the buildable guild channel

        Returns:
            (Channel): the created channel
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/channels', data=channel.to_dict())

        return Channel.from_dict(data, self._http)

    async def fetch_guild_member(self, user_id: int):
        """Fetch a member in this guild.
        !!! warning "Important"
            Requires the GUILD_MEMBERS privileged intent!

        Args:
            user_id (int): user ID of the member to fetch

        Returns:
            (MemberModel): member's data
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/members/{user_id}')

        return MemberModel.from_dict(data)
    
    async def fetch_guild_members(self, **kwargs: Unpack[FetchGuildMembersParams]):
        """Fetch guild members in this guild.
        !!! warning "Important"
            Requires the GUILD_MEMBERS privileged intent!

        Args:
            **kwargs: guild members fetch params
                !!! note
                    If no kwargs are provided, default to 1 guild member limit.

        Returns:
            (list[MemberModel]): list of member data
        """
        params = {"limit": 1, **kwargs}

        data = await self._http.request('GET', f'/guilds/{self.id}/members', params=params)

        return [MemberModel.from_dict(member) for member in data]

    async def add_guild_member_role(self, user_id: int, role_id: int):
        """Append a role to a guild member of this guild.

        Permissions:
            * MANAGE_ROLES → required to add a role to the user
        
        Args:
            user_id (int): ID of the member for the role
            role_id (int): ID of the role to append
        """
        await self._http.request('PUT', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')
    
    async def remove_guild_member_role(self, user_id: int, role_id: int):
        """Remove a role from a guild member of this guild.

        Permissions:
            * MANAGE_ROLES → required to remove a role from the user

        Args:
            user_id (int): ID of the member with the role
            role_id (int): ID of the role to remove
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')

    async def fetch_guild_role(self, role_id: int):
        """Fetch a role in this guild.

        Args:
            role_id (int): ID of the role to fetch

        Returns:
            (RoleModel): fetched role's data
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/roles/{role_id}')
        
        return RoleModel.from_dict(data)

    async def fetch_guild_roles(self):
        """Fetch all roles in this guild.

        Returns:
            (list[RoleModel]): list of fetched roles' data
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/roles')
        
        return [RoleModel.from_dict(role) for role in data]

    async def create_guild_role(self, role: Role):
        """Create a role in this guild.

        Permissions:
            * MANAGE_ROLES → required to add a role to the guild

        Args:
            role (Role): role to create

        Returns:
            (RoleModel): new role data
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/roles', data=role.to_dict())

        return RoleModel.from_dict(data)

    async def modify_guild_role(self, role_id: int, role: Role):
        """Modify a role in this guild.

        Permissions:
            * MANAGE_ROLES → required to modify a role in the guild

        Args:
            role (Role): role with changes

        Returns:
            (RoleModel): role with changes
        """
        data = await self._http.request('PATCH', f'/guilds/{self.id}/roles/{role_id}', data=role.to_dict())

        return RoleModel.from_dict(data)
    
    async def delete_guild_role(self, role_id: int):
        """Delete a role in this guild.

        Permissions:
            * MANAGE_ROLES → required to delete a role in the guild

        Args:
            role_id (int): ID of role to delete
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/roles/{role_id}')
