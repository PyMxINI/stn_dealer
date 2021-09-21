import asyncio
import re

import aiohttp
import requests
from bs4 import BeautifulSoup

import api
import effectEnum


def print_percentage(num: int, maximum: int):
    print("{:.2f}%".format((100 / maximum) * num))


STN_URL = "https://stntrading.eu/item/tf2/"
BACKPACK_URL = "https://backpack.tf/overview/"


def fill():
    loop = asyncio.get_event_loop()

    print("Loading site")
    response = requests.get("https://backpack.tf/spreadsheet")

    http = response.text

    response.close()
    print("Site loaded")

    soup = BeautifulSoup(http, "html.parser")
    table = soup.find("table").find("tbody")

    name_list = []

    for name in table.find_all("tr"):
        name_list.append(re.sub(" \(Non-Craftable\)", "", name.find_all("td")[0].text))

    corountines = []
    couter = 1
    count = len(name_list)
    for name in set(name_list):

        if couter % 75 == 0:
            loop.run_until_complete(asyncio.gather(*corountines))
            corountines.clear()
            print_percentage(couter, count)
        couter += 1
        if "#" in name or "Australium" in name or "What's" in name or "Dangeresque, Too?" in name:
            continue

        corountines.append(test_backpack_url(name))
    print(couter)


async def test_backpack_url(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(BACKPACK_URL + name) as response:
            try:
                html = await response.text(encoding="latin 1")

                a_list = BeautifulSoup(html, "html.parser").find(class_="overview").find_all("a")
            except:
                return
            corountines = []

            for a in a_list:
                type_url = BACKPACK_URL + a["href"][1:]
                type_url_listed = type_url.split("/")

                quality = type_url_listed[5]

                if "Unusual" in quality:
                    corountines.append(test_stn_url(quality, name, type_url, type_url_listed[-1]))
                elif "Unique" in quality:
                    corountines.append(test_stn_url("", name, type_url, ""))
                else:
                    corountines.append(test_stn_url(quality, name, type_url, ""))

            return asyncio.gather(*corountines)


async def test_stn_url(quality, name, backpack_url, effect_id):
    effect = effectEnum.effect[effect_id]
    effect = "" if effect == "" else effect + " "
    quality = "" if quality == "" else quality + " "
    url = STN_URL + quality + effect + name

    async with aiohttp.ClientSession() as session:
        async with session.get(url, cookies=api.STN_COOKIE) as response:
            text = await response.text()

            if "error-text" in text:
                return

            # TODO: implementovat databázi


#     table = soup.find("table").find("tbody")
#
#     corountines_list = []
#
#     for row in table.find_all("tr"):
#         name = re.sub(" \(Non-Craftable\)", "", row.find_all("td")[0].text)
#         craftable = row["data-craftable"]
#         url_list = ["https://backpack.tf" + soup["href"] for soup in row.find_all("a")]
#
#         for backpack_url in url_list:
#             if len(corountines_list) % 50 == 0:
#                 loop.run_until_complete(asyncio.gather(*corountines_list))
#                 corountines_list.clear()
#
#             corountines_list.append(check(name, craftable, backpack_url))
#
#
# async def check(name, craftable, backpack_url):
#     parsed_url = urllib.parse.unquote(backpack_url)
#     quality_soup = re.search("stats/((\w|Collector\'s)+)/", parsed_url)
#     if quality_soup is None:
#         return
#
#     quality = quality_soup.group(1)
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(backpack_url) as response:
#             html = await response.text(encoding="latin 1")
#             item_type_block = BeautifulSoup(html, "html.parser").find(class_="stats-header-controls").findChild()
#
#             item_types = item_type_block.find_all("a")
#
#             for item_type in item_types:
#                 text = item_type.text
#
#                 if "Genuine" in text or "Vintage" in text or "Unique" in text or "Strange" in text\
#                         or "Haunted" in text or "Collector's" in text or "Non-Craftable" in text:
#                     continue
#
#                 print(text)
#
#
#
fill()
