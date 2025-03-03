"Utilizado para mocks ou fixtures gerais do pytest"
import os
from unittest.mock import MagicMock, patch
import pytest
from database.connector import Database


patch("discord.FFmpegPCMAudio", new=MagicMock()).start()


@pytest.fixture(scope="session", autouse=True)
def test_sql_file():
    Database().migrate_all()
    yield
    os.remove("teste.db")
