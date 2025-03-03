"Utilizado para mocks ou fixtures gerais do pytest"
from unittest.mock import MagicMock, patch


patch("discord.FFmpegPCMAudio", new=MagicMock()).start()
