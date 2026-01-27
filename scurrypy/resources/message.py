from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..models.emoji import EmojiModel,  ReactionTypes
from ..models.message import MessageModel
from ..models.user import UserModel

from ..parts.message import MessagePart

from ..params.message import EditMessageParams

@dataclass
class Message(BaseResource):
    """A Discord message."""

    id: int
    """ID of the message"""

    channel_id: int
    """Channel ID of the message."""

    async def fetch(self) -> MessageModel:
        """Fetches the message data based on the given channel ID and message id.

        Returns:
            (MessageModel): queried message
        """
        data = await self._http.request('GET', f"/channels/{self.channel_id}/messages/{self.id}")

        return MessageModel.from_dict(data)
    
    async def edit(self, **options: Unpack[EditMessageParams]) -> MessageModel:
        """Edits this message.
        Fires [`MessageUpdateEvent`][scurrypy.events.message_events.MessageUpdateEvent].

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES` *only* if editing another user's message or to edit flags

        Args:
            options (EditMessageParams): fields to edit for the message

        Returns:
            (MessageModel): updated message
        """
        message = MessagePart(**options)

        data = await self._http.request(
            "PATCH", 
            f"/channels/{self.channel_id}/messages/{self.id}", 
            data=message._prepare().to_dict(),
            files=[fp.path for fp in message.attachments] if message.attachments else None)

        return MessageModel.from_dict(data)

    async def crosspost(self) -> MessageModel:
        """Crosspost this message in an Annoucement channel to all following channels.
        Fires [`MessageUpdateEvent`][scurrypy.events.message_events.MessageUpdateEvent].

        !!! important "Permissions"
            * `SEND_MESSAGES` → required to publish your own messages
            * `MANAGE_MESSAGES` → required to publish messages from others

        Returns:
            (MessageModel): published (crossposted) message
        """
        data = await self._http.request('POST', f'/channels/{self.channel_id}/messages/{self.id}/crosspost')

        return MessageModel.from_dict(data)

    async def delete(self):
        """Deletes this message.
        Fires [`MessageDeleteEvent`][scurrypy.events.message_events.MessageDeleteEvent].
        """
        await self._http.request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}")

    async def pin(self) -> None:
        """Pin this message to its channel's pins.
        Fires [`ChannelPinsUpdateEvent`][scurrypy.events.channel_events.ChannelPinsUpdateEvent].
        """
        await self._http.request('PUT', f'/channels/{self.channel_id}/messages/pins/{self.id}')
    
    async def unpin(self) -> None:
        """Unpin this message from its channel's pins.
        Fires [`ChannelPinsUpdateEvent`][scurrypy.events.channel_events.ChannelPinsUpdateEvent].
        """
        await self._http.request('DELETE', f'/channels/{self.channel_id}/messages/pins/{self.id}')

    async def fetch_emoji_reactions(self, emoji: EmojiModel | str, type: int = ReactionTypes.NORMAL, after: int = None, limit: int = 25) -> list[UserModel]:
        """Fetches users who reacted with the specified emoji parameters.

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
            type (int, optional): Type of emoji. Defaults to `ReactionTypes.NORMAL`.
            after (int, optional): users after this ID
            limit (int, optional): Max number of users to return. Defaults to `25`.

        Returns:
            list[UserModel]: list of users who reacted with this emoji
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        data = self._http.request(
            'GET',
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}",
            params={
                'type': type,
                'after': after,
                'limit': limit
            }
        )
        return [UserModel.from_dict(user) for user in data]

    async def add_reaction(self, emoji: EmojiModel | str) -> None:
        """Add a reaction to this message.
        Fires [`MessageReactionAddEvent`][scurrypy.events.reaction_events.ReactionAddEvent].

        !!! important "Permissions"
            Requires `READ_MESSAGE_HISTORY` and `ADD_REACTIONS`

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self._http.request(
            "PUT",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_reaction(self, emoji: EmojiModel | str) -> None:
        """Remove the bot's reaction from this message.
        Fires [`MessageReactionRemoveEvent`][scurrypy.events.reaction_events.ReactionRemoveEvent].

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_user_reaction(self, emoji: EmojiModel | str, user_id: int) -> None:
        """Remove a specific user's reaction from this message.
        Fires [`MessageReactionRemoveEvent`][scurrypy.events.reaction_events.ReactionRemoveEvent].

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
            user_id (int): user's ID
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)

        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/{user_id}")

    async def remove_emoji_reaction(self, emoji: EmojiModel | str) -> None:
        """Clear all reactions for a given emoji from this message.

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`

        Args:
            emoji (EmojiModel | str): the standard emoji (str) or custom emoji (EmojiModel)
        """
        if isinstance(emoji, str):
            emoji = EmojiModel(emoji)
        
        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions/{emoji.api_code}/@me")

    async def remove_all_reactions(self) -> None:
        """Clear all reactions from this message.
        Fires [`MessageReactionRemoveAllEvent`][scurrypy.events.reaction_events.ReactionRemoveAllEvent].

        !!! important "Permissions"
            Requires `MANAGE_MESSAGES`
        """
        await self._http.request(
            "DELETE",
            f"/channels/{self.channel_id}/messages/{self.id}/reactions")
