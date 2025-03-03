from unittest.mock import patch
import pytest
from services.songs_counter import MetaClassSongsCounter, SongsCounter
from tests.unit.mocks.song_counter import SongsCounterSaveMock

# pylint: disable=protected-access


# Mock de Singleton para evitar side effects
@pytest.fixture(autouse=True)
def reset_singleton():
    with patch.object(SongsCounter, "_instance", None), patch.object(
        MetaClassSongsCounter, "_instances", {}
    ):
        yield


@pytest.fixture(name="valid_json")
def valid_json_fixture():
    return "tests/unit/services/json_examples/valid.json"


@pytest.fixture(name="invalid_json")
def invalid_json_fixture():
    return "tests/unit/services/json_examples/invalid.json"


@pytest.fixture(name="file_not_exist_json")
def file_not_exist_json_fixture():
    return "tests/unit/services/json_examples/notExist.json"


def test_add(valid_json: str):
    counter = SongsCounterSaveMock(valid_json)
    counter.add("Teste")
    assert counter.get("Teste") == 1


def test_load_json_happy_path(valid_json):
    """Load é feito no instanciamento de classe"""
    counter = SongsCounter(valid_json)
    assert len(counter._dict_count) == 150


def test_load_json_sad_path(invalid_json):
    "Testa json invalido, um json invalido gera um dicionario vazio"
    counter = SongsCounter(invalid_json)
    assert not counter._dict_count


def test_load_json_path_dont_exist(file_not_exist_json):
    "Testa json invalido, um json invalido gera um dicionario vazio"
    counter = SongsCounter(file_not_exist_json)
    assert not counter._dict_count


@patch("services.songs_counter.SongsCounter._load")
def test_save(mock_loads):
    mock_loads.return_value = {}
    counter = SongsCounter("/tmp/teste.json")
    counter.add("Teste")
    counter.add("Teste")
    counter = SongsCounter("/tmp/teste.json")
    assert counter.get("Teste") == 2
