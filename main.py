import os
from discord import Intents
from application.commands import BaseCommands
from application.listener import Listener
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
    base_command = BaseCommands(bots, instance_manager)
    client = Listener(
        intents=Intents.all(), bots=bots, base_commands_provider=base_command
    )
    client.run(os.environ.get("TOKEN", ""), **logs.client_config())


if __name__ == "__main__":  # pragma: no cover
    main()
