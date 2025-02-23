import threading
import time
from discord_client.bot.manager import RagdeaBot, SingletonRagdeaBotMeta
from services.queue.music import MusicQueueManager


class MusicsEventDaemon(threading.Thread):

    def __init__(
        self, queue_manager_provider: MusicQueueManager, bot_provider: RagdeaBot
    ) -> None:
        super().__init__()
        self.bot = bot_provider
        self.queue_manager = queue_manager_provider

    def process(self):
        self.bot.play(self.queue_manager.get_song())

    def _loop(self):
        while True:
            if (
                self.queue_manager.get_size() > 0
                and not self.bot.voice_client.is_playing()
            ):
                self.process()
            time.sleep(5)

    def run(self):
        self._loop()


def create_daemon_songs(music_queue_manager_provider: MusicQueueManager):
    while RagdeaBot not in SingletonRagdeaBotMeta._instances:
        time.sleep(1)
    MusicsEventDaemon(music_queue_manager_provider, RagdeaBot(None, None, None)).start()
