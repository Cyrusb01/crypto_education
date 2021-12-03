from flask import Flask, request, render_template, make_response
from quantstats.utils import make_portfolio
import yfinance as yf
from pandas_highcharts.core import serialize
import json
import pandas as pd
from helpers import pandas_to_highcharts, get_crypto_price, get_stock_price, get_prices
from newsapi import NewsApiClient
import os
import quantstats as qs 
import bt
qs.extend_pandas()

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

        ################################## FIND COIN NAME/INFO ############################################
        ticker_df = pd.read_csv("Coins.csv")
        ticker_df = ticker_df.set_index("Tickers")
        # print(ticker_df)

        ticker = ticker.upper()
        coin_name = ticker_df.loc[ticker]["Name"]
        coin_link = ticker_df.loc[ticker]["Link"]
        coin_logo = ticker_df.loc[ticker]["Logo"]
        coin_description = ticker_df.loc[ticker]["Description"]

        

        ################################## DOWNLOAD DATA ####################################################
        data = yf.download(ticker + "-USD", start="2017-01-01", end="2021-11-01")
        df = pd.DataFrame(data)
        df = df[["Close"]]
        df.columns = [ticker]
        json_dict = pandas_to_highcharts(df)

        ##################################################### GET NEWS ##########################################################
        news_api_key = os.getenv("NEWS_API_KEY")
        newsapi = NewsApiClient(api_key=news_api_key)
        sources = newsapi.get_sources()
        top_headlines = newsapi.get_everything(
            q=ticker,
            sources='decrypt,bloomberg,forbes,the-block,coindesk,google-news',
            #   category='business',
            language="en",
            #   country='us',
            from_param="2021-11-20",
            to="2021-12-03",
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
    
    ############################################### SEND REQUESTS #############################################################
    title = {"text": ticker}
    chartID = "chart_ID"
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
            url3 = urls[2],
            logo = coin_logo,
            link = coin_link
        )
        
    else:
        data_series = []
        data = yf.download("BTC-USD", start="2017-01-01", end="2021-11-01")
        df = pd.DataFrame(data)
        df = df[["Close"]]
        df.columns = ["Bitcoin"]
        df = df.pct_change()
        df = get_prices(df, "Bitcoin")
        btc_ret = "$" + str(round(df.iloc[-1]["Bitcoin"]))
        print(type(btc_ret))
        data_series += pandas_to_highcharts(df)
        #gold 
        data = yf.download("GLD", start="2017-01-01", end="2021-11-01")
        df = pd.DataFrame(data)
        df = df[["Close"]]
        df.columns = ["Gold"]
        df = df.pct_change()
        df = get_prices(df, "Gold")
        gld_ret = "$" + str(round(df.iloc[-1]["Gold"]))
        data_series += pandas_to_highcharts(df)

        
        return render_template(
            "research.html", ticker=ticker, title=title, chartID=chartID, data=data_series, btc_ret = btc_ret, gld_ret = gld_ret
        )




