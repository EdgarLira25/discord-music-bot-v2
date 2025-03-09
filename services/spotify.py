from logging import getLogger
import requests
from models.music import MusicEvent
from settings.consts import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


logs = getLogger(__name__)


class Spotify:
    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    base_url = "https://api.spotify.com/v1"
    _token = ""

    @property
    def token(self):
        self._token = requests.post(
            url="https://accounts.spotify.com/api/token",
            auth=self.auth,
            data={"grant_type": "client_credentials"},
            timeout=10,
        ).json()["access_token"]
        return self._token

    def search_by_link(self, search: str) -> list[MusicEvent]:
        element_id = search.split("/")[-1]
        if "album/" in search:
            return self._get_album(album_id=element_id)
        if "playlist/" in search:
            return self._get_playlist(playlist_id=element_id)
        if "track/" in search:
            return self._get_music(music_id=element_id)
        return []

    def _get_album(self, album_id: str) -> list[MusicEvent]:
        response = requests.request(
            method="GET",
            url=f"{self.base_url}/albums/{album_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10,
        )

        if not response.ok:
            logs.warning(
                "Erro ao encontrar a album do spotify (verifique se o album é público)"
            )
            return []

        return [
            MusicEvent(
                source=music["external_urls"]["spotify"],
                title=f"{music['artists'][0]['name']} {music['name']}",
                type_url="spotify",
            )
            for music in response.json()["tracks"]["items"]
        ]

    def _get_playlist(self, playlist_id: str) -> list[MusicEvent]:
        response = requests.request(
            method="GET",
            url=f"{self.base_url}/playlists/{playlist_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10,
        )

        if not response.ok:
            logs.warning(
                "Erro ao encontrar a playlist do spotify (verifique se a playlist é pública)"
            )
            return []

        return [
            MusicEvent(
                source=music["track"]["external_urls"]["spotify"],
                title=f"{music['track']['artists'][0]['name']} {music['track']['name']}",
                type_url="spotify",
            )
            for music in response.json()["tracks"]["items"]
        ]

    def _get_music(self, music_id: str) -> list[MusicEvent]:
        url = f"{self.base_url}/tracks/{music_id}"
        response = requests.request(
            method="GET",
            url=url,
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=10,
        )

        if not response.ok:
            logs.warning(
                "Erro ao encontrar a música do spotify (verifique se a música é pública)"
            )
            return []

        music = response.json()

        return [
            MusicEvent(
                source=url,
                title=music["artists"][0]["name"] + music["name"],
                type_url="spotify",
            )
        ]
