import discord
from discord.ext import commands

import mycord


db = mycord.DB()


db.create_table(
    "coc_accounts",
    """
    discord_id INTEGER PRIMARY KEY,
    player_tag TEXT NOT NULL
    """
)


class Clash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="coc", invoke_without_command=True)
    async def coc(self, ctx):
        await ctx.send(
            "🏰 **Clash of Clans**\n\n"
            "`!coc link #PLAYER_TAG`\n"
            "`!coc profile`"
        )

    @coc.command(name="link")
    async def link(self, ctx, player_tag):

        player_tag = player_tag.upper()

        if not player_tag.startswith("#"):
            player_tag = "#" + player_tag

        existing = db.fetchone(
            "coc_accounts",
            {
                "discord_id": ctx.author.id
            }
        )

        if existing:
            db.update(
                "coc_accounts",
                {
                    "player_tag": player_tag
                },
                {
                    "discord_id": ctx.author.id
                }
            )
        else:
            db.insert(
                "coc_accounts",
                {
                    "discord_id": ctx.author.id,
                    "player_tag": player_tag
                }
            )

        await ctx.send(
            f"✅ Your Clash of Clans account is now linked:\n"
            f"`{player_tag}`"
        )

    @coc.command(name="profile")
    async def profile(self, ctx):

        account = db.fetchone(
            "coc_accounts",
            {
                "discord_id": ctx.author.id
            }
        )

        if not account:
            await ctx.send(
                "❌ You haven't linked a Clash of Clans account yet."
            )
            return

        player_tag = account["player_tag"]

        await ctx.send(
            f"🏰 Linked account: `{player_tag}`"
        )


async def setup(bot):
    await bot.add_cog(Clash(bot))