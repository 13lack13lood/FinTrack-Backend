from flask import Flask, request
from flask_cors import CORS, cross_origin
import stock_data
import general_stock_data

import stock_news

app = Flask(__name__)
cors = CORS(app)


@cross_origin()
@app.route("/", methods=["GET"])
def home():
    return {
        "response": "connected"
    }


@cross_origin()
@app.route("/quick_info/<ticker>", methods=["GET"])
def quick_info(ticker):
    data = stock_data.quick_info(ticker)
    return data


@cross_origin()
@app.route("/stock/<ticker>", methods=["GET"])
def stock_info(ticker):
    data = stock_data.get_stock(ticker)
    return data


@cross_origin()
@app.route("/history", methods=["POST"])
def stock_history():
    data = request.get_json()
    return stock_data.get_stock_history(data["ticker"], data["period"])


@cross_origin()
@app.route("/popular_stocks", methods=["GET"])
def popular_stocks():
    data = {
                "trending": general_stock_data.find_popular_stocks_preview("https://stockanalysis.com/markets/active/"),
                "gainers": general_stock_data.find_popular_stocks_preview("https://stockanalysis.com/markets/gainers/"),
                "losers": general_stock_data.find_popular_stocks_preview("https://stockanalysis.com/markets/losers/")
            }

    return data


@cross_origin()
@app.route("/popular_stocks/gainers", methods=["GET"])
def popular_stocks_gainers():
    data = {
        "data": general_stock_data.find_popular_stocks("https://stockanalysis.com/markets/gainers/"),
    }

    return data


@cross_origin()
@app.route("/popular_stocks/trending", methods=["GET"])
def popular_stocks_trending():
    data = {
        "data": general_stock_data.find_popular_stocks_active(),
    }

    return data


@cross_origin()
@app.route("/popular_stocks/losers", methods=["GET"])
def popular_stocks_losers():
    data = {
        "data": general_stock_data.find_popular_stocks("https://stockanalysis.com/markets/losers/"),
    }

    return data

@cross_origin()
@app.route("/news", methods=["GET"])
def general_news():
    return stock_news.general_stock_news()


@cross_origin()
@app.route("/index/^GSPC", methods=["GET"])
def snp500_data():
    return general_stock_data.snp500_data()


@cross_origin()
@app.route("/index/^DJI", methods=["GET"])
def dji_data():
    return general_stock_data.djia_data()


@cross_origin()
@app.route("/index/^IXIC", methods=["GET"])
def nasdaq_comp_data():
    return general_stock_data.nasdaq_comp_data()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
