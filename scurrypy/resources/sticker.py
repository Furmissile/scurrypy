from dataclasses import dataclass

from ..core.snowflake import Snowflake

from .base_resource import BaseResource

from ..models.sticker import StickerModel, StickerPackModel

@dataclass
class Sticker(BaseResource):
    """Represents the Sticker resource."""

    async def fetch(self, sticker_id: Snowflake) -> StickerModel:
        """Fetch a sticker.
        
        Args:
            sticker_id (Snowflake): ID of the sticker to fetch

        Returns:
            (StickerModel): queried sticker
        """
        data = await self._http.request('GET', f'/stickers/{sticker_id}')

        return StickerModel.from_dict(data)

    async def fetch_sticker_pack(self, pack_id: Snowflake) -> StickerPackModel:
        """Fetch a sticker pack.

        Args:
            pack_id (Snowflake): ID of the pack to fetch

        Returns:
            (StickerPackModel): queried sticker pack
        """
        data = await self._http.request('GET', f'/sticker-packs/{pack_id}')

        return StickerPackModel.from_dict(data)

    async def fetch_sticker_packs(self) -> list[StickerPackModel]:
        """Fetch available sticker packs.

        Returns:
            list[StickerPackModel]: queried list of sticker packs.
        """
        data = await self._http.request('GET', '/sticker-packs')

        stickers = data.get('sticker_packs')

        return [StickerPackModel.from_dict(i) for i in stickers]
