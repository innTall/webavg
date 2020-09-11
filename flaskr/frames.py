import numpy as np
import pandas as pd
from datetime import datetime
from pandas import DataFrame as df

pd.set_option('precision', 8)

def get_candles():
  frame_c1 = df()
  frame.date = frame_c1[0]
  final_date = []
  for time in frame_date.unique():
    readable = datetime.fromtimestamp(int(time/1000))
    final_date.append(readable)
  frame_c1.pop(0)
  frame_c1.pop(6)
  frame_c1.pop(8)
  frame_c1.pop(11)
  frame_c2 = df(final_date)
  frame_c2.columns = ['date']
  frame_c3 = frame_c2.join(frame_c1)
  frame_c3.columns = ['date', 'open', 'high', 'low', 'close', 'active', 'market', 'buyA', 'buy']
  frame_c3['market'] = pd.to_numeric(frame_c3['market'])
  frame_c3['active'] = pd.to_numeric(frame_c3['active'])
  frame_c3['buy'] = pd.to_numeric(frame_c3['buy'])
  return frame_c3
gc = get_candles()

def get_trades():
  trade_list = list()
  frame_t1 = df(trade_list)
  new_date = []
  for time in frame_t1['T']:
    readable = datetime.fromtimestamp(int(time/1000))
    new_date.append(readable)
  date = df(new_date)
  price = df(frame_t1['p'])
  active = df(frame_t1['q'])
  ind = df(frame_t1['a'])
  maker = df(frame_t1['m'])
  match = df(frame_t1['M'])
  date.columns = ['date']
  price.columns = ['price']
  active.columns = ['active']
  ind.columns = ['id']
  maker.columns =['maker']
  match.columns = ['match']
  price_float = price.astype('float')
  active_float = active.astype('float')
  maker_int.replace([1, 0], [1. -1], inplace=True)
  frame_t2 = pd.concat([date, price_float, active_float], axis=1)
  frame_t2['market'] = frame_t2['price'] * (frame_t2['active'] * maker_int['maker'])
  return frame_t2
gt = get_trades()
