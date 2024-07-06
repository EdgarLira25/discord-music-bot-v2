from discord import Message, Client
from utils import clean_word
from dotenv import load_dotenv
import os

nome_disponivel = "music"
prefix = "-"
load_dotenv()
#NOTE: crie um arquivo .env com os nomes de quem está autorizado a pedir comandos ao BOT
# Exemplo: AUTHORIZED=abc|efef|rfrfr
autorizados = os.getenv("AUTHORIZED").split("|")


async def access_controller(message: Message, client: Client) -> bool:
    if message.author == client.user:
        return False
    if (
        str(message.author) in autorizados
        and message.content.startswith(prefix)
        and nome_disponivel in clean_word(message.channel.name)
    ):
        return True
    elif (not str(message.author) in autorizados) and message.content.startswith(
        prefix
    ):
        await message.channel.send(
            "Você Não Tem Permissão Para Usar Este Bot Fale Com o Owner Dele"
        )
    elif (
        (nome_disponivel in clean_word(message.channel.name)) == False
        and str(message.author) in autorizados
        and message.content.startswith(prefix)
    ):
        await message.channel.send(
            f"""Utilize um Chat com a seguinte sequencia de caracter -> {nome_disponivel}"""
        )
    return False
