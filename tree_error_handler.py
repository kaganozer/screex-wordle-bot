import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime

from assets.embeds import ErrorEmbed


class TreeErrorHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        bot.tree.on_error = self.on_tree_error
        self.bot = bot

    async def on_tree_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        user = interaction.user
        guild = interaction.guild
        channel = interaction.channel

        command_name = interaction.command.name
        embed = ErrorEmbed(interaction).embed

        if command_name in ["bitir", "peset", "stats"]:
            embed.description = (
                "Bu komutu sadece kendi Wordle oyun kanalında kullanabilirsin."
            )
        if isinstance(error, app_commands.errors.MissingPermissions):
            embed.description = (
                "Bu komutu kullanmak için gerekli yetkilere sahip değilsin!"
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

        current_time = datetime.now()
        formatted_time = current_time.strftime("%d.%m.%Y %H:%M:%S")

        print("-----")
        print(f"[{formatted_time}]")
        print(
            f"{user.name} used /{command_name} on Guild: {guild.name}, Channel: {channel.name}"
        )
        print(f"User ID: {user.id}, Guild ID: {guild.id}, Channel ID: {channel.id}")
        print(f"{error.__class__.__name__}: {error}")
        print("-----")


async def setup(bot):
    await bot.add_cog(TreeErrorHandler(bot))
