from typing import (
    List,
)

from .api import LyricsTranslateAPI
from .converter import (
    Converter,
    Suggestion,
    TrackHTMLResult,
)


class LyricsTranslateClient():
    def __init__(
        self,
        api: LyricsTranslateAPI,
        converter: Converter,
    ):
        self._api = api
        self._converter = converter

    async def search(self, query: str) -> List[Suggestion]:
        result = await self._api.search(query)
        return self._converter.convert_search_response(result)

    async def get_song_by_url(self, url: str) -> TrackHTMLResult:
        result = await self._api.get_song_by_url(url)
        return self._converter.convert_song_html_response(result)
