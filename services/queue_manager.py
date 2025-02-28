"""Gerenciador de Fila Genérico"""

import time
from queue import Empty, Full, Queue
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
            except Full:
                time.sleep(0.1)

    def add_many(self, items: list[T]):
        size = len(items)
        index = 0
        while index < size:
            try:
                self.queue.put(items[index], block=False)
                index += 1
            except Full:
                time.sleep(0.1)

    def list_many(self, n: int = 10) -> list[T]:
        """Retorna os primeiros n itens da fila."""
        return list(self.queue.queue)[:n]

    def get(self) -> T:
        while True:
            try:
                return self.queue.get(block=False)
            except Empty:
                time.sleep(0.1)

    def size(self) -> int:
        return self.queue.qsize()

    def clear(self):
        while self.size() > 0:
            self.get()
