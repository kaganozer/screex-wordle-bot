import discord
from discord.ext import commands
from discord import app_commands

from database.database import get_node
from assets.embeds import CommandEmbed
from wordle.functions.check_player import player_is_on_correct_channel
from wordle.functions.check_stats import check_stats, stat_message


class Stats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="stats", description="Wordle oyunundaki istatistiklerini gösterir."
    )
    @app_commands.check(player_is_on_correct_channel)
    async def stats(self, interaction: discord.Interaction):
        user = interaction.user
        guild = interaction.guild

        embed = CommandEmbed(interaction).embed

        user_game = get_node(f"{guild.id}/games/{user.id}").get()

        remaining_attempts = user_game["remaining_attempts"]
        if not remaining_attempts == 0:
            embed.title = "İsteğin gerçekleştirilemedi."
            embed.description = (
                "Bu komutu yalnızca oyunun bittikten sonra kullanabilirsin."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        word_length = user_game["word_length"]
        guesses = list(
            filter(lambda word: word != "-" * word_length, user_game["guesses"])
        )

        if not guesses:
            embed.title = (
                "Herhangi bir tahminde bulunmadığın için istatistiklerini göremezsin."
            )
            embed.description = "Bir dahaki sefere oyunu oynamayı da dene!"
        else:
            secret = user_game["secret"]
            word_counts = check_stats(guesses, secret)

            embed.title = "İşte istatistiklerin:"
            embed.description = f"Başlangıçta {word_counts[0]} kelime vardı."

            for index, guess in enumerate(guesses):
                initial = word_counts[index]
                remaining = word_counts[index + 1]
                message = stat_message(initial, remaining, guess == secret)
                embed.add_field(
                    name=guess.capitalize(),
                    value=message,
                    inline=False,
                )

            if user_game["given_up"]:
                remaining_attempts = 6 - len(guesses)
                embed.add_field(
                    name="Pes ettin!",
                    value=f"{word_counts[-1]} kelime ve {remaining_attempts} hakkın kalmışken pes ettin.",
                )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Stats(bot))
