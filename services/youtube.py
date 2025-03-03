"Wrapper ao redor do YoutubeDL"
from logging import getLogger
from typing import List
from colorama import Fore, Style
from yt_dlp import YoutubeDL
from models.music import MusicEvent

log = getLogger(__name__)


class Youtube:

    @staticmethod
    def get_audio_url(url: str) -> str:
        """Busca url do áudio de um video"""
        log.info("Buscando áudio a partir de uma url de vídeo %s", url)
        with YoutubeDL(
            {
                "quiet": True,
                "format": "bestaudio",
                "noplaylist": "True",
                "cookiefile": "cookies.txt",
            }
        ) as ydl:
            if info := ydl.extract_info(url, download=False):
                return info["url"]
        log.error(
            "Erro ao recuperar informaçoes do link: %s, Verifique o Link ou o Youtube bloqueou seu acesso",
            url,
        )
        return ""

    def search_single_song(self, url: str) -> List[MusicEvent]:
        """Busca uma música"""
        with YoutubeDL(
            {
                "quiet": True,
                "format": "bestaudio",
                "noplaylist": "True",
                "cookiefile": "cookies.txt",
            }
        ) as ydl:
            log.info("Buscando música: %s", url)
            if info := ydl.extract_info(f"ytsearch: {url}", download=False):
                generated_info = info["entries"][0]

                log.info(
                    "Música encontrada: %s%s%s",
                    Fore.MAGENTA,
                    generated_info["original_url"],
                    Style.RESET_ALL,
                )
                return [
                    MusicEvent(
                        source=generated_info["url"],
                        title=generated_info["title"],
                        type_url="audio",
                    )
                ]
        log.error("Problema de rede ou o youtube bloqueou seu acesso")

        return []

    def search_by_link(self, url) -> List[MusicEvent]:
        """Faz uma busca por link, retornando uma musica ou lista de música(playlist)"""
        with YoutubeDL(
            {
                "quiet": True,
                "format": "m4a/bestaudio/best",
                "extract_flat": True,
                "skip_download": True,
                "cookiefile": "cookies.txt",
            }
        ) as ydl:
            log.info("Extraindo informações do link %s", url)
            if info := ydl.extract_info(url, download=False):
                if "entries" in info:

                    log.info(
                        "Playlist encontrada %s%s%s", Fore.MAGENTA, url, Style.RESET_ALL
                    )

                    return [
                        MusicEvent(
                            type_url="video",
                            source=item["url"],
                            title=item["title"],
                        )
                        for item in info["entries"]
                    ]
                log.info("Música encontrada: %s", url)
                return [
                    MusicEvent(
                        source=info["url"],
                        title=info["title"],
                        type_url="audio",
                    )
                ]
        log.error(
            "Erro ao recuperar informaçoes do link: %s, Verifique o Link ou o Youtube bloqueou seu acesso",
            url,
        )
        return []
