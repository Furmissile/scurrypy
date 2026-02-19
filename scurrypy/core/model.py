from dataclasses import dataclass, fields

from .serialization import convert, serialize

@dataclass
class DataModel:    
    """DataModel is a base class for Discord JSONs that provides 
        hydration from raw dicts, and optional field defaults.
    """

    @classmethod
    def from_dict(cls, data: dict):
        """Hydrates the given data into the dataclass.

        Args:
            data (dict): the JSON data

        Returns:
            (cls): hydrated dataclass
        """
        if data is None:
            return None
        
        kwargs = {}

        for f in fields(cls):
            if not f.init: # ignore init=False fields
                continue

            kwargs[f.name] = convert(f.type, data.get(f.name))

        return cls(**kwargs)
        
    def to_dict(self):
        """Recursively turns the dataclass into a dictionary and drops empty fields.

        Returns:
            (dict): serialized dataclasss
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
