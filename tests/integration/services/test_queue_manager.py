"""Módulo para testes que interagem dois métodos de GET e ADD"""

from queue import Queue
import threading
import pytest
from services.queue_manager import QueueManager


@pytest.fixture(name="queue_object")
def queue_object_fixture():
    return Queue()


def test_get_with_add(queue_object: Queue[int]):
    manager = QueueManager(queue_object)
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    manager.add(1)
    threading.Thread(target=manager.get).start()
    manager.add(2)
    manager.add(3)


def test_get_with_add_many(queue_object: Queue[int]):
    """Tentativa de exaurir a interação da fila entra adicionar e remover"""
    manager = QueueManager(queue_object)
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(
        target=manager.add_many, args=([1, 2, 3, 4, 5, 6, 7, 7, 8, 8, 9, 9, 9, 10],)
    ).start()
    threading.Thread(
        target=manager.add_many, args=([1, 2, 3, 4, 5, 6, 7, 7, 8, 8, 9, 9, 9, 10],)
    ).start()
    threading.Thread(target=manager.add_many, args=([1, 2],)).start()
    threading.Thread(target=manager.add_many, args=([1, 2],)).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()


def test_get_with_add_and_add_many(queue_object: Queue[int]):
    """Tentativa de exaurir a fila com muitas threads"""
    manager = QueueManager(queue_object)
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    manager.add_many([1, 2, 3])
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    manager.add_many([1, 2])
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    manager.add(1)
    manager.add_many([1, 2, 3, 4, 5, 6])


def test_get_with_add_and_add_many_with_max_size():
    """Valida possibilidade de deadlock com limite de tamanho na fila"""
    manager = QueueManager(Queue(3))
    threading.Thread(target=manager.add_many, args=([1, 2, 3, 4],)).start()
    threading.Thread(target=manager.add, args=(1,)).start()
    threading.Thread(target=manager.add, args=(2,)).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
    threading.Thread(target=manager.get).start()
