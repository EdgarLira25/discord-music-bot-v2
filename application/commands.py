import random
from discord import Interaction
from discord.app_commands import Command
from application.publisher_message import PublisherMessage
from services.instance_manager import InstanceManager
from services.songs_counter import SongsCounter


class BaseCommands:
    def __init__(
        self, instance_provider: InstanceManager, publisher_provider: PublisherMessage
    ):
        self.instance = instance_provider
        self.publisher = publisher_provider
        self.counter = SongsCounter()

    def _send_interaction(self, interaction: Interaction, prefix: str, item: str = ""):
        self.publisher.publish(
            interaction, interaction.client.loop, prefix=prefix, item=item
        )

    async def play(self, interaction: Interaction, music: str):
        if not music.strip():
            await interaction.response.defer()
            await interaction.delete_original_response()
            return
        await interaction.response.send_message(f"-play {music}")
        self._send_interaction(interaction, prefix="-play", item=music)

    async def pause(self, interaction: Interaction):
        await interaction.response.send_message("-pause")
        self._send_interaction(interaction, prefix="-pause")

    async def skip(self, interaction: Interaction):
        await interaction.response.send_message("-skip")
        self._send_interaction(interaction, prefix="-skip")

    async def clear(self, interaction: Interaction):
        await interaction.response.send_message("-clear")
        self._send_interaction(interaction, prefix="-clear")

    async def kill(self, interaction: Interaction):
        await interaction.response.send_message("-kill")
        self._send_interaction(interaction, prefix="-kill")

    async def queue(self, interaction: Interaction):
        await interaction.response.send_message("-queue")
        self._send_interaction(interaction, prefix="-queue")

    async def random(self, interaction: Interaction):
        if all_songs := self.counter.get_all():
            await interaction.response.send_message("-random")
            song = random.choice(all_songs)
            return self._send_interaction(
                interaction, prefix="-play", item=song["name"]
            )
        await interaction.response.defer()
        await interaction.delete_original_response()

    async def help_command(self, interaction: Interaction):
        await interaction.response.send_message("-help")
        self._send_interaction(interaction, prefix="-help")

    def get(self) -> list[Command]:
        return [
            Command(
                name="play",
                description="Nova Música (Youtube/Spotify)",
                callback=self.play,
            ),
            Command(name="pause", description="Pausar/Despausar", callback=self.pause),
            Command(name="skip", description="Pular", callback=self.skip),
            Command(name="clear", description="Limpa fila", callback=self.clear),
            Command(name="kill", description="Desliga Bot", callback=self.kill),
            Command(name="queue", description="Fila", callback=self.queue),
            Command(
                name="random",
                description="Nova Música Aleatória",
                callback=self.random,
            ),
            Command(name="help", description="Ajuda", callback=self.help_command),
        ]
