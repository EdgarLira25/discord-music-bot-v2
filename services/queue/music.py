from queue import Empty, Queue
import time
from model.music import MusicEvent

QUEUE_SONGS = Queue()


class MusicQueueManager:
    def __init__(self, queue=QUEUE_SONGS) -> None:
        self.queue = queue

    def add_song(self, song: MusicEvent):
        while True:
            try:
                QUEUE_SONGS.put(song, block=False)
                return
            except:
                time.sleep(0.075)

    def add_many_songs(self, songs: list[MusicEvent]):
        size = len(songs)
        index = 0
        while index < size:
            try:
                QUEUE_SONGS.put(songs[index], block=False)
                index += 1
            except:
                time.sleep(0.1)

    def get_many_songs(self) -> list[MusicEvent]:
        "Retorna os 10 primeiros itens da fila"
        return list(self.queue.queue)[:10]

    def get_song(self) -> MusicEvent:
        queue: MusicEvent | None = None
        while not isinstance(queue, MusicEvent):
            try:
                queue = self.queue.get(block=False)
            except Empty:
                time.sleep(0.1)
        return queue

    def get_size(self) -> int:
        return self.queue.qsize()

    def clear(self):
        while self.get_size() > 0:
            self.get_song()
