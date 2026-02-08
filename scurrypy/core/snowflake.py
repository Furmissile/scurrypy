from datetime import datetime, timezone

DISCORD_EPOCH = 1420070400000

class Snowflake(int):
    """Represents a Discord snowflake ID."""

    @property
    def timestamp_ms(self) -> int:
        return (self >> 22) + DISCORD_EPOCH

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp_ms / 1000, tz=timezone.utc)

    @property
    def isoformat(self) -> str:
        return self.datetime.isoformat()

    @property
    def worker_id(self) -> int:
        return (self & 0x3E0000) >> 17

    @property
    def process_id(self) -> int:
        return (self & 0x1F000) >> 12

    @property
    def increment(self) -> int:
        return self & 0xFFF
