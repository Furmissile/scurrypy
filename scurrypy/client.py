import asyncio

from .config import BaseConfig
from .intents import Intents
from .gateway import GatewayClient
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
        from .http import HTTPClient
        from .resources.bot_emojis import BotEmojis
        from .dispatch.event_dispatcher import EventDispatcher
        from .dispatch.prefix_dispatcher import PrefixDispatcher
        from .dispatch.command_dispatcher import CommandDispatcher

        self.token = token
        self.intents = intents
        self.application_id = application_id
        self.config = config

        self._logger = Logger(debug_mode, quiet)
        
        self._http = HTTPClient(self._logger)

        self.shards: list[GatewayClient] = []
        self.dispatcher = EventDispatcher(self)
        self.prefix_dispatcher = PrefixDispatcher(self, prefix)
        self.command_dispatcher = CommandDispatcher(self)

        self._global_commands = [] # SlashCommand
        self._guild_commands = {} # {guild_id : [commands], ...}

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
        # if guild is queued to register commands, this was a mistake!
        if self._guild_commands.get(guild_id):
            self._logger.log_warn(f"Guild {guild_id} already queued, skipping clear.")
            return
        
        self._guild_commands[guild_id] = []

    async def _start_shards(self):
        """Starts all shards batching by max_concurrency."""

        from .events.gateway_events import GatewayEvent

        # request gateway info
        data = await self._http.request('GET', '/gateway/bot')

        # translate it to a dataclass
        gateway = GatewayEvent.from_dict(data)

        # pull important values for easier access
        total_shards = gateway.shards
        batch_size = gateway.session_start_limit.max_concurrency

        tasks = []
        
        for batch_start in range(0, total_shards, batch_size):
            batch_end = min(batch_start + batch_size, total_shards)

            self._logger.log_info(f"Starting shards {batch_start}-{batch_end - 1} of {total_shards}")

            for shard_id in range(batch_start, batch_end):
                shard = GatewayClient(self, gateway.url, shard_id, total_shards)
                self.shards.append(shard)

                # Fire and forget
                tasks.append(asyncio.create_task(shard.start()))
                tasks.append(asyncio.create_task(self._listen_shard(shard)))

            # wait before next batch to respect identify rate limit
            await asyncio.sleep(5)

        return tasks

    async def _listen_shard(self, shard: GatewayClient):
        """Listen to websocket queue for events. Only OP code 0 passes!"""

        while True:
            try:
                dispatch_type, event_data = await shard.event_queue.get()
                
                if self.prefix_dispatcher.prefix and dispatch_type == 'MESSAGE_CREATE':
                    await self.prefix_dispatcher.dispatch(event_data)
                    
                elif dispatch_type == 'INTERACTION_CREATE':
                    await self.command_dispatcher.dispatch(event_data)

                await self.dispatcher.dispatch(dispatch_type, event_data)
            except:
                break # stop task if an error occurred

    async def _start(self):
        """Starts the HTTP/Websocket client, run startup hooks, and registers commands."""

        try:
            await self._http.start(self.token)
            
            # setup hooks if hooks were set
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

            # run websocket indefinitely
            tasks = await asyncio.create_task(self._start_shards())

            await asyncio.gather(*tasks)
                
        except asyncio.CancelledError:
            self._logger.log_high_priority("Connection cancelled via KeyboardInterrupt.")
        except Exception as e:
            self._logger.log_error(f"{type(e).__name__} - {e}")
        finally:
            await self._close()

    async def _close(self):    
        """Gracefully close HTTP session, websocket connections, and run shutdown hooks."""   

        # Run shutdown hooks first
        for hook in self._shutdown_hooks:
            try:
                self._logger.log_info(f"Executing shutdown hook {hook.__name__}")
                await hook(self)
            except Exception as e:
                self._logger.log_error(f"Shutdown hook failed: {type(e).__name__}: {e}")

        self._logger.log_info("Closing HTTP session...")
        await self._http.close()

        for shard in self.shards:
            await shard.close_ws()

    def run(self):
        """User-facing entry point for starting the client."""  

        try:
            asyncio.run(self._start())
        except KeyboardInterrupt:
            self._logger.log_info("Shutdown requested via KeyboardInterrupt.")
        except Exception as e:
            self._logger.log_error(f"{type(e).__name__} {e}")
        finally:
            self._logger.log_high_priority("Bot shutting down.")
            self._logger.close()
