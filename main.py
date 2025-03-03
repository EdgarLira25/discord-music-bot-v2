import os
from discord import Intents
from application.listener import Listener
from database.connector import Database
from settings import logs


def main():
    logs.init_basic_config()
    Database().migrate_all()
    client = Listener(intents=Intents.all())
    client.run(os.environ.get("TOKEN", ""), **logs.client_config())


if __name__ == "__main__":  # pragma: no cover
    main()
