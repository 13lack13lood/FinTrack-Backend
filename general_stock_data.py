from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json


def find_popular_stocks(url):
    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    stock_table = html.find(id="main-table").find("tbody").find_all("tr")[:5]

    stocks = []

    for stock in stock_table:
        data = {
            "ticker": stock.a.text,
            "name": stock.find("td", {"class": "slw"}).text,
            "change": stock.div.text
        }
        stocks.append(data)

    return stocks


print(find_popular_stocks("https://stockanalysis.com/markets/losers/"))
