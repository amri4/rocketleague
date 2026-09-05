import aiohttp


class ClashAPI:

    BASE_URL = "https://api.clashofclans.com/v1"

    def __init__(self, token):
        self.token = token

    async def get_player(self, tag):

        tag = tag.upper()

        if not tag.startswith("#"):
            tag = "#" + tag

        url = f"{self.BASE_URL}/players/{tag[1:]}"

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers=headers
            ) as response:

                if response.status != 200:
                    return None

                return await response.json()