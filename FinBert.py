import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# headlines_df = pd.read_csv('test_data.csv')
# print(headlines_df.head(10))
#
# headlines_array = np.array(headlines_df)
# np.random.shuffle(headlines_array)
# headlines_list = list(headlines_array[:, 1])


def finbert_analyze(headlines_list):
    print(headlines_list)

    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    inputs = tokenizer(headlines_list, padding=True, truncation=True, return_tensors='pt')

    outputs = model(**inputs)
    print(outputs.logits.shape)

    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

    positive = predictions[:, 0].tolist()
    negative = predictions[:, 1].tolist()
    neutral = predictions[:, 2].tolist()

    table = {"Positive": positive,
             "Negative": negative,
             "Neutral": neutral}

    df = pd.DataFrame(table)

    print(df.to_numpy())

    return df


def stock_news_analysis(stock_ticker):
    # URL for news
    url = "https://finviz.com/quote.ashx?t=" + stock_ticker

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
        data.append([day, time, text])

    dataframe = pd.DataFrame(data, columns=['date', 'time', 'text'])

    finbert_df = finbert_analyze(list(dataframe["text"]))

    output = dataframe.join(finbert_df)

    output["compound"] = output.apply(lambda x: 0 if float(x["Neutral"]) > 0.8 or float(x["Positive"]) == float(x["Negative"]) else float(x["Positive"]) if float(x["Positive"]) > float(x["Negative"]) else -float(x["Negative"]), axis=1)

    mean_df = output[["date", "compound"]].groupby(["date"]).mean().reset_index().iloc[::-1]

    return output, mean_df


stock_news_analysis("AAPL")

