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

def get_candles(candles, unit=15):
  frame1c = df(candles)
  frame_date = frame1c[0]
  final_date = []
  for time in frame_date.unique():
    readable = datetime.fromtimestamp(int(time/1000))
    final_date.append(readable)
  frame1c.pop(0)
  frame1c.pop(6)
  frame1c.pop(8)
  frame1c.pop(11)
  frame2c = df(final_date)
  frame2c.columns = ['date']
  frame3c = frame2c.join(frame1c)
  frame3c.columns = ['date', 'open', 'high', 'low', 'close',
                    'active', 'market', 'buyA', 'buy']
  frame3c['market'] = pd.to_numeric(frame3c['market'])
  frame3c['active'] = pd.to_numeric(frame3c['active'])
  frame3c['buy'] = pd.to_numeric(frame3c['buy'])
  frame3c['low'] = pd.to_numeric(frame3c['low'])
  frame3c['high'] = pd.to_numeric(frame3c['high'])
  frame3c['close'] = pd.to_numeric(frame3c['close'])
  frame4c = df(frame3c, columns=['date', 'price', 'open', 'high', 'low',
               'close', 'active', 'market', 'buy', 'sell', '%', 'ao', 'rsi'])
  frame4c['price'] = round((frame4c['market'] / frame4c['active']), 8)
  frame4c['sell'] = round((frame4c['market'] - frame4c['buy']), 8)
  frame4c['diff'] = frame4c['buy'] - frame4c['sell']
  frame4c['%'] = round(((frame4c['buy'] - frame4c['sell']) *100 / frame4c['sell']), 2)
  frame4c['ao'] = ta.momentum.ao(high=frame4c['high'], low=frame4c['low'])
  frame4c['rsi'] = ta.momentum.rsi(close=frame4c['close'])
  total = frame4c.pivot_table(['buy', 'sell', 'market', 'diff'], ['price'], aggfunc='sum')
  last_price = frame4c['price'].iloc[-1]
  min_can = min(frame4c['low'])
  max_can = max(frame4c['high'])
  avr_can = round(sum((frame4c['market']) / sum(frame4c['active'])), 8)
  buy_ticks = int((last_price - min_can) * unit / (max_can - min_can))
  if buy_ticks < 2: buy_ticks = 2
  if buy_ticks > 13: buy_ticks = 13
  sell_ticks = unit - buy_ticks
  one_buy = round(((last_price - min_can) / last_price) * 100 / (buy_ticks - 1), 2)
  one_sell = round(((max_can - last_price) / last_price) * 100 / (sell_ticks - 1), 2)
  arr_buy = range(buy_ticks) # диапазон значений переменной
  arr_sell = range(sell_ticks) # диапазон значений переменной
  res_buy = list(map(lambda var: var * one_buy / 100, arr_buy)) # расчет вниз
  res_sell = list(map(lambda var: var * one_sell / 100, arr_sell)) # расчет вверх
  up_scale = last_price + last_price * np.array(res_sell) # процентная шкала вверх от текущей цены
  down_scale = last_price - last_price * np.array(res_buy) # процентная шкала вниз от текущей цены
  scale_can = np.hstack((up_scale, down_scale)) # создание массива % значений
  down = round(((avr_can - min_can) / 3), 8) # 3 зоны вниз от средней
  buy_down = min_can + down # нижняя бай-зона
  sell_down = avr_can - down # нижняя селл-зона
  up = round(((max_can - avr_can) / 3), 8) # 3 зоны вверх от средней
  buy_up = avr_can + up # верхняя бай-зона
  sell_up = max_can - up # верхняя селл-зона
  numstr = len(frame4c['open'])
  first_date = frame4c['date'].iloc[0]
  last_date = frame4c['date'].iloc[-1]
  vol_max = round(max(frame4c['market']), 2)
  vol_mbuy = round(max(frame4c['buy']), 2)
  vol_msell = round(max(frame4c['sell']), 2)
  vol_bs = max(vol_mbuy, vol_msell) # макс значение объема (бай/селл)
  vol_aver = round(sum(frame4c['market']/2/numstr), 4) # среднее значение бай/селл объемов за период
  diff_mbuy = max(frame4c['%'])
  diff_msell = max(np.abs(frame4c['%']))
  diff_bs = max(diff_mbuy, diff_msell)
  return (frame4c, total, last_price, min_can, max_can, avr_can, scale_can, buy_down, sell_down,
  buy_up, sell_up, numstr, first_date, last_date, vol_max, vol_mbuy, vol_msell, vol_bs,
  vol_aver, diff_mbuy, diff_msell, diff_bs)

  (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb, vms,
  vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
#export_csv = gc.to_csv (r"C:\Users\Usuario\downloads\gc1.csv", index = True, header=True)
#export_csv = piv.to_csv (r"C:\Users\Usuario\downloads\piv1.csv", index = True, header=True)
#print(f'lpc={lpc}, mic={mic}, mac={mac}, avc={avc}, scac={scac}, buyd={buyd}, selld={selld},\
#buyu={buyu}, sellu={sellu}, nums={nums}, fd={fd}, ld={ld}, vma={vma}, vmb={vmb},\
#vms={vms}, vbs={vbs}, vav={vav}, dmb={dmb}, dms={dms}, dbs={dbs}')

def get_trades(trades, unit=15, period=15):
  trade_list = list(trades)
  frame1t = df(trade_list)
  new_date = []
  for time in frame1t['T']:
    readable = datetime.fromtimestamp(int(time/1000))
    new_date.append(readable)
  date = df(new_date)
  price = df(frame1t['p'])
  active = df(frame1t['q'])
  ind = df(frame1t['a'])
  maker = df(frame1t['m'])
  match = df(frame1t['M'])
  date.columns = ['date']
  price.columns = ['price']
  active.columns = ['active']
  ind.columns = ['id']
  maker.columns =['maker']
  match.columns = ['match']
  price_float = price.astype('float')
  active_float = active.astype('float')
  maker_int = maker.astype('int')
  maker_int.replace([1, 0], [1, -1], inplace=True)
  frame2t = pd.concat([date, price_float, active_float], axis=1)
  frame2t['market'] = frame2t['price'] * (frame2t['active'] * maker_int['maker'])
  frame3t = df(frame2t, columns=['date', 'price', 'market', 'active', 'trade', 'buy'])
  frame3t['buy'] = np.array(frame3t['market'])
  frame3t['trade'] = np.array(frame3t['market'])
  frame3t = df(frame3t.rename(columns={'trade': 'sell'}))
  frame4t = frame3t[frame3t['sell'] > 0] # выбор значений - бай
  frame4t = df(frame4t, columns=['date', 'price', 'market', 'active', 'sell', 'order']) # колонка с типом ордера
  frame4t['order'] = np.dtype(frame4t['order'], str()) # формат - текст
  frame4t['order'] = 'sell' # вставить тип ордера
  frame5t = df(frame4t, columns=['date', 'price', 'market', 'active', 'sell', 'order']) # бай-таблица
  frame5t = frame3t[frame3t['buy'] < 0] # выбор значений - селл
  frame5t = df(frame5t, columns=['price', 'market', 'active', 'buy'])
  frame5t = np.abs(frame5t) # убрать знак "-"
  frame5t['date'] = frame3t['date'] # выравнивание фреймов для даты
  frame6t = df(frame5t, columns=['date', 'price', 'market', 'active', 'buy', 'order']) # селл-таблица
  frame6t['order'] = np.dtype(frame6t['order'], str()) # формат - текст
  frame6t['order'] = 'buy' # вставить тип ордера
  frame7t = frame4t.combine_first(frame6t) # объединить бай и селл таблицы
  frame8t = df(frame7t, columns=['date', 'price', 'market', 'active', 'buy', 'sell', 'order']) # объединенная таблица
  totalt2 = frame8t.pivot_table(['price', 'buy', 'sell'], ['date'], aggfunc='sum')

  last_price = frame8t['price'].iloc[-1]
  min_tr = min(frame8t['price'])
  max_tr = max(frame8t['price'])
  avr_tr = round(sum((np.abs(frame8t['market'])) / sum(frame8t['active'])), 8)
  buy_ticks = int((last_price - min_tr) * unit / (max_tr - min_tr))
  if buy_ticks < 2: buy_ticks = 2
  if buy_ticks > 13: buy_ticks = 13
  sell_ticks = unit - buy_ticks
  one_buy = round((last_price - min_tr) / last_price * 100 / (buy_ticks - 1), 2)
  one_sell = round((max_tr - last_price) / last_price * 100 / (sell_ticks - 1), 2)
  arr_buy = range(buy_ticks)
  arr_sell = range(sell_ticks)
  res_buy = list(map(lambda var: var * one_buy / 100, arr_buy))
  res_sell = list(map(lambda var: var * one_sell / 100, arr_sell))
  up_scale = last_price + last_price * np.array(res_sell)
  down_scale = last_price - last_price * np.array(res_buy)
  scale_tr = np.hstack((up_scale, down_scale))
  
  down = round(((avr_tr - min_tr) / 3), 8)
  buy_down = min_tr + down
  sell_down = avr_tr - down
  up = round(((max_tr - avr_tr) / 3), 8)
  buy_up = avr_tr + up
  sell_up = max_tr - up
 
  first = frame8t['date'].iloc[0] # первая дата периода ордеров
  last = frame8t['date'].iloc[-1] # последняя дата периода ордеров
  diff = last - first
  diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
  tf15 = round(diff_minutes / period, 2) # количество 15-мин периодов
  frame8t['buy'] = frame8t['buy'].fillna(0)
  summa_buy = round(sum(frame8t['buy']), 8) # сумма бай-ордеров за период
  ave_buy = round(sum(frame8t['buy']) / tf15, 8) # средний размер бай-ордера за 15 мин
  max_buy = round(max(frame8t['buy']), 8) # макс размер бай-ордера
  frame8t['sell'] = frame8t['sell'].fillna(0)
  summa_sell = round(sum(frame8t['sell']), 8) # сумма селл-ордеров за период
  ave_sell = round(sum(frame8t['sell']) / tf15, 8) # средний размер селл-ордера за 15 мин
  max_sell = round(max(frame8t['sell']), 8) # макс размер селл-ордера
  abs_max = max(max_buy, max_sell) # абсолютный макс ордера (бай/селл)
  min_ave = min(ave_buy, ave_sell) # средний мин ордер (бай/селл) за 15 мин
  vol_aver = (summa_buy + summa_sell) / 2 # среднее ордеров по объемам (бай/селл)
  aver15 = round((ave_buy + ave_sell) / 2, 8) # средний по 15мин (бай/селл)
  
  frame9t = df(frame8t, columns=['date', 'price', 'market', 'buy', 'sell', 'order']) # почти финальная таблица
  frame10t = frame9t[frame9t['market'] > aver15] # выбор всех ордеров больше значения 15 мин
  frame11t = df(frame10t, columns=['date', 'price', 'market', 'buy', 'sell', 'order'])
  totalt3 = frame11t.pivot_table(['price', 'buy', 'sell'], ['date'], aggfunc='sum')
  return (totalt2, frame8t, frame11t, totalt3, last_price, min_tr, max_tr, avr_tr, scale_tr,
  buy_down, sell_down, buy_up, sell_up, first, last, ave_buy, max_buy, ave_sell, max_sell,
  abs_max, min_ave, vol_aver, aver15)
  
  (tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
  avs, mas, absma, miav, vav, a15) = get_trades(trades, unit=15, period=15)
#export_csv = f8t.to_csv (r'C:\Users\Usuario\downloads\f8t1.csv', index = True, header=True)
#export_csv = tot2.to_csv (r'C:\Users\Usuario\downloads\tot2.csv', index = True, header=True)
#export_csv = tot3.to_csv (r'C:\Users\Usuario\downloads\tot3.csv', index = True, header=True)
#print(f'lp={lp}, mit={mit}, mat={mat}, avt={avt}, scat={scat}, buyd={buyd}, selld={selld},\
#buyu={buyu}, sellu={sellu}, fd={fd}, ld={ld}, avb={avb}, mab={mab}, avs={avs},\
#mas={mas}, absma={absma}, miav={miav}, vav={vav}, a15={a15}')