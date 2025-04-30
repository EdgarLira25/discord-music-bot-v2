import asyncio
from queue import Queue
import threading
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from application.bot import Bot
from models.music import MusicEvent
from services.queue_manager import QueueManager
from services.songs_counter import SongsCounter
from services.youtube import Youtube
from tests.unit.mocks.message import TextChannelMock
from tests.unit.mocks.voice_client import VoiceClientMock


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


@pytest.fixture(scope="function", autouse=True)
def mock_count_music_safely():
    "Evitar warnings de ctypes + pytest"
    with patch.object(Bot, "_count_music_safely"):
        yield


@pytest.fixture(name="music_events")
def music_events_fixture():
    return [
        MusicEvent(source="Link Spotify", title="Song A", type_url="audio"),
        MusicEvent(source="Link YouTube", title="Music Video B", type_url="video"),
        MusicEvent(source="Link Apple Music", title="Song C", type_url="audio"),
    ]


@pytest.fixture(name="music_event_audio")
def music_event_audio_fixture():
    return MusicEvent(source="Link Apple Music", title="Song C", type_url="audio")


@pytest.fixture(name="music_event_video")
def music_event_video_fixture():
    return MusicEvent(source="Link Apple Music", title="Song C", type_url="video")


@pytest.fixture(scope="function", autouse=True)
def auto_close_event_loop():
    yield
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(loop.stop)


@pytest.fixture(name="bot")
def bot_fixture():
    music_manager = QueueManager(Queue())
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    threading.Thread(target=start_loop, args=(event_loop,), daemon=True).start()
    return Bot(
        1,
        TextChannelMock(False),
        VoiceClientMock(False, loop=event_loop),
        music_manager,
    )


def mock_counter_add_get(*_):
    return None


def mock_youtube_get_audio(*_):
    return "my string"


@patch.object(SongsCounter, "get", mock_counter_add_get)
@patch.object(SongsCounter, "add", mock_counter_add_get)
def test_play_command_audio(bot: Bot, music_event_audio: MusicEvent):
    bot.message_channel.send = AsyncMock()
    bot.play(music_event_audio)
    bot.message_channel.send.assert_called_once()


@patch.object(SongsCounter, "get", mock_counter_add_get)
@patch.object(SongsCounter, "add", mock_counter_add_get)
@patch.object(Youtube, "get_audio_url", mock_youtube_get_audio)
def test_play_command_video(bot: Bot, music_event_video: MusicEvent):
    bot.message_channel.send = AsyncMock()
    bot.play(music_event_video)
    bot.message_channel.send.assert_called_once()


def test_pause_command_not_paused_and_playing(bot: Bot):
    bot.voice_client.is_paused = MagicMock()
    bot.voice_client.is_playing = MagicMock()
    bot.voice_client.is_playing.return_value = True
    bot.message_channel.send = AsyncMock()
    bot.voice_client.is_paused.return_value = False
    bot.pause()
    bot.message_channel.send.assert_called_once()


def test_pause_command_bot_is_paused(bot: Bot):
    bot.voice_client.is_paused = MagicMock()
    bot.message_channel.send = AsyncMock()
    bot.voice_client.is_paused.return_value = True
    bot.pause()
    bot.message_channel.send.assert_called_once()


def test_send_queue_message_is_playing(bot: Bot):
    bot.voice_client.is_playing = MagicMock()
    bot.voice_client.is_playing.return_value = True
    bot.message_channel.send = AsyncMock()
    bot.send_queue_message()
    bot.message_channel.send.assert_called_once()


def test_send_queue_message_is_not_playing(bot: Bot):
    bot.voice_client.is_playing = MagicMock()
    bot.voice_client.is_playing.return_value = False
    bot.message_channel.send = AsyncMock()
    bot.send_queue_message()
    bot.message_channel.send.assert_not_called()


def test_send_command(bot: Bot):
    bot.message_channel.send = AsyncMock()
    bot.send("Teste")
    bot.message_channel.send.assert_called_once()
    bot.message_channel.send.assert_called_with("Teste")


def test_skip_command(bot: Bot):
    bot.voice_client.stop = MagicMock()
    bot.skip()
    bot.voice_client.stop.assert_called_once()


def test_queue_command(bot: Bot, music_events: list[MusicEvent]):
    bot.music_manager.add_many(music_events)
    bot.message_channel.send = AsyncMock()
    bot.queue()
    bot.message_channel.send.assert_called_once()
    bot.music_manager.clear()


def test_queue_many_musics_command(bot: Bot, music_events: list[MusicEvent]):
    bot.music_manager.add_many(music_events * 5)
    bot.message_channel.send = AsyncMock()
    bot.queue()
    bot.message_channel.send.assert_called_once()
    bot.music_manager.clear()


def test_queue_without_music_command(bot: Bot):
    bot.message_channel.send = AsyncMock()
    bot.queue()
    bot.message_channel.send.assert_called_once()
    bot.music_manager.clear()


def test_kill_command(bot: Bot):
    bot.voice_client.disconnect = AsyncMock()
    bot.kill()
    bot.voice_client.disconnect.assert_called_once()


def test_clear_command(bot: Bot):
    bot.message_channel.send = AsyncMock()
    bot.clear()
    bot.message_channel.send.assert_called_once()
    bot.message_channel.send.assert_called_with("Fila de Músicas Limpa")


def test_help_command(bot: Bot):
    bot.message_channel.send = AsyncMock()
    bot.help()
    bot.message_channel.send.assert_called_once()
