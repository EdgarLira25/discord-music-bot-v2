"""Módulo que valida se uma instância do bot deve continuar viva"""

import time
from datetime import datetime, timedelta
from logging import getLogger
import threading
from models.bot import Bots
from settings.consts import MONITOR_TIME

logs = getLogger(__name__)


class MonitorDaemon(threading.Thread):

    def __init__(self, bot_instances: Bots) -> None:
        super().__init__()
        self.bot_instances = bot_instances
        self.is_running = True

    def process(self, bot_ids: list[int]):
        for bot_id in bot_ids:
            logs.info("Matando instância: %s", bot_id)
            self.bot_instances[bot_id].message_daemon.stop()
            self.bot_instances[bot_id].music_daemon.stop()
            self.bot_instances.pop(bot_id)

    def _loop(self):
        while self.is_running:
            instances_to_kill: list[int] = []
            for bot_id, instance in self.bot_instances.items():
                if (
                    datetime.now() - instance.last_activity
                    > timedelta(seconds=MONITOR_TIME)
                    and instance.message_event_queue.size() == 0
                    and instance.music_event_queue.size() == 0
                    and instance.bot_instance.voice_client
                    and not instance.bot_instance.voice_client.is_playing()
                ):
                    instances_to_kill.append(bot_id)

            self.process(instances_to_kill)
            time.sleep(MONITOR_TIME)

    def run(self):
        self._loop()


def create_monitor_daemon(bot_instances: Bots):
    MonitorDaemon(bot_instances).start()
