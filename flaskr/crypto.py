import numpy as np
import pandas as pd
from datetime import datetime
from pandas import DataFrame as df
import ta
from binance.client import Client

client = Client()
#name = 'ZENBNB'

prices = client.get_all_tickers()
agg_prices_list = list(prices)
frame = df(agg_prices_list)
#export_csv = frame.to_csv (r"C:\Users\Usuario\downloads\prices.csv", index = True, header=True)
symbols = frame['symbol']

btc=[]
for symbol in symbols:
  if symbol[-3:] == 'BTC':
    btc.append(symbol)
    #print(btc)

eth=[]
for symbol in symbols:
  if symbol[-3:] == 'ETH':
    eth.append(symbol)
    #print(eth)

bnb=[]
for symbol in symbols:
  if symbol[-3:] == 'BNB':
    bnb.append(symbol)
    #print(bnb)

usdt=[]
for symbol in symbols:
  if symbol[-4:] == 'USDT':
    usdt.append(symbol)
    #print(usdt) 
print(btc, eth, bnb, usdt)