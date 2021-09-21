import asyncio

import DbHandlers as db
from items.Item import Item


def print_percentage(num: int, maximum: int):
    print("{:.2f}%".format((100 / maximum) * num))


class Bot:
    def __init__(self):
        handler = db.DbHander()
        self.items = handler.get_items()
        self.wallet = handler.get_wallet()
        self.items_objects = []

    def start(self):
        self._set_up_items()
        self._start_trading()

    def _start_trading(self):
        loop = asyncio.get_event_loop()
        func_list = []
        counter = 0
        count = len(self.items)
        for item in self.items_objects:
            print_percentage(counter, count)
            if counter % 100 == 0:
                loop.run_until_complete(asyncio.gather(*func_list))
                func_list = []


            func_list.append(item.start())
            counter += 1

    def _set_up_items(self):
        for item in self.items:
            self.items_objects.append(Item(item, self.wallet))


Bot().start()
