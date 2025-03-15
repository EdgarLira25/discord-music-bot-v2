from asyncio import AbstractEventLoop
from logging import getLogger
from queue import Queue
from discord import Message
from application.bot import Bot
from daemons.message import create_messaging_daemon
from daemons.music import create_music_daemon
from models.bot import BotId, Bots, BotServices
from models.music import MusicEvent
from services.queue_manager import QueueManager

logs = getLogger(__name__)


class InstanceManager:
    def __init__(self, bots: Bots) -> None:
        self.bots = bots

    def init_bot_services(self, bot_id: BotId, channel, event_loop: AbstractEventLoop):
        """Inicializa instância do bot com todas suas dependências"""
        logs.info("Iniciando nova instância para servidor: %s", bot_id)

        music_queue_manager = QueueManager(Queue[MusicEvent]())
        event_queue_manager = QueueManager(Queue[Message]())
        bot = Bot(bot_id, channel, None, music_queue_manager)

        return BotServices(
            bot_instance=bot,
            music_event_queue=music_queue_manager,
            message_event_queue=event_queue_manager,
            music_daemon=create_music_daemon(music_queue_manager, bot),
            message_daemon=create_messaging_daemon(
                event_queue_manager, music_queue_manager, bot, event_loop
            ),
        )

    def add_event(self, bot_id: BotId, message: Message, event_loop: AbstractEventLoop):

        if bot_id not in self.bots:
            self.bots[bot_id] = self.init_bot_services(bot_id, message, event_loop)

        self.bots[bot_id].message_event_queue.add(message)
