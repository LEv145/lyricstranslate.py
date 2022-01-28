from .api import LyricsTranslateAPI
from .converter import Converter


class LyricsTranslateClient():
    def __init__(
        self,
        api: LyricsTranslateAPI,
        converter: Converter,
    ):
        self._api = api
        self.converter = converter

