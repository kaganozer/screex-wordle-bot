import discord
from discord.ext import commands
from discord import app_commands

from database.database import ref, get_node
from wordle.functions.check_player import guild_has_a_start_channel
from assets.embeds import CommandEmbed


class SetServer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="ayarla", description="Sunucu için bir oyun kategorisi oluşturur."
    )
    @commands.has_permissions(manage_channels=True)
    async def set_server(self, interaction: discord.Interaction):
        guild = interaction.guild

        embed = CommandEmbed(interaction).embed
        if guild_has_a_start_channel(guild):
            start_channel_id = get_node(f"{guild.id}/start_channel").get()
            embed.title = f"Bu sunucu zaten bir oyun kategorisine sahip!"
            embed.description = f"Oyun kanalı: <#{start_channel_id}>"
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        embed.title = "Kategori oluşturuluyor."
        embed.description = (
            "Screex Bot'un rolünü diğer rollerden yukarı taşımayı unutma!"
        )
        await interaction.response.send_message(embed=embed)

        game_category = await guild.create_category(name="screex")
        start_channel = await guild.create_text_channel(
            name="oyun-baslat",
            category=game_category,
            topic="Bu kanala mesaj göndererek oynamak istediğin oyunu başlatabilirsin!",
            slowmode_delay=5,
        )

        ref.update({guild.id: {"start_channel": str(start_channel.id)}})

        await start_channel.send(
            "Bu kanala mesaj göndererek oynamak istediğin oyunu başlatabilirsin!"
        )
        await start_channel.send("Şu an oynayabileceğin oyunlar: `Wordle`")


async def setup(bot):
    await bot.add_cog(SetServer(bot))
