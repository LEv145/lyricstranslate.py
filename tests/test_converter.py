from unittest import TestCase
from pathlib import Path

from lyricstranslate.converter import (
    Converter,
    Suggestion,
    TrackHTMLResult,
)


class TestConverter(TestCase):
    def setUp(self) -> None:
        self.converter = Converter()

    def test_convert_search_response(self) -> None:
        with open(Path("tests/testdata/search_response.txt")) as fp:
            raw_data = fp.read()

        result = self.converter.convert_search_response(raw_data)
        self.assertIsInstance(result[0], Suggestion)

    def test_convert_song_html_response(self) -> None:
        with open(Path("tests/testdata/song_html_response.txt")) as fp:
            raw_data = fp.read()

        result = self.converter.convert_song_html_response(raw_data)
        self.assertIsInstance(result, TrackHTMLResult)