tickers = []
allocations = []
@app.route('/portfolio', methods= ['GET', 'POST'])
def portfolio():
    lastPrice = 0
    global tickers
    global allocations

    # tickers = ["BTC", "ETH", "AAPL"]
    # allocations = [.40, .30, .30]
    df = pd.DataFrame()
    series = []
    scatter = []
    hello = 0
    # if request.method == 'POST':
    if True:
        # if request.form['submitbutton'] == "reset":

        if hello == 1:
            tickers = []
            allocations = []
        else:
            try:
                hi
                ticker = request.form["add_ticker"]
                tickers.append(ticker)
                print(tickers)

                allocation = request.form["add_allocation"]
                allocation = float(allocation)/100
                allocations.append(allocation)
            except:
                tickers = ["AAPL", "MSFT"]
                data_tickers = ["AAPL", "MSFT", "BTC", "ETH"]
                allocations = [.5, .5]

        data_tickers = tickers.copy()
        if "BTC" not in data_tickers:
            data_tickers.append("BTC")
            data_tickers.append("ETH")
            data_tickers.append("BNB")
            data_tickers.append("ADA")
            # data_tickers.append("XRP")
        
        #get Data for these

        data = pd.DataFrame()
        for ticker in data_tickers: 
            got_data = True
            try: #Try and get crypto data 
                df = get_crypto_price(ticker, "USD", 1000)
            except: #either not a crypto or dont have data for it
                try:
                    df = get_stock_price(ticker)
                    
                except:
                    got_data = False
            if(not got_data):
                print(ticker, "FAILED")
                #RETURN ERROR MESSAGE HERE 
            else:
                try:
                    data = data.join(df, how="outer")
                except:
                    print("error")
        data = data.dropna()
            
        series = []
        if len(tickers) != 0:
            series = []
            
            #Make portfolio for user strategy
            
            stock_dic = {tickers[i]: allocations[i] for i in range(len(tickers))}
            print(stock_dic)
            # control = qs.utils.make_index(stock_dic, returns=data, rebalance="1Q")
            # df = pd.DataFrame(control)
            # df.columns = ["Your Strategy"]
            # df = get_prices(df, "Your Strategy")
            strategy_ = bt.Strategy(
                    "Your Portfolio",
                    [
                        bt.algos.RunOnce(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighSpecified(**stock_dic),
                        bt.algos.Rebalance(),
                    ],
            )

            test = bt.Backtest(strategy_, data)
            results = bt.run(test)

            #This is the series data 
            df = results._get_series(None).rebase()
            print(df)

            # print(df)
            series += pandas_to_highcharts(df)

            # print(df)
            

            print(data)
            #Generate three different portfolios

            #conservative one = 3% into BTC 
            if ("BTC" not in tickers):
                conserv_tickers = tickers.copy()
                conserv_tickers.append("BTC")
                new_alloc = allocations.copy()
                new_alloc = [(x*100-(x*100)*.03)/100 for x in new_alloc]
                new_alloc.append(.03)
                print("Light")
                # print(new_alloc)
                stock_dic = {conserv_tickers[i]: new_alloc[i] for i in range(len(conserv_tickers))}
                print(stock_dic)
                # conserv = qs.utils.make_index(stock_dic, returns = data, rebalance="1Q")

                strategy_ = bt.Strategy(
                    "Light Crypto",
                    [
                        bt.algos.RunOnce(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighSpecified(**stock_dic),
                        bt.algos.Rebalance(),
                    ],
                )

                test = bt.Backtest(strategy_, data)
                results = bt.run(test)

                #This is the series data 
                df_conserv = results._get_series(None).rebase()
                print(df_conserv)


                # df_conserv = pd.DataFrame(conserv)
                df_conserv.columns = ["Light Crypto"]
                # print(df_conserv)
                # df_conserv = get_prices(df_conserv, "Light Crypto")
                series += pandas_to_highcharts(df_conserv)
                # print(df_conserv)
            else:
                conserv_tickers = tickers.copy()
                # conserv_tickers.append("BTC")
                new_alloc = allocations.copy()
                new_alloc = [x-(x*100)*.03 for x in new_alloc]

                new_alloc[conserv_tickers.index("BTC")] += .03
                # new_alloc.append(.03)
                
                stock_dic = {conserv_tickers[i]: new_alloc[i] for i in range(len(conserv_tickers))}
                conserv = qs.utils.make_index(stock_dic, returns = data, rebalance="1Q")

                df_conserv = pd.DataFrame(conserv)
                df_conserv.columns = ["Light Crypto"]
                df_conserv = get_prices(df_conserv, "Light Crypto")
                series += pandas_to_highcharts(df_conserv)
                # print(df_conserv)

            #More involved = 3% BTC 3% ETH
            if ("BTC" not in tickers):
                medium_tickers = tickers.copy()
                medium_tickers.append("BTC")
                medium_tickers.append("ETH")
                new_alloc = allocations.copy()
                new_alloc = [(x*100-(x*100)*.06)/100 for x in new_alloc]
                new_alloc.append(.03)
                new_alloc.append(.03)
                print("Medium")
                # new_alloc = [45, 45, 5, 5]
                # print(new_alloc)
                
                stock_dic = {medium_tickers[i]: new_alloc[i] for i in range(len(medium_tickers))}
                print(stock_dic)
                # medium = qs.utils.make_index(stock_dic, returns = data, rebalance="1Q")
                strategy_ = bt.Strategy(
                    "Medium Crypto",
                    [
                        bt.algos.RunOnce(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighSpecified(**stock_dic),
                        bt.algos.Rebalance(),
                    ],
                )

                test = bt.Backtest(strategy_, data)
                results = bt.run(test)

                #This is the series data 
                df_medium = results._get_series(None).rebase()

                # df_medium = pd.DataFrame(medium)
                # df_medium.columns = ["Medium Crypto"]
                # df_medium = get_prices(df_medium, "Medium Crypto")
                series += pandas_to_highcharts(df_medium)
                print(df_medium)

            #Very risky = 2% BTC 2% ETH 2% BNB 2% ADA 2% XRP
            if ("BTC" not in tickers):
                heavy_tickers = tickers.copy()
                heavy_tickers.append("BTC")
                heavy_tickers.append("ETH")
                heavy_tickers.append("BNB")
                heavy_tickers.append("ADA")
                # heavy_tickers.append("XRP")
                new_alloc = allocations.copy()
                print(new_alloc)
                new_alloc = [(x*100-(x*100)*.1)/100 for x in new_alloc]
                new_alloc.append(.025)
                new_alloc.append(.025)
                new_alloc.append(.025)
                new_alloc.append(.025)
                # new_alloc.append(.02)
                print("Heavy")
                # print(new_alloc)
                stock_dic = {heavy_tickers[i]: new_alloc[i] for i in range(len(heavy_tickers))}
                print(stock_dic)
                # heavy = qs.utils.make_index(stock_dic, returns = data, rebalance="1Q")
                strategy_ = bt.Strategy(
                    "Agressive Crypto",
                    [
                        bt.algos.RunOnce(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighSpecified(**stock_dic),
                        bt.algos.Rebalance(),
                    ],
                )

                test = bt.Backtest(strategy_, data)
                results = bt.run(test)

                #This is the series data 
                df_heavy = results._get_series(None).rebase()

                # df_heavy = pd.DataFrame(heavy)
                # df_heavy.columns = ["Agressive Crypto"]
                # df_heavy = get_prices(df_heavy, "Agressive Crypto")
                series += pandas_to_highcharts(df_heavy)
                print(df_heavy)
            

            ####################################### SCATTER PLOT ########################################################
            df = df.pct_change()
            df.index = pd.to_datetime(df.index, unit = 'ms')
            port_return = df.cagr()
            port_volatility = df.volatility()
            
            df_conserv = df_conserv.pct_change()
            df_conserv.index = pd.to_datetime(df_conserv.index, unit = 'ms')
            conserv_return = df_conserv.cagr()
            conserv_volatility = df_conserv.volatility()

            df_medium = df_medium.pct_change()
            df_medium.index = pd.to_datetime(df_medium.index, unit = 'ms')
            medium_return = df_medium.cagr()
            medium_volatility = df_medium.volatility()

            df_heavy = df_heavy.pct_change()
            df_heavy.index = pd.to_datetime(df_heavy.index, unit = 'ms')
            heavy_return = df_heavy.cagr()
            heavy_volatility = df_heavy.volatility()
            
            scatter = [["Your Portfolio", port_return[0]*100, port_volatility[0]*100], ["Light Crypto", conserv_return[0]*100, conserv_volatility[0]*100], ["Medium Crypto", medium_return[0]*100, medium_volatility[0]*100], ["Agressive Crypto", heavy_return[0]*100, heavy_volatility[0]*100]] 

            
            
            ###################################### STATS ####################################################################
            metrics = qs.reports.metrics(df,  display = False)
            metrics_l = qs.reports.metrics(df_conserv,  display = False)
            metrics_m = qs.reports.metrics(df,  display = False)
            metrics_h = qs.reports.metrics(df,  display = False)
            bad_formatted = ["Risk-Free Rate ", "Time in Market ", "Cumulative Return ", "CAGR﹪", "Max Drawdown ", "MTD ", "3M ", "6M ", "YTD ", "1Y ", "3Y (ann.) ", "5Y (ann.) ", "10Y (ann.) ", "All-time (ann.) ", "Avg. Drawdown "]

            for stat in bad_formatted:
                try:
                    metrics.loc[stat]["Strategy"] = str(round(float(str(metrics.loc[stat]["Strategy"]).replace(",", ""))  * 100, 1)) + "%"
                except:
                    h = 9
                try:
                    metrics_l.loc[stat]["Strategy"] = str(round(float(str(metrics_l.loc[stat]["Strategy"]).replace(",", ""))  * 100, 1)) + "%"
                except:
                    h = 9
                try:
                    metrics_m.loc[stat]["Strategy"] = str(round(float(str(metrics.loc[stat]["Strategy"]).replace(",", ""))  * 100, 1)) + "%"
                except:
                    h = 9
                try:
                    metrics_h.loc[stat]["Strategy"] = str(round(float(str(metrics.loc[stat]["Strategy"]).replace(",", ""))  * 100, 1)) + "%"
                except:
                    h = 9
                

            # metrics.columns = ["Your Portfolio"]
            # metrics_l.columns = ["Light Crypto"]
            # print(metrics.index)
            stats = [metrics, metrics_l, metrics_m, metrics_h]
            things = ["Cumulative Return ", "Sortino", "Sharpe", "Max Drawdown ", "Recovery Factor", "Serenity Index"]
            stat_table = []
            for thing in things:
                for metric in stats:
                    stat_table.append(metric.loc[thing]["Strategy"])

            print(stat_table)


            

    table_list = []
    for i in range(len(tickers)):
        temp = [tickers[i], str(allocations[i]) + "%"]
        table_list.append(temp)
    print(table_list)
    # json_dict = pandas_to_highcharts(df)
    print(scatter)
    title = {"text": "Compare Portfolios"}
    chartID = "chart_ID"
    return render_template("portfolio.html", tickers = table_list, title=title, chartID=chartID, data=series, scatterplotlist = scatter, stats = stat_table)




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


@app.route("/faq")
def faq():
    return render_template("faq.html")

if __name__ == "__main__":

    app.run(debug=True, passthrough_errors=True)
