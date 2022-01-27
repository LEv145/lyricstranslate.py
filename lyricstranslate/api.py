import json  # TODO: json inject
from typing import (
    TYPE_CHECKING,
    AsyncIterator,
    Any,
)
from contextlib import asynccontextmanager


if TYPE_CHECKING:
    from aiohttp import ClientSession, ClientResponse


BASE_URL = "https://lyricstranslate.com"


class LyricsTranslateAPI():
    def __init__(self, session: "ClientSession") -> None:
        self._session = session

    async def close(self):
        await self._session.close()

    async def search(self, query: str) -> str:
        async with self._request(
            "GET",
            url=f"{BASE_URL}/en/ajax/lyricstranslategoogleautocomplete/autocomplete",
            params={
                "query": query.lower()
            },
        ) as response:
            text: str = await response.text()

        return text

    async def get_song_by_url(self, url: str) -> str:
        async with self._request(url=url) as response:
            text: str = await response.text()

        return text

    @asynccontextmanager
    async def _request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> AsyncIterator["ClientResponse"]:  # TODO: PyLance typing
        response = await self._session.request(method, url, **kwargs)

        try:
            yield response
        finally:
            await response.__aexit__(None, None, None)
