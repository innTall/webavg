import numpy as np
import pandas as pd
from pandas import DataFrame as df
#from binance.client import Client

#client = Client()
#prices = client.get_all_tickers()

def get_pairs(prices):
  agg_prices_list = list(prices)
  frame = df(agg_prices_list)
  symbols = frame['symbol']

  btc=[]
  eth=[]
  bnb=[]
  usdt=[]
  for symbol in symbols:
    if symbol[-3:] == 'BTC':
      btc.append(symbol)
    elif symbol[-3:] == 'ETH':
      eth.append(symbol)
    elif symbol[-3:] == 'BNB':
      bnb.append(symbol)
    elif symbol[-4:] == 'USDT':
      usdt.append(symbol)

  return (btc, eth, bnb, usdt)
  (btc, eth, bnb, usdt) = get_cryptos(prices)