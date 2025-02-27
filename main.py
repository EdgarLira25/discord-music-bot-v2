from discord import Intents
from discord_client.listener import Listener
from settings.consts import TOKEN


if __name__ == "__main__":
    client = Listener(intents=Intents.all())
    client.run(TOKEN)
