from bs4 import BeautifulSoup
import requests
import api
import re

soup = BeautifulSoup(requests.get("https://stntrading.eu/item/tf2/Hooded%20Haunter", cookies=api.STN_COOKIE).text, "html.parser")



sell_block = soup.find(class_="d-flex justify-content-center").parent
buy_block = soup.find(class_="btn btn-success rounded-0").parent

#print(sell_block)

print("disabled" in str(sell_block.find(class_="input-group")))