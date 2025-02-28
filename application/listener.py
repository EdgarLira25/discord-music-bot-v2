from queue import Queue
from typing import Any, Optional
from discord import Client, Intents, Message, TextChannel
from application.bot import RagdeaBot
from models.music import MusicEvent
from services.daemons.message import create_messaging_daemon
from services.daemons.music import create_musics_daemon
from services.queue_manager import QueueManager
from utils.formatters import normalize_text


class Listener(Client):

    def __init__(
        self,
        *,
        intents: Intents,
        **options: Any,
    ) -> None:
        super().__init__(intents=intents, **options)

    dict_queue: dict[int, Queue[Message]] = {}

    def _get_guild_id_if_valid_command(self, message: Message) -> Optional[int]:

        if (
            message.guild
            and not message.author.bot
            and isinstance(message.channel, TextChannel)
            and message.content.startswith("-")
            and "music" in normalize_text(message.channel.name)
        ):
            return message.guild.id


    async def _init_bot_instance(self, guild_id: int, message: Message):
        music_queue = Queue[MusicEvent]()
        music_queue_manager = QueueManager(music_queue)
        event_queue = Queue[Message]()
        event_queue_manager = QueueManager(event_queue)
        self.dict_queue[guild_id] = event_queue
        bot = RagdeaBot(
            guild_id,
            message.author.voice.channel,  # type: ignore
            message.channel,
            None,
            music_queue_manager,
        )
        create_messaging_daemon(
            event_queue_manager, music_queue_manager, bot, self.loop
        )
        create_musics_daemon(music_queue_manager, bot)

    async def on_message(self, message: Message):
        guild_id = self._get_guild_id_if_valid_command(message)
        if not guild_id or len(self.dict_queue) > 4:
            return

        if guild_id not in self.dict_queue:
            await self._init_bot_instance(guild_id, message)

        QueueManager(self.dict_queue[guild_id]).add_item(message)
