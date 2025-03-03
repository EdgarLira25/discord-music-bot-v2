from queue import Queue
import pytest
from services.queue_manager import QueueManager


@pytest.fixture(name="queue_object")
def queue_fixture():
    return Queue()


def test_add(queue_object: Queue):
    "Valida se o item é adicionado corretamente a fila"
    manager = QueueManager(queue_object)
    manager.add(1)
    assert manager.size() == 1
    manager.add(2)
    assert manager.size() == 2
    manager.add(3)
    assert manager.size() == 3


def test_size_queue(queue_object: Queue):
    "Valida se o tamanho da fila é retornado corretamente sincronamente"
    manager = QueueManager(queue_object)
    manager.add(1)
    manager.add(2)
    manager.add(3)
    assert manager.size() == 3
    manager.get()
    assert manager.size() == 2
    manager.get()
    assert manager.size() == 1
    manager.get()
    assert manager.size() == 0


def test_clear(queue_object: Queue):
    "Valida se a fila é limpa corretamente"
    manager = QueueManager(queue_object)
    manager.add(1)
    manager.add(2)
    manager.add(3)
    manager.clear()
    assert manager.size() == 0


def test_get(queue_object: Queue):
    "Valida se a fila é limpa corretamente"
    manager = QueueManager(queue_object)
    manager.add(1)
    item = manager.get()
    assert manager.size() == 0
    assert item == 1


def test_add_many(queue_object: Queue):
    "Testa adição de multiplos items a fila"
    manager = QueueManager(queue_object)
    manager.add_many([1, 2, 3, 4])
    assert manager.size() == 4


def test_list(queue_object: Queue):
    "Testa adição de multiplos items a fila"
    manager = QueueManager(queue_object)
    manager.add_many([1, 2, 3, 4])
    assert len(manager.list_many()) == 4
