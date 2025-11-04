import fnmatch

from ..client_like import ClientLike

from ..events.interaction_events import ApplicationCommandData, MessageComponentData, ModalData, InteractionEvent
from ..resources.interaction import Interaction, InteractionDataTypes

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

        self.config = client.config

        self._component_handlers = {}
        """Mapping of component custom IDs to handler."""

        self._handlers = {}
        """Mapping of command names to handler."""

        self._message_handlers = {}
        """Mapping of message command names to handler."""

        self._user_handlers = {}
        """Mapping of user command names to handler."""

    async def _register_guild_commands(self, commands: dict):
        """Registers a command at the guild level.

        Args:
            commands (dict): mapping of guild IDs to respective serialized command data
        """
        
        for guild_id, cmds in commands.items():
            # register commands PER GUILD
            await self._http.request(
                'PUT', 
                f"applications/{self.application_id}/guilds/{guild_id}/commands", 
                data=[command.to_dict() for command in cmds]
            )
    
    async def _register_global_commands(self, commands: list):
        """Registers a command at the global/bot level. (ALL GUILDS)

        Args:
            commands (list): list of serialized commands
        """

        global_commands = [command.to_dict() for command in commands]

        await self._http.request('PUT', f"applications/{self.application_id}/commands", data=global_commands)

    def command(self, name: str, handler):
        """Decorator to register slash commands.

        Args:
            name (str): name of the command to register
            handler (callable): callback handle for command response
        """
        self._handlers[name] = handler

    def user_command(self, name: str, handler):
        """Decorator to register user commands.

        Args:
            name (str): name of the command to register
            handler (callable): callback handle for user command response
        """
        self._user_handlers[name] = handler

    def message_command(self, name: str, handler):
        """Decorator to register message commands.

        Args:
            name (str): name of the command to register
            handler (callable): callback handle for message command response
        """
        self._message_handlers[name] = handler

    def component(self, func, custom_id: str):
        """Decorator to register component interactions.

        Args:
            custom_id (str): Identifier of the component 
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        self._component_handlers[custom_id] = func

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
                        handler = self._handlers.get(name)
                    case InteractionDataTypes.USER_COMMAND:
                        handler = self._user_handlers.get(name)
                    case InteractionDataTypes.MESSAGE_COMMAND:
                        handler = self._message_handlers.get(name)

            case InteractionTypes.MESSAGE_COMPONENT:
                name = event.data.custom_id
                for k, v in self._component_handlers.items():
                    if fnmatch.fnmatch(name, k) == True:
                        handler = v
                # handler = self._component_handlers.get(name)

            case InteractionTypes.MODAL_SUBMIT:
                name = event.data.custom_id
                for k, v in self._component_handlers.items():
                    if fnmatch.fnmatch(name, k) == True:
                        handler = v
                # handler = self._component_handlers.get(name)

        if not handler:
            self._logger.log_warn(f"No handler registered for interaction '{name}'")
            return

        try:
            await handler(self.bot, event) # NOTE: treat command options as args!
            self._logger.log_info(f"Interaction Event '{name}' Acknowledged.")
        except Exception as e:
            self._logger.log_error(f"Error in interaction '{name}': {e}")
            self._logger.log_traceback()