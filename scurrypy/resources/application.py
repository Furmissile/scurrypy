from dataclasses import dataclass

from ..core.snowflake import Snowflake

from ..models.application import ApplicationModel

from .base_resource import BaseResource

@dataclass
class Application(BaseResource):
    """Represents a Discord application."""

    id: Snowflake
    """ID of the application."""

    async def fetch(self) -> ApplicationModel:
        """Fetch this application's data.

        Returns:
            (Application): queried application
        """
        data = await self._http.request('GET', '/applications/@me')

        return ApplicationModel.from_dict(data)
