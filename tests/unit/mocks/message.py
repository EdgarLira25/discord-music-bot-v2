from dataclasses import dataclass
from unittest.mock import MagicMock
from discord import ClientException, Message, TextChannel, VoiceClient

# pylint: skip-file


@dataclass
class GuildMock:
    id: int | None


class ChannelMock:
    def __init__(self, should_raise: bool) -> None:
        self.should_raise = should_raise

    async def connect(self) -> VoiceClient:
        "Deveria ser async, mas não configurei o ambiente bem o suficiente para o funcionamento ideal disso"
        if self.should_raise is True:
            raise ClientException
        return MagicMock(spec=VoiceClient)


class VoiceMock:
    def __init__(self, should_raise=False) -> None:
        self.channel = ChannelMock(should_raise)


class AuthorMock:
    def __init__(self, bot: bool, voice: VoiceMock | None = None) -> None:
        self.bot = bot
        self.voice = voice


class TextChannelMock(TextChannel):
    def __init__(self, name):
        self.id = 1
        self.name = name


class MessageMock(Message):
    def __init__(
        self,
        guild: GuildMock | None,
        author: AuthorMock,
        channel: TextChannelMock | None,
        content: str,
    ) -> None:
        self.guild = guild
        self.author = author
        self.channel = channel
        self.content = content
