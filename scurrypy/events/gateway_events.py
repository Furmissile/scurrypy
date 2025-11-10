from dataclasses import dataclass
from ..model import DataModel

@dataclass
class SessionStartLimit(DataModel):
    total: int
    remaining: int
    reset_after: int
    max_concurrency: int

@dataclass
class GatewayEvent(DataModel):
    url: str 
    shards: int
    session_start_limit: SessionStartLimit
