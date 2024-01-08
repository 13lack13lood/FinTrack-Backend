import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from fin_bert import stock_news_analysis


def get_finviz_headlines(stock_ticker):
    url = "https://finviz.com/quote.ashx?t=" + stock_ticker + "&p=d"

    req = Request(url=url, headers={"user-agent": "stock-app"})
    response = urlopen(req)
    html = BeautifulSoup(response, features="html.parser")

    news_table = html.find(id="news-table")

    data = []

    day = ""

    for i, row in enumerate(news_table.findAll("tr")):
        text = row.a.text
        time = row.td.text.strip()
        if " " in time:
            day = time[:time.find(" ")]

            time = time[time.find(" ") + 1:]

        link = row.find("div", {"class": "news-link-left"}).a["href"]
        publisher = row.find("div", {"class": "news-link-right"}).text.strip()[1:-1]

        data.append([day, time, text, link, publisher])

    dataframe = pd.DataFrame(data, columns=['date', 'time', 'headline', 'link', 'publisher'])

    return dataframe


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
    news = get_finviz_headlines(ticker)

    # output = stock_news_analysis(news)

    # mean_df = output[["date", "compound"]].groupby(["date"]).mean().reset_index().iloc[::-1]

    return news.to_json()  # mean_df.set_index("date").round(2).to_json()


def general_stock_news():
    news = general_stock_news_scrape()

    # output = stock_news_analysis(news)

    return news.to_json()


