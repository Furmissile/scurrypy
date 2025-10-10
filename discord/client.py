import asyncio

from .config import BaseConfig
from .intents import Intents
from .error import DiscordError
from .client_like import ClientLike

from .parts.command import SlashCommand, MessageCommand, UserCommand

class Client(ClientLike):
    """Main entry point for Discord bots.
        Ties together the moving parts: gateway, HTTP, event dispatching, command handling, and resource managers.
    """
    def __init__(self, 
        *,
        token: str,
        application_id: int,
        intents: int = Intents.DEFAULT,
        config: BaseConfig = None,
        debug_mode: bool = False,
        prefix = None,
        quiet: bool = False
    ):
        """
        Args:
            token (str): the bot's token
            application_id (int): the bot's user ID
            intents (int, optional): gateway intents. Defaults to Intents.DEFAULT.
            config (BaseConfig, optional): user-defined config data
            debug_mode (bool, optional): toggle debug messages. Defaults to False.
            prefix (str, optional): set message prefix if using command prefixes
            quiet (bool, optional): if INFO, DEBUG, and WARN should be logged
        """
        if not token:
            raise ValueError("Token is required")
        if not application_id:
            raise ValueError("Application ID is required")
        
        from .logger import Logger
        from .gateway import GatewayClient
        from .http import HTTPClient
        from .resources.bot_emojis import BotEmojis
        from .dispatch.event_dispatcher import EventDispatcher
        from .dispatch.prefix_dispatcher import PrefixDispatcher
        from .dispatch.command_dispatcher import CommandDispatcher

        self.token = token
        self.application_id = application_id
        self.config = config

        self._logger = Logger(debug_mode, quiet)
        self._ws = GatewayClient(token, intents, self._logger)
        self._http = HTTPClient(token, self._logger)

        if prefix and (intents & Intents.MESSAGE_CONTENT == 0):
            self._logger.log_warn('Prefix set without message content enabled.')

        self.dispatcher = EventDispatcher(self)
        self.prefix_dispatcher = PrefixDispatcher(self, prefix)
        self.command_dispatcher = CommandDispatcher(self)

        self._global_commands = [] # SlashCommand
        self._guild_commands = {} # {guild_id : [commands], ...}

        self._is_set_up = False
        self._setup_hooks = []
        self._shutdown_hooks = []
        
        self.emojis = BotEmojis(self._http, self.application_id)

    def prefix_command(self, func):
        """Decorator registers prefix commands by the name of the function.

        Args:
            func (callable): callback handle for command response
        """
        self.prefix_dispatcher.register(func.__name__, func)

    def component(self, custom_id: str):
        """Decorator registers a function for a component handler.

        Args:
            custom_id (str): Identifier of the component 
                !!! warning "Important"
                    Must match the `custom_id` set where the component was created.
        """
        def decorator(func):
            self.command_dispatcher.component(func, custom_id)
            return func
        return decorator

    def command(self, command: SlashCommand | MessageCommand | UserCommand, guild_ids: list[int] | None = None):
        """Decorator to register a function as a command handler.

        Args:
            command (SlashCommand | MessageCommand | UserCommand): The command to register.
            guild_ids (list[int] | None): Guild IDs for guild-specific commands. None for global commands.
        """
        def decorator(func):
            # Map command types to dispatcher registration functions
            handler_map = {
                MessageCommand: self.command_dispatcher.message_command,
                UserCommand: self.command_dispatcher.user_command,
                SlashCommand: self.command_dispatcher.command,
            }

            # Resolve dispatcher method based on command type
            for cls, handler in handler_map.items():
                if isinstance(command, cls):
                    handler(command.name, func)
                    break
            else:
                raise ValueError(
                    f"Command {getattr(command, 'name', '<unnamed>')} must be one of "
                    f"SlashCommand, UserCommand, MessageCommand; got {type(command).__name__}."
                )

            # Queue command for later registration
            if guild_ids:
                gids = [guild_ids] if isinstance(guild_ids, int) else guild_ids
                for gid in gids:
                    self._guild_commands.setdefault(gid, []).append(command)
            else:
                self._global_commands.append(command)

            return func  # ensure original function is preserved
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

    def shutdown_hook(self, func):
        """Decorator registers a shutdown hook.
            (Runs once before the bot exits the loop)

        Args:
            func (callable): callback to the shutdown function
        """
        self._shutdown_hooks.append(func)

    def fetch_application(self, application_id: int):
        """Creates an interactable application resource.

        Args:
            application_id (int): id of target application

        Returns:
            (Application): the Application resource
        """
        from .resources.application import Application

        return Application(application_id, self._http)

    def fetch_guild(self, guild_id: int):
        """Creates an interactable guild resource.

        Args:
            guild_id (int): id of target guild

        Returns:
            (Guild): the Guild resource
        """
        from .resources.guild import Guild

        return Guild(guild_id, self._http)

    def fetch_channel(self, channel_id: int):
        """Creates an interactable channel resource.

        Args:
            channel_id (int): id of target channel

        Returns:
            (Channel): the Channel resource
        """
        from .resources.channel import Channel

        return Channel(channel_id, self._http)

    def fetch_message(self, channel_id: int, message_id: int):
        """Creates an interactable message resource.

        Args:
            message_id (int): id of target message
            channel_id (int): channel id of target message

        Returns:
            (Message): the Message resource
        """
        from .resources.message import Message

        return Message(message_id, channel_id, self._http)
    
    def fetch_user(self, user_id: int):
        """Creates an interactable user resource.

        Args:
            user_id (int): id of target user

        Returns:
            (User): the User resource
        """
        from .resources.user import User

        return User(user_id, self._http)
    
    async def clear_guild_commands(self, guild_id: int):
        """Clear a guild's slash commands.

        Args:
            guild_id (int): id of the target guild
        """
        if self._guild_commands.get(guild_id):
            self._logger.log_warn(f"Guild {guild_id} already queued, skipping clear.")
            return
        
        self._guild_commands[guild_id] = []

    async def _listen(self):
        """Main event loop for incoming gateway requests."""
        while self._ws.is_connected():
            try:
                message = await self._ws.receive()
                if not message:
                    raise ConnectionError("No message received.")

                op_code = message.get('op')

                match op_code:
                    case 0:
                        dispatch_type = message.get('t')
                        self._logger.log_info(f"DISPATCH -> {dispatch_type}")
                        event_data = message.get('d')
                        self._ws.sequence = message.get('s') or self._ws.sequence

                        if dispatch_type == "READY":
                            self._ws.session_id = event_data.get("session_id")
                            self._ws.connect_url = event_data.get("resume_gateway_url", self._ws.connect_url)

                        if self.prefix_dispatcher.prefix and dispatch_type == 'MESSAGE_CREATE':
                            await self.prefix_dispatcher.dispatch(event_data)
                            
                        elif dispatch_type == 'INTERACTION_CREATE':
                            await self.command_dispatcher.dispatch(event_data)

                        await self.dispatcher.dispatch(dispatch_type, event_data)
                    case 7:
                        raise ConnectionError("Reconnect requested by server.")
                    case 9:
                        self._ws.session_id = None
                        self._ws.sequence = None
                        raise ConnectionError("Invalid session.")
                    case 11:
                        self._logger.log_info("Heartbeat ACK received")

            except asyncio.CancelledError:
                break
            except DiscordError as e:
                if e.fatal:
                    self._logger.log_error(f"Fatal DiscordError: {e}")
                    break
                else:
                    self._logger.log_warn(f"Recoverable DiscordError: {e}")
            except ConnectionError as e:
                self._logger.log_warn(f"Connection lost: {e}")
                raise
            except Exception as e:
                self._logger.log_error(f"{type(e).__name__} - {e}")
                self._logger.log_traceback()
                continue

    async def _start(self):
        """Runs the main lifecycle of the bot.
            Handles connection setup, heartbeat management, event loop, and automatic reconnects.
        """
        try:
            await self._http.start()
            await self._ws.connect()
            await self._ws.start_heartbeat()

            while self._ws.is_connected():
                if self._ws.session_id and self._ws.sequence:
                    await self._ws.reconnect()
                else:
                    await self._ws.identify()

                if not self._is_set_up:
                    await self._startup()
                    self._is_set_up = True

                await self._listen()
                
                # If we get here, connection was lost - reconnect
                await self._ws.close() 
                await asyncio.sleep(5)
                await self._ws.connect()
                await self._ws.start_heartbeat()

        except asyncio.CancelledError:
            self._logger.log_high_priority("Connection cancelled via KeyboardInterrupt.")
        except Exception as e:
            self._logger.log_error(f"{type(e).__name__} - {e}")
        finally:
            await self._close()

    async def _startup(self):
        """Start up bot by registering user-defined hooks and commands."""
        try:
            if self._setup_hooks:
                for hook in self._setup_hooks:
                    self._logger.log_info(f"Setting hook {hook.__name__}")
                    await hook(self)
                self._logger.log_high_priority("Hooks set up.")

            # register GUILD commands
            await self.command_dispatcher._register_guild_commands(self._guild_commands)

            # register GLOBAL commands
            await self.command_dispatcher._register_global_commands(self._global_commands)

            self._logger.log_high_priority("Commands set up.")
        except Exception:
            raise

    async def _close(self):    
        """Gracefully close HTTP and websocket connections."""    
        # Run shutdown hooks first
        for hook in self._shutdown_hooks:
            try:
                self._logger.log_info(f"Executing shutdown hook {hook.__name__}")
                await hook(self)
            except Exception as e:
                self._logger.log_error(f"Shutdown hook failed: {type(e).__name__}: {e}")

        # Close HTTP before gateway since it's more important
        self._logger.log_debug("Closing HTTP session...")
        await self._http.close()

        # Then try websocket with short timeout
        try:
            self._logger.log_debug("Closing websocket connection...")
            await asyncio.wait_for(self._ws.close(), timeout=1.0)
        except:
            pass  # Don't care if websocket won't close
        
    def run(self):
        """Starts the bot.
            Handles starting the session, WS, and heartbeat, reconnection logic,
            setting up emojis and hooks, and then listens for gateway events.
        """        
        try:
            asyncio.run(self._start())
        except KeyboardInterrupt:
            self._logger.log_debug("Shutdown requested via KeyboardInterrupt.")
        except Exception as e:
            self._logger.log_error(f"{type(e).__name__} {e}")
            self._logger.log_traceback()
        finally:
            self._logger.log_high_priority("Bot shutting down.")
            self._logger.close()
