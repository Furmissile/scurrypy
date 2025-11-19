from dataclasses import dataclass
from typing import Optional, Unpack

from ..core.http import HTTPClient
from ..core.model import DataModel

from ..parts.modal import ModalPart
from ..parts.message import MessagePart, MessageFlagParams

from ..models import GuildModel, MemberModel, InteractionCallbackModel

from .channel import Channel

class InteractionDataTypes:
    """Interaction data types constants."""

    SLASH_COMMAND = 1
    """The interaction is a slash command."""

    USER_COMMAND = 2
    """The interaction is attached to a user."""

    MESSAGE_COMMAND = 3
    """The interaction is attached to a message."""

class InteractionCallbackTypes:
    """Interaction callback types constants."""

    PONG = 1
    """Acknowledge a Ping."""

    CHANNEL_MESSAGE_WITH_SOURCE = 4
    """Respond to an interaction with a message."""

    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    """Acknowledge an interaction and edit a response later. User sees a loading state."""

    DEFERRED_UPDATE_MESSAGE = 6
    """
        Acknowledge an interaction and edit the original message later. 
        The user does NOT see a loading state. (Components only)
    """

    UPDATE_MESSAGE = 7
    """Edit the message in which the component was attached."""

    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    """Respond to an autocomplete interaction with suggested choices."""

    MODAL = 9
    """Respond to an interaction with a popup modal (not available for MODAL_SUBMIT and PING interactions)."""

    LAUNCH_ACTIVITY = 12
    """Launch an activity associated with the app (Activities must be enabled)."""

@dataclass
class Interaction(DataModel):
    """Represents a Discord Interaction object."""

    id: int
    """ID of the interaction."""

    token: str
    """Continuation token for responding to the interaction."""

    _http: HTTPClient
    """HTTP session for requests."""

    type: int
    """Type of interaction. See [`InteractionTypes`][scurrypy.dispatch.command_dispatcher.InteractionTypes]."""

    channel_id: int
    """ID of the channel where the interaction was sent."""

    application_id: int
    """ID of the application that owns the interaction."""

    app_permissions: int
    """Bitwise set of permissions pertaining to the location of the interaction."""

    member: MemberModel = None # guild member invoking the interaction
    """Guild member invoking the interaction."""

    locale: str = None
    """Invoking user's locale."""

    guild_locale: str = None
    """Locale of the guild the interaction was invoked (if invoked in a guild)."""

    guild_id: Optional[int] = None
    """ID of guild the interaction was invoked (if invoked in a guild)."""

    guild: Optional[GuildModel] = None
    """Partial guild object of the guild the interaction was invoked (if invoked in a guild)."""

    channel: Optional[Channel] = None
    """Partial channel object the interaction was invoked."""

    def _prepare_message(self, message: MessagePart, t: int):
        """Prepares a message to be sent to HTTPClient.

        Args:
            message (MessagePart): the message content
            t (int): the interaction type. See [`InteractionTypes`][scurrypy.dispatch.command_dispatcher.InteractionTypes].

        Returns:
            (dict): the complete interaction content payload
        """
        # set attachment IDs (if any)
        if message.attachments:
            for idx, file in enumerate(message.attachments):
                file.id = idx

        return {'type': t, 'data': message.to_dict()}

    async def respond(self, message: str | MessagePart, with_response: bool = False, **flags: Unpack[MessageFlagParams]):
        """Create a message in response to an interaction.

        Args:
            message (str | MessagePart): content as a string or from MessagePart
            with_response (bool, optional): if the interaction data should be returned. Defaults to False.
            **flags: message flags to set. (set respective flag to True to toggle.)

        Raises:
            TypeError: invalid `message` type
        """
        if isinstance(message, str):
            message = MessagePart(content=message).set_flags(**flags)
        elif not isinstance(message, MessagePart):
            raise TypeError(f"Interaction.respond expects type str or MessagePart, got {type(message).__name__}")
        
        data = await self._http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data=self._prepare_message(message, InteractionCallbackTypes.CHANNEL_MESSAGE_WITH_SOURCE), 
            files=[fp.path for fp in message.attachments],
            params={'with_response': with_response}
        )

        if with_response:
            return InteractionCallbackModel.from_dict(data, self._http)
        
    async def update(self, message: str | MessagePart, **flags: Unpack[MessageFlagParams]):
        """Update a message in response to an interaction.

        Args:
            message (str | MessagePart): content as a string or from MessagePart
            **flags: message flags to set

        Raises:
            TypeError: invalid `message` type
        """
        if isinstance(message, str):
            message = MessagePart(content=message).set_flags(**flags)
        elif not isinstance(message, MessagePart):
            raise TypeError(f"Interaction.update expects type str or MessagePart, got {type(message).__name__}")

        await self._http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data=self._prepare_message(message, InteractionCallbackTypes.UPDATE_MESSAGE), 
            files=[fp.path for fp in message.attachments])

    async def respond_modal(self, modal: ModalPart):
        """Create a modal in response to an interaction.

        Args:
            modal (ModalPart): modal data

        Raises:
            TypeError: invalid `modal` type
        """
        if not isinstance(modal, ModalPart):
            raise TypeError(f"Interaction.respond_modal expects type ModalPart, got {type(modal).__name__}")
        
        content = {
            'type': InteractionCallbackTypes.MODAL,
            'data': modal.to_dict()
        }

        await self._http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data=content)
