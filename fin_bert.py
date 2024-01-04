import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


def finbert_analyze(headlines_list):
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

    inputs = tokenizer(headlines_list, padding=True, truncation=True, return_tensors='pt')

    outputs = model(**inputs)

    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

    positive = predictions[:, 0].tolist()
    negative = predictions[:, 1].tolist()
    neutral = predictions[:, 2].tolist()

    table = {"Positive": positive,
             "Negative": negative,
             "Neutral": neutral}

    df = pd.DataFrame(table).round(2)

    return df


def stock_news_analysis(headlines):
    finbert_df = finbert_analyze(list(headlines["headline"]))

    output = finbert_df.join(headlines)

    output["compound"] = output.apply(lambda x:
                                      0 if float(x["Neutral"]) > 0.8 or float(x["Positive"]) == float(x["Negative"])
                                      else float(x["Positive"]) if float(x["Positive"]) > float(x["Negative"])
                                      else -float(x["Negative"]), axis=1)

    return output.drop(columns=["Positive", "Negative", "Neutral"]).round(2)

