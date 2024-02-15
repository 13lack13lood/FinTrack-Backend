import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def get_stock_headlines(stock_ticker):
    url = "https://stockanalysis.com/stocks/" + stock_ticker + "/"

    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    news_table = html.find_all("div", {"class": "gap-4"})

    data = []

    for news in news_table:
        link = news.a["href"]
        img_src = news.a.img["src"]
        header = news.div.find("div", {"class": "text-faded"}).text.split("-")
        timestamp = header[0].strip()
        publisher = header[1].strip()
        headline = news.div.h3.a.text
        description = news.div.p.text
        ticker_array = [ticker.text for ticker in news.div.find_all("a", {"class": "ticker"})]

        data.append([link, img_src, timestamp, publisher, headline, description, ticker_array])

    stock_news_df = pd.DataFrame(data, columns=["link", "img_src", "timestamp", "publisher", "headline", "description",
                                                "tickers"])

    return stock_news_df


def general_stock_news_scrape():
    url = "https://stockanalysis.com/news/all-stocks/"

    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    news_table = html.find_all("div", {"class": "gap-4"})

    data = []

    for news in news_table:
        link = news.a["href"]
        img_src = news.a.img["src"]
        header = news.div.find("div", {"class": "text-faded"}).text.split("-")
        timestamp = header[0].strip()
        publisher = header[1].strip()
        headline = news.div.h3.a.text
        description = news.div.p.text
        ticker_array = [ticker.text for ticker in news.div.find_all("a", {"class": "ticker"})]

        data.append([link, img_src, timestamp, publisher, headline, description, ticker_array])

    stock_news_df = pd.DataFrame(data, columns=["link", "img_src", "timestamp", "publisher", "headline", "description", "tickers"])

    return stock_news_df


def finviz_news(ticker):
    news = get_stock_headlines(ticker)
    # output = stock_news_analysis(news)

    # mean_df = output[["date", "compound"]].groupby(["date"]).mean().reset_index().iloc[::-1]

    return news.to_json()  # mean_df.set_index("date").round(2).to_json()


def general_stock_news():
    news = general_stock_news_scrape()
    # output = stock_news_analysis(news)

    return news.to_json()


