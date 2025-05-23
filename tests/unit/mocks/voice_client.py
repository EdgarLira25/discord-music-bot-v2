from asyncio import AbstractEventLoop
from typing import Any
from discord import VoiceClient

# pylint: skip-file


class VoiceClientMock(VoiceClient):
    def __init__(
        self,
        return_is_playing: bool,
        loop: None | AbstractEventLoop = None,
        is_paused=False,
    ) -> None:
        self.return_is_playing = return_is_playing
        self.loop = loop
        self._is_paused = is_paused

    def is_playing(self):
        return self.return_is_playing

    def pause(self):
        return None

    def is_paused(self):
        return False

    def resume(self):
        return None

    def play(self, source: Any):
        return None
