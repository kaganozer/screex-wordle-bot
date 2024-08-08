import discord
from discord.ext import commands
from discord import app_commands

from typing import Union

from database.database import get_node
from assets.embeds import CommandEmbed
from game.functions.stop import stop_game
from wordle.functions.check_player import player_is_on_correct_channel


class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="bitir", description="Devam eden oyununu bitirir.")
    @app_commands.check(player_is_on_correct_channel)
    async def stop(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild
        
        game_node = get_node(f"{guild.id}/games/{user.id}")
        await stop_game(interaction, game_node)
    
    @app_commands.command(name="avatar", description="İstenilen kullanıcının profil fotoğrafını gösterir.")
    async def avatar(self, interaction: discord.Interaction, member: Union[None, discord.Member] = None):
        user = interaction.user
        if not member:
            member = user
        
        member_avatar = member.avatar if member.avatar else member.default_avatar
        
        embed = CommandEmbed(interaction).embed
        embed.description = f"**{member.name}** adlı kullanıcının profil fotoğrafı"
        
        embed.set_image(url=member_avatar)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Game(bot))
