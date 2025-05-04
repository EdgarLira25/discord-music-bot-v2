import asyncio
from queue import Queue
from unittest.mock import AsyncMock, MagicMock, patch
from discord import Intents
import pytest
from application.commands import BaseCommands
from application.listener import Listener
from application.publisher_message import PublisherMessage
from models.bot import BotServices, Bots
from models.message import MessageEvent
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
    bots = Bots()
    instance_manager = InstanceManager(bots)
    publisher_message_event = PublisherMessage(instance_manager)
    base_command = BaseCommands(instance_manager, publisher_message_event)
    return Listener(Intents.all(), base_command, publisher_message_event)


@pytest.fixture(scope="function", autouse=True)
def auto_close_event_loop():
    yield
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(loop.stop)
    loop.stop()


def mock_init_bot_services(*_):
    return BotServices(
        bot_instance=MagicMock(),
        music_event_queue=MagicMock(),
        message_event_queue=QueueManager(Queue[MessageEvent]()),
        message_daemon=MagicMock(),
        music_daemon=MagicMock(),
    )


@pytest.fixture(name="message_mock")
def message_mock_fixture():
    return MessageMock(
        GuildMock(50),
        AuthorMock(False, VoiceMock(False)),
        TextChannelMock("musicTeste"),
        "-p abcdeTeste",
    )


@pytest.mark.asyncio
@patch.object(InstanceManager, "init_bot_services", mock_init_bot_services)
async def test_on_message_with_pre_none_guild_id(
    listener: Listener, message_mock: MessageMock
):
    message = message_mock
    await listener.on_message(message=message)
    assert len(listener.publisher.instance_manager.bots) == 1
    assert listener.publisher.instance_manager.bots.get(1)


@pytest.mark.asyncio
@patch.object(InstanceManager, "init_bot_services", mock_init_bot_services)
async def test_on_message_with_pre_exist_guild_id(
    listener: Listener, message_mock: MessageMock
):
    message = message_mock
    await listener.on_message(message=message)
    message = message_mock
    assert len(listener.publisher.instance_manager.bots) == 1
    assert listener.publisher.instance_manager.bots.get(1)


@pytest.mark.asyncio
@patch.object(Listener, "tree", AsyncMock())
async def test_on_ready(listener):
    "Apenas verifica se o fluxo não quebra"
    await listener.on_ready()
