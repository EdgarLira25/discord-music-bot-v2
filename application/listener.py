"""Módulo para ouvir eventos do Discord"""

from logging import getLogger
from queue import Queue
from discord import Client, Intents, Message
from application.bot import Bot
from daemons.spotify_listener import create_spotify_daemon
from models.music import InstanceParams, MusicEvent
from daemons.message import create_messaging_daemon
from daemons.music import create_musics_daemon
from services.queue_manager import QueueManager
from utils import valid_message

logs = getLogger(__name__)


class Listener(Client):

    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)

    dict_queue: dict[int, InstanceParams] = {}

    def _init_bot_instance(self, guild_id: int, message: Message):
        """Inicializa instância do bot com todas suas dependências"""
        logs.info("Iniciando nova instância para servidor: %s", guild_id)
        music_queue = Queue[MusicEvent]()
        music_queue_manager = QueueManager(music_queue)
        event_queue = Queue[Message]()
        event_queue_manager = QueueManager(event_queue)
        self.dict_queue[guild_id] = InstanceParams(
            music_queue=music_queue, event_queue=event_queue, mode="discord"
        )
        bot = Bot(
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

    async def on_ready(self):
        logs.info("BOT INICIADO")

    @valid_message
    async def on_message(self, message: Message, guild_id: int):
        "Receptor de todas mensagens do discord"
        if guild_id not in self.dict_queue:
            self._init_bot_instance(guild_id, message)

        if message.guild:
            logs.info("Adicionando Evento à: %s", message.guild.name)

        if "-switch" in message.content:
            if self.dict_queue[guild_id]["mode"] == "spotify":
                self.dict_queue[guild_id]["mode"] = "discord"
            else:
                code = message.content.split(" ")[-1]
                self.dict_queue[guild_id]["mode"] = "spotify"
                bot = Bot(guild_id, None, None, None, None)
                QueueManager(self.dict_queue[guild_id]["event_queue"]).add(message)
                create_spotify_daemon(
                    QueueManager(self.dict_queue[guild_id]["music_queue"]), bot, code
                )

        if self.dict_queue[guild_id]["mode"] == "discord":
            QueueManager(self.dict_queue[guild_id]["event_queue"]).add(message)
