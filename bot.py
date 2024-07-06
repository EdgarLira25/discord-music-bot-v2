import os
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from discord import (
    Client,
    Intents,
    Message,
    FFmpegPCMAudio,
    VoiceClient,
    StageChannel,
    GroupChannel,
)
from access_controller import access_controller
from utils import (
    mapper_command,
    help_message,
)

from songs import songs


class MyClient(Client):

    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }
    YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "True"}
    song_queue = []
    voice_client: VoiceClient = None
    message_channel: GroupChannel = None
    voice_channel: StageChannel = None
    atual = None

    async def on_ready(self):
        print("ONLINE")

    async def on_message(self, message: Message):

        if await access_controller(message=message, client=self):

            self.message_channel = message.channel
            self.voice_channel = message.author.voice.channel

            command = mapper_command(message.content.split(" ")[0])

            match command:
                case "-play":
                    if self.voice_client == None:
                        self.voice_client = await self.voice_channel.connect()
                    await self._play(" ".join(message.content.split(" ")[1:]))
                case "-pause":
                    await self._pause()
                case "-skip":
                    await self._skip()
                case "-clear":
                    self._clear()
                case "-kill":
                    await self._kill()
                case "-queue":
                    await self._queue()
                case "-help":
                    await self._help()
                case _:
                    await self.send_message(
                        "Comando Digitado Não Existe. -help Para Listar os Comandos"
                    )

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch: {item}", download=False)["entries"][
                    0
                ]
            except Exception:
                return False

        return {"source": info["url"], "title": info["title"]}

    def _aux_play(self):
        if len(self.song_queue) > 0 and self.voice_client.is_playing() == False:
            if self.song_queue[0]["title"] in songs.dict_count:
                songs.dict_count[self.song_queue[0]["title"]] += 1
            else:
                songs.dict_count[self.song_queue[0]["title"]] = 1
            
            songs.save()
            self.voice_client.play(
                FFmpegPCMAudio(self.song_queue[0]["source"], **self.FFMPEG_OPTIONS),
                after=lambda e: self._aux_play(),
            )
            self.song_queue.pop(0)

    async def _play(self, query: str = ""):
        if query:

            song = self.search_yt(query)
            self.song_queue.append(song)

            if self.voice_client.is_playing() == True:
                await self.send_message(
                    f"Música Adicionada a Fila -> Posição {len(self.song_queue)}"
                )

        if len(self.song_queue) > 0 and self.voice_client.is_playing() == False:
            if self.song_queue[0]["title"] in songs.dict_count:
                songs.dict_count[self.song_queue[0]["title"]] += 1
            else:
                songs.dict_count[self.song_queue[0]["title"]] = 1
            
            songs.save()

            self.voice_client.play(
                FFmpegPCMAudio(self.song_queue[0]["source"], **self.FFMPEG_OPTIONS),
                after=lambda e: self._aux_play(),
            )
            await self.send_message(f"""Tocando -> {self.song_queue[0]["title"]}, pela {songs.dict_count[self.song_queue[0]["title"]]}° vez""")
            self.song_queue.pop(0)

    async def _skip(self):
        self.voice_client.stop()
        await self.send_message("Pulando Música...")

    async def _pause(self):
        if self.voice_client.is_paused():
            self.voice_client.resume()
            await self.send_message("Despausando Música...")

        elif not self.voice_client.is_paused() and self.voice_client.is_playing():
            self.voice_client.pause()
            await self.send_message("Música Pausada.")

    async def send_message(self, string: str):
        await self.message_channel.send(string)

    async def _queue(self):
        if len(self.song_queue) >= 1:
            await self.send_message(
                "\n".join(
                    f"{pos + 1} - {item['title']}"
                    for pos, item in enumerate(self.song_queue)
                )
            )
        else:
            await self.send_message("Nenhuma Música na Fila.")

    async def _kill(self):
        self.song_queue = []
        await self.voice_client.disconnect()
        self.voice_client.stop()
        self.voice_client = None
        self.message_channel = None
        self.voice_channel = None

    def _clear(self):
        self.song_queue = []

    async def _help(self):
        await self.send_message(help_message)


load_dotenv()

client = MyClient(intents=Intents.all())
client.run(os.environ.get("TOKEN"))
