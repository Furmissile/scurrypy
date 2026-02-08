## Contributing to ScurryPy

*Thank you for your interest in contributing to ScurryPy*!

Contributions must adhere to ScurryPy’s existing architectural patterns.
ScurryPy is *feature-neutral* but *architecture-opinionated*. 
It doesn’t enforce how users must build bots, only how the library itself stays consistent.

## What's Needed

ScurryPy is officially in its "maintenance" stage, meaning add and modify only with Discord's API changes.

**Not Accepting:**

* Auto-caching (architectural decision)
* Voice support and *Group* DM (out of scope)
* Sub-commands and automodding (lots of overhead for not enough gain)
* Auditing (includes many unsupported features)
* Endpoints with non-`bot` auth scopes, are unstable/experimental, or related to voice.
* Anything monetization based (e.g., entitlements and subscriptions)

While ScurryPy itself may not offer these features by default, you are more than welcome to extend ScurryPy to include these features.

> [!TIP]
> The following formats assume this [mindset](https://scurry-works.github.io/scurrypy/getting_started/mindset/).

## Reference

### Models

```python
from dataclasses import dataclass
from .model import DataModel

from typing import Optional # only if you need it

@dataclass
class YourModel(DataModel):
    """Your model's description."""

    field_1: type
    """This is a mandatory field."""

    field_2: Optional[type]
    """This is an optional field. It might be omitted."""
```
> [!NOTE]
> Objects must be unique (no partial copies) with their fields replicating Discord's and be fully documented.

### Resources

```python
from dataclasses import dataclass
from .base_resource import BaseResource

@dataclass
class YourResource(BaseResource):
    """Your resource's description."""

    # fields needed to fetch this resource

    # endpoints as functions
```

Then in the client class:

```python
def your_resource(self, some_id: int, etc, *, context = None):
    """Creates an interactable resource.

    Args:
        some_id (int): ID of target resource

    Returns:
        (YourResource): the class resource
    """
    from .resources.me import YourResource

    return YourResource(self._http, context, some_id, etc...)
```

### Parts

```python
@dataclass
class YourPart(DataModel):
    """Your model's description."""

    field_1: type = None
    """This is a field that must be filled out at some point."""

    field_2: Optional[type] = None
    """This is an optional field. It can be omitted."""
```

### Parameters

```python
from typing import TypedDict, Optional

class MyParams(TypedDict, total=False):
    """Your params description."""

    field_1: type
    """This field must be filled out."""

    field_2: Optional[type]
    """This field is optional and may be omitted."""
```
> [!NOTE]
> If including a dataclass, please prepare to convert it to a dictionary using `DataModel.to_dict` in the resource endpoint.

## Questions?
Open an issue or discussion!

Want to understand the architecture? See the [Technical Deep-Dive](https://scurry-works.github.io/scurrypy/internals/technical_writeup)!
