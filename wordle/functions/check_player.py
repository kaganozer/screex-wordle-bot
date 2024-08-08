import discord

from typing import Union

from database.database import get_node


def guild_has_a_start_channel(guild: discord.Guild):
    guild_object = get_node(f"{guild.id}").get()
    if not guild_object:
        return False
    start_channel_id = int(guild_object["start_channel"])
    for channel in guild.channels:
        if start_channel_id == channel.id:
            return True
    return False


def user_has_a_game(user: discord.Member):
    guild = user.guild
    if not guild_has_a_start_channel(guild):
        return False
    
    current_games =  get_node(f"{guild.id}/games").get()
    if not current_games:
        return False

    return str(user.id) in current_games


def user_is_playing_wordle(user: discord.Member):
    if not user_has_a_game(user):
        return False
    
    guild = user.guild
    user_game = get_node(f"{guild.id}/games/{user.id}").get()
    return user_game["game_type"] in ["wordle", "wordleduel"]


def player_is_on_correct_channel(information: Union[discord.Message, discord.Interaction]):
    if isinstance(information, discord.Interaction):
        user = information.user
    else:
        user = information.author
    
    if not user_is_playing_wordle(user):
        return False
    
    guild = information.guild
    channel = information.channel
    
    user_game = get_node(f"{guild.id}/games/{user.id}").get()
    return channel.id == int(user_game["channel_id"])


def user_is_opponent_on_duel(user: discord.Member) -> bool:
    if not user_has_a_game(user):
        return False
    
    guild = user.guild
    user_game = get_node(f"{guild.id}/games/{user.id}").get()
    return user_game["is_opponent"]
