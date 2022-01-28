import json

from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock

from lyricstranslate.api import LyricsTranslateAPI


class TestLyricsTranslateAPI(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.api = LyricsTranslateAPI(session=AsyncMock())

        # noinspection PydanticTypeChecker
        self.session: AsyncMock = self.api._session  # type: ignore

    async def asyncTearDown(self) -> None:
        await self.api.close()

    async def test_search(self):
        with open(Path("tests/testdata/search_response.txt")) as fp:
            search_response = fp.read()

        self.session.request.return_value = AsyncMock(
            **{"text.return_value": search_response}
        )

        result = await self.api.search(query="Сектор газа")

        self.assertEqual(result, search_response,)

    async def test_get_song_by_url(self):
        with open(Path("tests/testdata/song_html_response.txt")) as fp:
            song_html_response = fp.read()

        self.session.request.return_value = AsyncMock(
            **{"text.return_value": song_html_response}
        )

        result = await self.api.get_song_by_url(
            "https://lyricstranslate.com/en/sektor-gaza-sektor-gaza-%D1%81%D0%B5%D0%BA%D1%82%D0%BE%D1%80-%D0%B3%D0%B0%D0%B7%D0%B0-lyrics.html"
        )

        self.assertEqual(result, song_html_response)
