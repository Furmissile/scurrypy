import asyncio

from .logger import Logger
from .gateway import GatewayClient
from .http import HTTPClient
from .intents import Intents
from .error import DiscordError

from .resources.guild import Guild
from .resources.channel import Channel
from .resources.message import Message
from .resources.bot_emojis import BotEmojis
from .resources.user import User
from .resources.application import Application

from .parts.command import SlashCommand, MessageCommand, UserCommand

from .dispatch.event_dispatcher import EventDispatcher
from .dispatch.prefix_dispatcher import PrefixDispatcher
from .dispatch.command_dispatcher import CommandDispatcher

class Client:
    """Main entry point for Discord bots.
        Ties together the moving parts: gateway, HTTP, event dispatching, command handling, and resource managers.
    """
    def __init__(self, 
        *,
        token: str,
        application_id: int,
        intents: int = Intents.DEFAULT,
        debug_mode: bool = False,
        prefix = None,
        quiet: bool = False
    ):
        """
        Args:
            token (str): the bot's token
            application_id (int): the bot's user ID
            intents (int, optional): gateway intents. Defaults to Intents.DEFAULT.
            debug_mode (bool, optional): toggle debug messages. Defaults to False.
            prefix (str, optional): set message prefix if using command prefixes
            quiet (bool, optional): if INFO, DEBUG, and WARN should be logged
        """
        self.token = token
        self.application_id = application_id

        self._logger = Logger(debug_mode, quiet)
        self._ws = GatewayClient(token, intents, self._logger)
        self._http = HTTPClient(token, self._logger)

        if prefix and (intents & Intents.MESSAGE_CONTENT == 0):
            self._logger.log_warn('Prefix set without message content enabled.')

        self.dispatcher = EventDispatcher(self.application_id, self._http, self._logger)
        self.prefix_dispatcher = PrefixDispatcher(self._http, self._logger, prefix)
        self.command_dispatcher = CommandDispatcher(self.application_id, self._http, self._logger)

        self._global_commands = [] # SlashCommand
        self._guild_commands = {} # {guild_id : [commands], ...}

        self._is_set_up = False
        self._setup_hooks = []
        
        self.emojis = BotEmojis(self._http, self.application_id)

    def prefix_command(self, func):
        """Decorator registers prefix commands by the name of the function.

        Args:
            func (callable): callback handle for command response
        """
        self.prefix_dispatcher.register(func.__name__, func)

    def component(self, func):
        """Decorator registers a function for a component handler.

        Args:
            func (callable): callback handle for component response
        """
        self.command_dispatcher.component(func)

    def command(self, command: SlashCommand | MessageCommand | UserCommand, guild_id: int = 0):
        """Decorator registers a function for a command handler.

        Args:
            command (SlashCommand | MessageCommand | UserCommand): command to register
            guild_id (int): ID of guild in which to register command (if a guild command)
        """
        def decorator(func):
            # hash out command type
            if isinstance(command, MessageCommand):
                self.command_dispatcher.message_command(func)
            elif isinstance(command, UserCommand):
                self.command_dispatcher.user_command(func)
            elif isinstance(command, SlashCommand):
                self.command_dispatcher.command(func)
            else:
                raise ValueError(f'Command {func.__name__} expected to be of type SlashCommand, UserCommand, MessageCommand; \
                    got {type(command).__name__}.')
            
            # then hash out if this command should be guild or global level
            if guild_id != 0:
                self._guild_commands.setdefault(guild_id, []).append(command)
            else:
                self._global_commands.append(command)
        return decorator
    
    def event(self, event_name: str):
        """Decorator registers a function for an event handler.

        Args:
            event_name (str): event name (must be a valid event)
        """
        def decorator(func):
            self.dispatcher.register(event_name, func)
            return func
        return decorator
    
    def setup_hook(self, func):
        """Decorator registers a setup hook.
            (Runs once before the bot starts listening)

        Args:
            func (callable): callback to the setup function
        """
        self._setup_hooks.append(func)

    def application_from_id(self, application_id: int):
        """Creates an interactable application resource.

        Args:
            application_id (int): id of target application

        Returns:
            (Application): the Application resource
        """
        return Application(application_id, self._http)

    def guild_from_id(self, guild_id: int):
        """Creates an interactable guild resource.

        Args:
            guild_id (int): id of target guild

        Returns:
            (Guild): the Guild resource
        """
        return Guild(guild_id, self._http)

    def channel_from_id(self, channel_id: int):
        """Creates an interactable channel resource.

        Args:
            channel_id (int): id of target channel

        Returns:
            (Channel): the Channel resource
        """
        return Channel(channel_id, self._http)

    def message_from_id(self, channel_id: int, message_id: int):
        """Creates an interactable message resource.

        Args:
            message_id (int): id of target message
            channel_id (int): channel id of target message

        Returns:
            (Message): the Message resource
        """
        return Message(message_id, channel_id, self._http)
    
    def user_from_id(self, user_id: int):
        """Creates an interactable user resource.

        Args:
            user_id (int): id of target user

        Returns:
            (User): the User resource
        """
        return User(user_id, self._http)
    
    async def clear_guild_commands(self, guild_id: int):
        """Clear a guild's slash commands.

        Args:
            guild_id (int): id of the target guild
        """
        if self._guild_commands.get(guild_id):
            self._logger.log_info(f"Guild {guild_id} already queued, skipping clear.")
            return

        await self.command_dispatcher._register_guild_commands({guild_id: []})

    async def _listen(self):
        """Main event loop for incoming gateway requests."""
        while True:
            try:
                message = await self._ws.receive()
                if not message:
                    raise ConnectionError("No message received.")

                op_code = message.get('op')

                if op_code == 0:
                    dispatch_type = message.get('t')
                    self._logger.log_info(f"DISPATCH -> {dispatch_type}")
                    event_data = message.get('d')
                    self._ws.sequence = message.get('s') or self._ws.sequence

                    if dispatch_type == "READY":
                        self._ws.session_id = event_data.get("session_id")
                        self._ws.connect_url = event_data.get("resume_gateway_url", self._ws.connect_url)

                    try:
                        if self.prefix_dispatcher.prefix and dispatch_type == 'MESSAGE_CREATE':
                            await self.prefix_dispatcher.dispatch(event_data)
                            
                        elif dispatch_type == 'INTERACTION_CREATE':
                            await self.command_dispatcher.dispatch(event_data)

                        await self.dispatcher.dispatch(dispatch_type, event_data)
                    except DiscordError as e:
                        if e.fatal:
                            raise  # let run() handle fatal errors
                        else:
                            self._logger.log_warn(f"Recoverable DiscordError: {e}")
                            continue  # keep listening

                elif op_code == 7:
                    raise ConnectionError("Reconnect requested by server.")
                elif op_code == 9:
                    self._ws.session_id = None
                    self._ws.sequence = None
                    raise ConnectionError("Invalid session.")
            except asyncio.CancelledError:
                raise
            except DiscordError as e:
                if e.fatal:
                    raise  # propagate fatal errors
                else:
                    self._logger.log_warn(f"Recoverable DiscordError: {e}")
            except ConnectionError as e:
                self._logger.log_warn(f"Connection lost: {e}")
                await self._ws.close()
                await asyncio.sleep(2)

    async def start(self):
        """Runs the main lifecycle of the bot.
            Handles connection setup, heartbeat management, event loop, and automatic reconnects.
        """
        while True:
            try:
                await self._http.start_session()
                await self._ws.connect()
                await self._ws.start_heartbeat()

                if self._ws.session_id and self._ws.sequence:
                    await self._ws.reconnect()
                else:
                    await self._ws.identify()

                if not self._is_set_up:
                    if self._setup_hooks:
                        for hook in self._setup_hooks:
                            self._logger.log_info(f"Setting hook {hook.__name__}")
                            await hook()
                        self._logger.log_high_priority("Hooks set up.")

                    # register GUILD commands
                    await self.command_dispatcher._register_guild_commands(self._guild_commands)

                    # register GLOBAL commands
                    await self.command_dispatcher._register_global_commands(self._global_commands)

                    self._is_set_up = True

                await self._listen()

            except ConnectionError as e:
                self._logger.log_warn("Connection lost. Attempting reconnect...")
                await self._ws.close()
                await asyncio.sleep(2)
                continue
            except asyncio.CancelledError:
                self._logger.log_info("Cancelling connection...")
                break
            except DiscordError as e:
                self._logger.log_error(f"Fatal DiscordError: {e}")
                break
            except Exception as e:
                self._logger.log_error(f"Unspecified Error Type {type(e).__name__} - {e}")
                break
            finally:
                await self._ws.close()
                await self._http.close_session()

    def run(self):
        """Starts the bot.
            Handles starting the session, WS, and heartbeat, reconnection logic,
            setting up emojis and hooks, and then listens for gateway events.
        """
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            self._logger.log_debug("Shutdown requested via KeyboardInterrupt.")
        except Exception as e:
            self._logger.log_error(f"{type(e).__name__} {e}")
        finally:
            self._logger.log_high_priority("Bot shutting down.")
            self._logger.close()
