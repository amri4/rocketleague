import os

import discord
from discord.ext import commands

from utils.rocketleague import RocketLeagueAPI


class RocketLeague(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.api = RocketLeagueAPI(
            os.getenv("ROCKET_API_KEY")
        )

        self.accounts = {}

    @commands.group(name="rl", invoke_without_command=True)
    async def rl(self, ctx):

        await ctx.send(
            "🏎️ Rocket League\n\n"
            "`rl link <platform> <username>`\n"
            "`rl profile`"
        )

    @rl.command(name="link")
    async def link(self, ctx, platform, *, username):

        platform = platform.lower()

        platforms = {
            "epic": "epic",
            "steam": "steam",
            "ps": "psn",
            "psn": "psn",
            "playstation": "psn",
            "xbox": "xbl"
        }

        if platform not in platforms:
            await ctx.send(
                "❌ Platform must be `epic`, `steam`, `psn`, or `xbox`."
            )
            return

        platform = platforms[platform]

        data = await self.api.get_profile(
            platform,
            username
        )

        if not data:
            await ctx.send(
                "❌ I couldn't find that Rocket League account."
            )
            return

        self.accounts[ctx.author.id] = {
            "platform": platform,
            "username": username
        }

        await ctx.send(
            f"✅ Linked your Rocket League account!\n"
            f"Platform: `{platform}`\n"
            f"Player: `{username}`"
        )

    @rl.command(name="profile")
    async def profile(self, ctx):

        account = self.accounts.get(ctx.author.id)

        if not account:
            await ctx.send(
                "❌ You haven't linked a Rocket League account yet.\n"
                "Use `rl link <platform> <username>`."
            )
            return

        data = await self.api.get_profile(
            account["platform"],
            account["username"]
        )

        if not data:
            await ctx.send(
                "❌ Couldn't retrieve your Rocket League profile."
            )
            return

        profile = data.get("data", data)

        embed = discord.Embed(
            title="🏎️ Rocket League Profile",
            description=(
                f"**{account['username']}**\n"
                f"Platform: `{account['platform']}`"
            )
        )

        segments = profile.get("segments", [])

        overview = None
        playlists = []

        for segment in segments:

            if segment.get("type") == "overview":
                overview = segment

            elif segment.get("type") == "playlist":
                playlists.append(segment)

        if overview:

            stats = overview.get("stats", {})

            wins = stats.get("wins", {}).get(
                "displayValue",
                "0"
            )

            goals = stats.get("goals", {}).get(
                "displayValue",
                "0"
            )

            assists = stats.get("assists", {}).get(
                "displayValue",
                "0"
            )

            saves = stats.get("saves", {}).get(
                "displayValue",
                "0"
            )

            shots = stats.get("shots", {}).get(
                "displayValue",
                "0"
            )

            embed.add_field(
                name="📊 Lifetime",
                value=(
                    f"🏆 Wins: **{wins}**\n"
                    f"⚽ Goals: **{goals}**\n"
                    f"🅰️ Assists: **{assists}**\n"
                    f"🛡️ Saves: **{saves}**\n"
                    f"🎯 Shots: **{shots}**"
                ),
                inline=False
            )

        for playlist in playlists:

            metadata = playlist.get("metadata", {})
            stats = playlist.get("stats", {})

            name = metadata.get(
                "name",
                "Ranked"
            )

            rank = stats.get("rank", {}).get(
                "displayValue",
                "Unranked"
            )

            mmr = stats.get("rating", {}).get(
                "displayValue",
                "?"
            )

            embed.add_field(
                name=name,
                value=f"Rank: **{rank}**\nMMR: **{mmr}**",
                inline=True
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(RocketLeague(bot))