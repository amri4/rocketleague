import aiohttp


API_URL = "https://api.parse.bot/scraper/d0dcf8e8-3a72-4b21-bffb-8fa735257835/get_player_profile"


class RocketLeagueAPI:

    def __init__(self, api_key):
        self.api_key = api_key

    async def get_profile(self, platform, username):

        params = {
            "platform": platform,
            "username": username
        }

        headers = {
            "X-API-Key": self.api_key
        }

        async with aiohttp.ClientSession() as session:

            async with session.get(
                API_URL,
                params=params,
                headers=headers
            ) as response:

                if response.status != 200:
                    return None

                return await response.json()