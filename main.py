import os
from discord import Intents
from application.listener import Listener


if __name__ == "__main__":
    client = Listener(intents=Intents.all())
    client.run(os.environ.get("TOKEN", ""))
