import asyncio
from queue import Queue
import threading
from unittest.mock import MagicMock, patch
from discord import Message
import pytest
from application.bot import Bot
from daemons.message import MessageEventDaemon, create_messaging_daemon
from models.music import MusicEvent
from services.queue_manager import QueueManager
from services.youtube import Youtube
from tests.unit.mocks.bot import BotMock
from tests.unit.mocks.message import AuthorMock, MessageMock, TextChannelMock, VoiceMock
from tests.unit.mocks.voice_client import VoiceClientMock

# pylint: disable=protected-access


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


@pytest.fixture(scope="function", autouse=True)
def auto_close_event_loop():
    yield
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(loop.stop)


@pytest.fixture(name="message_daemon")
def message_daemon_fixture():
    event_manager = QueueManager(Queue[Message]())
    music_manager = QueueManager(Queue[MusicEvent]())
    bot = BotMock(VoiceClientMock(False))
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    threading.Thread(target=start_loop, args=(event_loop,), daemon=True).start()
    return MessageEventDaemon(event_manager, music_manager, bot, event_loop)


@patch.object(MessageEventDaemon, "_sync_bot_variables", MagicMock())
def test_handle_event_variables(message_daemon: MessageEventDaemon):
    message_daemon.event_queue.add(
        MessageMock(None, AuthorMock(True), channel=None, content="-p abcde")
    )
    command, content = message_daemon._handle_event_variables()
    assert isinstance(command, str)
    assert isinstance(content, list)


def test_reconnect_success(message_daemon: MessageEventDaemon):
    assert message_daemon._reconnect(
        MessageMock(
            None, AuthorMock(True, VoiceMock()), channel=None, content="-p abcde"
        )
    )


@patch.object(Youtube, "search_single_song")
def test_add_music_without_link(
    mock_search_single_song: MagicMock, message_daemon: MessageEventDaemon
):
    mock_search_single_song.return_value = [
        MusicEvent(
            source="https://sertanejo", title="Time in a bottle", type_url="audio"
        )
    ]
    message_daemon.add_music("Happier")
    mock_search_single_song.assert_called_once()
    assert message_daemon.music_queue.size() > 0


@patch.object(Youtube, "search_by_link")
def test_add_music_with_link(
    mock_search_by_link: MagicMock, message_daemon: MessageEventDaemon
):
    mock_search_by_link.return_value = [
        MusicEvent(
            source="https://sertanejo", title="Time in a bottle", type_url="audio"
        )
    ]
    message_daemon.add_music("https://www.youtube.com/musicashow")
    mock_search_by_link.assert_called_once()
    assert message_daemon.music_queue.size() > 0


def test_reconnect_fail(message_daemon: MessageEventDaemon):
    assert not message_daemon._reconnect(
        MessageMock(
            None,
            AuthorMock(True, VoiceMock(should_raise=True)),
            channel=None,
            content="-p abcde",
        )
    )


@patch.object(MessageEventDaemon, "_reconnect")
def test_sync_bot_variables(
    reconnect_mock: MagicMock, message_daemon: MessageEventDaemon
):
    reconnect_mock.return_value = "Voice Novo"
    text_channel_novo = TextChannelMock("Channel Novo")
    message_daemon.bot.voice_channel = "Voice Antigo"
    message_daemon.bot.message_channel = "Message Antigo"  # type:ignore
    message_daemon._sync_bot_variables(
        MessageMock(None, AuthorMock(False), channel=text_channel_novo, content="")
    )
    assert message_daemon.bot.message_channel == text_channel_novo
    assert str(message_daemon.bot.voice_client) == "Voice Novo"


@patch.object(MessageEventDaemon, "_loop")
def test_create_messaging_daemon(mock_loop):
    mock_loop.return_value = None
    event_manager = QueueManager(Queue[MusicEvent]())
    message_manager = QueueManager(Queue[Message]())
    bot = BotMock(VoiceClientMock(False))
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    threading.Thread(target=start_loop, args=(event_loop,), daemon=True).start()
    create_messaging_daemon(message_manager, event_manager, bot, event_loop)
    mock_loop.assert_called_once()


def test_loop_execution(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock()
    message_daemon._handle_event_variables = MagicMock()
    message_daemon._handle_event_variables.return_value = ("-invalid", [""])
    message_daemon.start()
    message_daemon.event_queue.add(MagicMock(spec=Message))
    while message_daemon._handle_event_variables.call_count == 0:
        pass
    message_daemon.is_running = False
    message_daemon._handle_event_variables.assert_called()


def test_pause_call(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock(spec=Bot)
    message_daemon.process("-pause", [])
    message_daemon.bot.pause.assert_called_once()


def test_skip_call(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock(spec=Bot)
    message_daemon.process("-skip", ["-s"])
    message_daemon.bot.skip.assert_called_once()


def test_clear_call(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock(spec=Bot)
    message_daemon.process("-clear", ["-c"])
    message_daemon.bot.clear.assert_called_once()


def test_kill_call(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock(spec=Bot)
    message_daemon.process("-kill", ["-k"])
    message_daemon.bot.kill.assert_called_once()


def test_queue_call(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock(spec=Bot)
    message_daemon.process("-queue", ["-q"])
    message_daemon.bot.queue.assert_called_once()


def test_help_call(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock(spec=Bot)
    message_daemon.process("-help", ["-help"])
    message_daemon.bot.help.assert_called_once()


def test_play_call(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock(spec=Bot)
    message_daemon.add_music = MagicMock()
    message_daemon.process("-play", ["-p", "musica braba"])
    message_daemon.bot.send_queue_message.assert_called_once()
    message_daemon.add_music.assert_called_once()


def test_invalid_command(message_daemon: MessageEventDaemon):
    message_daemon.bot = MagicMock(spec=Bot)
    message_daemon.process("-invalid", [])
    message_daemon.bot.send.assert_called_once_with("Comando não encontrado. Use -help")


def test_mapper_command_valid_keys(message_daemon):
    "Talvez não valesse o esforço testar um dicionario k"
    assert message_daemon._mapper_command("-p") == "-play"
    assert message_daemon._mapper_command("-s") == "-skip"
    assert message_daemon._mapper_command("-c") == "-clear"
    assert message_daemon._mapper_command("-k") == "-kill"
    assert message_daemon._mapper_command("-q") == "-queue"
    assert message_daemon._mapper_command("-help") == "-help"
