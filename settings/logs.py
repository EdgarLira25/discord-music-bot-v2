"Padrão de Logs: Referência: https://docs.python.org/3/howto/logging-cookbook.html#"
import logging
from typing import TypedDict
from colorama import Fore, Style


class ClientConfig(TypedDict):
    log_handler: logging.Handler
    log_level: int
    root_logger: bool


class ColoredFormatter(logging.Formatter):
    """Coloração para Logs"""

    COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Style.RESET_ALL)
        log_fmt = f"{Fore.CYAN}[%(asctime)s]{Style.RESET_ALL} {log_color}[%(levelname)s]{Style.RESET_ALL} %(message)s"
        formatter = logging.Formatter(log_fmt, "%H:%M:%S")
        return formatter.format(record)


def client_config() -> ClientConfig:
    discord_handler = logging.FileHandler("spam.log")
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.DEBUG)
    discord_logger.addHandler(discord_handler)
    discord_logger.propagate = False

    logging.getLogger("").info("Client logs Configurados")

    return ClientConfig(
        log_handler=discord_handler,
        log_level=logging.DEBUG,
        root_logger=False,
    )


def init_basic_config():
    spam = logging.FileHandler("spam.log")
    spam.setLevel(logging.DEBUG)

    info = logging.FileHandler("info.log")
    info.setLevel(logging.INFO)

    basic = logging.StreamHandler()
    basic.setLevel(logging.INFO)
    basic.setFormatter(ColoredFormatter())

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[spam, basic, info],
    )

    logging.getLogger("").info("🔥 Sistemas de Logs Iniciado! 🔥")
