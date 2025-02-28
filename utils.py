"""Módulo de métodos uteis para o projeto"""

from functools import wraps
from typing import Callable
import unicodedata
from discord import Message, TextChannel


def valid_message(func: Callable):
    "Decorator para validar toda mensagem de entrada no listener"

    @wraps(func)
    async def wrapper(self, message: Message, *args, **kwargs):
        if (
            message.guild
            and not message.author.bot
            and isinstance(message.channel, TextChannel)
            and message.content.startswith("-")
            and (
                "music"
                in "".join(
                    char
                    for char in unicodedata.normalize("NFD", message.channel.name)
                    if unicodedata.category(char) != "Mn"
                ).lower()
            )
        ):
            return await func(self, message, message.guild.id, *args, **kwargs)

    return wrapper
