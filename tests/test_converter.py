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

        result = self.converter.convert_search_response(
            11*"\n" + '{"suggestions": [{"value": "", "data": []}]}'
        )
        self.assertEqual(result, [])

    def test_convert_song_html_response(self) -> None:
        with open(Path("tests/testdata/song_html_response.txt")) as fp:
            raw_data = fp.read()

        result = self.converter.convert_song_html_response(raw_data)
        self.assertIsInstance(result, TrackHTMLResult)

        with self.assertRaises(ValueError):
            self.converter.convert_song_html_response(
                "<!DOCTYPE html>\n"
                "<html>\n"
                "  <head>\n"
                "    <meta charset=\"utf-8\">\n"
                "  </head>\n"
                "  <body>\n"
                "    <img src=\"images/firefox-icon.png\" alt=\"My test image\">\n"
                "  </body>\n"
                "</html>\n"
            )
