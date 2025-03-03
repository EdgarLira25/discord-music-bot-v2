from unittest.mock import AsyncMock
import pytest
from tests.unit.mocks.message import AuthorMock, GuildMock, MessageMock, TextChannelMock
from utils import valid_message


@pytest.fixture(name="async_func_mock")
def func_mock_fixture():
    return AsyncMock()


@pytest.mark.asyncio
async def test_valid_message_success(async_func_mock):
    message = MessageMock(
        GuildMock(1), AuthorMock(False), TextChannelMock("music"), "-p abcde"
    )
    decorated_func = valid_message(async_func_mock)
    response = await decorated_func(None, message=message)
    assert response


@pytest.mark.asyncio
async def test_valid_message_with_invalid_channel(async_func_mock):
    """Mensagem de canal invalido"""
    message = MessageMock(GuildMock(1), AuthorMock(False), None, "-p abcde")
    decorated_func = valid_message(async_func_mock)
    response = await decorated_func(None, message=message)
    assert not response


@pytest.mark.asyncio
async def test_valid_message_without_guild(async_func_mock):
    """Mensagem em chat que não é de servidor"""
    message = MessageMock(None, AuthorMock(False), TextChannelMock("music"), "-p abcde")
    decorated_func = valid_message(async_func_mock)
    response = await decorated_func(None, message=message)
    assert not response


@pytest.mark.asyncio
async def test_valid_message_invalid_prefix(async_func_mock):
    """Uso de prefixo invalido"""
    message = MessageMock(
        GuildMock(1), AuthorMock(False), TextChannelMock("music"), "p abcde"
    )
    decorated_func = valid_message(async_func_mock)
    response = await decorated_func(None, message=message)
    assert not response


@pytest.mark.asyncio
async def test_valid_message_invalid_channel_name(async_func_mock):
    """Verifica nome invalido de canal de texto"""
    message = MessageMock(
        GuildMock(1), AuthorMock(False), TextChannelMock("invalído"), "-p abcde"
    )
    decorated_func = valid_message(async_func_mock)
    response = await decorated_func(None, message=message)
    assert not response


@pytest.mark.parametrize(
    "channel_name",
    [
        "music",
        "Música",
        "MUSIC",
        "my-music-channel",
    ],
)
@pytest.mark.asyncio
async def test_valid_message_valid_channel_name(channel_name, async_func_mock):
    """Testa mensagem válida com varios nomes de canal _music_"""
    message = MessageMock(
        GuildMock(1), AuthorMock(False), TextChannelMock(channel_name), "-p abcde"
    )
    decorated_func = valid_message(async_func_mock)
    response = await decorated_func(None, message=message)
    assert response
