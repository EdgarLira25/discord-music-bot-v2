"""Módulo para ouvir eventos do Discord"""

from logging import getLogger
from discord import Intents, Message, Object
from discord.ext.commands import Bot
from application.commands import BaseCommands
from application.publisher_message import PublisherMessage

logs = getLogger(__name__)
MY_GUILD = Object(id=329013945845153795)


class Listener(Bot):
    def __init__(
        self,
        intents: Intents,
        base_commands_provider: BaseCommands,
        publisher_message_provider: PublisherMessage,
    ):
        super().__init__(command_prefix="-", intents=intents)
        self.base_commands = base_commands_provider
        self.publisher = publisher_message_provider
        self._register_commands()

    async def on_ready(self):
        synced = await self.tree.sync(guild=MY_GUILD)
        logs.info("%s Comandos Sincronizados", len(synced))
        logs.info("BOT INICIADO")

    async def on_message(self, message: Message):  # pylint: disable=arguments-differ
        self.publisher.publish(message, self.loop)

    def _register_commands(self):
        for command in self.base_commands.get():
            self.tree.add_command(command, guild=MY_GUILD)
