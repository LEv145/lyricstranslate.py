import re
import json
from typing import (
    List,
)

from bs4 import BeautifulSoup

from lyricstranslate.constants import BASE_URL
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
        soup = BeautifulSoup(raw_data, "lxml")  # TODO: Beautiful soup assert parser

        node_tag = soup.find("div", class_="node")
        if node_tag is None:
            raise BeautifulSoupParserError("Node tag not found")

        try:
            node_id = node_tag["id"]
        except KeyError:
            raise BeautifulSoupParserError("Node tag hasn't attribute id")

        track_id_match = re.match(r'node-(\d+)', node_id)
        if track_id_match is None:
            raise BeautifulSoupParserError("Track id not matched")

        track_id = track_id_match.group(1)

        track_title_tag = soup.find("h2", class_="title-h2")
        if track_title_tag is None:
            raise BeautifulSoupParserError("Title tag not found")

        track_title = track_title_tag.text.strip()

        ltf_tag = soup.find("div", class_="ltf")
        if ltf_tag is None:
            raise BeautifulSoupParserError("Ltf tag not found")

        track_lyrics = [
            part.text
            for part in ltf_tag.find_all("div", class_="par")
        ]

        return TrackHTMLResult(
            id_=track_id,
            title=track_title,
            lyrics=track_lyrics,
        )


class BeautifulSoupParserError(Exception):  # This error should be in BeautifulSoup
    """Error if parsed data is not valid."""
