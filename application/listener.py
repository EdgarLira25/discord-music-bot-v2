from queue import Queue
from discord import Client, Intents, Message
from application.bot import RagdeaBot
from models.music import MusicEvent
from daemons.message import create_messaging_daemon
from daemons.music import create_musics_daemon
from services.queue_manager import QueueManager
from utils import valid_message


class Listener(Client):

    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)

    dict_queue: dict[int, Queue[Message]] = {}

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

    @valid_message
    async def on_message(self, message: Message, guild_id: int):
        if guild_id not in self.dict_queue:
            await self._init_bot_instance(guild_id, message)

        QueueManager(self.dict_queue[guild_id]).add(message)
