import yfinance as yf
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def get_stock(ticker):
    stock = yf.Ticker(ticker.capitalize())

    return stock


def get_stock_history(ticker):
    stock = get_stock(ticker)

    history_df_max = stock.history(period="max", interval="1wk")[["Open", "High", "Low", "Close", "Volume"]]
    history_df_max["date"] = history_df_max.index.date

    history_df_max.to_json("output.json", index=False)

get_stock_history("arch")

def get_income(ticker):
    stock = get_stock(ticker)

    return stock.income_stmt.rename(columns=lambda x: x.year).to_json()


def get_income_quarter(ticker):
    stock = get_stock(ticker)

    return stock.quarterly_income_stmt.rename(columns=lambda x: x.to_period('Q')).to_json()


def get_balance(ticker):
    stock = get_stock(ticker)

    return stock.balance_sheet.rename(columns=lambda x: x.year).to_json()


def get_balance_quarter(ticker):
    stock = get_stock(ticker)

    return stock.quarterly_balance_sheet.rename(columns=lambda x: x.to_period('Q')).to_json()


def get_cashflow(ticker):
    stock = get_stock(ticker)

    return stock.cashflow.rename(columns=lambda x: x.year).to_json()


def get_cashflow_quarter(ticker):
    stock = get_stock(ticker)

    return stock.quarterly_cashflow.rename(columns=lambda x: x.to_period('Q')).to_json()


# gets full company name given stock ticker
def get_stock_full_name(stock_ticker):
    url = "https://finviz.com/quote.ashx?t=" + stock_ticker.capitalize()

    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    name = html.find("h2", {"class": "quote-header_ticker-wrapper_company"}).text.strip()

    return name


# gets company info (industry, ipo date, sector, etc.)
def get_company_info(stock_ticker):
    url = "https://stockanalysis.com/stocks/" + stock_ticker.capitalize()

    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    info_table = html.find("div", {"data-test": "overview-profile-values"}).find_all("div")

    data = {}

    for row in info_table:
        key = row.span.text.strip()
        full_text = row.text
        value = full_text.replace(key, "").strip()

        data[key] = value

    exchange_info_html = html.find("main", id="main")
    exchange_info = exchange_info_html.div.div.div.div.text.split("·")

    data["Exchange"] = exchange_info[0].strip()
    data["Currency"] = exchange_info[-1].strip()

    return data


# gets fundamental stock info (market cap, eps, pe, etc)
def get_stock_info(stock_ticker):
    url = "https://stockanalysis.com/stocks/" + stock_ticker.capitalize()

    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    info_table_left = html.find("table", {"data-test": "overview-info"}).find_all("tr")

    data = {}

    for row in info_table_left:
        key = row.td.text
        full_text = row.text
        value = full_text.replace(key, "").strip()

        data[key] = value

    info_table_right = html.find("table", {"data-test": "overview-quote"}).find_all("tr")

    for row in info_table_right:
        key = row.td.text
        full_text = row.text
        value = full_text.replace(key, "").strip()

        data[key] = value

    return data


def get_wiki(stock_ticker):
    name = get_stock_full_name(stock_ticker).replace(" ", "_")
    print(name)
    url = "https://en.wikipedia.org/wiki/" + name

    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    content = html.find("div", id="bodyContent")
    text = content.find("p", {"class": None})

    for sup in text.find_all("sup"):
        sup.decompose()

    return text.text
