from dataclasses import dataclass
from discord import Member, TextChannel
from discord.channel import VocalGuildChannel


@dataclass
class MessageEvent:
    guild_id: int
    voice_channel: VocalGuildChannel
    author: Member
    channel: TextChannel
    content: str
