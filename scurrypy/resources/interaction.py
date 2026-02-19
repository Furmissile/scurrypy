from dataclasses import dataclass
from typing import Unpack

from .base_resource import BaseResource

from ..core.snowflake import Snowflake
from ..core.serialization import serialize

from ..enums.message import MessageFlags
from ..enums.interaction import InteractionCallbackType

from ..api.interactions.modal import ModalPart
from ..api.interactions.interaction import InteractionCallbackModel
from ..api.messages.message import MessagePart
from ..api.commands.slash import CommandOptionChoicePart

from ..params.message import EditMessageParams

from .message import _EditMessageMixin

@dataclass
class Interaction(BaseResource, _EditMessageMixin):
    """Represents a Discord Interaction object."""

    id: Snowflake
    """ID of the interaction."""

    token: str
    """Continuation token for responding to the interaction."""

    async def respond(
        self, 
        message: str | MessagePart, 
        *, 
        with_response: bool = False, 
        ephemeral: bool = None, 
        suppress_embeds: bool = None
    ) -> InteractionCallbackModel | None:
        """Create a message in response to an interaction.
        Fires [`InteractionEvent`][scurrypy.events.interaction_events.InteractionEvent]
        and [`MessageCreateEvent`][scurrypy.events.message_events.MessageCreateEvent].

        Args:
            message (str | MessagePart): content as a string or MessagePart
            with_response (bool, optional): if the interaction data should be returned. Defaults to `False`.
            ephemeral (optional, bool): whether the response should be ephemeral
            suppress_embeds (optional, bool): whether the response's embeds should be removed

        Returns:
            (InteractionCallbackModel | None): interaction callback object (if `with_response` is toggled) else None
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        message.flags = MessageFlags.NO_FLAGS

        if ephemeral:
            message.flags |= MessageFlags.EPHEMERAL

        if suppress_embeds:
            message.flags |= MessageFlags.SUPPRESS_EMBEDS

        content = {
            'type': InteractionCallbackType.CHANNEL_MESSAGE_WITH_SOURCE, 
            'data': message._prepare().to_dict()
        }
        
        data = await self.http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data=content, 
            files=[fp.path for fp in message.attachments] if message.attachments else None,
            params={'with_response': with_response}
        )

        if with_response:
            return InteractionCallbackModel.from_dict(data)
        
    async def update(
        self,
        *,
        suppress_embeds: bool = None,
        **options: Unpack[EditMessageParams]
    ) -> None:
        """Edits the initial Interaction response.

        Args:
            options (EditMessageParams): fields to edit
            suppress_embeds (optional, bool): whether the response's embeds should be removed
        """
        options = serialize(options)
        self._apply_suppress_embeds(options, suppress_embeds)
        files = self._prepare_attachments(options)

        content = {
            "type": InteractionCallbackType.UPDATE_MESSAGE,
            "data": options,
        }

        await self.http.request(
            "POST",
            f"/interactions/{self.id}/{self.token}/callback",
            data=content,
            files=files
        )

    async def respond_modal(self, modal: ModalPart) -> None:
        """Create a modal in response to an interaction.
        Fires [`InteractionEvent`][scurrypy.events.interaction_events.InteractionEvent].

        Args:
            modal (ModalPart): modal data
        """
        content = {
            'type': InteractionCallbackType.MODAL,
            'data': modal.to_dict()
        }

        await self.http.request(
            'POST', 
            f'/interactions/{self.id}/{self.token}/callback', 
            data=content)

    async def respond_autocomplete(self, choices: list[CommandOptionChoicePart]) -> None:
        """Autocomplete a command in response to an interaction.
        Fires [`InteractionEvent`][scurrypy.events.interaction_events.InteractionEvent].

        Args:
            choices (list[CommandOptionChoicePart]): list of choices to autocomplete
        """
        content = {
            'type': InteractionCallbackType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT,
            'data': {
                'choices': [choice.to_dict() for choice in choices]
            }
        }

        await self.http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data=content
        )

    async def defer_respond(self, ephemeral: bool = None) -> None:
        """Defer creating a message in response to an interaction.
        Fires [`InteractionEvent`][scurrypy.events.interaction_events.InteractionEvent].

        Args:
            ephemeral (bool, optional): whether thinking + deferred interaction response is ephemeral
        """
        content = {
            'type': InteractionCallbackType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE,
            'data': {
                'flags': MessageFlags.EPHEMERAL if ephemeral else MessageFlags.NO_FLAGS
            }
        }

        await self.http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data=content
        )

    async def defer_update(self) -> None:
        """Defer updating a message in response to an interaction.
        Fires [`InteractionEvent`][scurrypy.events.interaction_events.InteractionEvent].
        """
        content = {
            'type': InteractionCallbackType.DEFERRED_UPDATE_MESSAGE,
        }

        await self.http.request(
            'POST',
            f'/interactions/{self.id}/{self.token}/callback',
            data=content
        )

    async def followup(
        self, 
        application_id: Snowflake, 
        message: str | MessagePart, 
        ephemeral: bool = None,
        suppress_embeds: bool = None
    ) -> None:
        """Create a new message to respond to a deferred interaction.
        Fires [`MessageCreateEvent`][scurrypy.events.message_events.MessageCreateEvent].

        !!! important
            Apps are limited to 5 followup messages PER interaction.

        Args:
            application_id (Snowflake): ID of the application
            message (str | MessagePart): content as a string or MessagePart
            ephemeral (optional, bool): whether the followup should be ephemeral
            suppress_embeds (optional, bool): whether the followup's embeds should be removed
        """
        if isinstance(message, str):
            message = MessagePart(content=message)

        message.flags = MessageFlags.NO_FLAGS

        if ephemeral:
            message.flags |= MessageFlags.EPHEMERAL

        if suppress_embeds:
            message.flags |= MessageFlags.SUPPRESS_EMBEDS

        content = message._prepare().to_dict()

        await self.http.request(
            'POST',
            f'/webhooks/{application_id}/{self.token}',
            data=content
        )

    async def edit_original(
        self,
        application_id: Snowflake,
        *,
        suppress_embeds: bool = None,
        **options: Unpack[EditMessageParams]
    ) -> None:
        """Edits the initial Interaction response.

        Args:
            application_id (Snowflake): bot's user ID
            options (EditMessageParams): fields to edit
            suppress_embeds (optional, bool): whether the response's embeds should be removed
        """
        options = serialize(options)
        self._apply_suppress_embeds(options, suppress_embeds)
        files = self._prepare_attachments(options)

        await self.http.request(
            "PATCH",
            f"/webhooks/{application_id}/{self.token}/messages/@original",
            data=options,
            files=files
        )
