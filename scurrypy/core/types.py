from typing import Any

JSON = dict[str, Any]

Serialized = JSON | str | Any | None

HTTPResponse = JSON | str | Any | None
