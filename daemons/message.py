"""Módulo que consome os eventos da fila de message"""

from logging import getLogger
from asyncio import AbstractEventLoop, run_coroutine_threadsafe
import threading
import time
from discord import ClientException, Message
from application.bot import Bot
from models.music import MusicEvent
from services.queue_manager import QueueManager
from services.spotify import Spotify
from services.youtube import Youtube
from settings.consts import TIME

logs = getLogger(__name__)


class MessageEventDaemon(threading.Thread):

    def __init__(
        self,
        event_queue: QueueManager[Message],
        music_queue: QueueManager[MusicEvent],
        bot_provider: Bot,
        event_loop: AbstractEventLoop,
    ) -> None:
        super().__init__()
        self.event_queue = event_queue
        self.music_queue = music_queue
        self.bot = bot_provider
        self.event_loop = event_loop
        self.voice_channel = None
        self.is_running = True

    def _reconnect(self, message: Message):
        try:
            return run_coroutine_threadsafe(
                message.author.voice.channel.connect(),  # type: ignore
                self.event_loop,
            ).result(10)
        except ClientException:
            return None

    def _sync_bot_variables(self, message: Message):
        voice_client = self._reconnect(message)
        if (
            self.bot.message_channel != message.channel
            or self.bot.voice_client != voice_client
        ):
            logs.info("Sincronizando canais")
            self.bot.message_channel = message.channel  # type: ignore
            if voice_client is not None:
                self.bot.voice_client = voice_client

    def _mapper_command(self, key: str):
        return {
            "-p": "-play",
            "-s": "-skip",
            "-c": "-clear",
            "-k": "-kill",
            "-q": "-queue",
            "-help": "-help",
        }.get(key, key)

    def add_music(self, search: str):
        songs = []
        if "https://" not in search:
            songs = Youtube().search_single_song(search)
        elif "youtube.com" in search:
            songs = Youtube().search_by_link(search)
        elif "open.spotify.com" in search:
            songs = Spotify().search_by_link(search)

        if not songs:
            logs.warning("Nenhuma música valida foi encontrada")

        self.music_queue.add_many(songs)

    def process(self, command: str, content: list[str]):
        match command:
            case "-play":
                if len(content) < 2:
                    logs.warning("Nenhuma música enviada")
                    return
                self.bot.send_queue_message()
                threading.Thread(
                    target=self.add_music,
                    args=(content[1],),
                ).start()
            case "-pause":
                self.bot.pause()
            case "-skip":
                self.bot.skip()
            case "-clear":
                self.bot.clear()
            case "-kill":
                self.bot.kill()
            case "-queue":
                self.bot.queue()
            case "-help":
                self.bot.help()
            case _:
                self.bot.send("Comando não encontrado. Use -help")

    def _handle_event_variables(self) -> tuple[str, list[str]]:
        """Realiza a leitura do evento e sincroniza as variaveis"""
        event = self.event_queue.get()
        content = event.content.split(" ", 1)
        command = self._mapper_command(content[0])
        self._sync_bot_variables(event)
        logs.info("Enviando evento para processamento...")
        return command, content

    def _loop(self):
        while self.is_running:
            if self.event_queue.size() > 0:
                logs.info("Evento encontrado, tratando...")
                self.process(*self._handle_event_variables())
            time.sleep(TIME)

    def run(self):
        self._loop()


def create_messaging_daemon(
    event_manager: QueueManager[Message],
    music_manager: QueueManager[MusicEvent],
    bot_provider: Bot,
    event_loop: AbstractEventLoop,
):
    MessageEventDaemon(event_manager, music_manager, bot_provider, event_loop).start()
