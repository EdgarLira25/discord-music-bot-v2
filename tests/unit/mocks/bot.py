from application.bot import Bot
from models.music import MusicEvent

# pylint: skip-file


class BotMock(Bot):
    def __init__(self, voice_client) -> None:
        self.voice_client = voice_client

    def play(self, event: MusicEvent):
        assert isinstance(event, MusicEvent)
