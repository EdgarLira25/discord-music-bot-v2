from typing import List
from yt_dlp import YoutubeDL
from models.music import MusicEvent


class Youtube:

    @staticmethod
    def get_audio_url(URL: str) -> str:
        with YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
            if info := ydl.extract_info(URL, download=False):
                return info["url"]
        return ""

    def search_single_song(self, URL: str) -> List[MusicEvent]:
        with YoutubeDL({"format": "bestaudio", "noplaylist": "True"}) as ydl:
            if info := ydl.extract_info(f"ytsearch: {URL}", download=False):
                generated_info = info["entries"][0]
                return [
                    MusicEvent(
                        source=generated_info["url"],
                        title=generated_info["title"],
                        type_url="audio",
                    )
                ]
        return []

    def search_by_link(self, URL) -> List[MusicEvent]:
        with YoutubeDL(
            {
                "quiet": True,
                "format": "m4a/bestaudio/best",
                "extract_flat": True,
                "skip_download": True,
            }
        ) as ydl:
            if info := ydl.extract_info(URL, download=False):
                if "entries" in info:
                    return [
                        MusicEvent(
                            type_url="video",
                            source=item["url"],
                            title=item["title"],
                        )
                        for item in info["entries"]
                    ]
                else:
                    return [
                        MusicEvent(
                            source=info["url"],
                            title=info["title"],
                            type_url="audio",
                        )
                    ]
        return []
