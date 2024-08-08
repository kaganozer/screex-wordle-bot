import discord

from typing import Literal

from wordle.functions.get_word_meaning import get_word_meaning


class CommandEmbed:
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction

    @property
    def embed(self):
        interaction = self.interaction
        user = interaction.user

        user_avatar = user.avatar if user.avatar else user.default_avatar

        embed = discord.Embed(color=discord.Color.green()).set_footer(
            text=f"{user.name} tarafından istendi.", icon_url=user_avatar.url
        )

        return embed


class ErrorEmbed:
    def __init__(self, interaction: discord.Interaction):
        self.interaction = interaction

    @property
    def embed(self):
        interaction = self.interaction
        user = interaction.user

        user_avatar = user.avatar if user.avatar else user.default_avatar

        embed = (
            discord.Embed(
                title="İsteğin gerçekleştirilemedi!", color=discord.Color.red()
            )
            .add_field(
                name="Komutu doğru kullandığını mı düşünüyorsun?",
                value="Beklenmeyen bir hata oluşmuş olabilir. Lütfen yetkililer ile iletişime geç.",
                inline=False
            )
            .set_footer(
                text=f"{user.name} tarafından istendi.", icon_url=user_avatar.url
            )
        )

        return embed


class WordleStartEmbed:
    @property
    def embed(self):
        return discord.Embed(
            title="Oyunun başladı!",
            description="Bu kanalda oyununu görüntüleyebilir ve tahminlerini yapabilirsin!",
            color=discord.Color.green(),
        ).add_field(
            name="Nasıl oynanıyor?",
            value=f"Oyunun kurallarını açılan Thread kanalında bulabilirsin.",
            inline=False,
        )


class WordleCommandsEmbed:
    @property
    def embed(self):
        return (
            discord.Embed(
                title="Hangi komutları kullanabilirsin?",
                description="İşte kullanabileceğin komutlar:",
                color=discord.Color.green(),
            )
            .add_field(
                name="/peset",
                value="Pes etmek için kullanabilirsin. Oyunu bitirir ancak kanalı silmez.",
                inline=False,
            )
            .add_field(
                name="/stats",
                value="Oyunun boyunca yaptığın tahminlerle gösterdiğin performansı gösterir.",
                inline=False
            )
            .add_field(
                name="/bitir",
                value="Oyunu bitirmek için kullanabilirsin.",
                inline=False,
            )
            .add_field(
                name="Uyarı!",
                value="`/bitir` komutu bu kanalı siler. Kullanırken dikkatli ol!",
                inline=False,
            )
        )


class WordleRulesEmbed:
    @property
    def embed(self):
        return (
            discord.Embed(
                title="Renkler ne anlama geliyor?",
                description="İşte tahminlerden sonra gördüğün renklerin anlamları:",
                color=discord.Color.green(),
            )
            .add_field(
                name="Yeşil renk :green_circle:",
                value="Harfin yerinin doğru bilindiğini gösterir.",
                inline=False,
            )
            .add_field(
                name="Sarı renk :yellow_circle:",
                value="Harfin gizli kelimenin içinde olduğunu ancak yerinin yanlış bilindiğini gösterir.",
                inline=False,
            )
            .add_field(
                name="Siyah renk :black_circle:",
                value="Harfin gizli kelimenin içine olmadığını gösterir.",
                inline=False,
            )
        )


class GameOverEmbed:
    def __init__(
        self,
        secret: str,
        game_state: Literal["correct_guess", "no_attempts_left", "given_up"],
    ):
        self.secret = secret
        self.game_state = game_state

    @property
    def embed(self):
        secret = self.secret
        game_state = self.game_state

        secret_meaning = get_word_meaning(secret)
        if not secret_meaning:
            secret_meaning = "Oluşan bir hata sonucu kelimenin anlamına ulaşılamadı."

        embed = (
            discord.Embed(color=discord.Color.green())
            .add_field(
                name="Kelimenin anlamı ne?",
                value=f"{secret.capitalize()}: {secret_meaning}.",
                inline=False,
            )
            .add_field(
                name="TDK Güncel Türkçe Sözlük",
                value="Detaylı bilgi için TDK'nin [web sitesini](https://sozluk.gov.tr) ziyaret edebilirsin.",
            )
            .add_field(
                name="Şimdi ne yapacağım?",
                value="İstatistiklerini görmek için `/stats` komutunu veya oyunu bitirmek için `/bitir` komutunu kullanabilirsin.",
                inline=False,
            )
        )
        if game_state == "correct_guess":
            embed.title = "Tebrikler!"
            embed.description = "Kelimeyi doğru tahmin ettin."
        elif game_state == "no_attempts_left":
            embed.title = "Bütün haklarını kullandın!"
            embed.description = f"Doğru kelime {secret} olacaktı."
        elif game_state == "given_up":
            embed.title = "Pes ettin!"
            embed.description = f"Doğru kelime {secret} olacaktı."

        return embed
