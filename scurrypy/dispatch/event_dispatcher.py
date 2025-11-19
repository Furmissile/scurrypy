import importlib
from ..core.client_like import ClientLike

from ..resources.message import Message

class EventDispatcher:
    """Central hub for handling Discord Gateway events."""

    RESOURCE_MAP = {
        'READY': ('scurrypy.events.ready_event', 'ReadyEvent'),

        'GUILD_CREATE': ('scurrypy.events.guild_events', 'GuildCreateEvent'),
        'GUILD_UPDATE': ('scurrypy.events.guild_events', 'GuildUpdateEvent'),
        'GUILD_DELETE': ('scurrypy.events.guild_events', 'GuildDeleteEvent'),

        'CHANNEL_CREATE': ('scurrypy.events.channel_events', 'GuildChannelCreateEvent'),
        'CHANNEL_UPDATE': ('scurrypy.events.channel_events', 'GuildChannelUpdateEvent'),
        'CHANNEL_DELETE': ('scurrypy.events.channel_events', 'GuildChannelDeleteEvent'),
        'CHANNEL_PINS_UPDATE': ('scurrypy.events.channel_events', 'ChannelPinsUpdateEvent'),

        'MESSAGE_CREATE': ('scurrypy.events.message_events', 'MessageCreateEvent'),
        'MESSAGE_UPDATE': ('scurrypy.events.message_events', 'MessageUpdateEvent'),
        'MESSAGE_DELETE': ('scurrypy.events.message_events', 'MessageDeleteEvent'),
        
        'MESSAGE_REACTION_ADD': ('scurrypy.events.reaction_events', 'ReactionAddEvent'),
        'MESSAGE_REACTION_REMOVE': ('scurrypy.events.reaction_events', 'ReactionRemoveEvent'),
        'MESSAGE_REACTION_REMOVE_ALL': ('scurrypy.events.reaction_events', 'ReactionRemoveAllEvent'),
        'MESSAGE_REACTION_REMOVE_EMOJI': ('scurrypy.events.reaction_events', 'ReactionRemoveEmojiEvent'),

        # and other events...
    }
    """Mapping of event names to respective dataclass. (lazy loading)"""
    
    def __init__(self, client: ClientLike):
        
        self.application_id = client.application_id
        """Bot's ID."""

        self.bot = client
        """Top-level discord client."""

        self._http = client._http
        """HTTP session for requests."""

        self._logger = client._logger
        """Logger instance to log events."""

        self.config = client.config
        """User-defined bot config for persistent data."""

        self._handlers = {}
        """Mapping of event names to handler."""

    def register(self, event_name: str, handler):
        """Registers the given handler to the given event name.
            (Event name must be a valid Discord event)

        Args:
            event_name (str): name of the event
            handler (callable): callback to handle event
        """
        self._handlers[event_name] = handler

    async def dispatch(self, event_name: str, data: dict):
        """Hydrate the corresponding dataclass and call the handler.

        Args:
            event_name (str): name of the event
            data (dict): Discord's raw event payload
        """
        module_info = self.RESOURCE_MAP.get(event_name)
        
        if not module_info:
            return
        
        module_name, class_name = module_info

        module = importlib.import_module(module_name)
        if not module:
            self._logger.log_error(f"Cannot find module '{module_name}'!")
            return

        cls = getattr(module, class_name)
        if not cls:
            self._logger.log_error(f"Cannot find class '{class_name}'!")
            return
        
        if isinstance(cls, Message) and cls.author.id == self.application_id:
            return # ignore bot's own messages
        
        handler = self._handlers.get(event_name, None)
        if handler:
            obj = cls.from_dict(data, self._http)
            obj.config = self.config
            await handler(self.bot, obj)
            self._logger.log_info(f"Event {event_name} Acknowledged.")
