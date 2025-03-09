from logging import getLogger
import requests
from models.music import MusicEvent
from settings.consts import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET


logs = getLogger(__name__)


class Spotify:
    auth = (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    base_url = "https://api.spotify.com/v1"
    _token = ""

    @staticmethod
    def personal_current_music(token: str):
        song = requests.request(
            method="GET",
            url="https://api.spotify.com/v1/me/player/currently-playing",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        return song["item"]["artists"][0]["name"] + " " + song["item"]["name"]

    def get_personal_token(self, code: str):
        req = requests.post(
            url="https://accounts.spotify.com/api/token",
            auth=self.auth,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": "https://edgar-bot-auth.netlify.app",
            },
            timeout=10,
        )
        
        return req.json()["access_token"]

    @property
    def token(self):
        self._token = requests.post(
            url="https://accounts.spotify.com/api/token",
            auth=self.auth,
            data={"grant_type": "client_credentials"},
            timeout=10,
        ).json()["access_token"]
        return self._token

    def get_playlist(self, playlist_id: str) -> list[MusicEvent]:
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

        playlist = response.json()["tracks"]["items"]

        return [
            MusicEvent(
                source=music["track"]["external_urls"]["spotify"],
                title=f"{music['track']['artists'][0]['name']} {music['track']['name']}",
                type_url="spotify",
            )
            for music in playlist
        ]

    def get_music(self, music_id: str) -> list[MusicEvent]:
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
