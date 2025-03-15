import asyncio
from queue import Queue
from unittest.mock import MagicMock, patch
from discord import Intents, Message
import pytest
from application.listener import Listener
from models.bot import BotServices, Bots
from services.instance_manager import InstanceManager
from services.queue_manager import QueueManager
from tests.unit.mocks.message import (
    AuthorMock,
    GuildMock,
    MessageMock,
    TextChannelMock,
    VoiceMock,
)


@pytest.fixture(name="listener")
def listener_fixture():
    return Listener(intents=Intents.all(), bots=Bots())


@pytest.fixture(scope="function", autouse=True)
def auto_close_event_loop():
    yield
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(loop.stop)


def mock_init_bot_services(*_):
    return BotServices(
        bot_instance=MagicMock(),
        music_event_queue=MagicMock(),
        message_event_queue=QueueManager(Queue[Message]()),
        message_daemon=MagicMock(),
        music_daemon=MagicMock(),
    )


@pytest.mark.asyncio
@patch.object(InstanceManager, "init_bot_services", mock_init_bot_services)
async def test_on_message_with_pre_none_guild_id(listener: Listener):
    message = MessageMock(
        GuildMock(1),
        AuthorMock(False, VoiceMock(False)),
        TextChannelMock("music"),
        "-p abcde",
    )
    await listener.on_message(message=message)  # type: ignore
    assert len(listener.bots) == 1
    assert listener.bots.get(1)


@pytest.mark.asyncio
@patch.object(InstanceManager, "init_bot_services", mock_init_bot_services)
async def test_on_message_with_pre_exist_guild_id(listener: Listener):
    message = MessageMock(
        GuildMock(1),
        AuthorMock(False, VoiceMock(False)),
        TextChannelMock("music"),
        "-p abcde",
    )
    await listener.on_message(message=message)  # type: ignore
    message = MessageMock(
        GuildMock(1),
        AuthorMock(False, VoiceMock(False)),
        TextChannelMock("music"),
        "-p abcde",
    )
    assert len(listener.bots) == 1
    assert listener.bots.get(1)


@pytest.mark.asyncio
@patch.object(InstanceManager, "init_bot_services", mock_init_bot_services)
async def test_on_message_with_pre_diff_guild_id(listener: Listener):
    message = MessageMock(
        GuildMock(1),
        AuthorMock(False, VoiceMock(False)),
        TextChannelMock("music"),
        "-p abcde",
    )
    await listener.on_message(message=message)  # type: ignore
    message = MessageMock(
        GuildMock(2),
        AuthorMock(False, VoiceMock(False)),
        TextChannelMock("music"),
        "-p abcde",
    )
    await listener.on_message(message=message)  # type: ignore
    assert len(listener.bots) == 2
    assert listener.bots.get(1)
    assert listener.bots.get(2)


@pytest.mark.asyncio
async def test_on_ready(listener):
    "Apenas verifica se o fluxo não quebra"
    await listener.on_ready()
