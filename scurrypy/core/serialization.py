from typing import get_args, get_origin, Union
from types import UnionType

from ..bases.components import Component

def serialize(val) -> dict:
    """Serialize the value.

    Args:
        val (Any): value to serialize

    Returns:
        (dict): serialized value
    """
    if hasattr(val, "to_dict"):
        return val.to_dict()
    
    if isinstance(val, list):
        return [serialize(v) for v in val if v is not None]
    
    if isinstance(val, dict):
        return {k: serialize(v) for k, v in val.items()}

    return val

def convert(t, v):
    """Convert the given value to the given type.

    Args:
        t (type): type in which to convert value
        v (Any): value to be converted

    Raises:
        (TypeError): ambiguous type

    Returns:
        (type): converted value
    """
    o = get_origin(t)

    if o in (Union, UnionType): # optional[T] or similar
        non_none = [a for a in get_args(t) if a is not type(None)]

        if len(non_none) > 1:
            raise TypeError(f"Expected deterministic type; got {non_none}.")
        
        return convert(non_none[0], v)
    
    if v is None: # missing field
        return None
    
    if t is bool:
        return v in ('true', 'True', True)
    
    if o is dict: # mappings
        from .snowflake import Snowflake
        vt = get_args(t)[1]
        return {
            Snowflake(k): convert(vt, x) 
            for k, x in v.items()
        }
    
    if o is list:
        lt = get_args(t)[0]
        return [convert(lt, x) for x in v]
    
    if t is Component:
        from ..api.components import MessageComponentFactory
        return MessageComponentFactory.from_dict(v)

    if hasattr(t, "from_dict"):
        return t.from_dict(v)

    # primitive / fallback
    return t(v)