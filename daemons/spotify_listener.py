import threading
import time
from application.bot import Bot
from models.music import MusicEvent
from services.queue_manager import QueueManager
from services.spotify import Spotify
from services.youtube import Youtube


class SpotifyEventDaemon(threading.Thread):

    def __init__(
        self,
        queue_manager_provider: QueueManager[MusicEvent],
        bot_provider: Bot,
        code: str,
    ) -> None:
        super().__init__()
        self.bot = bot_provider
        self.queue_manager = queue_manager_provider
        self.token = Spotify().get_personal_token(code)
        self.last_song = ""

    def process(self, music):
        self.bot.voice_client.stop()
        self.queue_manager.add_many(Youtube().search_single_song(music))

    def _loop(self):
        while True:
            try:
                current_song = Spotify.personal_current_music(self.token)
                if current_song != self.last_song:
                    self.last_song = current_song
                    self.process(self.last_song)
                time.sleep(5)
            except Exception as e:
                print("exceção", e)
                time.sleep(5)

    def run(self):
        self._loop()


def create_spotify_daemon(
    music_queue_manager_provider: QueueManager[MusicEvent], bot_provider: Bot, code: str
):
    SpotifyEventDaemon(music_queue_manager_provider, bot_provider, code).start()
