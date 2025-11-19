from dataclasses import dataclass
from typing import Optional, TypedDict, Unpack

from ..core.http import HTTPClient
from ..core.model import DataModel

from ..models import GuildModel, MemberModel

class FetchUserGuildsParams(TypedDict, total=False):
    before: int
    """Get guilds before this guild ID."""

    after: int
    """Get guilds after this guild ID."""

    limit: int
    """Max number of guilds to return. Range 1 - 200. Default 200."""

    with_counts: bool
    """Include approximate member and presence count."""

@dataclass
class User(DataModel):
    """A Discord user."""

    id: int
    """ID of the user."""

    _http: HTTPClient
    """HTTP session for requests."""

    username: str = None
    """Username of the user."""

    discriminator: str = None
    """Discriminator of the user (#XXXX)"""

    global_name: str = None
    """Global name of the user."""

    avatar: str = None
    """Image hash of the user's avatar."""

    bot: Optional[bool] = None
    """If the user is a bot."""

    system: Optional[bool] = None
    """If the user belongs to an OAuth2 application."""

    mfa_enabled: Optional[bool] = None
    """Whether the user has two factor enabled."""

    banner: Optional[str] = None
    """Image hash of the user's banner."""

    accent_color: Optional[int] = None
    """Color of user's banner represented as an integer."""

    locale: Optional[str] = None
    """Chosen language option of the user."""

    async def fetch(self):
        """Fetch this user by ID.
        !!! note
            Fetch includes both /users/@me AND /users/{user.id}!

        Returns:
            (User): the User object
        """
        data = await self._http.request('GET', f'/users/{self.id}')

        return User.from_dict(data, self._http)
    
    async def fetch_guilds(self, **kwargs: Unpack[FetchUserGuildsParams]):
        """Fetch this user's guilds.
        !!! warning "Important"
            Requires the OAuth2 guilds scope!

        Args:
            **kwargs: user guilds fetch params
                !!! note
                    If no kwargs are provided, default to 200 guilds limit.

        Returns:
            (list[GuildModel]): each guild's data
        """
        params = {
            'limit': 200,
            'with_counts': False,
            **kwargs
        }

        data = await self._http.request('GET', '/users/@me/guilds', params=params)

        return [GuildModel.from_dict(guild) for guild in data]

    async def fetch_guild_member(self, guild_id: int):
        """Fetch this user's guild member data.
        !!! warning "Important"
            Requires the OAuth2 guilds.members.read scope!

        Args:
            guild_id (int): ID of guild to fetch data from

        Returns:
            (MemberModel): member data from guild
        """
        data = await self._http.request('GET', f'/users/@me/{guild_id}/member')

        return MemberModel.from_dict(data)
