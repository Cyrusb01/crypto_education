from flask import Flask, request, render_template
import yfinance as yf
from pandas_highcharts.core import serialize
import json 
import pandas as pd 
from helpers import pandas_to_highcharts
from newsapi import NewsApiClient
import os 


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def index():
    news_api_key = os.getenv("NEWS_API_KEY")
    print(news_api_key)
    newsapi = NewsApiClient(api_key=news_api_key)
    sources = newsapi.get_sources()
    top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                        #   sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')
    print(top_headlines)
    return render_template('index.html')


@app.route('/btcgold')
def btcgold():
    return render_template('btc_gold.html')

@app.route('/learning')
def learning():
    return render_template('tickerlearning.html')

@app.route('/research', methods = ['GET', 'POST'])
def research():
    ticker = "BTC"
    if request.method == 'POST':
        ticker = request.form["ticker"]
        print(ticker)
    title = {"text": 'My Title'}
    chartID = "chart_ID"
    msft = yf.download(ticker+"-USD", start="2017-01-01", end="2021-11-01")
    df = pd.DataFrame(msft)
    df = df[['Close']]
    
    json_dict = pandas_to_highcharts(df)


    return render_template('research.html', ticker = ticker, title = title, chartID=chartID, data = json_dict)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/form', methods = ['GET', 'POST'])
def form():
    name = request.form["Name"]
    print(name)
    return render_template('form.html')

# @app.route('/h')
# def graph(chartID = 'chart_ID', chart_type = 'line', chart_height = 1000):
# 	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
# 	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
	
# 	xAxis = {"categories": [1, 2, 3]}
# 	yAxis = {"title": {"text": 'yAxis Label'}}
# 	return render_template('highchart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

@app.route('/h')
def high():
    title = {"text": 'My Title'}
    chartID = "chart_ID"
    msft = yf.download("MSFT", start="2017-01-01", end="2017-01-30")
    df = pd.DataFrame(msft)
    df = df[['Close']]
    
    json_dict = pandas_to_highcharts(df)
    
    
    # json_data = [{'data': list(value.values), 'name': key} for key, value in df.items()]
    # json_data = df.to_json()
    # print(json_dict)
    # json_data = dict(json_data)
    # print(type(json_data))
    # for key in json_data["Close"].keys():
    #     print(key)
        # temp = [float(key), float(json_data["Close"][key])]
        # data_list.append(temp)
        
    return render_template('highchart.html', title = title, chartID=chartID, data = json_dict)

if __name__ == "__main__":

    
	app.run(debug = True, passthrough_errors=True) 