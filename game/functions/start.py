import discord
from discord.ext import commands

import asyncio

from database.database import get_node
from assets.embeds import ErrorEmbed, CommandEmbed
from wordle.functions.check_player import guild_has_a_start_channel, user_has_a_game


async def start_game(bot: commands.Bot, interaction: discord.Interaction, gametype: str):
    user = interaction.user
    guild = interaction.guild
    channel = interaction.channel
    category = channel.category
    
    bot = guild.get_member(bot.user.id)
    
    embed = ErrorEmbed(interaction).embed
    
    if guild_has_a_start_channel(guild):
        guild_node = get_node(f"{guild.id}")
        
        start_channel_id = int(guild_node.child("start_channel").get())
        
        if channel.id == start_channel_id:
            if not user_has_a_game(user):
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=False
                    ),
                    bot: discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True
                    )
                }
                if bot.top_role >= user.top_role:
                    overwrites[user] = discord.PermissionOverwrite(
                        view_channel=True,
                        send_messages=True
                    )
                
                game_channel = await guild.create_text_channel(
                    name=f"{gametype}-{user.name}", category=category, overwrites=overwrites, slowmode_delay=1
                )
                
                embed = CommandEmbed(interaction).embed
                embed.title = "Oyunun hazır!"
                embed.description = f"Bu kanalda oynayabilirsin: <#{game_channel.id}>"
                
                await interaction.response.send_message(embed=embed)
                return game_channel
            else:
                user_game = guild_node.child(f"games/{user.id}").get()
                
                embed.description = f"<#{user_game["channel_id"]}> kanalında devam eden bir oyunun var."
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return None
        else:
            embed.description=f"Oyun başlatabilmek için <#{start_channel_id}> kanalında olman gerek!"
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
    else:
        embed.description = "Bu sunucuda bir oyun kategorisi yok."
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return None
