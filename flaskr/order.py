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

'''
def convert(btc_dict, eth_base, bnb_base, usdt_base):
  
  if isinstance(btc_dict, (list, tuple)):
    return [convert(i) for i in btc_dict]
  elif isinstance(btc_dict, dict):
    _, values = zip(*sorted(btc_dict.items()))  
    return convert(values)
  return btc_dict
  btcf = convert(btc_dict, eth_base, bnb_base, usdt_base)

  if isinstance(eth_base, (list, tuple)):
    return [convert(i) for i in eth_base]
  elif isinstance(eth_base, dict):
    _, values = zip(*sorted(eth_base.items()))  
    return convert(values)
  return eth_base
  ethf = convert(btc_dict, eth_base, bnb_base, usdt_base)

  if isinstance(bnb_base, (list, tuple)):
    return [convert(i) for i in bnb_base]
  elif isinstance(bnb_base, dict):
    _, values = zip(*sorted(bnb_base.items()))  
    return convert(values)
  return bnb_base
  bnbf = convert(btc_dict, eth_base, bnb_base, usdt_base)

  usdt_base = [{'symbol': name_usdt, 'quoteAsset': name_quote, 'baseAsset': name_base}]
  if isinstance(usdt_base, (list, tuple)):
    return [convert(i) for i in usdt_base]
  elif isinstance(usdt_base, dict):
    _, values = zip(*sorted(usdt_base.items()))  
    return convert(values)
  return usdt_base
  usdtf = convert(btc_dict, eth_base, bnb_base, usdt_base)

  #btcf, ethf, bnbf, usdtf = convert(btc_base, eth_base, bnb_base, usdt_base)
  print(json.dumps(convert(btcf, ethf, bnbf, usdtf)))

#new_dict = {}
#for i in keys:
#    new_dict[i] = []
#    for j in values:
#      if i in j:
#        new_dict[i].append(j)
#lst1 = ['wer12', 'rtgdf12', 'werfd12']
#lst1 = [str[:-2] for str in lst1]
#print(lst1)

#a = 'abccomputer.com'
#res = a.split('.com',1)[0]

#import re
#rm_sub('abcdc.me','.me')
#'abcdc'

#Я бы сделал регулярным выражением. Например строка mystr выглядит вот так asdw#df%mm!@* и надо удалить символы #%!@*, тогда
#mystr = re.sub(r"[#%!@*]", "", mystr)

#Если символов немного, на мой взгляд наиболее читабельный вариант:
#text.replace('#','').replace('@','').replace('!','')

#как из строки убрать все символы 'b':
#''.join(list(filter(lambda c: c!='b', 'abasfdbbbadfbg')))

#Удаление подстроки осуществляется заменой подстроки на пустую строку:
#'Bob was eating tasty plum'.replace('tasty', '')
#'Bob was eating plum'

#s = 'abc<def*gh?ikl'
#s.translate(None, '\/:*?"<>|')
#'abcdefghikl'


#export_csv = frame.to_csv (r"C:\Users\Usuario\downloads\prices.csv", index = True, header=True)
#btc = [{'symbol': 'ETHBTC', 'quoteAsset': 'ETH', 'baseAsset': 'BTC'}]
'''