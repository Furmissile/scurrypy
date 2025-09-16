from ..http import HTTPClient
from ..logger import Logger

from ..events.message_events import MessageCreateEvent

from ..resources.message import Message
from ..models.member import MemberModel

class PrefixDispatcher:
    """Handles text-based command messages that start with a specific prefix."""
    def __init__(self, http: HTTPClient, logger: Logger, prefix: str):
        self._http = http
        """HTTP session for requests."""

        self._logger = logger
        """Logger instance to log events."""

        self.prefix = prefix
        """User-defined command prefix."""

        self._handlers = {}
        """Mapping of command prefix names to handler"""

    def register(self, name: str, handler):
        """Registers a handler for a command name (case-insensitive)

        Args:
            name (str): name of handler (and command)
            handler (callable): handler callback
        """
        self._handlers[name.lower()] = handler

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

        if event.message._has_prefix(self.prefix):
            command, *args = event.message._extract_args(self.prefix)
            handler = self._handlers.get(command)
            if handler:
                try:
                    await handler(event, *args)
                    self._logger.log_info(f"Prefix Event '{command}' Acknowledged.")
                except Exception as e:
                    self._logger.log_error(f"Error in prefix command '{command}': {e}")
