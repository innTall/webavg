import numpy as np
import pandas as pd
from datetime import datetime
from pandas import DataFrame as df
import ta
#from candles.client import Client
#pd.set_option('precision', 8)
#client = Client()
#name = 'MDABTC'
#candles = client.get_klines(symbol=name, interval=Client.KLINE_INTERVAL_4HOUR)

def get_database_candles(candles):
  frame_candles = df(candles)
  frame_date = frame_candles[0]
  final_date = []
  for time in frame_date.unique():
    readable = datetime.fromtimestamp(int(time/1000))
    final_date.append(readable)
  frame_candles = frame_candles.drop(
                  frame_candles.columns[[6, 8, 11]], axis=1)  
  frame_candles.columns = ['date', 'open', 'high', 'low', 'close',
                           'active', 'market', 'buyA', 'buy']
  frame_candles['date'] = df(final_date)
  frame_candles['open'] = round(frame_candles['open'].astype('float64'), 8)
  frame_candles['high'] = round(frame_candles['high'].astype('float64'), 8)
  frame_candles['low'] = round(frame_candles['low'].astype('float64'), 8)
  frame_candles['close'] = round(frame_candles['close'].astype('float64'), 8)
  frame_candles['market'] = round(frame_candles['market'].astype('float64'), 4)
  frame_candles['buy'] = round(frame_candles['buy'].astype('float64'), 4)
  frame_candles['active'] = round(frame_candles['active'].astype('float64'), 1)
  frame_candles['buyA'] = round(frame_candles['buyA'].astype('float64'), 1)
  
  return frame_candles
  frame_candles = get_database_candles(candles)
#export_csv = frame_candles.to_csv(
#r"C:\Users\Usuario\Downloads\frame_candles1.csv", index = True, header=True)
#print(frame_candles.info())

def get_table_basic_can(frame_candles):
  frame1c = df(frame_candles, columns=['date', 'price', 'price_d', 'open',
        'high', 'low', 'close', 'market', 'buy', 'sell', 'diff', 'perc', 'ao',
        'rsi', 'active'])
  frame1c['price'] = round((frame1c['market'] / frame1c['active']), 8)
  frame1c['sell'] = round((frame1c['market'] - frame1c['buy']), 4)
  frame1c['diff'] = round(frame1c['buy'] - frame1c['sell'], 4)
  frame1c['ao'] = ta.momentum.ao(high=frame1c['high'], low=frame1c['low'])
  frame1c['rsi'] = ta.momentum.rsi(close=frame1c['close'])
  frame1c['perc'] = round((frame1c['diff'] *100 / frame1c['market']), 2)
  
  return frame1c
  frame1c = get_table_basic_can(frame_candles)
  # export_csv = frame1c.to_csv(
  # r"C:\Users\Usuario\Downloads\frame1c.csv", index = True, header=True)
  # print(frame1c.info())

def get_pivot_table_price(frame1c):
  total = frame1c.pivot_table(['buy', 'sell', 'market', 'diff', 'perc'],
  ['price'], aggfunc='sum')
  total['perc'] = round((total['diff'] *100 / total['market']), 2)
  total1 = total[['buy', 'sell', 'market', 'diff', 'perc']].copy()
  
  return total
  total = get_pivot_table_price(frame1c)
  # export_csv = total.to_csv(
  # r"C:\Users\Usuario\Downloads\total.csv", index = True, header=True)
  # print(total.info())

def get_price_base_params(frame1c):
  last_price = round(frame1c['price'].iloc[-1], 8)
  min_price = round(min(frame1c['low']), 8)
  max_price = round(max(frame1c['high']), 8)
  aver_price = round(sum((frame1c['market']) / sum(frame1c['active'])), 8)
  # уровни сопр/подд от средней цены
  downzone = round(((aver_price - min_price) / 3), 8) # 3 зоны вниз от средней
  buy_down = min_price + downzone # нижняя бай-зона
  sell_down = aver_price - downzone # нижняя селл-зона
  upzone = round(((max_price - aver_price) / 3), 8) # 3 зоны вверх от средней
  buy_up = aver_price + upzone # верхняя бай-зона
  sell_up = max_price - upzone # верхняя селл-зона

  return (last_price, min_price, max_price, aver_price, buy_down, sell_down,
        buy_up, sell_up)
  price_params = get_price_base_params(frame1c)
  #print(price_params)

def get_scale_percent(price_params, y_ticks=15):
  (last_price, min_price, max_price, aver_price, buy_down, sell_down,
        buy_up, sell_up) = price_params
  buy_ticks = int((last_price - min_price) * y_ticks // (max_price - min_price))
  if buy_ticks < 2: buy_ticks = 2
  if buy_ticks > (y_ticks - 2): buy_ticks = (y_ticks - 2)
  sell_ticks = y_ticks - buy_ticks
  one_tick_buy = round(((
      last_price - min_price) / last_price) * 100 / (buy_ticks - 1), 2)
  one_tick_sell = round(((
      max_price - last_price) / last_price) * 100 / (sell_ticks - 1), 2)
  res_buy = list(map(lambda var: var * one_tick_buy / 100, range(buy_ticks)))
  res_sell = list(map(lambda var: var * one_tick_sell / 100, range(sell_ticks)))
  up_scale = last_price + last_price * np.array(res_sell) # вверх от текущей цены
  down_scale = last_price - last_price * np.array(res_buy) # вниз от текущей цены
  scale_percent = np.hstack((up_scale, down_scale)) # full scale

  return scale_percent
  scale_percent = get_scale_percent(price_params, y_ticks=15)
  #print(scale_percent)

def get_volume_base_params(frame1c):
  amount = len(frame1c['open'])
  first_time = frame1c['date'].iloc[0]
  last_time = frame1c['date'].iloc[-1]
  max_volume = round(max(frame1c['market']), 2)
  max_buy_vol = round(max(frame1c['buy']), 2)
  max_sell_vol = round(max(frame1c['sell']), 2)
  max_buysell_vol = max(max_buy_vol, max_sell_vol)
  aver_volume = round(sum(frame1c['market']/2/amount), 4)
  aver_percent = round(sum(frame1c['diff']) * 100 / sum(frame1c['market']), 2)
  perc_max_buy = max(frame1c['perc'])
  perc_max_sell = max(np.abs(frame1c['perc']))
  perc_buysell_max = max(perc_max_buy, perc_max_sell)

  return (amount, first_time, last_time, max_volume, max_buy_vol, max_sell_vol,
  max_buysell_vol, aver_volume, aver_percent, perc_max_buy, perc_max_sell,
  perc_buysell_max)
  volume_params = get_volume_base_params(frame1c)
  #print(volume_params) 
