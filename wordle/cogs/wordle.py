import discord
from discord import app_commands
from discord.ext import commands

import json
import random
from typing import Literal

from database.database import get_node
from game.functions.start import start_game
from wordle.functions.result_image import result_image
from wordle.functions.keyboard_image import keyboard_image
from assets.images.image_to_file import image_to_file
from assets.embeds import WordleStartEmbed, WordleCommandsEmbed, WordleRulesEmbed
from assets.buttons import StopButton


class Wordle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="wordle", description="Bir Wordle oyunu başlatır.")
    @app_commands.rename(word_length="harf-sayısı")
    @app_commands.describe(
        word_length="Oyunu oynamak istediğin kelime uzunluğunu seç. Varsayılan uzunluk 5 harftir."
    )
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def wordle(
        self, interaction: discord.Interaction, word_length: Literal[5, 6, 7] = 5
    ):
        game_channel = await start_game(
            bot=self.bot, interaction=interaction, gametype="wordle"
        )
        if not game_channel:
            return
        
        start_embed = WordleStartEmbed().embed
        await game_channel.send(embed=start_embed)

        with open(
            f"wordle/words/{word_length}_harf.txt", "r", encoding="utf-8"
        ) as file:
            words = json.loads(file.read())

        secret = random.choice(words)
        guesses = (("-" * word_length + " ") * 6).split(" ")[:-1]

        result = result_image(guesses, secret)
        result_file = image_to_file(result)

        result_embed = discord.Embed(
            title=f"Wordle - {word_length} Harf",
            description="Kalan Hakların: 6",
            color=discord.Color.green(),
        )
        result_embed.set_image(url="attachment://result.png")
        result_message = await game_channel.send(
            file=result_file, embed=result_embed, view=StopButton()
        )

        game_thread = await game_channel.create_thread(
            name="Wordle Sohbet Kanalı", message=result_message
        )
        game_commands_embed = WordleCommandsEmbed().embed
        game_rules_embed = WordleRulesEmbed().embed
        await game_thread.send(embed=game_commands_embed)
        await game_thread.send(embed=game_rules_embed)

        letters = [dict(), dict(), dict()]
        for index, row in enumerate(["qwertyuıopğü", "asdfghjklşi", "zxcvbnmöç"]):
            for letter in row:
                letters[index][letter] = "d"

        keyboard = keyboard_image(letters)
        keyboard_file = image_to_file(keyboard, "keyboard.png")

        keyboard_embed = discord.Embed(
            title="Harf Durumun", color=discord.Color.green()
        )
        keyboard_embed.set_image(url="attachment://keyboard.png")
        keyboard_message = await game_channel.send(
            file=keyboard_file, embed=keyboard_embed
        )

        game_update = {
            "channel_id": f"{game_channel.id}",
            "result_message_id": f"{result_message.id}",
            "keyboard_message_id": f"{keyboard_message.id}",
            "game_type": "wordle",
            "secret": secret,
            "remaining_attempts": 6,
            "word_length": word_length,
            "guesses": guesses,
            "letters": letters,
            "given_up": False
        }
        get_node(f"{interaction.guild.id}/games").update(
            {f"{interaction.user.id}": game_update}
        )


async def setup(bot):
    await bot.add_cog(Wordle(bot))
