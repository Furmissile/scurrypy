## Contributing to ScurryPy

*Thank you for your interest in contributing to ScurryPy*!

Contributions must adhere to ScurryPy’s existing architectural patterns.
ScurryPy is *feature-neutral* but *architecture-opinionated*. 
It doesn’t enforce how users must build bots, only how the library itself stays consistent.

## What's Needed

ScurryPy is officially in its "maintenance" stage, meaning add and modify only with Discord's API changes.

**Not Accepting:**

* Auto-caching (opt-in only. See `scurrypy.ext.cache`)
* Voice support and *Group* DM (out of scope)
* Sub-commands and automodding (lots of overhead for not enough gain)
* Auditing (includes many unsupported features)
* Endpoints with non-`bot` auth scopes, are unstable/experimental, or related to voice.
* Anything monetization based (e.g., entitlements and subscriptions)

While ScurryPy itself may not offer these features by default, you are more than welcome to extend ScurryPy to include these features.

> [!TIP]
> The following formats assume this [mindset](https://scurry-works.github.io/scurrypy/getting_started/mindset/).

## Reference

### API (Parts and Models)

```python
@dataclass
class YourPart(DataModel):
    """Your model's description."""

    field_1: type | None = None
    """This is a field that must be filled out at some point."""

    field_2: type | None = None
    """This is an optional field. It can be omitted."""

@dataclass
class YourModel(DataModel):
    """Your model's description."""

    field_1: type
    """This field will always be hydrated by Discord."""

    field_2: type | None
    """This field might be hydrated by Discord."""
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

    return YourResource(self._http, some_id, etc...)
```

### Parameters

```python
from typing import TypedDict

class MyParams(TypedDict, total=False):
    """Your params description."""

    field_1: type
    """This field must be filled out."""

    field_2: type | None
    """This field is optional and may be omitted."""
```
> [!NOTE]
> If a DataModel is included, please use `scurrypy.core.serialization.serialize` before passing to `HTTPClient.request`.

## Questions?
Open an issue or discussion!

Want to understand the architecture? See the [Technical Deep-Dive](https://scurry-works.github.io/scurrypy/internals/technical_writeup)!
