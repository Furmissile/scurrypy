from dataclasses import dataclass

@dataclass
class BaseConfig:
    """Config class that lives inside Client and can be extended by the dev to add persistent data (like a database)."""
    pass
