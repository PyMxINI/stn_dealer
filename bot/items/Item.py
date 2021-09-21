import asyncio
import os
import io
from bot.items.Currency import Currency
from bot.items.sites.backpack_site.Backpack import Backpack
from bot.items.sites.stn_site.Stn import Stn


class Item:
    def __init__(self, item: dict, wallet):
        self.item = item
        self.wallet = wallet

        self.backpack = Backpack(item["backpack_url"])
        self.stn = Stn(item["stn_url"])

        self.valid = True

        self.stn_to_backpack_profitable = False
        self.backpack_to_stn_profitable = False

        self.stn_to_backpack: float = None
        self.backpack_to_stn: float = None

    async def start(self):
        await self._start_load()
        self._check_validity()

        if not self.valid:
            return

        self._set_profitability()
        self._export_log()

    def _start_load(self):
        return asyncio.gather(self.backpack.load(), self.stn.load())

    def _check_validity(self):
        if not (self.backpack.valid and self.stn.valid):
            self.valid = False

    def _set_profitability(self):

        lowest_seller_bots = self.backpack.data.seller_bot_list
        higher_buyer_bots = self.backpack.data.buyer_bot_list

        self.stn_to_backpack = higher_buyer_bots[
                                   0].price - self.stn.data.seller_price if higher_buyer_bots else Currency(0, 0)
        self.backpack_to_stn = self.stn.data.buyer_price - lowest_seller_bots[
            0].price if lowest_seller_bots else Currency(0, 0)

        if self.stn_to_backpack > Currency(0, 0) and self.stn.data.seller_amount > 0:
            self.stn_to_backpack_profitable = True
            return

        if self.backpack_to_stn > Currency(0, 0) and self.stn.data.buyer_amount > 0:
            self.backpack_to_stn_profitable = True
            return

    def _export_log(self):
        if not (self.stn_to_backpack_profitable or self.backpack_to_stn_profitable):
            return

        file = io.open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', "..", "logs", "export.txt")), "a", encoding="utf-8")
        file.write(f"""
        =====================================================\n
        {self.item["quality"]} {self.item["name"]}\n
        {self.item["backpack_url"]}\n
        {self.item["stn_url"]}\n\n
        {("Stn to backpack:" + str(self.stn_to_backpack)) if self.stn_to_backpack_profitable else None}\n
        {("Backpack to stn:" + str(self.backpack_to_stn)) if self.backpack_to_stn_profitable else None}\n
        =====================================================
        
        """)
