import time
from queue import Empty, Queue
from typing import Generic, TypeVar

T = TypeVar("T")


class QueueManager(Generic[T]):
    def __init__(self, queue: Queue[T]) -> None:
        self.queue = queue

    def add(self, item: T):
        while True:
            try:
                self.queue.put(item, block=False)
                return
            except:
                time.sleep(0.1)

    def add_many(self, items: list[T]):
        size = len(items)
        index = 0
        while index < size:
            try:
                self.queue.put(items[index], block=False)
                index += 1
            except:
                time.sleep(0.1)

    def get_many(self, limit: int = 10) -> list[T]:
        """Retorna os primeiros `limit` itens da fila."""
        return list(self.queue.queue)[:limit]

    def get(self) -> T:
        item: T | None = None
        while item is None:
            try:
                item = self.queue.get(block=False)
            except Empty:
                time.sleep(0.1)
        return item

    def size(self) -> int:
        return self.queue.qsize()

    def clear(self):
        while self.size() > 0:
            self.get()
