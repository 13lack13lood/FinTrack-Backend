import yfinance as yf
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json
from stock_news import finviz_news
from datetime import date


def get_stock(ticker):
    stock = yf.Ticker(ticker.capitalize())

    try:
        name = get_stock_full_name(ticker)
    except:
        name = "null"

    try:
        info = get_company_info(ticker)
    except:
        info = "null"

    try:
        wiki = get_wiki(ticker)
    except:
        wiki = "null"

    try:
        stock_info = get_stock_info(ticker)
        history = get_stock_history(ticker)
    except:
        stock_info = "null"
        history = "null"

    try:
        income = get_income(stock)
        income_quarter = get_income_quarter(stock)
    except:
        income = "null"
        income_quarter = "null"

    try:
        balance = get_balance(stock)
        balance_quarter = get_balance_quarter(stock)
    except:
        balance = "null"
        balance_quarter = "null"

    try:
        cashflow = get_cashflow(stock)
        cashflow_quarter = get_cashflow_quarter(stock)
    except:
        cashflow = "null"
        cashflow_quarter = "null"

    try:
        news, news_mean = finviz_news(ticker)
        news = json.loads(news)
        news_mean = json.loads(news_mean)
    except:
        news, news_mean = "null", "null"

    data = {
        "name": name,
        "info": info,
        "wiki": wiki,
        "stock_info": stock_info,
        "history": history,
        "income": income,
        "income_quarter": income_quarter,
        "balance": balance,
        "balance_quarter": balance_quarter,
        "cashflow": cashflow,
        "cashflow_quarter": cashflow_quarter,
        "news": news,
        "news_mean": news_mean
    }

    return data


def get_stock_history(stock_ticker, period="1d"):
    stock = yf.Ticker(stock_ticker.capitalize())

    if period == "1d":
        return json.loads(stock.history(period="1d", interval="1m")[["Open"]].round(2).to_json())

    if period == "5d":
        return json.loads(stock.history(period="5d", interval="5m")[["Open"]].round(2).to_json())

    if period == "1mo":
        return json.loads(stock.history(period="1mo", interval="1h")[["Open"]].round(2).to_json())

    if period == "ytd":
        return json.loads(stock.history(start=date(date.today().year, 1, 1).strftime("%Y-%m-%d"), interval="1d")[["Open"]].round(2).to_json())

    if period == "5y":
        return json.loads(stock.history(period="5y", interval="5d")[["Open"]].round(2).to_json())

    if period == "max":
        return json.loads(stock.history(period="max", interval="1wk")[["Open"]].round(2).to_json())

    return json.loads(stock.history(period=period, interval="1d")[["Open"]].round(2).to_json())


def get_income(stock):
    return json.loads(stock.income_stmt.rename(columns=lambda x: x.year).to_json())


def get_income_quarter(stock):
    return json.loads(stock.quarterly_income_stmt.rename(columns=lambda x: x.to_period('Q')).to_json())


def get_balance(stock):
    return json.loads(stock.balance_sheet.rename(columns=lambda x: x.year).to_json())


def get_balance_quarter(stock):
    return json.loads(stock.quarterly_balance_sheet.rename(columns=lambda x: x.to_period('Q')).to_json())


def get_cashflow(stock):
    return json.loads(stock.cashflow.rename(columns=lambda x: x.year).to_json())


def get_cashflow_quarter(stock):
    return json.loads(stock.quarterly_cashflow.rename(columns=lambda x: x.to_period('Q')).to_json())


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

    data = {}

    info_table_left = html.find("table", {"data-test": "overview-info"}).find_all("tr")

    for row in info_table_left:
        key = row.td.text.strip()
        full_text = row.text
        value = full_text.replace(key, "").strip()

        data[key] = value

    info_table_right = html.find("table", {"data-test": "overview-quote"}).find_all("tr")

    for row in info_table_right:
        key = row.td.text.strip()
        full_text = row.text
        value = full_text.replace(key, "").strip()

        data[key] = value

    return data


def get_wiki(stock_ticker, url=None):
    url = url if url is not None else "https://en.wikipedia.org/wiki/" + get_stock_full_name(stock_ticker).replace(" ", "_")

    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    content = html.find("div", id="bodyContent")
    text = content.find("p", {"class": None})

    for sup in text.find_all("sup"):
        sup.decompose()

    data = {
        "url": url,
        "text": text.text
    }

    return data
