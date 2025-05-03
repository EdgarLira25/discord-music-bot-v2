from dataclasses import dataclass
from typing import overload
from unittest.mock import MagicMock
from discord import ClientException, Message, TextChannel, VoiceClient, Member
from discord.channel import VocalGuildChannel


from models.message import MessageEvent

# pylint: skip-file


@dataclass
class GuildMock:
    id: int | None
    name = "Teste"


class ChannelMock(VocalGuildChannel):
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


@dataclass()
class MessageEventMock(MessageEvent):
    guild_id: int | None
    voice_channel: ChannelMock | None
    author: AuthorMock | None
    channel: TextChannelMock | None
    content: str | None
