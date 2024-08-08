import discord
from discord.ext import commands
from discord import app_commands

from database.database import get_node
from wordle.functions.check_player import player_is_on_correct_channel
from wordle.functions.game_over import game_over
from assets.embeds import ErrorEmbed


class GiveUp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="peset", description="Pes etmek için kullanabilirsin.")
    @app_commands.check(player_is_on_correct_channel)
    async def giveup(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild

        game_node = get_node(f"{guild.id}/games/{user.id}")
        user_game = game_node.get()
        
        remaining_attempts = user_game["remaining_attempts"]
        if not remaining_attempts:
            embed = ErrorEmbed(interaction).embed
            embed.description = "Oyun bittikten sonra bu komutu kullanamazsın."
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        secret = user_game["secret"]
        await game_over(interaction, secret, "given_up")
        game_node.update({"remaining_attempts": 0, "given_up": True})


async def setup(bot):
    await bot.add_cog(GiveUp(bot))
