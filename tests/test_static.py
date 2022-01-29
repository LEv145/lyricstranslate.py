import os
from unittest import IsolatedAsyncioTestCase, skipUnless

from injector import Injector

from lyricstranslate import (
    LyricsTranslateModule,
    LyricsTranslateClient,
    TrackHTMLResult,
    BeautifulSoupParserError,
)


@skipUnless(
    condition=os.getenv("ONLINE_TEST", "0") == "1",
    reason="Requires online mode",
)
class TestLyricsTranslateAPI(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        injector = Injector(LyricsTranslateModule)
        self.client = injector.get(LyricsTranslateClient)

    async def test_search(self):
        async with self.client as client:
            result = await client.search("Сектор газа")
            self.assertIsInstance(result, list)

            result = await client.search("43728943264986324982")
            self.assertIsInstance(result, list)

            result = await client.search(" \t\t ")
            self.assertIsInstance(result, list)

    async def test_get_song_by_url(self):
        async with self.client as client:
            result = await client.get_song_by_url("https://lyricstranslate.com/en/sektor-gaza-sektor-gaza-%D1%81%D0%B5%D0%BA%D1%82%D0%BE%D1%80-%D0%B3%D0%B0%D0%B7%D0%B0-lyrics.html")
            self.assertIsInstance(result, TrackHTMLResult)

            with self.assertRaises(ValueError):
                await client.get_song_by_url(" \t\t ")

            with self.assertRaises(ValueError):
                await client.get_song_by_url("https://www.gnu.org")

            with self.assertRaises(BeautifulSoupParserError):
                await client.get_song_by_url("https://lyricstranslate.com/en/bts-bangtan-boys-lyrics.html")
