"Utilizado para mocks ou fixtures gerais do pytest"

# pylint: skip-file

import os
from unittest.mock import MagicMock, patch
import pytest

patch("discord.FFmpegPCMAudio", new=MagicMock()).start()

from application.publisher_message import PublisherMessage
from database.connector import Database
from tests.unit.mocks.message import (
    AuthorMock,
    ChannelMock,
    MessageEventMock,
    TextChannelMock,
)

patch("logging.getLogger", new=MagicMock()).start()


def mock_message_event(*_):
    return MessageEventMock(
        guild_id=1,
        voice_channel=ChannelMock(should_raise=False),
        author=AuthorMock(True),
        channel=TextChannelMock("teste"),
        content="-p abcde",
    )


patch.object(PublisherMessage, "create_message_event", mock_message_event).start()


@pytest.fixture(scope="session", autouse=True)
def test_sql_file():
    Database().migrate_all()
    yield
    os.remove("teste.db")
