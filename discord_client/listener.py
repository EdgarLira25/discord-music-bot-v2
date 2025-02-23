import threading
from typing import Any
from discord import Client, Intents, Message, TextChannel, VoiceChannel
from discord_client.bot.manager import RagdeaBot
from services.queue.music import MusicQueueManager
from services.youtube import Youtube
from utils import clean_word


class Listener(Client):

    def __init__(
        self,
        *,
        music_queue_manager: MusicQueueManager,
        intents: Intents,
        **options: Any,
    ) -> None:
        super().__init__(intents=intents, **options)
        self.queue_manager = music_queue_manager

    voice_client = None  # type: ignore

    def _mapper_command(self, key: str):
        return {
            "-p": "-play",
            "-s": "-skip",
            "-c": "-clear",
            "-k": "-kill",
            "-q": "-queue",
            "-help": "-help",
        }.get(key, key)

    async def on_ready(self):
        print("ONLINE")

    async def connect_if_not_connected(self, voice_channel) -> None:
        if not self.voice_client or not self.voice_client.is_connected():  # type: ignore
            self.voice_client: VoiceChannel = await voice_channel.connect()

    def _command_controller(self, message: Message) -> bool:
        if message.author.bot:
            return False
        if (
            isinstance(message.channel, TextChannel)
            and message.content.startswith("-")
            and "music" in clean_word(message.channel.name)
        ):
            return True

        return False

    async def on_message(self, message: Message):
        if not self._command_controller(message):
            return

        content = message.content.split(" ", 1)
        command = self._mapper_command(content[0])

        await self.connect_if_not_connected(message.author.voice.channel)  # type: ignore

        bot = RagdeaBot(
            message.author.voice.channel,  # type: ignore
            message.channel,
            self.voice_client,
        )

        if (
            bot.message_channel != message.channel
            or bot.voice_client != self.voice_client
        ):
            bot.message_channel = message.channel
            bot.voice_client = self.voice_client

        match command:
            case "-play":
                bot.send_queue_message()
                threading.Thread(
                    target=(
                        Youtube().search_single_song
                        if "https://" not in content[1]
                        else Youtube().search_by_link
                    ),
                    args=(content[1],),
                ).start()
            case "-pause":
                await bot.pause()
            case "-skip":
                await bot.skip()
            case "-clear":
                await bot.clear()
            case "-kill":
                await bot.kill()
            case "-queue":
                await bot.queue()
            case "-help":
                await bot.help()
            case _:
                bot.send("Comando não encontrado. Use -help")
