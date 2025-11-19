from dataclasses import dataclass
from typing import TypedDict, Unpack, Optional, Literal

from ..core.http import HTTPClient
from ..core.model import DataModel
from .message import Message

from ..parts.channel import GuildChannel
from ..parts.message import MessagePart

class MessagesFetchParams(TypedDict, total=False):
    """Params when fetching guild channel messages."""

    limit: int
    """Max number of messages to return. Range 1 - 100. Default 50."""

    before: int
    """Get messages before this message ID."""

    after: int
    """Get messages after this message ID."""

    around: int
    """Get messages around this message ID."""

class PinsFetchParams(TypedDict, total=False):
    """Params when fetching pinned messages."""

    before: str
    """Get pinned messages before this ISO8601 timestamp."""

    limit: int
    """Max number of pinned messages to return. Range 1 - 50. Default 50."""

class ThreadFromMessageParams(TypedDict, total=False):
    """Params when attaching a thread to a message."""

    rate_limit_per_user: Literal[60, 1440, 4320, 10080]
    """time (minutes) of inactivity before thread is archived."""

    rate_limit_per_user: int
    """time (seconds) user waits before sending another message."""

@dataclass
class PinnedMessage(DataModel):
    """Pinned message data."""

    message: Message
    """Message resource of the pinned message."""

    pinned_at: Optional[str] = None
    """ISO8601 timestamp of when the message was pinned."""

@dataclass
class Channel(DataModel):
    """Represents a Discord guild channel."""

    id: int
    """ID of the channel."""

    _http: HTTPClient
    """HTTP session for requests."""

    type: Optional[int] = None
    """Type of channel."""

    guild_id: Optional[int] = None
    """Guild ID of the channel."""

    parent_id: Optional[int] = None
    """Category ID of the channel."""

    position: Optional[int] = None
    """Position of the channel."""

    name: Optional[str] = None
    """Name of the channel."""

    topic: Optional[str] = None
    """Topic of the channel."""

    nsfw: Optional[bool] = None
    """If the channel is flagged NSFW."""

    last_message_id: Optional[int] = None
    """ID of the last message sent in the channel."""

    last_pin_timestamp: Optional[str] = None
    """ISO8601 timestamp of the last pinned messsage in the channel."""

    rate_limit_per_user: Optional[int] = None
    """Seconds user must wait between sending messages in the channel."""

    def _update(self, data: dict):
        """Update this channel in place.

        Args:
            data (dict): channel data as a dict
        """
        self.__dict__.update(Channel.from_dict(data, self._http).__dict__)

    async def fetch(self):
        """Fetch the full channel data from Discord.

        Returns:
            (Channel): A new Channel object with all fields populated
        """
        data = await self._http.request("GET", f"/channels/{self.id}")

        # Hydrate a new Channel object with HTTP client    
        return Channel.from_dict(data, self._http)
    
    async def fetch_messages(self, **kwargs: Unpack[MessagesFetchParams]):
        """Fetches this channel's messages.

        Permissions:
            * VIEW_CHANNEL → required to access channel messages
            * READ_MESSAGE_HISTORY → required for user, otherwise no messages are returned

        Args:
            **kwargs: message fetch params
                !!! note
                    if no kwargs are provided, default to 50 fetched messages limit.

        Returns:
            (list[Message]): queried messages
        """
        # Set default limit if user didn't supply one
        params = {"limit": 50, **kwargs}

        data = await self._http.request('GET', f'/channels/{self.id}/messages', params=params)

        return [Message.from_dict(msg, self._http) for msg in data]
    
    async def send(self, message: str | MessagePart):
        """
        Send a message to this channel.

        Permissions:
            * SEND_MESSAGES → required to create a message in this channel

        Args:
            message (str | MessagePart): can be just text or the MessagePart for dynamic messages

        Returns:
            (Message): The created Message object
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        data = await self._http.request("POST", f"/channels/{self.id}/messages", data=message.to_dict())

        return Message.from_dict(data, self._http)

    async def edit(self, channel: GuildChannel):
        """Edit this channel's settings.

        Permissions:
            * MANAGE_CHANNELS → required to edit this channel

        Args:
            channel (GuildChannel): channel changes

        Returns:
            (Channel): The updated channel object
        """
        data = await self._http.request("PATCH", f"/channels/{self.id}", data=channel.to_dict())
        self._update(data)

        return self
    
    async def create_thread_from_message(self, message_id: int, name: str, **kwargs: Unpack[ThreadFromMessageParams]):
        """Create a thread from this message

        Args:
            message_id: ID of message to attach thread
            name (str): thread name
            **kwargs (Unpack[ThreadFromMessageParams]): thread create params

        Returns:
            (Channel): The updated channel object
        """

        content = {
            'name': name, 
            **kwargs
        }

        data = await self._http.request('POST', f"channels/{self.id}/messages/{message_id}/threads", data=content)

        return Channel.from_dict(data, self._http)
    
    async def fetch_pins(self, **kwargs: Unpack[PinsFetchParams]):
        """Get this channel's pinned messages.

        Permissions:
            * VIEW_CHANNEL → required to access pinned messages
            * READ_MESSAGE_HISTORY → required for reading pinned messages

        Args:
            **kwargs: pinned message fetch params
                !!! note
                    If no kwargs are provided, default to 50 fetched messages limit.
            
        Returns:
            (list[PinnedMessage]): list of pinned messages
        """
        # Set default limit if user didn't supply one
        params = {"limit": 50, **kwargs}

        data = await self._http.request('GET', f'/channels/{self.id}/pins', params=params)

        pins = [Message.from_dict(item, self._http) for item in data]
        return pins

    async def delete(self):
        """Deletes this channel from the server.

        Permissions:
            * MANAGE_CHANNELS → required to delete this channel
        """
        await self._http.request("DELETE", f"/channels/{self.id}")
