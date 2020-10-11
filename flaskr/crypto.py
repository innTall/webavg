import numpy as np
import pandas as pd
from datetime import datetime
from pandas import DataFrame as df
import ta
import json
#from binance.client import Client

#client = Client()

#prices = client.get_all_tickers()
def get_crypto(prices):
  agg_prices_list = list(prices)
  frame = df(agg_prices_list)
  symbols = frame['symbol']

  btc_b=[]
  name_quote=[]
  name_base=[]
  for symbol in symbols:
    if symbol[-3:] == 'BTC':
      btc_b.append(symbol)
  name_btc = btc_b
  name_quote = btc_b
  name_quote = [str[:-3] for str in name_quote] #btc_base = dict(zip(keys, values))
  name_base = btc_b
  name_base = [str[-3:] for str in name_base] # print(btc_base)
  keys = ('symbol', 'quoteAsset', 'baseAsset')
  values = (name_btc, name_quote, name_base)
  btc_base = [{key: value for key, value in zip(keys, values)}]
  # btc_base = {'symbol': name_btc, 'quoteAsset': name_quote, 'baseAsset': name_base}
  btc_frame = pd.DataFrame(btc_base)
    
  eth_e=[]
  name_quote=[]
  name_base=[]
  for symbol in symbols:
    if symbol[-3:] == 'ETH':
      eth_e.append(symbol)
  name_eth = eth_e
  name_quote = eth_e
  name_quote = [str[:-3] for str in name_quote]
  name_base = eth_e
  name_base = [str[-3:] for str in name_base]
  eth_base = [{'symbol': name_eth, 'quoteAsset': name_quote, 'baseAsset': name_base}]
  #  print(eth_base)
  
  bnb_bn=[]
  name_quote=[]
  name_base=[]
  for symbol in symbols:
    if symbol[-3:] == 'BNB':
      bnb_bn.append(symbol)
  name_bnb = bnb_bn
  name_quote = bnb_bn
  name_quote = [str[:-3] for str in name_quote]
  name_base = bnb_bn
  name_base = [str[-3:] for str in name_base]
  bnb_base = [{'symbol': name_bnb, 'quoteAsset': name_quote, 'baseAsset': name_base}]
  #  print(bnb_base)
  
  usdt_u=[]
  name_quote=[]
  name_base=[]
  for symbol in symbols:
    if symbol[-4:] == 'USDT':
      usdt_u.append(symbol)
  name_usdt = usdt_u
  name_quote = usdt_u
  name_quote = [str[:-4] for str in name_quote]
  name_base = usdt_u
  name_base = [str[-4:] for str in name_base]
  usdt_base = [{'symbol': name_usdt, 'quoteAsset': name_quote, 'baseAsset': name_base}]
  
  return btc_base, btc_frame, eth_base, bnb_base, usdt_base
  btc_dict, btcf, eth_dict, bnb_dict, usdt_dict = get_crypto(prices)
  print(btcf)
  #print(btc_dict, eth_dict, bnb_dict, usdt_dict)
  #json.dumps(btc_dict, eth_dict, bnb_dict, usdt_dict)
