"Módulo do daemon que consome a fila de músicas do bot"

from logging import getLogger
import threading
import time
from application.bot import Bot
from models.music import MusicEvent
from services.queue_manager import QueueManager
from settings.consts import TIME

logs = getLogger(__name__)


class MusicEventDaemon(threading.Thread):

    def __init__(
        self, queue_manager_provider: QueueManager[MusicEvent], bot_provider: Bot
    ) -> None:
        super().__init__()
        self.bot = bot_provider
        self.queue_manager = queue_manager_provider
        self.is_running = True

    def process(self):
        self.bot.play(self.queue_manager.get())

    def _valid_state_to_process(self) -> bool:

        return bool(
            self.bot.voice_client
            and self.queue_manager.size() > 0
            and not self.bot.voice_client.is_playing()
        )

    def _loop(self):
        while self.is_running:
            if self._valid_state_to_process():
                logs.info("Música em estado válido para ser tocada")
                self.process()
            time.sleep(TIME)

    def stop(self):
        self.is_running = False

    def run(self):
        self._loop()


def create_music_daemon(
    music_queue_manager_provider: QueueManager[MusicEvent], bot_provider: Bot
):
    thread = MusicEventDaemon(music_queue_manager_provider, bot_provider)
    thread.start()
    return thread
