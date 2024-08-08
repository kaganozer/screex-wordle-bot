import discord
from discord.ext import commands

import json

from database.database import get_node
from wordle.functions.check_guess import check_guess
from wordle.functions.result_image import result_image
from wordle.functions.keyboard_image import keyboard_image
from wordle.functions.check_player import player_is_on_correct_channel
from wordle.functions.game_over import game_over
from assets.images.image_to_file import image_to_file
from assets.buttons import StopButton


class Guess(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not player_is_on_correct_channel(message):
            return

        guess = "".join(
            map(lambda x: "ı" if x == "I" else x.lower(), list(message.content))
        )
        guess_embed = discord.Embed(color=discord.Color.green())

        user = message.author
        guild = message.guild
        channel = message.channel

        user_node = get_node(f"{guild.id}/games/{user.id}")
        user_game = user_node.get()

        remaining_attempts = user_game["remaining_attempts"]
        if not remaining_attempts:
            return

        await message.delete()

        word_length = user_game["word_length"]
        if not len(guess) == word_length:
            guess_embed.description = f"Kelimen {word_length} harf uzunluğunda olmalı!"
            guess_embed.color = discord.Color.red()
            await channel.send(embed=guess_embed, delete_after=1)
            return

        secret = user_game["secret"]
        guesses = user_game["guesses"]
        letters_alphabetic = user_game["letters"]
        letters = [dict(), dict(), dict()]
        for index, row in enumerate(["qwertyuıopğü", "asdfghjklşi", "zxcvbnmöç"]):
            for letter in row:
                letters[index][letter] = letters_alphabetic[index][letter]

        with open(
            f"wordle/words/{word_length}_harf.txt", "r", encoding="utf-8"
        ) as file:
            words = json.loads(file.read())

        if guess not in words:
            guess_embed.description = "Bu kelime listemizde yok!"
            guess_embed.color = discord.Color.red()
            await channel.send(embed=guess_embed, delete_after=1)
            return
        if guess in guesses:
            guess_embed.description = "Bu kelimeyi zaten denedin!"
            guess_embed.color = discord.Color.red()
            await channel.send(embed=guess_embed, delete_after=1)
            return

        result_message_id = int(user_game["result_message_id"])
        result_message = channel.get_partial_message(result_message_id)

        guesses[6 - remaining_attempts] = guess
        remaining_attempts -= 1

        result = result_image(guesses, secret)
        result_file = image_to_file(result)

        result_embed = discord.Embed(
            title=f"Wordle - {word_length} Harf",
            description=f"Kalan hakların: {remaining_attempts}",
            color=discord.Color.green(),
        )
        result_embed.set_image(url="attachment://result.png")
        await result_message.edit(
            attachments=[result_file], embed=result_embed, view=StopButton()
        )

        keyboard_message_id = int(user_game["keyboard_message_id"])
        keyboard_message = channel.get_partial_message(keyboard_message_id)

        results = check_guess(guess, secret)
        for index, letter in enumerate(guess):
            for row in letters:
                if letter in row.keys():
                    if row[letter] == "g":
                        continue
                    if results[index] == "b" and row[letter] == "y":
                        continue
                    row[letter] = results[index]

        keyboard = keyboard_image(letters)
        keyboard_file = image_to_file(keyboard, "keyboard.png")

        keyboard_embed = discord.Embed(
            title="Harf Durumun", color=discord.Color.green()
        )
        keyboard_embed.set_image(url="attachment://keyboard.png")
        await keyboard_message.edit(attachments=[keyboard_file], embed=keyboard_embed)

        if guess == secret:
            await game_over(message, secret, "correct_guess")
            remaining_attempts = 0
        elif remaining_attempts == 0:
            await game_over(message, secret, "no_attempts_left")
        else:
            guess_embed.description = "Sonucun yukarıdaki tabloda."
            await channel.send(embed=guess_embed, delete_after=1)

        user_node.update(
            {
                "remaining_attempts": remaining_attempts,
                "guesses": guesses,
                "letters": letters,
            }
        )


async def setup(bot):
    await bot.add_cog(Guess(bot))
