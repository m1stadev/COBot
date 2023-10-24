import discord
from discord import app_commands
from discord.ext.commands import Cog

from cobot.bot import COBot


class CommandsCog(Cog):
    def __init__(self, bot: COBot) -> None:
        self.bot = bot

    # test commands for now
    @app_commands.command(name='rmguild')
    async def guild_remove(self, interaction: discord.Interaction) -> None:
        self.bot.dispatch('guild_remove', interaction.guild)
        await interaction.response.send_message(
            'dispatched guild_remove event', ephemeral=True
        )

    @app_commands.command(name='addguild')
    async def guild_join(self, interaction: discord.Interaction) -> None:
        self.bot.dispatch('guild_join', interaction.guild)
        await interaction.response.send_message(
            'dispatched guild_join event', ephemeral=True
        )


async def setup(bot: COBot) -> None:
    await bot.add_cog(CommandsCog(bot))
