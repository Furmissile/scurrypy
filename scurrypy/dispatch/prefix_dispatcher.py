from ..core.client_like import ClientLike

from ..events.message_events import MessageCreateEvent

from ..resources.message import Message
from ..models import MemberModel

class PrefixDispatcher:
    """Handles text-based command messages that start with a specific prefix."""
    
    def __init__(self, client: ClientLike, prefix: str):

        self.bot = client
        """Bot session for user access to bot."""

        self._http = client._http
        """HTTP session for requests."""

        self._logger = client._logger
        """Logger instance to log events."""

        self.application_id = client.application_id
        """The client's application ID."""

        self.prefix = prefix
        """User-defined command prefix."""

        self.config = client.config
        """User-defined bot config for persistent data."""

        self._handlers = {}
        """Mapping of command prefix names to handler"""

    def register(self, name: str, handler):
        """Registers a handler for a command name

        Args:
            name (str): name of handler (and command)
            handler (callable): handler callback
        """
        self._handlers[name] = handler

    async def dispatch(self, data: dict):
        """Hydrate the corresponding dataclass and call the handler.

        Args:
            data (dict): Discord's raw event payload
        """
        event = MessageCreateEvent(
            guild_id=data.get('guild_id'),
            message=Message.from_dict(data, self._http),
            member=MemberModel.from_dict(data.get('member'))
        )

        # ignore bot responding to itself
        if event.message.author.id == self.application_id:
            return

        # ignore messages without prefix
        if not event.message._has_prefix(self.prefix):
            return
        
        command, *args = event.message._extract_args(self.prefix)
        handler = self._handlers.get(command)

        # warn if this command doesnt have a known handler
        if not handler:
            self._logger.log_warn(f"Prefix Event '{command}' not found.")
            return

        # now prefix info can be confidently set
        try:
            event.prefix_args = list(args)
            await handler(self.bot, event)
            
            self._logger.log_info(f"Prefix Event '{command}' acknowledged with args: {event.prefix_args or 'No args'}")
        except Exception as e:
            self._logger.log_error(f"Error in prefix command '{command}': {e}")
