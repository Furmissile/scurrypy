from dataclasses import dataclass

from .base_resource import BaseResource

from ..parts.channel import GuildChannel
from ..parts.role import Role

from ..models.role import RoleModel
from ..models.guild import GuildModel
from ..models.guild_member import GuildMemberModel
from ..models.channel import ChannelModel

@dataclass
class Guild(BaseResource):
    """Represents a Discord guild."""
    
    id: int
    """ID of the guild."""

    async def fetch(self, with_counts: bool = False) -> GuildModel:
        """Fetch the Guild object by the given ID.

        Args:
            with_counts (bool, optional): return the approximate member and presence counts for the guild. Defaults to `False`.
            
        Returns:
            (GuildModel): queried guild
        """
        params = {'with_counts': with_counts}

        data = await self._http.request('GET', f'/guilds/{self.id}', params=params)

        return GuildModel.from_dict(data)

    async def fetch_channels(self) -> list[ChannelModel]:
        """Fetch this guild's channels.

        Returns:
            (list[ChannelModel]): queried list of the guild's channels
        """
        data = await self._http.request('GET', f'guilds/{self.id}/channels')

        return [ChannelModel.from_dict(channel) for channel in data]

    async def create_channel(self, channel: GuildChannel) -> ChannelModel:
        """Create a channel in this guild.

        Permissions:
            * `MANAGE_CHANNELS` → required to create a channel

        Args:
            channel (GuildChannel): the guild channel to create

        Returns:
            (ChannelModel): created channel
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/channels', data=channel.to_dict())

        return ChannelModel.from_dict(data)

    async def fetch_guild_member(self, user_id: int) -> GuildMemberModel:
        """Fetch a member in this guild.

        !!! warning "Important"
            Requires the `GUILD_MEMBERS` privileged intent!

        Args:
            user_id (int): user ID of the member to fetch

        Returns:
            (GuildMemberModel): queried guild member
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/members/{user_id}')

        return GuildMemberModel.from_dict(data)
    
    async def fetch_guild_members(self, limit: int = 1, after: int = None) -> list[GuildMemberModel]:
        """Fetch guild members in this guild.

        !!! warning "Important"
            Requires the `GUILD_MEMBERS` privileged intent!

        Args:
            limit (int, optional): Max number of members to return Range 1 - 1000. Default `1`.
            after (int, optional): highest user ID in previous page

        Returns:
            (list[GuildMemberModel]): queried list of guild members
        """
        params = {
            "limit": limit, 
            "after": after
        }

        data = await self._http.request('GET', f'/guilds/{self.id}/members', params=params)

        return [GuildMemberModel.from_dict(member) for member in data]

    async def add_guild_member_role(self, user_id: int, role_id: int) -> None:
        """Append a role to a guild member of this guild.

        Permissions:
            * `MANAGE_ROLES` → required to add a role to the user
        
        Args:
            user_id (int): ID of the member for the role
            role_id (int): ID of the role to append
        """
        await self._http.request('PUT', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')
    
    async def remove_guild_member_role(self, user_id: int, role_id: int) -> None:
        """Remove a role from a guild member of this guild.

        Permissions:
            * `MANAGE_ROLES` → required to remove a role from the user

        Args:
            user_id (int): ID of the member with the role
            role_id (int): ID of the role to remove
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')

    async def fetch_guild_role(self, role_id: int) -> RoleModel:
        """Fetch a role in this guild.

        Args:
            role_id (int): ID of the role to fetch

        Returns:
            (RoleModel): queried guild role
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/roles/{role_id}')
        
        return RoleModel.from_dict(data)

    async def fetch_guild_roles(self) -> list[RoleModel]:
        """Fetch all roles in this guild.

        Returns:
            (list[RoleModel]): queried list of guild roles
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/roles')
        
        return [RoleModel.from_dict(role) for role in data]

    async def create_guild_role(self, role: Role) -> RoleModel:
        """Create a role in this guild.

        Permissions:
            * `MANAGE_ROLES` → required to add a role to the guild

        Args:
            role (Role): role to create

        Returns:
            (RoleModel): created role
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/roles', data=role.to_dict())

        return RoleModel.from_dict(data)

    async def edit_guild_role(self, role_id: int, role: Role) -> RoleModel:
        """Edit a role in this guild.

        Permissions:
            * `MANAGE_ROLES` → required to edit a role in the guild

        Args:
            role (Role): role with fields to edit

        Returns:
            (RoleModel): edited role
        """
        data = await self._http.request('PATCH', f'/guilds/{self.id}/roles/{role_id}', data=role.to_dict())

        return RoleModel.from_dict(data)
    
    async def delete_guild_role(self, role_id: int) -> None:
        """Delete a role in this guild.

        Permissions:
            * `MANAGE_ROLES` → required to delete a role in the guild

        Args:
            role_id (int): ID of role to delete
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/roles/{role_id}')
