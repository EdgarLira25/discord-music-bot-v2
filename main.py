import os
from discord import Intents
from application.listener import Listener


def main():
    client = Listener(intents=Intents.all())
    client.run(os.environ.get("TOKEN", ""))


if __name__ == "__main__":  # pragma: no cover
    main()
