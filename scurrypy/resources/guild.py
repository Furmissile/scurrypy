from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..parts.image_data import ImageAssetPart
from ..parts.guild import BulkGuildBanPart, GuildStickerPart
from ..parts.channel import GuildChannelPart
from ..parts.role import GuildRolePart

from ..models.role import RoleModel
from ..models.guild import GuildModel, GuildBanModel, BulkGuildBanModel, GuildWelcomeScreenModel, GuildOnboadingModel
from ..models.user import GuildMemberModel
from ..models.channel import ChannelModel, ActiveThreadsModel
from ..models.invite import InviteModel, InviteWithMetadataModel
from ..models.integration import IntegrationModel
from ..models.sticker import StickerModel

from ..params.guild import EditGuildRoleParams, EditGuildParams, EditGuildWelcomeScreenParams, EditOnboardingParams, EditGuildStickerParams
from ..params.user import EditGuildMemberParams

@dataclass
class Guild(BaseResource):
    """Represents a Discord guild."""
    
    id: int
    """ID of the guild."""

    # GUILD
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

    async def edit(self, **options: Unpack[EditGuildParams]) -> GuildModel:
        """Edit this guild.
        Fires [`GuildUpdateEvent`][scurrypy.events.guild_events.GuildUpdateEvent].

        Args:
            options (EditGuildParams): guild with fields to edit

        Returns:
            (GuildModel): edited guild
        """
        if options.get('banner'):
            options['banner'] = options['banner'].to_dict()
        
        if options.get('discovery_splash'):
            options['discovery_splash'] = options['discovery_splash'].to_dict()

        if options.get('icon'):
            options['icon'] = options['icon'].to_dict()

        if options.get('splash'):
            options['splash'] = options['splash'].to_dict()

        data = await self._http.request('PATCH', f'/guilds/{self.id}', data=options)

        return GuildModel.from_dict(data)

    # --- CHANNELS ---
    async def fetch_channels(self) -> list[ChannelModel]:
        """Fetch this guild's channels.

        !!! note
            Does not include threads!

        Returns:
            (list[ChannelModel]): queried list of the guild's channels
        """
        data = await self._http.request('GET', f'guilds/{self.id}/channels')

        return [ChannelModel.from_dict(channel) for channel in data]
    
    async def fetch_active_threads(self) -> ActiveThreadsModel:
        """Fetch all active threads in a guild (private and public).

        !!! note
            Threads are ordered by their ID in descending order.

        Returns:
            (ActiveThreadsModel): active guild threads
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/threads/active')

        return ActiveThreadsModel.from_dict(data)

    async def create_channel(self, channel: GuildChannelPart) -> ChannelModel:
        """Create a channel in this guild.
        Fires [`ChannelCreateEvent`][scurrypy.events.channel_events.ChannelCreateEvent].

        !!! important "Permissions"
            Requires `MANAGE_CHANNELS`

        Args:
            channel (GuildChannelPart): the guild channel to create

        Returns:
            (ChannelModel): created channel
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/channels', data=channel.to_dict())

        return ChannelModel.from_dict(data)

    # --- GUILD MEMBERS ---
    async def fetch_member(self, user_id: int) -> GuildMemberModel:
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

    async def fetch_members(self, limit: int = 1, after: int = None) -> list[GuildMemberModel]:
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

    async def add_member_role(self, user_id: int, role_id: int) -> None:
        """Append a role to a guild member of this guild.
        Fires [`GuildMemberUpdateEvent`][scurrypy.events.user_events.GuildMemberUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`
        
        Args:
            user_id (int): ID of the member for the role
            role_id (int): ID of the role to append
        """
        await self._http.request('PUT', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')
    
    async def remove_member_role(self, user_id: int, role_id: int) -> None:
        """Remove a role from a guild member of this guild.
        Fires [`GuildMemberUpdateEvent`][scurrypy.events.user_events.GuildMemberUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            user_id (int): ID of the member with the role
            role_id (int): ID of the role to remove
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/members/{user_id}/roles/{role_id}')

    async def search_members(self, query: str = None, limit: int = 1) -> list[GuildMemberModel]:
        """Fetch guild members whose username or nickname starts with the provided query.

        Args:
            query (str, optional): query string to match against
            limit (int, optional): Max number of members to return. Max `1000`. Defaults to `1`.

        Returns:
            list[GuildMemberModel]: queried list of guild members
        """
        data = await self._http.request(
            'GET', 
            f'guild/{self.id}/members/search',
            params={
                'query': query,
                'limit': limit
            }
        )

        return [GuildMemberModel.from_dict(m) for m in data]

    async def edit_member(self, user_id: int, **options: Unpack[EditGuildMemberParams]) -> GuildMemberModel:
        """Edit a guild member's attributes.
        Fires [`GuildMemberUpdateEvent`][scurrypy.events.user_events.GuildMemberUpdateEvent].

        Args:
            user_id (int): ID of the member to edit

        Returns:
            (GuildMemberModel): edited guid member
        """
        data = await self._http.request('PATCH', f'/guilds/{self.id}/members/{user_id}', data=options)

        return GuildMemberModel.from_dict(data)

    async def remove_member(self, user_id: int) -> None:
        """Remove a member from this guild.
        Fires [`GuildMemberRemoveEvent`][scurrypy.events.user_events.GuildMemberRemoveEvent].

        !!! important "Permissions"
            Requires `KICK_MEMBERS`

        Args:
            user_id (int): ID of the user to kick
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/members/{user_id}')

    # --- BANS ---
    async def fetch_ban(self, user_id: int) -> GuildBanModel:
        """Fetch a guild ban for the given user ID.

        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (int): ID of the user to fetch

        Returns:
            (GuildBan): queried ban
        """
        data = self._http.request('GET', f'/guild/{self.id}/bans/{user_id}')

        return GuildBanModel.from_dict(data)

    async def fetch_bans(self, limit: int = 1000, before: int = None, after: int = None) -> list[GuildBanModel]:
        """Fetch bans in this guild.

        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            limit (int, optional): max number of users to return. Defaults to `1000`.
            before (int, optional): fetch users before this ID
            after (int, optional): fetch users after this ID

        Returns:
            (list[GuildBan]): queried list of guild bans
        """
        data = await self._http.request(
            'GET',
            f'/guilds/{self.id}/bans',
            params={
                'limit': limit,
                'before': before,
                'after': after
            }
        )

        return [GuildBanModel.from_dict(i) for i in data]

    async def create_ban(self, user_id: int, delete_message_seconds: int = 0) -> None:
        """Create a guild ban and optionally delete messages sent by the banned user.
        Fires [`GuildBanAddEvent`][scurrypy.events.guild_events.GuildBanAddEvent].
        
        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (int): ID of the user to ban
            delete_message_seconds (int, optional): seconds back to delete messages. Max `604800` (7 days). Defaults to `0`.
        """
        await self._http.request(
            'PUT',
            f'/guilds/{self.id}/bans/{user_id}',
            params={'delete_message_seconds': delete_message_seconds}
        )

    async def remove_ban(self, user_id: int) -> None:
        """Remove the ban for a user.
        Fires [`GuildBanRemoveEvent`][scurrypy.events.guild_events.GuildBanRemoveEvent].

        !!! important "Permissions"
            Requires `BAN_MEMBERS`

        Args:
            user_id (int): ID of the user in which to remove the ban
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/bans/{user_id}')

    async def bulk_create_ban(self, bulk_ban: BulkGuildBanPart) -> BulkGuildBanModel:
        """Create guild bans and optionally delete messages sent by the banned users.

        !!! important "Permissions"
            Requires `BAN_MEMBERS` and `MANAGE_GUILD`

        Args:
            bulk_ban (BulkGuildBanPart): bulk ban to create
            
        Returns:
            (BulkGuildBanModel): bulk ban response
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/bulk-ban', data=bulk_ban.to_dict())

        return BulkGuildBanModel.from_dict(data)

    # --- ROLES ---
    async def fetch_role_member_counts(self) -> dict:
        """Fetch a map of role IDs to number of members with the role.

        !!! note
            Does not include `@everyone` role.

        Returns:
            (dict): map of role IDs to member count
        """
        return await self._http.request('GET', f'/guilds/{self.id}/roles/member-counts')

    async def fetch_role(self, role_id: int) -> RoleModel:
        """Fetch a role in this guild.

        Args:
            role_id (int): ID of the role to fetch

        Returns:
            (RoleModel): queried guild role
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/roles/{role_id}')
        
        return RoleModel.from_dict(data)
    
    async def fetch_roles(self) -> list[RoleModel]:
        """Fetch all roles in this guild.

        Returns:
            (list[RoleModel]): queried list of guild roles
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/roles')
        
        return [RoleModel.from_dict(role) for role in data]

    async def create_role(self, role: GuildRolePart) -> RoleModel:
        """Create a role in this guild.
        Fires [`RoleCreateEvent`][scurrypy.events.role_events.RoleCreateEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role (GuildRolePart): fields to create a role

        Returns:
            (RoleModel): created role
        """
        data = await self._http.request('POST', f'/guilds/{self.id}/roles', data=role.to_dict())

        return RoleModel.from_dict(data)

    async def edit_role(self, role_id: int, **options: Unpack[EditGuildRoleParams]) -> RoleModel:
        """Edit a role in this guild.
        Fires [`RoleUpdateEvent`][scurrypy.events.role_events.RoleUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role_id (int): ID of role to edit
            options (EditGuildRoleParams): role with fields to edit

        Returns:
            (RoleModel): edited role
        """
        if options.get('colors'):
            options['colors'] = options['colors'].to_dict()

        if options.get('icon'):
            options['icon'] = options['icon'].to_dict()

        data = await self._http.request('PATCH', f'/guilds/{self.id}/roles/{role_id}', data=options)

        return RoleModel.from_dict(data)

    async def delete_role(self, role_id: int) -> None:
        """Delete a role in this guild.
        Fires [`RoleDeleteEvent`][scurrypy.events.role_events.RoleDeleteEvent].

        !!! important "Permissions"
            Requires `MANAGE_ROLES`

        Args:
            role_id (int): ID of role to delete
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/roles/{role_id}')

    # --- INVITES ---
    async def fetch_invites(self) -> list[InviteModel]:
        """Fetch this guild's invites with no metadata.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` or `VIEW_AUDIT_LOG`

        Returns:
            (list[InviteModel]): queried list of invites without metadata
        """
        data = await self._http.request('GET', f'/guild/{self.id}/invites')

        return [InviteModel.from_dict(i) for i in data]

    async def fetch_invites_with_metadata(self) -> list[InviteWithMetadataModel]:
        """Fetch this guild's invites with metadata.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` and `MANAGE_GUILD` or `VIEW_AUDIT_LOG`

        Returns:
            (list[InviteModel]): queried list of invites with metadata
        """
        data = await self._http.request('GET', f'/guild/{self.id}/invites')

        return [InviteWithMetadataModel.from_dict(i) for i in data]

    # --- INTEGRATIONS ---
    async def fetch_integrations(self) -> list[IntegrationModel]:
        """Fetch this guild's integrations.

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Returns:
            (list[IntegrationModel]): queried integrations
        """
        data = await self._http.request('GET', f'/guild/{self.id}/integrations')

        return [IntegrationModel.from_dict(i) for i in data]

    async def delete_integration(self, integration_id: int) -> None:
        """Delete the attached integration object for this guild.
        Fires [`GuildIntegrationUpdateEvent`][scurrypy.events.integration_events.GuildIntegrationUpdateEvent] 
        and [`GuildIntegrationDeleteEvent`][scurrypy.events.integration_events.GuildIntegrationDeleteEvent].

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            integration_id (int): ID of the integration to delete
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/integrations/{integration_id}')

    # --- WELCOME SCREEN ---
    async def fetch_welcome_screen(self) -> GuildWelcomeScreenModel:
        """Fetch the welcome screen for this guild.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` if welcome screen is not enabled

        Returns:
            (GuildWelcomeScreenModel): queried welcome screen
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/welcome-screen')

        return GuildWelcomeScreenModel.from_dict(data)

    async def edit_welcome_screen(self, **options: Unpack[EditGuildWelcomeScreenParams]) -> GuildWelcomeScreenModel:
        """Edit this guild's welcome screen.
        May fire [`GuildUpdateEvent`][scurrypy.events.guild_events.GuildUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_GUILD`

        Args:
            options (EditGuildWelcomeScreen): fields to edit

        Returns:
            (GuildWelcomeScreenModel): edited welcome screen
        """
        if options.get('welcome_channels'):
            options['welcome_channels'] = [i.to_dict() for i in options['welcome_channels']]

        data = await self._http.request('PATCH', f'/guilds/{self.id}/welcome-screen', data=options)

        return GuildWelcomeScreenModel.from_dict(data)

    # --- ONBOARDING ---
    async def fetch_onboarding(self) -> GuildOnboadingModel:
        """Fetch this guild's onboarding flow.

        Returns:
            (GuildOnboadingModel): queried onboarding flow
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/onboarding')

        return GuildOnboadingModel.from_dict(data)

    async def edit_onboarding(self, **options: Unpack[EditOnboardingParams]) -> GuildOnboadingModel:
        """Modifies this guild's onboarding flow.

        !!! important "Permissions"
            Requires `MANAGE_GUILD` and `MANAGE_ROLES`

        !!! note
            Must be at least **7** Default Channels and at least **5** allow sending message to the @everyone role.
            Constraints depend on the new `mode`.

        Args:
            options (EditOnboardingParams): onboarding field to edit

        Returns:
            (GuildOnboadingModel): edited onboarding flow
        """
        if options.get('prompts'):
            options['prompts'] = [i.to_dict() for i in options['prompts']]
            
        data = await self._http.request(
            'PUT',
            f'/guilds/{self.id}/onboarding',
            params=options
        )
        return GuildOnboadingModel.from_dict(data)

    # --- STICKERS ---
    async def fetch_sticker(self, sticker_id: int) -> StickerModel:
        """Fetch a sticker from this guild.

        !!! note
            Includes the `user` field if the bot has
            `CREATE_GUILD_EXPRESSIONS` and `MANAGE_GUILD_EXPRESSIONS`

        Args:
            sticker_id (int): ID of the sticker to fetch

        Returns:
            (StickerModel): queried sticker
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/stickers/{sticker_id}')

        return StickerModel.from_dict(data)

    async def fetch_stickers(self) -> list[StickerModel]:
        """Fetch this guild's stickers.

        !!! note
            Includes the `user` field if the bot has
            `CREATE_GUILD_EXPRESSIONS` and `MANAGE_GUILD_EXPRESSIONS`

        Returns:
            list[StickerModel]: queried guild stickers
        """
        data = await self._http.request('GET', f'/guilds/{self.id}/stickers')

        return [StickerModel.from_dict(i) for i in data]

    async def create_sticker(self, sticker: GuildStickerPart, file: ImageAssetPart) -> StickerModel:
        """Add a sticker to this guild.
        Fires [`GuildStickersUpdateEvent`][scurrypy.events.guild_events.GuildStickersUpdateEvent].

        !!! important "Permissions"
            Requires `CREATE_GUILD_EXPRESSIONS`

        Args:
            sticker (GuildStickerPart): sticker to create
            file (ImageAssetPart): the sticker file to upload
                !!! note
                    Accepted file types: PNG, APNG, GIF, Lottie JSON file.

        Returns:
            (StickerModel): created sticker
        """
        data = await self._http.request(
            'POST', f'/guilds/{self.id}/stickers', 
            data=sticker.to_dict(),
            assets=file.to_dict()
        )
    
        return StickerModel.from_dict(data)

    async def edit_sticker(self, sticker_id: int, **options: Unpack[EditGuildStickerParams]) -> StickerModel:
        """Edit a sticker from this guild.
        Fires [`GuildStickersUpdateEvent`][scurrypy.events.guild_events.GuildStickersUpdateEvent].

        !!! important "Permissions"
            Requires `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS`.
            Requires `MANAGE_GUILD_EXPRESSIONS` if not created by the bot.

        Args:
            sticker_id (int): ID of the sticker to delete
            options (EditGuildStickerParams): fields to edit
        """
        data = await self._http.request('PATCH', f'/guilds/{self.id}/stickers/{sticker_id}', data=options)

        return StickerModel.from_dict(data)

    async def delete_sticker(self, sticker_id: int) -> None:
        """Delete a sticker from this guild.
        Fires [`GuildStickersUpdateEvent`][scurrypy.events.guild_events.GuildStickersUpdateEvent].

        !!! important "Permissions"
            Requires `CREATE_GUILD_EXPRESSIONS` or `MANAGE_GUILD_EXPRESSIONS`.
            Requires `MANAGE_GUILD_EXPRESSIONS` if not created by the bot.

        Args:
            sticker_id (int): ID of the sticker to delete
        """
        await self._http.request('DELETE', f'/guilds/{self.id}/stickers/{sticker_id}')
