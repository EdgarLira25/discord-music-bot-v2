import time
from unittest.mock import patch, MagicMock
from queue import Queue
from daemons.music import MusicsEventDaemon, create_musics_daemon
from models.music import MusicEvent
from services.queue_manager import QueueManager
from tests.unit.mocks.bot import BotMock
from tests.unit.mocks.voice_client import VoiceClientMock

# pylint: disable=protected-access


def test_valid_state_to_process_success():
    """Testa caminho feliz para processar"""
    manager = QueueManager(Queue[MusicEvent]())
    manager.add(MusicEvent("", "", "audio"))
    assert (
        MusicsEventDaemon(
            manager, BotMock(VoiceClientMock(False))
        )._valid_state_to_process()
        is True
    )


def test_valid_state_to_process_fail_empty_queue():
    """Testa se o bot toca musica com fila vazia"""
    manager = QueueManager(Queue())
    daemon = MusicsEventDaemon(manager, BotMock(VoiceClientMock(False)))
    assert daemon._valid_state_to_process() is False


def test_valid_state_to_process_fail_no_voice_client():
    """Valida se o bot toca musica se não tem voice client"""
    manager = QueueManager(Queue())
    manager.add(MusicEvent("", "", "audio"))
    daemon = MusicsEventDaemon(manager, BotMock(None))
    assert daemon._valid_state_to_process() is False


def test_valid_state_to_process_fail_is_playing():
    """Não processa se bot esta tocando musica"""
    manager = QueueManager(Queue())
    manager.add(MusicEvent("", "", "audio"))
    daemon = MusicsEventDaemon(manager, BotMock(VoiceClientMock(True)))
    assert daemon._valid_state_to_process() is False


def test_proccess_function():
    """Infelizmente ela não faz muita coisa, então provavelmente nem falhará,
    mas farei o fluxo caso algo quebre eventualmente"""
    manager = QueueManager(Queue[MusicEvent]())
    manager.add(MusicEvent("", "", "audio"))
    MusicsEventDaemon(manager, BotMock(False)).process()


@patch.object(MusicsEventDaemon, "_loop")
def test_create_musics_daemon(mock_loop):
    mock_loop.return_value = None
    music_queue_manager_provider = MagicMock()
    bot_provider = MagicMock()
    create_musics_daemon(music_queue_manager_provider, bot_provider)
    time.sleep(0.1)
    mock_loop.assert_called_once()


def test_musics_loop():
    manager = QueueManager(Queue[MusicEvent]())
    manager.add(MusicEvent("", "", "audio"))
    abc = MusicsEventDaemon(manager, BotMock(VoiceClientMock(False)))
    abc.start()
    abc.is_running = False
