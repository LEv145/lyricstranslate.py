from aiohttp import ClientSession
from injector import (
    Module,
    provider,
)

from .api import LyricsTranslateAPI
from .client import LyricsTranslateClient
from .converter import Converter


class LyricsTranslateModule(Module):
    """Module for automatic dependencies."""

    @provider
    def provide_client(self, api: LyricsTranslateAPI) -> LyricsTranslateClient:
        """
        Provide `LyricsTranslateClient`.
        Args:
            api: Object required for dependence.
        Returns:
            Provided object for injector.
        """
        return LyricsTranslateClient(api=api, converter=Converter())

    @provider
    def provide_api(self, session: ClientSession) -> LyricsTranslateAPI:
        """
        Provide `LyricsTranslateAPI`.
        Args:
            session: Object required for dependence.
        Returns:
            Provided object for injector.
        """
        return LyricsTranslateAPI(session=session)

    @provider
    def provide_client_session(self) -> ClientSession:
        """
        Provide `ClientSession`.
        Returns:
            Provided object for injector.
        """
        return ClientSession()
