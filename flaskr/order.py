import numpy as np
import pandas as pd
from datetime import datetime
from pandas import DataFrame as df
import ta
from binance.client import Client

pd.set_option('precision', 8)

client = Client()
name = 'ZENBNB'


#candles = client.get_klines(symbol=name, interval=Client.KLINE_INTERVAL_4HOUR)
#trades = client.aggregate_trade_iter(symbol=name, start_str='2 days ago UTC')

#depth = client.get_order_book(symbol='BNBBTC')
#agg_depth_list = list(depth)
#frame1 = df(agg_depth_list)
#export_csv = frame1.to_csv (r"C:\Users\Usuario\downloads\depth.csv", index = True, header=True)
#print(depth)

#trades = client.get_recent_trades(symbol='BNBBTC')
#agg_trades_list = list(trades)
#frame4 = df(agg_trades_list)
#export_csv = frame4.to_csv (r"C:\Users\Usuario\downloads\trades.csv", index = True, header=True)

#orders = client.get_all_orders(symbol='BNBBTC', limit='20')
#agg_orders_list = list(orders)
#frame5 = df(orders)
#export_csv = frame5.to_csv (r"C:\Users\Usuario\downloads\orders.csv", index = True, header=True)

#prices = client.get_all_tickers()
#agg_prices_list = list(prices)
#frame2 = df(agg_prices_list)
#export_csv = frame2.to_csv (r"C:\Users\Usuario\downloads\prices.csv", index = True, header=True)

#tickers = client.get_orderbook_tickers()
#agg_tickers_list = list(tickers)
#frame3 = df(agg_tickers_list)
#export_csv = frame3.to_csv (r"C:\Users\Usuario\downloads\tickers.csv", index = True, header=True)

