from dataclasses import dataclass, fields, is_dataclass
from typing import get_args, get_origin, Union

from .http import HTTPClient

@dataclass
class DataModel:    
    """DataModel is a base class for Discord JSONs that provides hydration from raw dicts, 
        optional field defaults, and access to HTTP-bound methods.
    """
    
    @classmethod
    def from_dict(cls, data: dict, http: HTTPClient = None):
        """Hydrates the given data into the dataclass child.

        Args:
            data (dict): JSON data
            http (HTTPClient, optional): HTTP session for requests

        Returns:
            (dataclass): hydrated dataclass
        """
        kwargs = {}

        def unwrap_optional(typ):
            """Remove NoneType from Optional or leave Union as-is."""
            if get_origin(typ) is Union:
                args = tuple(a for a in get_args(typ) if a is not type(None))
                if len(args) == 1:
                    return args[0]  # single type left
                else:
                    return Union[args]  # multi-type union remains
            return typ
        
        for field in fields(cls):
            # property must be in given json!
            value = data.get(field.name)
            
            inner_type = unwrap_optional(field.type)

            # Handle None
            if value is None:
                kwargs[field.name] = None
            # Integers stored as strings
            elif isinstance(value, str) and value.isdigit():
                kwargs[field.name] = int(value)
            # Nested dataclass
            elif is_dataclass(inner_type):
                kwargs[field.name] = inner_type.from_dict(value, http)
            # List type
            elif get_origin(inner_type) is list:
                list_type = get_args(inner_type)[0]
                kwargs[field.name] = [
                    list_type.from_dict(v, http) if is_dataclass(list_type) else v
                    for v in value
                ]
            # Everything else (primitive, Union of primitives)
            else:
                kwargs[field.name] = value
            
        instance = cls(**kwargs)

        # attach HTTP if given
        if http:
            instance._http = http

        return instance

    def _to_dict(self):
        """Recursively turns the dataclass into a dictionary and drops empty fields.

        Returns:
            (dict): serialized dataclasss
        """
        def serialize(value):
            if isinstance(value, list):
                return [serialize(v) for v in value]
            if isinstance(value, DataModel):
                return value._to_dict()
            return value
    
        result = {}
        for f in fields(self):
            if f.name.startswith('_'): # ignore private fields
                continue
            value = getattr(self, f.name)
            if value not in (None, [], {}, "", 0):
                result[f.name] = serialize(value)
        
        return result
