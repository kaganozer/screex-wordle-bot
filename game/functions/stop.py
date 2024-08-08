import discord

from firebase_admin import db


async def stop_game(interaction: discord.Interaction, game: db.Reference):
    channel = interaction.channel
    
    await interaction.response.send_message("Oyun bitiriliyor.")
    await channel.delete()
    game.delete()
