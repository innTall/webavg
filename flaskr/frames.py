import numpy as np
import pandas as pd
from datetime import datetime
from pandas import DataFrame as df
import ta
#from binance.client import Client

pd.set_option('precision', 8)

#client = Client()
#name = 'ZENBNB'

#candles = client.get_klines(symbol=name, interval=Client.KLINE_INTERVAL_4HOUR)
#trades = client.aggregate_trade_iter(symbol=name, start_str='2 days ago UTC')

def get_candles(candles, y_ticks=15):
  frame1c = df(candles)
  frame_date = frame1c[0]
  final_date = []
  for time in frame_date.unique():
    readable = datetime.fromtimestamp(int(time/1000))
    final_date.append(readable)
  frame1c = frame1c.drop(frame1c.columns[[6, 8, 11]], axis=1)
  frame1c.columns = ['date', 'open', 'high', 'low', 'close',
                    'active', 'market', 'buyA', 'buy']
  frame1c['date'] = df(final_date)
  frame1c['high'] = pd.to_numeric(frame1c['high'])
  frame1c['low'] = pd.to_numeric(frame1c['low'])
  frame1c['close'] = pd.to_numeric(frame1c['close'])
  frame1c['active'] = pd.to_numeric(frame1c['active'])
  frame1c['market'] = round(pd.to_numeric(frame1c['market']), 4)
  frame1c['buy'] = round(pd.to_numeric(frame1c['buy']), 4)
  frame2c = df(frame1c, columns=['date', 'price', 'open', 'high', 'low',
               'close', 'active', 'market', 'buy', 'sell', 'diff', 'perc', 'ao', 'rsi'])
  frame2c['price'] = round((frame2c['market'] / frame2c['active']), 8)
  frame2c['sell'] = round((frame2c['market'] - frame2c['buy']), 4)
  frame2c['diff'] = round(frame2c['buy'] - frame2c['sell'], 4)
  frame2c['ao'] = ta.momentum.ao(high=frame2c['high'], low=frame2c['low'])
  frame2c['rsi'] = ta.momentum.rsi(close=frame2c['close'])
  frame2c['perc'] = round((frame2c['diff'] *100 / frame2c['market']), 2)
  total = frame2c.pivot_table(['buy', 'sell', 'market', 'diff', 'perc'], ['price'], aggfunc='sum')
  total['perc'] = round((total['diff'] *100 / total['market']), 2)
  total1 = total[['buy', 'sell', 'market', 'diff', 'perc']].copy()
  # основные параметры цены
  last_price = round(frame2c['price'].iloc[-1], 8)
  min_price = round(min(frame2c['low']), 8)
  max_price = round(max(frame2c['high']), 8)
  aver_price = round(sum((frame2c['market']) / sum(frame2c['active'])), 8)
  # расчет процентной шкалы цен
  buy_ticks = int((last_price - min_price) * y_ticks // (max_price - min_price))
  if buy_ticks < 2: buy_ticks = 2
  if buy_ticks > (y_ticks - 2): buy_ticks = (y_ticks - 2)
  sell_ticks = y_ticks - buy_ticks
  one_tick_buy = round(((last_price - min_price) / last_price) * 100 / (buy_ticks - 1), 2)
  one_tick_sell = round(((max_price - last_price) / last_price) * 100 / (sell_ticks - 1), 2)
  res_buy = list(map(lambda var: var * one_tick_buy / 100, range(buy_ticks))) # расчет вниз
  res_sell = list(map(lambda var: var * one_tick_sell / 100, range(sell_ticks))) # расчет вверх
  up_scale = last_price + last_price * np.array(res_sell) # процентная шкала вверх от текущей цены
  down_scale = last_price - last_price * np.array(res_buy) # процентная шкала вниз от текущей цены
  scale_percent = np.hstack((up_scale, down_scale)) # создание массива perc значений
  # уровни сопр/подд от средней цены
  downzone = round(((aver_price - min_price) / 3), 8) # 3 зоны вниз от средней
  buy_down = min_price + downzone # нижняя бай-зона
  sell_down = aver_price - downzone # нижняя селл-зона
  upzone = round(((max_price - aver_price) / 3), 8) # 3 зоны вверх от средней
  buy_up = aver_price + upzone # верхняя бай-зона
  sell_up = max_price - upzone # верхняя селл-зона
  # общие данные по объемам сделок
  amount = len(frame2c['open'])
  first_time = frame2c['date'].iloc[0]
  last_time = frame2c['date'].iloc[-1]
  max_volume = round(max(frame2c['market']), 2)
  max_buy_vol = round(max(frame2c['buy']), 2)
  max_sell_vol = round(max(frame2c['sell']), 2)
  max_buysell_vol = max(max_buy_vol, max_sell_vol) # макс значение объема (бай/селл)
  aver_volume = round(sum(frame2c['market']/2/amount), 4) # среднее значение бай/селл объемов за период
  aver_percent = round(sum(frame2c['diff']) * 100 / sum(frame2c['market']), 2)
  perc_max_buy = max(frame2c['perc'])
  perc_max_sell = max(np.abs(frame2c['perc']))
  perc_buysell_max = max(perc_max_buy, perc_max_sell)
  
  return [frame2c, total, last_price, min_price, max_price, aver_price, scale_percent,
  buy_down, sell_down, buy_up, sell_up, amount, first_time, last_time, max_volume,
  max_buy_vol, max_sell_vol, max_buysell_vol, aver_volume, aver_percent, perc_max_buy,
  perc_max_sell, perc_buysell_max]

  [f2c, pivtab1, lastpc, mic, mac, avc, perscalec, buyd, selld, buyu, sellu, nums, ft, lt,
  volmax, volmab, volmas, volbs, volav, averperc, percmab, percmas, percmabs] = get_candles(candles, y_ticks=15)
  #export_csv = f5c.to_csv (r"C:\Users\Usuario\downloads\f5c.csv", index = True, header=True)

def get_trades(trades, y_ticks=15, period=15):
  agg_trade_list = list(trades)
  frame1t = df(agg_trade_list)
  new_date = []
  for time in frame1t['T']:
    readable = datetime.fromtimestamp(int(time/1000))
    new_date.append(readable)
  frame1t.columns = ['date', 'price', 'active', 'a4', 'a5', 'a6', 'maker', 'a8']
  frame1t['date'] = df(new_date)
  frame1t = frame1t.drop(['a4', 'a5', 'a6', 'a8'], axis=1)
  frame1t['price'] = pd.to_numeric(frame1t['price'])
  frame1t['active'] = pd.to_numeric(frame1t['active'])

  frame2t = df(frame1t, columns=['date', 'price', 'active', 'maker', 'market', 'buy', 'sell'])
  frame2t['maker'].replace([1, 0], [1, -1], inplace=True)
  frame2t['market'] = round(frame2t['price'] * (frame2t['active'] * frame2t['maker']), 4)
  frame2t['buy'] = np.array(frame2t['market'])
  frame2t['sell'] = np.array(frame2t['market'])
  
  frame3t = frame2t[frame2t['sell'] > 0] # выбор значений - бай
  frame3t = df(frame3t, columns=['date', 'price', 'market', 'active', 'sell', 'order']) # колонка с типом ордера
  frame3t['order'] = np.dtype(frame3t['order'], str()) # формат - текст
  frame3t['order'] = 'sell' # вставить тип ордера

  frame4t = frame2t[frame2t['buy'] < 0] # выбор значений - селл
  frame4t = df(frame4t, columns=['price', 'market', 'active', 'buy']) # промежуточный
  frame4t = np.abs(frame4t) # убрать знак "-"
  frame4t['date'] = frame2t['date'] # выравнивание фреймов для даты
  frame5t = df(frame4t, columns=['date', 'price', 'market', 'active', 'buy', 'order']) # селл-таблица
  frame5t['order'] = np.dtype(frame5t['order'], str()) # формат - текст
  frame5t['order'] = 'buy' # вставить тип ордера

  frame6t = frame3t.combine_first(frame5t) # объединить бай и селл таблицы
  frame7t = df(frame6t, columns=['date', 'price', 'market', 'active', 'buy', 'sell', 'order']) # объединенная таблица
  total = frame7t.pivot_table(['price', 'buy', 'sell'], ['date'], aggfunc='sum')
  # основные параметры цены
  last_price = round(frame7t['price'].iloc[-1], 8)
  min_price = round(min(frame7t['price']), 8)
  max_price = round(max(frame7t['price']), 8)
  aver_price = round(sum((np.abs(frame7t['market'])) / sum(frame7t['active'])), 8)
  # расчет процентной шкалы цен
  buy_ticks = int((last_price - min_price) * y_ticks // (max_price - min_price))
  if buy_ticks < 2: buy_ticks = 2
  if buy_ticks > (y_ticks - 2): buy_ticks = (y_ticks - 2)
  sell_ticks = y_ticks - buy_ticks
  one_tick_buy = round(((last_price - min_price) / last_price) * 100 / (buy_ticks - 1), 2)
  one_tick_sell = round(((max_price - last_price) / last_price) * 100 / (sell_ticks - 1), 2)
  res_buy = list(map(lambda var: var * one_tick_buy / 100, range(buy_ticks)))
  res_sell = list(map(lambda var: var * one_tick_sell / 100, range(sell_ticks)))
  up_scale = last_price + last_price * np.array(res_sell)
  down_scale = last_price - last_price * np.array(res_buy)
  scale_percent = np.hstack((up_scale, down_scale)) # создание массива perc значений
  # уровни сопр/подд от средней цены
  downzone = round(((aver_price - min_price) / 3), 8) # 3 зоны вниз от средней
  buy_down = min_price + downzone # нижняя бай-зона
  sell_down = aver_price - downzone # нижняя селл-зона
  upzone = round(((max_price - aver_price) / 3), 8) # 3 зоны вверх от средней
  buy_up = aver_price + upzone # верхняя бай-зона
  sell_up = max_price - upzone # верхняя селл-зона
  # основные данные по параметрам времени
  first_time = frame7t['date'].iloc[0] # первая дата периода ордеров
  last_time = frame7t['date'].iloc[-1] # последняя дата периода ордеров
  diff = last_time - first_time
  diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
  sum_15m = round(diff_minutes / period, 2) # количество 15-мин периодов
  # расчет основных параметров данных по объемам ордеров
  frame7t['buy'] = frame7t['buy'].fillna(0)
  sum_buy_order = round(sum(frame7t['buy']), 4) # сумма бай-ордеров за период
  aver_buy15_order = round(sum(frame7t['buy']) / sum_15m, 4) # средний размер бай-ордера за 15 мин
  max_buy_order = round(max(frame7t['buy']), 4) # макс размер бай-ордера
  frame7t['sell'] = frame7t['sell'].fillna(0)
  sum_sell_order = round(sum(frame7t['sell']), 4) # сумма селл-ордеров за период
  aver_sell15_order = round(sum(frame7t['sell']) / sum_15m, 4) # средний размер селл-ордера за 15 мин
  max_sell_order = round(max(frame7t['sell']), 4) # макс размер селл-ордера
  max_buysell_order = max(max_buy_order, max_sell_order) # абсолютный макс ордера (бай/селл)
  min_aver_buysell = min(aver_buy15_order, aver_sell15_order) # средний мин ордер (бай/селл) за 15 мин
  aver_volume = (sum_buy_order + sum_sell_order) / 2 # среднее ордеров по объемам (бай/селл)
  aver_15m_vol = round((aver_buy15_order + aver_sell15_order) / 2, 4) # средний по 15мин (бай/селл)
  # последние таблицы по объемам
  frame8t = df(frame7t, columns=['date', 'price', 'market', 'buy', 'sell', 'order']) # почти финальная таблица
  frame9t = frame8t[frame8t['market'] > aver_15m_vol] # выбор всех ордеров больше значения 15 мин
  frame10t = df(frame9t, columns=['date', 'price', 'market', 'buy', 'sell', 'order'])
  total2 = frame10t.pivot_table(['price', 'buy', 'sell'], ['date'], aggfunc='sum')
  
  return [total, frame8t, frame10t, total2, last_price, min_price, max_price, aver_price, scale_percent,
  buy_down, sell_down, buy_up, sell_up, first_time, last_time, aver_buy15_order, max_buy_order,
  aver_sell15_order, max_sell_order, max_buysell_order, min_aver_buysell, aver_volume, aver_15m_vol]

  [pivtab, f8t, f10t, pivtab2, lastpt, minpr, maxpr, averpr, percscat, buyd, selld, buyu,
  sellu, firstt, last, aver15b, maxb, aver15s, maxs, maxbs, minaver, volaver,
  aver15] = get_trades(trades, y_ticks=15, period=15)
  #export_csv = f8t.to_csv (r'C:\Users\Usuario\downloads\f8t1.csv', index = True, header=True)
  
  #from binance.client import Client
  #client = Client()
  #name = 'ZENBNB'
  #candles = client.get_klines(symbol=name, interval=Client.KLINE_INTERVAL_4HOUR)
  #trades = client.aggregate_trade_iter(symbol=name, start_str='2 days ago UTC')