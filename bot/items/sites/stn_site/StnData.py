import requests
from bs4 import BeautifulSoup

from bot.items.Currency import Currency


class StnData():
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self.valid = True

        self.buyer_amount = None
        self.seller_amount = None
        self.seller_price = None
        self.buyer_price = None

    def init_data(self):
        try:
            sell_block = self.soup.find(class_="d-flex justify-content-center").parent
            buy_block = self.soup.find(class_="btn btn-success rounded-0").parent

            self.buyer_amount = int(buy_block.find_all("b")[1].get_text())
            self.seller_amount = int(sell_block.find_all("b")[1].get_text())

            self.buyer_price = Currency(buy_block.find("b").get_text())
            self.seller_price = Currency(sell_block.find("b").get_text())

            if "disabled" in str(sell_block.find(class_="input-group")):
                self.seller_amount = 0

            if not (self.seller_price.valid and self.buyer_price.valid):
                self.valid = False


        except:
            self.valid = False



idkk = StnData(BeautifulSoup(requests.get("https://stntrading.eu/item/tf2/Strange%20Cremator's%20Conscience").text, "html.parser"))
idkk.init_data()