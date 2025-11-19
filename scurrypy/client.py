import asyncio

from .core.config import BaseConfig
from .core.intents import Intents
from .core.gateway import GatewayClient
from .core.client_like import ClientLike

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
        sync_commands: bool = True,
        prefix = None,
        quiet: bool = False
    ):
        """
        Args:
            token (str): the bot's token
            application_id (int): the bot's user ID
            intents (int, optional): gateway intents. Defaults to Intents.DEFAULT.
            config (BaseConfig, optional): user-defined config data
            sync_commands (bool, optional): toggle registering commands. Defaults to True.
            debug_mode (bool, optional): toggle debug messages. Defaults to False.
            prefix (str, optional): set message prefix if using command prefixes
            quiet (bool, optional): if INFO, DEBUG, and WARN should be logged
        """
        if not token:
            raise ValueError("Token is required")
        if not application_id:
            raise ValueError("Application ID is required")
        
        from .core.logger import Logger
        from .core.http import HTTPClient
        from .resources.bot_emojis import BotEmojis
        from .dispatch.event_dispatcher import EventDispatcher
        from .dispatch.prefix_dispatcher import PrefixDispatcher
        from .dispatch.command_dispatcher import CommandDispatcher

        self.token = token
        self.intents = intents
        self.application_id = application_id
        self.config = config
        self.sync_commands = sync_commands

        self._logger = Logger(debug_mode, quiet)
        
        self._http = HTTPClient(self._logger)

        self.shards: list[GatewayClient] = []
        self.dispatcher = EventDispatcher(self)
        self.prefix_dispatcher = PrefixDispatcher(self, prefix)
        self.command_dispatcher = CommandDispatcher(self)

        self._setup_hooks = []
        self._shutdown_hooks = []
        
        self.emojis = BotEmojis(self._http, self.application_id)

    def prefix_command(self, name: str):
        """Decorator registers prefix commands by the name of the function.

        Args:
            name (str): name of the command
                !!! warning "Important"
                    Prefix commands are CASE-INSENSITIVE.
        """
        def decorator(func):
            self.prefix_dispatcher.register(name.lower(), func)
            return func
        return decorator

    def component(self, custom_id: str):
        """Decorator registers a function for a component handler.

        Args:
            custom_id (str): Identifier of the component. Must match the `custom_id` set where the component was created.
        """
        def decorator(func):
            self.command_dispatcher.component(func, custom_id)
            return func
        return decorator
    
    def command(self, command: SlashCommand | MessageCommand | UserCommand, guild_ids: list[int] = None):
        """Decorator registers a function to a command handler.

        Args:
            command (SlashCommand | MessageCommand | UserCommand): the command object
            guild_ids (list[int], optional): Guild IDs to register command to (if any). If omitted, the command is **global**.
        """
        def decorator(func):
            if not isinstance(command, (SlashCommand, MessageCommand, UserCommand)):
                raise ValueError(f"Expected SlashCommand, MessageCommand, or UserCommand; got {type(command).__name__}")
            
            # maps command type -> command registry
            handler_map = {
                SlashCommand: self.command_dispatcher.add_slash_command,
                MessageCommand: self.command_dispatcher.add_message_command,
                UserCommand: self.command_dispatcher.add_user_command
            }

            # can guarantee at this point command is one of SlashCommand | MessageCommand | UserCommand
            handler = handler_map[type(command)]

            handler(command, func, guild_ids)
            return func
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
            application_id (int): ID of target application

        Returns:
            (Application): the Application resource
        """
        from .resources.application import Application

        return Application(application_id, self._http)

    def fetch_guild(self, guild_id: int):
        """Creates an interactable guild resource.

        Args:
            guild_id (int): ID of target guild

        Returns:
            (Guild): the Guild resource
        """
        from .resources.guild import Guild

        return Guild(guild_id, self._http)

    def fetch_channel(self, channel_id: int):
        """Creates an interactable channel resource.

        Args:
            channel_id (int): ID of target channel

        Returns:
            (Channel): the Channel resource
        """
        from .resources.channel import Channel

        return Channel(channel_id, self._http)

    def fetch_message(self, channel_id: int, message_id: int):
        """Creates an interactable message resource.

        Args:
            message_id (int): ID of target message
            channel_id (int): channel ID of target message

        Returns:
            (Message): the Message resource
        """
        from .resources.message import Message

        return Message(message_id, channel_id, self._http)
    
    def fetch_user(self, user_id: int):
        """Creates an interactable user resource.

        Args:
            user_id (int): ID of target user

        Returns:
            (User): the User resource
        """
        from .resources.user import User

        return User(user_id, self._http)
    
    async def clear_commands(self, guild_ids: list[int] = None):
        """Clear a guild's or global commands (all types).

        Args:
            guild_ids (list[int]): ID of the target guild. If omitted, **global** commands will be cleared.
        """
        self.command_dispatcher.clear_commands(guild_ids)

    async def _start_shards(self):
        """Starts all shards batching by max_concurrency."""

        from .events.gateway_events import GatewayEvent

        data = await self._http.request('GET', '/gateway/bot')

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

                # fire and forget
                tasks.append(asyncio.create_task(shard.start()))
                tasks.append(asyncio.create_task(self._listen_shard(shard)))

            # wait before next batch to respect identify rate limit
            await asyncio.sleep(5)

        return tasks

    async def _listen_shard(self, shard: GatewayClient):
        """Listen to websocket queue for events. Only OP code 0 passes!

        Args:
            shard (GatewayClient): the shard or gateway to listen on
        """
        while True:
            try:
                dispatch_type, event_data = await shard.event_queue.get()
                
                # check prefix first (only if a prefix is set)
                if self.prefix_dispatcher.prefix and dispatch_type == 'MESSAGE_CREATE':
                    await self.prefix_dispatcher.dispatch(event_data)
                    
                # then try interaction
                elif dispatch_type == 'INTERACTION_CREATE':
                    await self.command_dispatcher.dispatch(event_data)

                # otherwise this must be an event!
                await self.dispatcher.dispatch(dispatch_type, event_data)
            except:
                break # stop task if an error occurred

    async def _start(self):
        """Starts the HTTP/Websocket client, run startup hooks, and registers commands."""

        try:
            await self._http.start(self.token)
            
            if self._setup_hooks:
                for hook in self._setup_hooks:
                    self._logger.log_info(f"Setting hook {hook.__name__}")
                    await hook(self)
                self._logger.log_high_priority("Hooks set up.")

            if self.sync_commands:
                await self.command_dispatcher.register_guild_commands()

                await self.command_dispatcher.register_global_commands()

                self._logger.log_high_priority("Commands set up.")

            tasks = await asyncio.create_task(self._start_shards())

            # end all ongoing tasks
            await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            self._logger.log_high_priority("Connection cancelled via KeyboardInterrupt.")
        except Exception as e:
            self._logger.log_error(f"{type(e).__name__} - {e}")
        finally:
            await self._close()

    async def _close(self):    
        """Gracefully close HTTP session, websocket connections, and run shutdown hooks."""   

        for hook in self._shutdown_hooks:
            try:
                self._logger.log_info(f"Executing shutdown hook {hook.__name__}")
                await hook(self)
            except Exception as e:
                self._logger.log_error(f"Shutdown hook failed: {type(e).__name__}: {e}")

        self._logger.log_info("Closing HTTP session...")
        await self._http.close()

        # close each connection or shard
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
