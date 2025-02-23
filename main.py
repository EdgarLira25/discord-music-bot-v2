import threading
from discord import Intents
from discord_client.listener import Listener
from services.daemon.music_event import create_daemon_songs
from services.queue.music import MusicQueueManager
from settings.consts import TOKEN


if __name__ == "__main__":
    manager = MusicQueueManager()
    client = Listener(music_queue_manager=manager, intents=Intents.all())
    threading.Thread(target=create_daemon_songs, args=(manager,)).start()
    client.run(TOKEN)
