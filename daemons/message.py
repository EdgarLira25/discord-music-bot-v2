from asyncio import AbstractEventLoop, run_coroutine_threadsafe
import threading
import time
from discord import Message
from application.bot import RagdeaBot
from models.music import MusicEvent
from services.queue_manager import QueueManager
from services.youtube import Youtube


class MessageEventDaemon(threading.Thread):

    def __init__(
        self,
        event_queue: QueueManager[Message],
        music_queue: QueueManager[MusicEvent],
        bot_provider: RagdeaBot,
        event_loop: AbstractEventLoop,
    ) -> None:
        super().__init__()
        self.event_queue = event_queue
        self.music_queue = music_queue
        self.bot = bot_provider
        self.event_loop = event_loop
        self.voice_channel = None

    def _reconnect(self, message: Message):
        try:
            return run_coroutine_threadsafe(message.author.voice.channel.connect(), self.event_loop).result(10)  # type: ignore
        except Exception:
            return None

    def _sync_bot_variables(self, message: Message):
        voice_client = self._reconnect(message)
        if (
            self.bot.message_channel != message.channel
            or self.bot.voice_client != voice_client
        ):
            self.bot.message_channel = message.channel
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
        ytb = Youtube()
        songs = (
            ytb.search_single_song(search)
            if "https://" not in search
            else ytb.search_by_link(search)
        )
        self.music_queue.add_many(songs)

    def process(self, command, content):
        match command:
            case "-play":
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

    def _loop(self):
        while True:
            if self.event_queue.size() > 0:
                event = self.event_queue.get()
                content = event.content.split(" ", 1)
                command = self._mapper_command(content[0])
                self._sync_bot_variables(event)
                self.process(command, content)
            time.sleep(1)

    def run(self):
        self._loop()


def create_messaging_daemon(
    event_manager: QueueManager[Message],
    music_manager: QueueManager[MusicEvent],
    bot_provider: RagdeaBot,
    event_loop: AbstractEventLoop,
):
    MessageEventDaemon(event_manager, music_manager, bot_provider, event_loop).start()
