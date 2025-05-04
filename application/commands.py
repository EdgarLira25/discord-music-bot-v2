from discord import Interaction
from discord.app_commands import Command
from models.bot import Bots
from services.instance_manager import InstanceManager
from application.util import create_message_event


class BaseCommands:
    def __init__(self, bots: Bots, instance_provider: InstanceManager):
        self.bots = bots
        self.instance_manager = instance_provider

    def publish_event(self, interaction: Interaction, prefix: str, item: str = ""):
        if message_event := create_message_event(interaction, prefix, item):
            self.instance_manager.add_event(
                message_event.guild_id, message_event, interaction.client.loop
            )

    async def play(self, interaction: Interaction, music: str):
        if not music.strip():
            await interaction.response.defer()
            await interaction.delete_original_response()
            return
        await interaction.response.send_message(f"-play {music}")
        self.publish_event(interaction, prefix="-play", item=music)

    async def pause(self, interaction: Interaction):
        await interaction.response.send_message("-pause")
        self.publish_event(interaction, prefix="-pause")

    async def skip(self, interaction: Interaction):
        await interaction.response.send_message("-skip")
        self.publish_event(interaction, prefix="-skip")

    async def clear(self, interaction: Interaction):
        await interaction.response.send_message("-clear")
        self.publish_event(interaction, prefix="-clear")

    async def kill(self, interaction: Interaction):
        await interaction.response.send_message("-kill")
        self.publish_event(interaction, prefix="-kill")

    async def queue(self, interaction: Interaction):
        await interaction.response.send_message("-queue")
        self.publish_event(interaction, prefix="-queue")

    async def help_command(self, interaction: Interaction):
        await interaction.response.send_message("-help")
        self.publish_event(interaction, prefix="-help")

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
            Command(name="help", description="Ajuda", callback=self.help_command),
        ]
