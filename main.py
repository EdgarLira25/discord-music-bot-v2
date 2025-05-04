import os
from discord import Intents
from application.commands import BaseCommands
from application.listener import Listener
from application.publisher_message import PublisherMessage
from daemons.monitor import create_monitor_daemon
from database.connector import Database
from models.bot import Bots
from services.instance_manager import InstanceManager
from settings import logs


def main():
    bots = Bots()
    logs.init_basic_config()
    Database().migrate_all()
    create_monitor_daemon(bots)
    instance_manager = InstanceManager(bots)
    publisher_message_event = PublisherMessage(instance_manager)
    base_command = BaseCommands(instance_manager, publisher_message_event)
    client = Listener(
        intents=Intents.all(),
        base_commands_provider=base_command,
        publisher_message_provider=publisher_message_event,
    )
    client.run(os.environ.get("TOKEN", ""), **logs.client_config())


if __name__ == "__main__":  # pragma: no cover
    main()
