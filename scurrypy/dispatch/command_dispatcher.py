import fnmatch

from ..core.client_like import ClientLike

from ..events.interaction_events import ApplicationCommandData, MessageComponentData, ModalData, InteractionEvent
from ..resources.interaction import Interaction, InteractionDataTypes
from ..parts.command import SlashCommand, MessageCommand, UserCommand

class InteractionTypes:
    """Interaction types constants."""

    APPLICATION_COMMAND = 2
    """Slash command interaction."""

    MESSAGE_COMPONENT = 3
    """Message component interaction (e.g., button, select menu, etc.)."""

    MODAL_SUBMIT = 5
    """Modal submit interaction."""

class CommandDispatcher:
    """Central hub for registering and dispatching interaction responses."""

    RESOURCE_MAP = { # maps discord events to their respective dataclass
        InteractionTypes.APPLICATION_COMMAND: ApplicationCommandData,
        InteractionTypes.MESSAGE_COMPONENT: MessageComponentData,
        InteractionTypes.MODAL_SUBMIT: ModalData
    }
    """Maps [`InteractionTypes`][scurrypy.dispatch.command_dispatcher.InteractionTypes] to their respective dataclass."""

    def __init__(self, client: ClientLike):
        
        self.application_id = client.application_id
        """Bot's application ID."""

        self.bot = client
        """Bot session for user access to bot."""

        self._http = client._http
        """HTTP session for requests."""

        self._logger = client._logger
        """Logger instance to log events."""

        self._global_commands = []
        """List of all Global commands."""

        self._guild_commands = {}
        """Guild commands mapped by guild ID."""

        self.component_handlers = {}
        """Mapping of component custom IDs to handler."""

        self.slash_handlers = {}
        """Mapping of command names to handler."""

        self.message_handlers = {}
        """Mapping of message command names to handler."""

        self.user_handlers = {}
        """Mapping of user command names to handler."""

    async def register_guild_commands(self):
        """Registers commands at the guild level."""
        
        for guild_id, cmds in self._guild_commands.items():
            # register commands PER GUILD
            await self._http.request(
                'PUT', 
                f"applications/{self.application_id}/guilds/{guild_id}/commands", 
                data=[command.to_dict() for command in cmds]
            )
    
    async def register_global_commands(self):
        """Registers a command at the global/bot level. (ALL GUILDS)"""

        await self._http.request(
            'PUT', 
            f"applications/{self.application_id}/commands", 
            data=[command.to_dict() for command in self._global_commands]
        )

    def _queue_command(self, command: SlashCommand | UserCommand | MessageCommand, guild_ids: list[int] = None):
        """Queue a command to be registered by Discord.

        Args:
            command (SlashCommand | UserCommand | MessageCommand): the command object
            guild_ids (list[int], optional): guild IDs to register command to (if any)
        """
        
        if guild_ids:
            gids = [guild_ids] if isinstance(guild_ids, int) else guild_ids
            for gid in gids:
                self._guild_commands.setdefault(gid, []).append(command)
        else:
            self._global_commands.append(command)

    def clear_commands(self, guild_ids: list[int] = None):
        """Clear a guild's or global commands (all types).

        Args:
            guild_ids (list[int], optional): guild IDs to register command to (if any)
        """
        if guild_ids:
            gids = [guild_ids] if isinstance(guild_ids, int) else guild_ids
            for gid in gids:
                removed = self._guild_commands.pop(gid, None)
                if removed is None:
                    self._logger.log_warn(f"Guild ID {gid} not found; skipping...")
        else:
            self._global_commands.clear()

    def add_slash_command(self, command: SlashCommand, handler, guild_ids: list[int]):
        """Add a slash command to be registered by Discord.

        Args:
            command (SlashCommand): the command object
            handler (callable): user-defined callback when this command is invoked
            guild_ids (list[int]): guild IDs to register command to (if any)
        """
        self.slash_handlers[command.name] = handler
        self._queue_command(command, guild_ids)

    def add_message_command(self, command: MessageCommand, handler, guild_ids: list[int]):
        """Add a slash command to be registered by Discord.

        Args:
            command (MessageCommand): the command object
            handler (callable): user-defined callback when this command is invoked
            guild_ids (list[int]): guild IDs to register command to (if any)
        """
        self.message_handlers[command.name] = handler
        self._queue_command(command, guild_ids)

    def add_user_command(self, command: UserCommand, handler, guild_ids: list[int]):
        """Add a user command to be registered by Discord.

        Args:
            command (UserCommand): the command object
            handler (callable): user-defined callback when this command is invoked
            guild_ids (list[int]): guild IDs to register command to (if any)
        """
        self.user_handlers[command.name] = handler
        self._queue_command(command, guild_ids)

    def component(self, func, custom_id: str):
        """Decorator to register component interactions.

        Args:
            custom_id (str): Identifier of the component 
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        self.component_handlers[custom_id] = func

    def _get_handler(self, name: str):
        """Helper function for fetching a handler by `fnmatch`."""
        for k, v in self.component_handlers.items():
            if fnmatch.fnmatch(name, k) == True:
                return v
        return False

    async def dispatch(self, data: dict):
        """Dispatch a response to an `INTERACTION_CREATE` event

        Args:
            data (dict): interaction data
        """
        event = InteractionEvent(interaction=Interaction.from_dict(data, self._http))

        event_data_obj = self.RESOURCE_MAP.get(event.interaction.type)

        if not event_data_obj:
            return
        
        event.data = event_data_obj.from_dict(data.get('data'))
        handler = None
        name = None

        match event.interaction.type:
            case InteractionTypes.APPLICATION_COMMAND:
                name = event.data.name

                match event.data.type:
                    case InteractionDataTypes.SLASH_COMMAND:
                        handler = self.slash_handlers.get(name)
                    case InteractionDataTypes.USER_COMMAND:
                        handler = self.user_handlers.get(name)
                    case InteractionDataTypes.MESSAGE_COMMAND:
                        handler = self.message_handlers.get(name)

            # BOTH modals and message components have custom IDs!
            case InteractionTypes.MESSAGE_COMPONENT | InteractionTypes.MODAL_SUBMIT:
                name = event.data.custom_id
                handler = self._get_handler(name)

        if not handler:
            self._logger.log_warn(f"No handler registered for interaction '{name}'")
            return

        try:
            await handler(self.bot, event)
            self._logger.log_info(f"Interaction Event '{name}' Acknowledged.")
        except Exception as e:
            self._logger.log_error(f"Error in interaction '{name}': {e}")
