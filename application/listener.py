"""Módulo para ouvir eventos do Discord"""

from logging import getLogger
from discord import Intents, Message, Object
from discord.ext.commands import Bot
from application.commands import BaseCommands
from application.util import publish_event
from models.bot import Bots

logs = getLogger(__name__)
MY_GUILD = Object(id=329013945845153795)


class Listener(Bot):
    def __init__(
        self, intents: Intents, bots: Bots, base_commands_provider: BaseCommands
    ):
        super().__init__(command_prefix="-", intents=intents)
        self.bots = bots
        self.base_commands = base_commands_provider
        self.register_commands()

    async def on_ready(self):
        synced = await self.tree.sync(guild=MY_GUILD)
        logs.info("%s Comandos Sincronizados", len(synced))
        logs.info("BOT INICIADO")

    async def on_message(self, message: Message):  # pylint: disable=arguments-differ
        publish_event(message, self.bots, self.loop)

    def register_commands(self):
        for command in self.base_commands.get():
            self.tree.add_command(command, guild=MY_GUILD)
