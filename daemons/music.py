import threading
import time
from application.bot import RagdeaBot
from models.music import MusicEvent
from services.queue_manager import QueueManager


class MusicsEventDaemon(threading.Thread):

    def __init__(
        self, queue_manager_provider: QueueManager[MusicEvent], bot_provider: RagdeaBot
    ) -> None:
        super().__init__()
        self.bot = bot_provider
        self.queue_manager = queue_manager_provider

    def process(self):
        self.bot.play(self.queue_manager.get())

    def _loop(self):
        while True:
            if (
                self.bot.voice_client
                and self.queue_manager.size() > 0
                and not self.bot.voice_client.is_playing()
            ):
                self.process()
            time.sleep(1)

    def run(self):
        self._loop()


def create_musics_daemon(
    music_queue_manager_provider: QueueManager[MusicEvent], bot_provider: RagdeaBot
):
    MusicsEventDaemon(music_queue_manager_provider, bot_provider).start()
