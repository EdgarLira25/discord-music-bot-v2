import asyncio
from typing import Optional
from discord import FFmpegPCMAudio
from discord_client.bot.counter import SongsCounter
from threading import Lock
from model.music import MusicEvent
from services.queue.music import MusicQueueManager
from services.youtube import Youtube


class SingletonRagdeaBotMeta(type):
    "Metaclasse para singleton seguro entre threads"

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class RagdeaBot(metaclass=SingletonRagdeaBotMeta):
    _instance: Optional["RagdeaBot"] = None

    def __init__(
        self,
        voice_channel,
        message_channel,
        voice_client,
        music_manager_provider=MusicQueueManager(),
    ) -> None:
        self.voice_channel = voice_channel
        self.message_channel = message_channel
        self.voice_client = voice_client
        self.music_manager = music_manager_provider
        self.counter = SongsCounter()

    async def connect_if_not_connected(self) -> None:
        if not self.voice_client or not self.voice_client.is_connected():
            self.voice_client = await self.voice_channel.connect()  # type: ignore

    def play(self, event: MusicEvent):

        asyncio.run_coroutine_threadsafe(
            self.connect_if_not_connected(), self.voice_client.loop
        )

        url = (
            event.source
            if event.type_url == "audio"
            else Youtube.get_audio_url(event.source)
        )
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

    async def skip(self) -> None:
        self.voice_client.stop()
        self.send("Pulando Música...")

    async def pause(self) -> None:
        "Pausa ou despausa a música"
        if self.voice_client.is_paused():
            self.voice_client.resume()
            self.send("Despausando Música...")

        elif not self.voice_client.is_paused() and self.voice_client.is_playing():
            self.voice_client.pause()
            self.send("Música Pausada.")

    def send(self, string: str):
        "Envia mensagem para o discord"
        asyncio.run_coroutine_threadsafe(
            self.message_channel.send(string), self.voice_client.loop
        )

    def send_queue_message(self):
        "Envia mensagem para o discord"
        if self.voice_client.is_playing():
            self.send(
                f"Música(s) Adicionada(s) à Fila -> Posição {self.music_manager.get_size() + 1}"
            )

    def update_voice_channel(self):
        "Evita Bugs de Troca de Canal"
        asyncio.run_coroutine_threadsafe(
            self.connect_if_not_connected(), self.voice_client.loop
        )

    async def queue(self) -> None:
        "Mostra a Fila do Bot"
        if self.music_manager.get_size() > 0:

            queue = "\n".join(
                f"{pos + 1} - {item.title}"
                for pos, item in enumerate(self.music_manager.get_many_songs())
            )

            if self.music_manager.get_size() > 10:
                queue += f"\nTamanho Atual da Fila: {self.music_manager.get_size()}"

            self.send(queue)
        else:
            self.send("Nenhuma Música na Fila.")

    async def kill(self) -> None:
        "Mata e desconecta o bot"
        self.voice_client.stop()
        await self.voice_client.disconnect()

    async def clear(self) -> None:
        "Limpa Fila do Bot"
        self.music_manager.clear()
        self.send(f"Fila de Músicas Limpa")

    async def help(self) -> None:
        "Mostra comandos do bot"
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
