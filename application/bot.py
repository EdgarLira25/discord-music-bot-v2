import asyncio
from logging import getLogger
from threading import Lock
from typing import Optional
from colorama import Fore, Style
from discord import FFmpegPCMAudio, TextChannel, VoiceClient
from models.music import MusicEvent
from services.songs_counter import SongsCounter
from services.queue_manager import QueueManager
from services.youtube import Youtube

logs = getLogger(__name__)


class SingletonBotMeta(type):
    "Metaclasse para singleton seguro entre threads baseado em chave instance_id"

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if args[0] not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[args[0]] = instance
        return cls._instances[args[0]]


class Bot(metaclass=SingletonBotMeta):
    _instance: Optional["Bot"] = None

    def __init__(
        self,
        instance_id: int,
        message_channel,
        voice_client,
        music_manager_provider: QueueManager[MusicEvent],
    ) -> None:
        self.instance_id: int = instance_id
        self.message_channel: TextChannel = message_channel
        self.voice_client: VoiceClient = voice_client
        self.music_manager: QueueManager[MusicEvent] = music_manager_provider
        self.counter = SongsCounter()

    def play(self, event: MusicEvent):

        match event.type_url:
            case "audio":
                url = event.source
            case "video":
                url = Youtube.get_audio_url(event.source)
            case "spotify":
                if events := Youtube().search_single_song(event.title):
                    event = events[0]
                    url = event.source
                else:
                    return

        self.counter.add(event.title)
        self.voice_client.play(
            FFmpegPCMAudio(
                url,
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                options="-vn",
            )
        )
        self.send(
            f"""Tocando -> {event.title}, pela {self.counter.get(event.title)}° vez"""
        )

    def skip(self) -> None:
        self.voice_client.stop()
        self.send("Pulando Música...")

    def pause(self) -> None:
        "Pausa ou despausa a música"
        if self.voice_client.is_paused():
            self.voice_client.resume()
            self.send("Despausando Música...")

        elif not self.voice_client.is_paused() and self.voice_client.is_playing():
            self.voice_client.pause()
            self.send("Música Pausada.")

    def send(self, string: str):
        "Envia mensagem para o discord"
        logs.info("%s%s%s", Fore.MAGENTA, string, Style.RESET_ALL)
        asyncio.run_coroutine_threadsafe(
            self.message_channel.send(string), self.voice_client.loop
        )

    def send_queue_message(self) -> None:
        "Envia mensagem sobre a fila para o discord"
        if self.voice_client and self.voice_client.is_playing():
            self.send(
                f"Música(s) Adicionada(s) à Fila -> Posição {self.music_manager.size() + 1}"
            )

    def queue(self) -> None:
        if self.music_manager.size() > 0:
            queue = "\n".join(
                f"{pos + 1} - {item.title}"
                for pos, item in enumerate(self.music_manager.list_many())
            )
            if self.music_manager.size() > 10:
                queue += f"\nTamanho Atual da Fila: {self.music_manager.size()}"
            self.send(queue)
        else:
            self.send("Nenhuma Música na Fila.")

    def kill(self) -> None:
        self.voice_client.stop()
        asyncio.run_coroutine_threadsafe(
            self.voice_client.disconnect(), self.voice_client.loop
        )

    def clear(self) -> None:
        self.music_manager.clear()
        self.send("Fila de Músicas Limpa")

    def help(self) -> None:
        self.send(
            """
```-p ou -play <Musica> -> Adiciona Música na Fila
-pause -> Pausa e Despausa a Música
-s ou -skip -> Pula para próxima música da Fila
-c ou -clear -> Limpa Fila De Músicas
-k ou -kill-> Reinicia Todas as Variáveis - Usado Caso o Bot Bug
-q ou -queue -> Mostra a Fila De Músicas 
-help -> Lista Comandos```
"""
        )
