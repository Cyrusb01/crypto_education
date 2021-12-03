from time import strptime
import pandas as pd 
from datetime import datetime, timedelta
import requests 
import os
import yfinance as yf


# def daily_price_historical(symbol, comparison_symbol, all_data=True, limit=1, aggregate=1, exchange=''):
#     url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
#             .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
#     if exchange:
#         url += '&e={}'.format(exchange)
#     if all_data:
#         url += '&allData=true'
#     page = requests.get(url)
#     data = page.json()['Data']
#     df = pd.DataFrame(data)
#     df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]

#     # df_filtered = df[df['close'] != 0]
#     # df_filtered = df_filtered[df_filtered["conversionType"] == "direct"]
    
#     return df

# df = daily_price_historical("ETH", "USDT")
# print(df)


def get_crypto_price(symbol, exchange, days):
    api_key = os.getenv("CRYPTO_COMPARE")
    api_url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym='+str(symbol)+'&tsym='+str(exchange)+'&limit='+str(days)+'&api_key='+str(api_key)
    raw = requests.get(api_url).json()
    df = pd.DataFrame(raw['Data']['Data'])[['time', 'high', 'low', 'open']].set_index('time')
    df.index = pd.to_datetime(df.index, unit = 's')
    df = df[df['open'] != 0]
    
    
    df = pd.DataFrame(df["open"])
    df.rename(columns={"open": symbol}, inplace= True)
    
    return df

df = get_crypto_price("ADA", "USD", 2000)
# print(df)

def get_stock_price(symbol):


    today = datetime.now()
    # print(now)
    today = today.strftime('%Y-%m-%d')
    start = datetime.fromisoformat(today) - timedelta(1000)
    start = start.strftime('%Y-%m-%d')
    
    # print(now_wo_seconds)
    

    df = yf.download(symbol, start= start, end= today)

    df = pd.DataFrame(df["Open"])
    df.rename(columns={"Open": symbol}, inplace= True)
    return df


# print(get_stock_price("AAPL"))

def pandas_to_highcharts(df):
    df.index = [t.value // 10 ** 6 for t in df.index]
    json_dict = {}
    for key, value in df.items():
        # print("main")
        json_dict["name"] = key
        data_list = []
        for i in range(len(value.index)):
            temp = [int(value.index[i]), float(value.values[i])]
            # print(value.index[0], " , ", value.values[0])
            data_list.append(temp)
        json_dict["data"] = data_list
    
    return [json_dict]


def get_prices(df, name):
    for i in range(len(df)):
        if i == 0:
            df[name][i] = 100
        else:
            df[name][i] = df[name][i-1] * ( 1 + df[name][i])
    
    return df