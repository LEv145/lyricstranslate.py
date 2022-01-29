import re
import json
from typing import (
    List,
)

from bs4 import BeautifulSoup

from lyricstranslate.constants import BASE_URL
from .beautiful_soup import assert_find
from .models import (
    Suggestion,
    Category,
    TrackHTMLResult,
)


class Converter():
    def convert_search_response(self, raw_data: str) -> List[Suggestion]:
        json_data = json.loads(raw_data[11:])

        # noinspection PyProtectedMember
        return [
            Suggestion(
                category=(
                    Category(category_raw_data)
                    if (
                        category_raw_data := raw_suggestion["data"]["category"]
                    ) in Category._value2member_map_
                    else Category.UNKNOWN
                ),
                name=raw_suggestion["value"],
                url=f'{BASE_URL}{raw_suggestion["data"]["url"]}',
            )
            for raw_suggestion in json_data["suggestions"]
            if raw_suggestion["value"]
        ]

    def convert_song_html_response(self, raw_data: str) -> TrackHTMLResult:
        soup = BeautifulSoup(raw_data, "lxml")

        node_tag = assert_find(soup, "div", class_="node")
        node_id = node_tag["id"]

        track_id_match = re.match(r'node-(\d+)', node_id)
        if track_id_match is None:
            raise ValueError("Track ID not matched")  # TODO?: Another error

        track_id = track_id_match.group(1)
        track_title = assert_find(soup, "h2", class_="title-h2").text.strip()
        track_lyrics = [
            part.text
            for part in assert_find(soup, "div", class_="ltf").find_all("div", class_="par")
        ]

        return TrackHTMLResult(
            id_=track_id,
            title=track_title,
            lyrics=track_lyrics,
        )
