from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json
import yfinance as yf
import stock_data


def snp500_data():
    name = "S&P 500"

    history = stock_data.get_stock_history("^GSPC")

    wiki = stock_data.get_wiki("", url="https://en.wikipedia.org/wiki/S%26P_500")

    data = {
        "name": name,
        "ticker": "^GSPC",
        "history": history,
        "wiki": wiki
    }

    return data


def djia_data():
    name = "Dow Jones Industrial Average"

    history = stock_data.get_stock_history("^DJI")

    wiki = stock_data.get_wiki("", url="https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average")

    data = {
        "name": name,
        "ticker": "^DJI",
        "history": history,
        "wiki": wiki
    }

    return data


def nasdaq_comp_data():
    name = "NASDAQ Composite"

    history = stock_data.get_stock_history("^IXIC")

    wiki = stock_data.get_wiki("", url="https://en.wikipedia.org/wiki/Nasdaq_Composite")

    data = {
        "name": name,
        "ticker": "^IXIC",
        "history": history,
        "wiki": wiki
    }

    return data


def find_popular_stocks_preview(url):
    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    stock_table = html.find(id="main-table").find("tbody").find_all("tr")[:5]

    stocks = []

    for stock in stock_table:
        data = {
            "ticker": stock.a.text,
            "name": stock.find("td", {"class": "slw"}).text,
            "change": stock.span.text
        }
        stocks.append(data)

    return stocks


def find_popular_stocks(url):
    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    stock_table = html.find(id="main-table").find("tbody").find_all("tr")

    stocks = []

    for stock in stock_table:
        all_data = stock.find_all("td")
        data = {
            "index": all_data[0].text,
            "ticker": all_data[1].text,
            "name": all_data[2].text,
            "change": all_data[3].text,
            "stock_price": all_data[4].text,
            "volume": all_data[5].text,
            "market_cap": all_data[6].text
        }
        stocks.append(data)

    return stocks


def find_popular_stocks_active():
    req = Request(url="https://stockanalysis.com/markets/active/", headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    stock_table = html.find(id="main-table").find("tbody").find_all("tr")

    stocks = []

    for stock in stock_table:
        all_data = stock.find_all("td")
        data = {
            "index": all_data[0].text,
            "ticker": all_data[1].text,
            "name": all_data[2].text,
            "change": all_data[5].text,
            "stock_price": all_data[4].text,
            "volume": all_data[3].text,
            "market_cap": all_data[6].text
        }
        stocks.append(data)

    return stocks

