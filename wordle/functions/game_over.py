import discord

from typing import Union, Literal

from assets.embeds import GameOverEmbed


async def game_over(
    information: Union[discord.Interaction, discord.Message],
    secret: str,
    game_state: Literal["correct_guess", "no_attempts_left", "given_up"]
):
    channel = information.channel

    embed = GameOverEmbed(secret, game_state).embed
    if isinstance(information, discord.Interaction):
        await information.response.send_message(embed=embed)
    else:
        await channel.send(embed=embed)

    await channel.edit(slowmode_delay=0)
