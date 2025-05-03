from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from application.bot import Bot
from daemons.message import MessageEventDaemon
from daemons.music import MusicEventDaemon
from models.message import MessageEvent
from models.music import MusicEvent
from services.queue_manager import QueueManager


@dataclass
class BotServices:
    bot_instance: Bot
    music_event_queue: QueueManager[MusicEvent]
    message_event_queue: QueueManager[MessageEvent]
    message_daemon: MessageEventDaemon
    music_daemon: MusicEventDaemon
    last_activity: datetime = datetime.now()


BotId: TypeAlias = int
Bots = dict[BotId, BotServices]
