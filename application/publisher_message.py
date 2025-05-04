from asyncio import AbstractEventLoop
import unicodedata
from discord import Member, Message, Interaction, TextChannel
from discord.channel import VocalGuildChannel
from models.message import MessageEvent
from services.instance_manager import InstanceManager

# pylint: disable=too-many-boolean-expressions


class PublisherMessage:
    def __init__(self, instance_manager_provider: InstanceManager) -> None:
        self.instance_manager = instance_manager_provider

    def create_message_event(
        self, message: Interaction | Message, prefix: str = "", item: str = ""
    ) -> MessageEvent | None:
        content = (
            f"{prefix.strip()} {item.strip()}"
            if isinstance(message, Interaction)
            else message.content
        )
        user = message.user if isinstance(message, Interaction) else message.author

        if (
            message.guild
            and not user.bot
            and isinstance(user, Member)
            and user.voice
            and isinstance(user.voice.channel, VocalGuildChannel)
            and isinstance(message.channel, TextChannel)
            and content.startswith("-")
            and (
                "music"
                in "".join(
                    char
                    for char in unicodedata.normalize("NFD", message.channel.name)
                    if unicodedata.category(char) != "Mn"
                ).lower()
            )
        ):
            return MessageEvent(
                message.guild.id,
                user.voice.channel,
                user,
                message.channel,
                content,
            )
        return None

    def publish(
        self, source: Interaction | Message, loop: AbstractEventLoop, prefix="", item=""
    ):
        if message_event := self.create_message_event(source, prefix, item):
            self.instance_manager.add_event(message_event.guild_id, message_event, loop)
