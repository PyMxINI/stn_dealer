import aiohttp
from bs4 import BeautifulSoup

from bot.items.sites.backpack_site.BackpackData import BackpackData


class Backpack:
    def __init__(self, url: str):
        self.url = url

        self.data:BackpackData = None
        self.valid:bool = True

    async def load(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                text = await response.text("latin-1")
                if response.url == "backpack.tf":
                    self.valid = False
                    return

                soup = BeautifulSoup(text, "html.parser")

                self.data = BackpackData(soup)
                self.data.init_data()
                self.valid = self.data.valid
