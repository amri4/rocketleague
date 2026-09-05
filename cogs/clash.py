import os

import discord
from discord.ext import commands

from utils.clash_api import ClashAPI


class Clash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.api = ClashAPI(
            os.getenv("COC_API_TOKEN")
        )

        self.accounts = {}

    @commands.group(name="coc", invoke_without_command=True)
    async def coc(self, ctx):

        await ctx.send(
            "🏰 **Clash of Clans**\n\n"
            "`!coc link #PLAYER_TAG`\n"
            "`!coc profile`"
        )

    @coc.command(name="link")
    async def link(self, ctx, tag):

        data = await self.api.get_player(tag)

        if not data:
            await ctx.send(
                "❌ I couldn't find that player."
            )
            return

        self.accounts[ctx.author.id] = data["tag"]

        await ctx.send(
            f"✅ Linked **{data['name']}**!\n"
            f"Tag: `{data['tag']}`"
        )

    @coc.command(name="profile")
    async def profile(self, ctx):

        tag = self.accounts.get(ctx.author.id)

        if not tag:
            await ctx.send(
                "❌ You haven't linked a Clash of Clans account.\n"
                "Use `!coc link #PLAYER_TAG`."
            )
            return

        data = await self.api.get_player(tag)

        if not data:
            await ctx.send(
                "❌ Couldn't retrieve your player."
            )
            return

        embed = discord.Embed(
            title=f"🏰 {data['name']}",
            description=f"`{data['tag']}`"
        )

        embed.add_field(
            name="🏠 Town Hall",
            value=data.get("townHallLevel", "?"),
            inline=True
        )

        embed.add_field(
            name="⭐ XP Level",
            value=data.get("expLevel", "?"),
            inline=True
        )

        embed.add_field(
            name="🏆 Trophies",
            value=data.get("trophies", "?"),
            inline=True
        )

        embed.add_field(
            name="🏆 Best Trophies",
            value=data.get("bestTrophies", "?"),
            inline=True
        )

        embed.add_field(
            name="⚔️ War Stars",
            value=data.get("warStars", "?"),
            inline=True
        )

        clan = data.get("clan")

        if clan:
            embed.add_field(
                name="🏰 Clan",
                value=(
                    f"**{clan['name']}**\n"
                    f"`{clan['tag']}`"
                ),
                inline=False
            )

        if data.get("league"):
            embed.add_field(
                name="🏆 League",
                value=data["league"]["name"],
                inline=True
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Clash(bot))