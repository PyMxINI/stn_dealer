import bs4

from bot.items.Currency import Currency
from bot.items.sites.backpack_site.BackpackBot import BackpackBotSeller, BackpackBotBuyer


class BackpackData:
    def __init__(self, soup: bs4.BeautifulSoup):
        self.soup = soup
        self.valid = True
        self.buyer_bot_list: list[BackpackBotBuyer] = []
        self.seller_bot_list: list[BackpackBotSeller] = []

    def init_data(self):
        try:
            sell_panel = self.soup.find(text="Sell Orders").find_parent(class_="col-md-6")
            buy_panel = self.soup.find(text="Buy Orders").find_parent(class_="col-md-6")

            seller_listings = list(
                map(lambda elem: elem.find_parent(class_="listing"), sell_panel.find_all(class_="fa-flash")))
            buyer_listings = list(
                map(lambda elem: elem.find_parent(class_="listing"), buy_panel.find_all(class_="fa-flash")))

            for listing in seller_listings:
                desc = str(listing.find(class_="quote-box").p.get_text)
                url = str(listing.find(class_="listing-buttons").find("a", href=True)["href"])
                price = Currency(desc)
                if price.valid:
                    self.seller_bot_list.append(BackpackBotSeller(price, url))

            for listing in buyer_listings:
                desc = str(listing.find(class_="quote-box").p.get_text)
                url = str(listing.find(class_="listing-buttons").find("a", href=True)["href"])
                price = Currency(desc)
                if price.valid:
                    self.buyer_bot_list.append(BackpackBotBuyer(price, url))

        except:
            self.valid = False
