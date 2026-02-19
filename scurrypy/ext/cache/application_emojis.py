from scurrypy import Client
from scurrypy.bases import Addon
from scurrypy.core import Snowflake
from scurrypy.api import EmojiModel

class ApplicationEmojisCacheAddon(Addon):
    """Defines caching bot emojis and lookup."""

    def __init__(self, client: Client, application_id: Snowflake):
        self.bot = client
        self.application_id = application_id

        self.emojis: dict[str, EmojiModel] = {}   # index by unique name

        client.add_startup_hook(self.load_bot_emojis)

    async def load_bot_emojis(self):
        """Fetch all bot's emojis and add them to the cache."""
        emojis = await self.bot.bot_emoji(self.application_id).fetch_all()

        for emoji in emojis:
            self.emojis[emoji.name] = emoji

    def get_emoji(self, name: str):
        """Get an emoji from the cache.

        Args:
            name (str): name of the emoji

        Returns:
            (EmojiModel | None): the emoji object if found else None
        """
        return self.emojis.get(name)
