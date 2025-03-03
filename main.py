import os
from discord import Intents
from application.listener import Listener
from database.connector import Database


def main():
    Database().migrate_all()
    client = Listener(intents=Intents.all())
    client.run(os.environ.get("TOKEN", ""))


if __name__ == "__main__":  # pragma: no cover
    main()
