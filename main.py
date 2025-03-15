import os
from discord import Intents
from application.listener import Listener
from daemons.monitor import create_monitor_daemon
from database.connector import Database
from models.bot import Bots
from settings import logs


def main():
    logs.init_basic_config()
    Database().migrate_all()

    bots = Bots()
    create_monitor_daemon(bots)

    client = Listener(intents=Intents.all(), bots=bots)
    client.run(os.environ.get("TOKEN", ""), **logs.client_config())


if __name__ == "__main__":  # pragma: no cover
    main()
