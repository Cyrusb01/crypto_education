from flask import Flask, request, render_template
import yfinance as yf
from pandas_highcharts.core import serialize
import json
import pandas as pd
from helpers import pandas_to_highcharts
from newsapi import NewsApiClient
import os


app = Flask(__name__)


@app.route("/")
@app.route("/home")
def index():

    return render_template("index.html")


@app.route("/btcgold")
def btcgold():
    return render_template("btc_gold.html")


@app.route("/learning")
def learning():
    return render_template("tickerlearning.html")


@app.route("/research", methods=["GET", "POST"])
def research():
    ticker = "BTC"
    if request.method == "POST":
        ticker = request.form["ticker"]

    ticker_df = pd.read_csv("Coins.csv")
    ticker_df = ticker_df.set_index("Tickers")
    # print(ticker_df)

    ticker = ticker.upper()
    coin_name = ticker_df.loc[ticker]["Name"]
    coin_link = ticker_df.loc[ticker]["Link"]
    coin_logo = ticker_df.loc[ticker]["Logo"]
    coin_description = ticker_df.loc[ticker]["Description"]

    title = {"text": ticker}
    chartID = "chart_ID"

    # Downloading the data
    data = yf.download(ticker + "-USD", start="2017-01-01", end="2021-11-01")
    df = pd.DataFrame(data)
    df = df[["Close"]]
    json_dict = pandas_to_highcharts(df)

    # TESTING - Z
    print(df.iloc[-1])
    # END TESTING

    ##################################################### GET NEWS ##########################################################
    news_api_key = os.getenv("NEWS_API_KEY")
    # print(news_api_key)
    newsapi = NewsApiClient(api_key=news_api_key)
    sources = newsapi.get_sources()
    top_headlines = newsapi.get_everything(
        q=ticker,
        #   sources='bbc-news,the-verge',
        #   category='business',
        language="en",
        #   country='us',
        from_param="2021-11-01",
        to="2021-11-10",
        sort_by="relevancy",
        #   page = 1
    )
    sources = []
    headlines = []
    urls = []
    for i in range(3):
        article = top_headlines["articles"][i]

        sources.append(article["source"]["name"])
        headlines.append(article["title"])
        urls.append(article["url"])
    print(urls[2])
    if request.method == "POST":
        return render_template(
            "tickerlearning.html",
            ticker=ticker,
            title=title,
            chartID=chartID,
            data=json_dict,
            coin_name=coin_name,
            coin_description=coin_description,
            source1 = sources[0],
            headline1 = headlines[0],
            url1 = urls[0],
            source2 = sources[1],
            headline2 = headlines[1],
            url2 = urls[1],
            source3 = sources[2],
            headline3  = headlines[2],
            url3 = urls[2]
        )
        
    else:
        return render_template(
            "research.html", ticker=ticker, title=title, chartID=chartID, data=json_dict
        )

@app.route('/portfolio', methods= ['GET', 'POST'])
def portfolio():
    lastPrice = 0
    if request.method == 'POST':
        ticker = request.form.get("add_ticker")
        tickeryf = yf.Ticker( ticker + "-USD" )
        data = tickeryf.history()
        lastPrice = (data.tail(1)['Close'].iloc[0])
        #print( ticker, lastPrice )
        chartID = "chart_ID"
        data = yf.download(ticker + "-USD", start="2017-01-01", end="2021-11-01")
        df = pd.DataFrame(data)
        df = df[["Close"]]
        json_dict = pandas_to_highcharts(df)

        return (str( lastPrice ))


    # Update table on page with data from "tickers" array
    # Update graph on page with "tickers"
    return render_template("portfolio.html")




@app.route("/form", methods=["GET", "POST"])
def form():
    name = app.form["Name"]
    print(name)
    return render_template("form.html")


# @app.route('/h')
# def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 1000):
# 	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
# 	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]

# 	xAxis = {"categories": [1, 2, 3]}
# 	yAxis = {"title": {"text": 'yAxis Label'}}
# 	return render_template('highchart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)


@app.route("/h")
def high():
    title = {"text": "My Title"}
    chartID = "chart_ID"
    msft = yf.download("MSFT", start="2017-01-01", end="2017-01-30")
    df = pd.DataFrame(msft)
    df = df[["Close"]]

    json_dict = pandas_to_highcharts(df)

    return render_template(
        "highchart.html", title=title, chartID=chartID, data=json_dict
    )


if __name__ == "__main__":

    app.run(debug=True, passthrough_errors=True)
