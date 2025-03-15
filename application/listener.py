"""Módulo para ouvir eventos do Discord"""

from logging import getLogger
from discord import Client, Intents, Message
from models.bot import Bots
from services.instance_manager import InstanceManager
from utils import valid_message

logs = getLogger(__name__)


class Listener(Client):

    def __init__(self, intents: Intents, bots: Bots) -> None:
        super().__init__(intents=intents)
        self.bots = bots

    async def on_ready(self):
        logs.info("BOT INICIADO")

    @valid_message
    async def on_message(self, message: Message, guild_id: int, guild_name: str):
        "Receptor de todas mensagens do discord"
        logs.info("Adicionando Evento à: %s", guild_name)

        InstanceManager(self.bots).add_event(guild_id, message, self.loop)
