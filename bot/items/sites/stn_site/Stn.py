import aiohttp
from bs4 import BeautifulSoup

import api
from bot.items.sites.stn_site.StnData import StnData


class Stn:
    def __init__(self, url: str):
        self.url = url

        self.data:StnData = None
        self.valid:bool = True

    async def load(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, cookies=api.STN_COOKIE) as response:
                text = await response.text()
                if "error-text" in text:
                    self.valid = False
                    return

                soup = BeautifulSoup(text, "html.parser")

                self.data = StnData(soup)
                self.data.init_data()
                self.valid = self.data.valid
