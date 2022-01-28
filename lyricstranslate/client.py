from typing import (
    TypeVar,
    List,
    Type,
)
from types import TracebackType

from .api import LyricsTranslateAPI
from .converter import (
    Converter,
    Suggestion,
    TrackHTMLResult,
)


class LyricsTranslateClient():
    LyricsTranslateClientType = TypeVar("LyricsTranslateClientType")

    def __init__(
        self,
        api: LyricsTranslateAPI,
        converter: Converter,
    ) -> None:
        self._api = api
        self._converter = converter

    async def __aenter__(
        self: LyricsTranslateClientType,
    ) -> LyricsTranslateClientType:
        return self

    async def __aexit__(
        self,
        _exception_type: Type[BaseException],
        _exception: BaseException,
        _traceback: TracebackType,
    ) -> None:
        await self.close()

    async def search(self, query: str) -> List[Suggestion]:
        result = await self._api.search(query)
        return self._converter.convert_search_response(result)

    async def get_song_by_url(self, url: str) -> TrackHTMLResult:
        result = await self._api.get_song_by_url(url)
        return self._converter.convert_song_html_response(result)

    async def close(self) -> None:
        await self._api.close()
