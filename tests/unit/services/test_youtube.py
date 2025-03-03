from unittest.mock import patch
from yt_dlp import YoutubeDL
import pytest
from models.music import MusicEvent
from services.youtube import Youtube


@pytest.fixture(name="mock_extract_info")
def mock_extract_info_fixture():
    """Mock do YoutubeDL usado em todas as funções do wrapper sobre o ytb-dlp"""
    with patch.object(YoutubeDL, "extract_info") as extract_info:
        yield extract_info


def test_get_audio_url(mock_extract_info):
    """Testa a obtenção da URL de áudio de um vídeo"""
    mock_extract_info.return_value = {"url": "https://audio.url"}
    url = "https://youtube.com/watch?v=123"
    result = Youtube.get_audio_url(url)
    assert result == "https://audio.url"


def test_get_audio_url_fail(mock_extract_info):
    """Testa quando a URL do áudio não é encontrada"""
    mock_extract_info.return_value = ""

    url = "https://youtube.com/watch?v=123"
    result = Youtube.get_audio_url(url)

    assert not result


def test_search_single_song(mock_extract_info):
    """Testa a busca de uma única música"""
    mock_extract_info.return_value = {
        "entries": [
            {"url": "https://song.url", "title": "Test Song", "original_url": ""}
        ]
    }
    url = "test song finded"
    result = Youtube().search_single_song(url)
    assert result == [
        MusicEvent(source="https://song.url", title="Test Song", type_url="audio")
    ]


def test_search_single_song_fail(mock_extract_info):
    """Testa a busca quando a música não é encontrada"""
    mock_extract_info.return_value = []
    url = "song not found"
    result = Youtube().search_single_song(url)
    assert not result


def test_search_by_link_single_song(mock_extract_info):
    """Testa a busca por um link retornando uma única música"""
    mock_extract_info.return_value = {
        "url": "https://single.url",
        "title": "Single Song",
    }
    result = Youtube().search_by_link("https://youtube.com/watch?v=123")
    assert result == [
        MusicEvent(source="https://single.url", title="Single Song", type_url="audio")
    ]


def test_search_by_link_playlist(mock_extract_info):
    """Testa a busca por um link retornando uma playlist"""
    mock_extract_info.return_value = {
        "entries": [
            {"url": "https://song1.url", "title": "Song 1"},
            {"url": "https://song2.url", "title": "Song 2"},
        ]
    }

    result = Youtube().search_by_link("https://youtube.com/playlist?list=XYZ")
    assert result == [
        MusicEvent(source="https://song1.url", title="Song 1", type_url="video"),
        MusicEvent(source="https://song2.url", title="Song 2", type_url="video"),
    ]


def test_search_by_link_fail(mock_extract_info):
    """Testa a busca por um link inválido"""
    mock_extract_info.return_value = []
    result = Youtube().search_by_link("https://youtube.com/invalid")
    assert not result
