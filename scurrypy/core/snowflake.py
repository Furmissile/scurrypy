from dataclasses import dataclass
from datetime import datetime, timezone

DISCORD_EPOCH = 1420070400000

@dataclass(frozen=True)
class Snowflake:
    """Represents Discord's ID with helper methods.
    
    !!! tip
        This class resolves to an integer, and therefore, it should be treated like an integer.
    """

    value: int
    """Snowflake value."""

    @property
    def timestamp_ms(self) -> int:
        """Get the timestamp of this snowflake in milliseconds (ms).

        Returns:
            (int): timestamp in ms
        """
        return (self.value >> 22) + DISCORD_EPOCH

    @property
    def datetime(self) -> datetime:
        """Get the datetime object of this snowflake.

        Returns:
            (datetime): datetime
        """
        return datetime.fromtimestamp(
            self.timestamp_ms / 1000,
            tz=timezone.utc,
        )

    @property
    def isoformat(self) -> str:
        """Get the ISO8601 format for this snowflake's timestamp.

        Returns:
            (str): ISO8601 formatted timestamp
        """
        return self.datetime.isoformat()

    @property
    def worker_id(self) -> int:
        """Get this snowflake's worker ID.

        Returns:
            (int): worker ID
        """
        return (self.value & 0x3E0000) >> 17

    @property
    def process_id(self) -> int:
        """Get this snowflake's process ID.

        Returns:
            (int): process ID
        """
        return (self.value & 0x1F000) >> 12

    @property
    def increment(self) -> int:
        """Get this snowflake's increment.

        Returns:
            (int): increment
        """
        return self.value & 0xFFF

    # ---- hashing & display ----
    def __int__(self) -> int:
        return self.value

    def __index__(self) -> int:
        return self.value
    
    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return str(self.value)
