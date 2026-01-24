## Contributing to ScurryPy

First and foremost, *thank you for your interest in contributing to ScurryPy*!

Future contributions should adhere to clean and understandable architecture. With this said, a lot of the infrastructure is already in place, it's just the matter of coverage and mimicking what's already there. 
ScurryPy is *feature-neutral* but *architecture-opinionated*. It doesn’t enforce how users must build bots, only how the library itself stays consistent.

The following sections will detail what's left and how it's expected to be filled out.

## Philosophy

ScurryPy prioritizes **clarity over magic**. When contributing:

* Every operation should be traceable
* No hidden behavior or side effects
* No attribute modification from outside the class
* Simple, explicit code over clever abstractions
* If you can't explain it in 3-6 steps, simplify it

## What's Needed

**High Priority:**
* Missing endpoints and resources (see [Discord API docs](https://discord.com/developers/docs))
* Documentation improvements

**Nice to Have:**
* Example bots
* Guide

**Not Accepting:**
* Auto-caching (architectural decision)
* Voice support (out of scope for now)
* Subcommands (lots of overhead for not enough gain)
* Endpoints with non-`bot` auth scopes, are unstable/experimental, or related to voice.
* Anything monetization based (e.g., entitlements and subscriptions)

> **Important Note**: Throughout this document, Discord's payloads are called objects and ScurryPy's models are called data classes.

## Models

All models and resources in ScurryPy are data classes themselves and inherit the `DataModel` base class. 

Please refer to the following template for how all of ScurryPy's objects are expected to be formatted:

```python
from dataclasses import dataclass
from .model import DataModel

from typing import Optional # only if you need it

@dataclass
class YourModel(DataModel):
    """Your model's description."""

    field_1: type
    """This is a mandatory field. It needs to be filled NOW."""

    field_2: Optional[type]
    """This is an optional field. It might be omitted."""
```
Notes:
* Fields must mimic objects verbatim. (e.g., if an object field is named `icon`, the dataclass field must also be called `icon`.)
* Descriptions are preferrably in your own words, but you can also just use Discord's docs.
* If an object appears that was already defined, use that model; don't create a new model! (e.g., the user object appears in many places. Always use the defined `UserModel`.)

For MODELS ONLY:
* Models should have NO helper functions. Functions in models will be removed! The only exception is if the helper function can be *widely* used (e.g., `Channel.user_can`).
* Models are NOT responsible for HTTP requests. Resources do this!

## Resources
Resources are just like model, but with added functionality. All resources inherit the [`BaseResource`](https://scurry-works.github.io/scurrypy/internals/model/#scurrypy.resources.base_resource.BaseResource) class.

Please refer to the following example for how the resource is expected to be laid out:

```python
from dataclasses import dataclass
from .base_resource import BaseResource

@dataclass
class YourResource(BaseResource):
    """Your resource's description."""

    # fields needed to fetch this resource

    # endpoints as functions
```

[`Client`](https://scurry-works.github.io/scurrypy/api/client/#scurrypy.client.Client) provides a thin layer for requesting resources. If you implement a new resource, please also add it to the client as follows:

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
> **NOTE:** document the function completely!

## Endpoints
All endpoints should send requests through [`HTTPClient.request()`](https://scurry-works.github.io/scurrypy/internals/http/#scurrypy.core.http.HTTPClient.request) and be attached to their respective resource. Which resource gets the endpoint is based on the criteria of the endpoint, NOT based on how Discord organizes them. 
For example, the endpoint for fetching messages falls under the Message resource by Discord's docs. However, by ScurryPy's standards, the endpoint falls under the Channel resource because the endpoint requires a channel ID.

Discord's resources have 4 common actions: fetch, create, edit, and delete. These functions must always be implemented as:

* *DELETE/PUT*: parameters to the endpoint's function
* *POST*: add a part or use an existing part from `/parts`
* *PATCH*: add a param or use an existing param in `/params`

    ### Parts
    Parts are used to model Discord payloads the user sends. Parts are just like models, except all fields are deferrable, meaning they must be set to `None`. 

    If you implement a new part, it should be formatted as follows:

    ```python
    @dataclass
    class YourPart(DataModel):
        """Your model's description."""

        field_1: type = None
        """This is a field that must be filled out at some point."""

        field_2: Optional[type] = None
        """This is an optional field. It can be omitted."""
    ```

    > **NOTE:** querying params are NOT a part!

    ### Parameters
    Modifying endpoints that edit discord objects should have a parameters object defined in `params/`. These objects represent the fields that can be modified.

    If you implement a new param, it should be formatted as follows:

    ```python
    from typing import TypedDict, Optional

    class MyParams(TypedDict, total=False):
        """Your params description."""

        field_1: type
        """This field must be filled out."""

        field_2: Optional[type]
        """This field is optional and may be omitted."""
    ```

    > **NOTE:** if including a dataclass, please prepare to convert it to a dictionary using `DataModel.to_dict` in the resource endpoint.

## Questions?
Open an issue or discussion!

Want to understand the architecture? See the [Technical Deep-Dive](https://scurry-works.github.io/scurrypy/internals/technical_writeup)!
