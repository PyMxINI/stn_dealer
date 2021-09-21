import asyncio

import aiohttp

import api
from DbHandlers import AsyncDbHandler as a_db
from DbHandlers import DbHander
from fillers.backpack_item_filler import print_percentage


def fill():
    db = DbHander()
    db.connect()
    items = db.get_items()
    loop = asyncio.get_event_loop()

    gather_list = []
    couter = 1
    count = len(items)
    print("start")

    for item in items:
        gather_list.append(test_item(item["id"], item["craftable"], item["quality"], item["name"], loop))

        if couter % 50:
            loop.run_until_complete(asyncio.gather(*gather_list))
            gather_list = []
            print_percentage(couter, count)

        couter += 1

    loop.run_until_complete(asyncio.gather(*gather_list))

    print("end")
    db.disconnect()


async def test_item(id, craftable, quality, name, loop):
    quality = quality + " " if quality != "Unique" else ""
    craftable = "Non-Craftable " if craftable == 0 else ""

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://stntrading.eu/item/tf2/{craftable}{quality}{name}", cookies=api.STN_COOKIE) as response:
            html = await response.text()
            if not "error-text" in html:
                await a_db.insert_stn_url(id, response.url, loop)
                return
        async with session.get(f"https://stntrading.eu/item/tf2/{craftable}{quality}The {name}", cookies=api.STN_COOKIE) as response:
            html = await response.text()
            if not "error-text" in html:
                await a_db.insert_stn_url(id, response.url, loop)

        await session.close()


fill()
