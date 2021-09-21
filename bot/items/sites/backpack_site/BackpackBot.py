from bot.items.Currency import Currency


class BackpackBot:
    def __init__(self, price: Currency, trade_url):
        self.price = price
        self.trade_url = trade_url


class BackpackBotSeller(BackpackBot):
    def __init__(self, price: Currency, trade_url):
        super().__init__(price, trade_url)


class BackpackBotBuyer(BackpackBot):
    def __init__(self, price: Currency, trade_url):
        super().__init__(price, trade_url)
