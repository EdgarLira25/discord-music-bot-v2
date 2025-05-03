"""Módulo para ouvir eventos do Discord"""

from logging import getLogger
from discord import Intents, Message, Interaction, Object
from discord.app_commands import Command
from discord.ext.commands import Bot
from application.util import create_message_event
from models.bot import Bots
from services.instance_manager import InstanceManager

logs = getLogger(__name__)

MY_GUILD = Object(id=329013945845153795)


class Listener(Bot):
    def __init__(self, intents: Intents, bots: Bots):
        super().__init__(command_prefix="-", intents=intents)
        self.register_commands()
        self.bots = bots

    async def on_ready(self):
        synced = await self.tree.sync(guild=MY_GUILD)
        logs.info("%s Comandos Sincronizados", len(synced))
        logs.info("BOT INICIADO")

    async def on_message(self, message: Message):  # pylint: disable=arguments-differ
        self.publish_event(message)

    def publish_event(self, source: Interaction | Message, prefix="", item=""):
        if message_event := create_message_event(source, prefix, item):
            InstanceManager(self.bots).add_event(
                message_event.guild_id, message_event, self.loop
            )

    def register_commands(self):
        def create_cmd(name: str, desc: str, prefix: str, extra_item: bool = False):
            async def callback(message: Interaction):
                await message.response.send_message(prefix)
                self.publish_event(message, prefix=prefix)

            async def callback_with_item(message: Interaction, music: str = ""):
                if not music.strip():
                    await message.response.defer()
                    await message.delete_original_response()
                    return
                await message.response.send_message(f"{prefix} {music}")
                self.publish_event(message, prefix=prefix, item=music)

            command = Command(
                name=name,
                description=desc,
                callback=callback if not extra_item else callback_with_item,
            )

            self.tree.add_command(command, guild=MY_GUILD)

        create_cmd("play", "Nova Música (Youtube/Spotify)", "-play", True)
        create_cmd("pause", "Pausar/Despausar", "-pause")
        create_cmd("skip", "Pular", "-skip")
        create_cmd("clear", "Limpa fila", "-clear")
        create_cmd("kill", "Desliga Bot", "-kill")
        create_cmd("queue", "Fila", "-queue")
        create_cmd("help", "Ajuda", "-help")
