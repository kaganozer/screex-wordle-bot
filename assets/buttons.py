import discord

from database.database import get_node
from wordle.functions.check_player import player_is_on_correct_channel
from game.functions.stop import stop_game


class StopButton(discord.ui.View):
    @discord.ui.button(label="Oyunu Bitir", style=discord.ButtonStyle.danger)
    async def button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if player_is_on_correct_channel(information=interaction):
            user = interaction.user
            guild = interaction.guild
            
            game_node = get_node(f"{guild.id}/games/{user.id}")
            await stop_game(interaction, game_node)