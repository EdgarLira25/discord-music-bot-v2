import asyncio
from queue import Queue
import threading
from unittest.mock import patch
from discord import Intents, Message
import pytest
from application.listener import Listener
from tests.unit.mocks.message import (
    AuthorMock,
    GuildMock,
    MessageMock,
    TextChannelMock,
    VoiceMock,
)


@pytest.fixture(name="listener")
def listener_fixture():
    return Listener(intents=Intents.all())


@pytest.fixture(scope="function", autouse=True)
def auto_close_event_loop():
    yield
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(loop.stop)


def mock_init_bot_instance(cls: Listener, guild_id, _):
    cls.dict_queue[guild_id] = Queue[Message]()


@pytest.mark.asyncio
@patch.object(Listener, "_init_bot_instance", mock_init_bot_instance)
async def test_on_message_with_pre_none_guild_id(listener: Listener):
    message = MessageMock(
        GuildMock(1), AuthorMock(False), TextChannelMock("music"), "-p abcde"
    )
    await listener.on_message(message=message)  # type: ignore
    assert len(listener.dict_queue) == 1
    assert listener.dict_queue.get(1)


@pytest.mark.asyncio
@patch.object(Listener, "_init_bot_instance", mock_init_bot_instance)
async def test_on_message_with_pre_exist_guild_id(listener: Listener):
    message = MessageMock(
        GuildMock(1), AuthorMock(False), TextChannelMock("music"), "-p abcde"
    )
    await listener.on_message(message=message)  # type: ignore
    message = MessageMock(
        GuildMock(1), AuthorMock(False), TextChannelMock("music"), "-p abcde"
    )
    assert len(listener.dict_queue) == 1
    assert listener.dict_queue.get(1)


@pytest.mark.asyncio
@patch.object(Listener, "_init_bot_instance", mock_init_bot_instance)
async def test_on_message_with_pre_diff_guild_id(listener: Listener):
    message = MessageMock(
        GuildMock(1), AuthorMock(False), TextChannelMock("music"), "-p abcde"
    )
    await listener.on_message(message=message)  # type: ignore
    message = MessageMock(
        GuildMock(2), AuthorMock(False), TextChannelMock("music"), "-p abcde"
    )
    await listener.on_message(message=message)  # type: ignore
    assert len(listener.dict_queue) == 2
    assert listener.dict_queue.get(1)
    assert listener.dict_queue.get(2)


def test_create_instance(listener: Listener):
    guild_id = 1
    message = MessageMock(
        GuildMock(guild_id),
        AuthorMock(False, voice=VoiceMock()),
        TextChannelMock("music"),
        "-p abcde",
    )

    threading.Thread(
        target=listener._init_bot_instance,  # pylint: disable=protected-access
        args=(1, message),
        daemon=True,
    ).start()
