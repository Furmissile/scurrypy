from dataclasses import dataclass, fields

from .serialization import convert, serialize

from typing import TypeVar, Self

T = TypeVar("T", bound="DataModel")

from .types import Serialized, HTTPResponse

@dataclass
class DataModel:    
    """DataModel is a base class for Discord JSONs that provides 
        hydration from raw dicts, and optional field defaults.
    """

    @classmethod
    def from_dict(cls, data: HTTPResponse) -> Self:
        """Hydrates the given data into the dataclass.

        Args:
            data (HTTPResponse): the JSON data

        Returns:
            (cls): hydrated dataclass
        """
        assert data is not None

        kwargs = {}

        for f in fields(cls):
            if not f.init: # ignore init=False fields
                continue

            assert isinstance(data, dict)
            kwargs[f.name] = convert(f.type, data.get(f.name))

        return cls(**kwargs)
        
    def to_dict(self) -> Serialized:
        """Recursively turns the dataclass into a dictionary and drops empty fields.

        Returns:
            (Serialized): serialized dataclasss
        """
        result = {}
        for f in fields(self):
            if f.name.startswith('_'):
                continue
            val = getattr(self, f.name)
            # only include real values
            if val is not None:
                result[f.name] = serialize(val)
        return result
