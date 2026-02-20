import asyncio
import inspect

from .intents import Intents
from .core.http import HTTPClient, HTTPClientProtocol
from .core.gateway import GatewayClient, GatewayClientProtocol
from .core.error import DiscordError
from .core.snowflake import Snowflake

from .events.gateway_events import GatewayEvent

import logging

logger = logging.getLogger("scurrypy.client")
logger.addHandler(logging.NullHandler())

class Client:
    """Main entry point for Discord bots.
        Ties together the moving parts: gateway, HTTP and event dispatching.
    """

    token: str
    """Bot's token."""

    intents: Intents
    """Bot intents for listening to events."""

    http: HTTPClientProtocol
    """Public HTTP session for requests."""

    shards: GatewayClientProtocol
    """Shards as a list of gateways."""

    events: dict[str: list[callable]]
    """Events for the client to listen to."""

    startup_hooks: list[callable]
    """Handlers to call once before the bot starts."""

    shutdown_hooks: list[callable]
    """Handlers to call once after the bot shuts down."""

    def __init__(self,
        *,
        token: str,
        intents: Intents = Intents.DEFAULT,
        shard_count: int = 0,
        http: HTTPClientProtocol = None,
        gateway_impl: GatewayClientProtocol = None
    ):
        """
        Args:
            token (str): the bot's token
            intents (Intents, optional): gateway intents. Defaults to `Intents.DEFAULT`.
            shard_count (int, optional): number of shards to spawn. Defaults to `0` or recommended shard count.
            http (HTTPClientProtocol, optional): HTTP protocol implementation. Leave blank for default client.
            gateway_impl (GatewayClientProtocol, optional): Gateway protocol implementation. Leave blank for default client.
        """
        if not isinstance(intents, Intents):
            raise ValueError("Invalid intents type.")
        
        self.token = token
        self.intents = intents
        self.shard_count = shard_count
        
        self.http = http or HTTPClient()

        self.shards: list[GatewayClientProtocol] = []
        self.shard_type = gateway_impl or GatewayClient

        self.events = {}
        self.startup_hooks = []
        self.shutdown_hooks = []

    def add_event_listener(self, event: str, handler):
        """Helper function to register listener functions.

        Args:
            event (str): name of the event to listen
            handler (callable): listener function
        """
        if not callable(handler):
            raise TypeError(f"{handler} is not a callable function.")
        
        params_len = len(inspect.signature(handler).parameters)

        if params_len != 1:
            raise TypeError(
                f"Event listener '{handler.__name__}' must accept exactly one parameter (event)."
            )
    
        self.events.setdefault(event, []).append(handler)

    def add_startup_hook(self, handler):
        """Helper function to register startup functions.
            Runs once on startup BEFORE READY event.

        Args:
            handler (callable): startup function
        """
        if not callable(handler):
            raise TypeError(f"{handler} is not a callable function.")
        
        params_len = len(inspect.signature(handler).parameters)

        if params_len != 0:
            raise TypeError(
                f"Startup hook '{handler.__name__}' must accept no parameters."
            )
        
        self.startup_hooks.append(handler)

    def add_shutdown_hook(self, handler):
        """Helper function to register shutdown functions.
            Runs once on shutdown.

        Args:
            handler (callable): shutdown function
        """
        if not callable(handler):
            raise TypeError(f"{handler} is not a callable function.")
        
        params_len = len(inspect.signature(handler).parameters)

        if params_len != 0:
            raise TypeError(
                f"Shutdown hook '{handler.__name__}' must accept no parameters."
            )

        self.shutdown_hooks.append(handler)

    def application(self, application_id: Snowflake):
        """Creates an interactable application resource.

        Args:
            application_id (Snowflake): ID of target application

        Returns:
            (Application): the Application resource
        """
        from .resources.application import Application

        return Application(self.http, application_id)
    
    def bot_emoji(self, application_id: Snowflake):
        """Creates an interactable bot emoji resource.

        Args:
            application_id (Snowflake): ID of target application

        Returns:
            (BotEmojis): the BotEmoji resource
        """
        from .resources.emoji import ApplicationEmoji

        return ApplicationEmoji(self.http, application_id)
    
    def guild_emoji(self, guild_id: Snowflake):
        """Creates an interactable emoji resource.

        Args:
            guild_id (Snowflake): guild ID of target emojis

        Returns:
            (GuildEmoji): the GuildEmoji resource
        """
        from .resources.emoji import GuildEmoji

        return GuildEmoji(self.http, guild_id)

    def guild(self, guild_id: Snowflake):
        """Creates an interactable guild resource.

        Args:
            guild_id (Snowflake): ID of target guild

        Returns:
            (Guild): the Guild resource
        """
        from .resources.guild import Guild

        return Guild(self.http, guild_id)

    def channel(self, channel_id: Snowflake):
        """Creates an interactable guild channel resource.

        Args:
            channel_id (Snowflake): ID of target channel

        Returns:
            (GuildChannel): the GuildChannel resource
        """
        from .resources.channel import Channel

        return Channel(self.http, channel_id)
    
    def invite(self, code: str):
        """Creates an interactable invite resource.

        Args:
            code (str): unique invite code
        """
        from .resources.invite import Invite

        return Invite(self.http, code)
    
    def global_command(self, application_id: Snowflake):
        """Creates an interactable command resource.

        Args:
            application_id (Snowflake): bot's user ID

        Returns:
            (GlobalCommand): the GlobalCommand resource
        """
        from .resources.command import GlobalCommand

        return GlobalCommand(self.http, application_id)
    
    def guild_command(self, application_id: Snowflake, guild_id: Snowflake = None):
        """Creates an interactable command resource.

        Args:
            application_id (Snowflake): bot's user ID
            guild_id (Snowflake, optional): ID of guild if command is in guild scope

        Returns:
            (GuildCommand): the GuildCommand resource
        """
        from .resources.command import GuildCommand

        return GuildCommand(self.http, application_id, guild_id)

    def message(self, channel_id: Snowflake, message_id: Snowflake):
        """Creates an interactable message resource.

        Args:
            message_id (Snowflake): ID of target message
            channel_id (Snowflake): channel ID of target message

        Returns:
            (Message): the Message resource
        """
        from .resources.message import Message

        return Message(self.http, message_id, channel_id)
    
    def interaction(self, id: Snowflake, token: str):
        """Creates an interactable interaction resource.

        Args:
            id (Snowflake): ID of the interaction
            token (str): interaction token

        Returns:
            (Interaction): the Interaction resource
        """
        from .resources.interaction import Interaction

        return Interaction(self.http, id, token)
    
    def sticker(self):
        """Creates an interactable sticker resource

        Returns:
            (Sticker): the Sticker resource
        """
        from .resources.sticker import Sticker

        return Sticker(self.http)
    
    def user(self):
        """Creates an interactable user resource.

        Returns:
            (User): the User resource
        """
        from .resources.user import User

        return User(self.http)

    async def listen_shard(self, shard: GatewayClient):
        """Consume a GatewayClient's event queue.

        Args:
            shard (GatewayClient): gateway to listen on
        """

        while True:
            try:
                dispatch_type, event_data = await shard.event_queue.get()

                if dispatch_type not in self.events.keys():
                    logger.debug(f"SHARD ID {shard.shard_id} DISPATCH -> {dispatch_type}")
                else:
                    logger.info(f"SHARD ID {shard.shard_id} DISPATCH -> {dispatch_type}")

                from .core.events import EVENTS
                event_model = EVENTS.get(dispatch_type)
                if not event_model:
                    logger.warning(f"Event {dispatch_type} is not implemented.")
                    continue

                obj = event_model.from_dict(event_data)
                obj.name = dispatch_type
                obj.raw = event_data

                handlers = self.events.get(dispatch_type, [])
                for handler in handlers:
                    try:
                        result = handler(obj)
                        if inspect.isawaitable(result):
                            await result
                    except DiscordError as e:
                        logger.error(e)
                        continue

            except Exception:
                # catastrophic errors (network, shard death, unexpected OP code)
                logger.exception(f"SHARD ID {shard.shard_id}: Dispatcher error")
                continue

    async def start_shards(self, gateway: GatewayEvent):
        """Starts all shards batching by max_concurrency."""

        # pull important values for easier access
        total_shards = self.shard_count or gateway.shards
        batch_size = gateway.session_start_limit.max_concurrency

        tasks = []
        
        for batch_start in range(0, total_shards, batch_size):
            batch_end = min(batch_start + batch_size, total_shards)

            logger.debug(f"Starting shards {batch_start}-{batch_end} of {total_shards}")

            for shard_id in range(batch_start, batch_end):
                shard = self.shard_type()
                self.shards.append(shard)

                # fire and forget
                tasks.append(asyncio.create_task(shard.start(self.token, self.intents, shard_id, total_shards)))
                tasks.append(asyncio.create_task(self.listen_shard(shard)))

            # wait before next batch to respect identify rate limit
            await asyncio.sleep(5)

        return tasks
    
    async def run_startup_hooks(self):
        for hook in self.startup_hooks:
            try:
                logger.debug(f"Running hook {hook.__qualname__}...")
                result = hook()
                if inspect.isawaitable(result):
                    await asyncio.wait_for(result, timeout=60)
            except Exception:
                logger.exception("Error in shartup hook")
    
    async def start(self):
        """Starts the HTTP/Websocket client, run startup logic, and registers commands."""
        
        try:
            await self.http.start(self.token)

            data = await self.http.request('GET', '/gateway/bot')

            if not data:
                return

            gateway = GatewayEvent.from_dict(data)

            await self.run_startup_hooks()

            tasks = await asyncio.create_task(self.start_shards(gateway))

            await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            logger.info("Connection cancelled via KeyboardInterrupt.")
        except DiscordError as e:
            logger.error(e)
        except Exception:
            logger.exception(f"Unhandled client start exception.")
        finally:
            await self.close()

    async def run_shutdown_hooks(self):
        for hook in self.shutdown_hooks:
            try:
                logger.debug(f"Running hook {hook.__qualname__}...")
                result = hook()
                if inspect.isawaitable(result):
                    await asyncio.wait_for(result, timeout=60)
            except Exception:
                logger.exception("Error in shutdown hook")

    async def close(self):
        """Gracefully close HTTP session, websocket connections, and run shutdown logic."""  

        await self.run_shutdown_hooks()

        # close each connection or shard BEFORE HTTP
        await asyncio.gather(
            *(shard.close_ws() for shard in self.shards),
            return_exceptions=True
        )

        logger.info("Closing HTTP session...")
        await self.http.close()
    
    def run(self):
        """User-facing entry point for starting the client."""  

        try:
            asyncio.run(self.start())
        except Exception as e:
            logger.exception(f"{type(e).__name__} {e}")
        finally:
            logger.info("Bot shutting down.")
