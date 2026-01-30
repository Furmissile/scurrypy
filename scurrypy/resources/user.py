from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..models.channel import ChannelModel
from ..models.user import GuildMemberModel
from ..models.user import UserModel

from ..params.user import EditUserParams

@dataclass
class User(BaseResource):
    """A Discord user."""

    async def fetch(self, user_id: int) -> UserModel:
        """Fetch this user by ID.

        Args:
            user_id (int): ID of user to fetch

        Returns:
            (UserModel): queried user
        """
        data = await self._http.request('GET', f'/users/{user_id}')

        return UserModel.from_dict(data)

    async def fetch_guild_member(self, guild_id: int, user_id: int) -> GuildMemberModel:
        """Fetch this user's guild member data.

        Args:
            guild_id (int): ID of guild to fetch data from
            user_id (int): ID of user to fetch

        Returns:
            (GuildMemberModel): queried guild member for the user
        """
        data = await self._http.request('GET', f'/guilds/{guild_id}/members/{user_id}')

        return GuildMemberModel.from_dict(data)

    async def modify_current_user(self, **options: Unpack[EditUserParams]) -> UserModel:
        """Modify the bot's account settings.
        Fires [`UserUpdateEvent`][scurrypy.events.user_events.UserUpdateEvent].

        Args:
            options (EditUserParams): fields to edit

        Returns:
            (UserModel): edited user
        """
        if options.get('avatar'):
            options['avatar'] = options['avatar'].to_dict()

        if options.get('banner'):
            options['banner'] = options['banner'].to_dict()

        data = await self._http.request('PATCH', '/users/@me', data=options)

        return UserModel.from_dict(data)

    async def leave_guild(self, guild_id: int) -> None:
        """Make the bot leave a guild.
        Fires [`GuildDeleteEvent`][scurrypy.events.guild_events.GuildDeleteEvent]
        and [`GuildMemberRemoveEvent`][scurrypy.events.user_events.GuildMemberRemoveEvent].

        Args:
            guild_id (int): ID of the guild to leave
        """
        await self._http.request('DELETE', f'/users/@me/guilds/{guild_id}')

    async def create_dm(self, user_id: int) -> ChannelModel:
        """Create a DM between the bot and this user.

        Args:
            user_id (int): ID of user to create DM with
        
        Returns:
            (ChannelModel): created or existing DM channel
        """
        data = await self._http.request(
            'POST', 
            '/users/@me/channels', 
            data={'recipient_id': user_id}
        )

        return ChannelModel.from_dict(data)
