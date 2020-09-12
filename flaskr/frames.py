import numpy as np
import pandas as pd
from datetime import datetime
from pandas import DataFrame as df

pd.set_option('precision', 8)

def get_candles(candles):
  frame_c1 = df(candles)
  frame_date = frame_c1[0]
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

def get_trades(trades):
  trade_list = list(trades)
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

def all_parameters_of_prices(gc, gt):
  last_price = gt['price'].iloc[-1]
  min_can = min(gc['low'])
  max_can = max(gc['high'])
  avr_can = round(sum(gc['market']) / sum(gc['active']), 4)
  min_tr = min(gt['price'])
  max_tr = max(gt['price'])
  gt['market'] = np.abs(gt['market'])
  avr_tr = round(sum(gt['market']) / sum(gt['active']), 4)
  return last_price, min_can, max_can, avr_can, min_tr, max_tr, avr_tr
  pl, mic, mac, avc, mit, mat, avt = all_parameters_of_prices(gc, gt)

def percent_scale_of_candle_price(pl, mic, mac, unit=15):
  buy_ticks = int(round((pl - mic) * unit // (mac - mic)))
  sell_ticks = unit - buy_ticks
  one_buy = round((pl - mic) / pl * 100 / (buy_ticks - 1), 2)
  one_sell = round((mac - pl) / pl * 100 / (sell_ticks - 1), 2)
  arr_buy = range(buy_ticks)
  arr_sell = range(sell_ticks)
  res_buy = list(map(lambda var: var * one_buy / 100, arr_buy))
  res_sell = list(map(lambda var: var * one_sell / 100, arr_sell))
  up_scale = pl + pl * np.array(res_sell)
  down_scale = pl - pl * np.array(res_buy)
  scale_can = np.hstack((up_scale, down_scale))
  return scale_can
  perc = percent_scale_of_candle_price(pl, mic, mac, unit=15)

def percent_scale_of_trade_price(pl, mit, mat, unit=15):
  buy_ticks = int(round((pl - mit) * unit // (mat - mit)))
  sell_ticks = unit - buy_ticks
  one_buy = round((pl - mit) / pl * 100 / (buy_ticks - 1), 2)
  sell_buy = round((mat - pl) / pl * 100 / (sell_ticks - 1), 2)
  arr_buy = range(buy_ticks)
  arr_sell = range(sell_ticks)
  res_buy = list(map(lambda var: var * one_buy / 100, arr_buy))
  res_sell = list(map(lambda var: var * one_sell / 100, arr_sell))
  up_scale = pl + pl * np.array(res_sell)
  down_scale = pl - pl * np.array(res_buy)
  scale_tr = np.hstack((up_scale, down_scale))
  return scale_tr
  pert = percent_scale_of_trade_price(pl, mit, mat, unit=15)

def levels_of_price_candles(avc, mic, mac):
  down = round((avc - mic) / 3, 8)
  buy_down = mic + down
  sell_down = avc - down
  up = round((mac - avc) / 3, 8)
  buy_up = avc + up
  sell_up = mac - up
  return buy_down, sell_down, buy_up, sell_up
  onec, twoc, fourc, fivec = levels_of_price_candles(avc, mic, mac)

def levels_of_price_trades(avt, mit, mat):
  down = round((avt - mit) / 3, 8)
  buy_down = mit + down
  sell_down = avt - down
  up = round((mat - avt) / 3, 8)
  buy_up = avt + up
  sell_up = mat - up
  return buy_down, sell_down, buy_up, sell_up
  onet, twot, fourt, fivet = levels_of_price_trades(avt, mit, mat)

def base_tabel_of_candles(gc):
  frame1c = df(gc, columns=['date', 'price', 'open', 'high', 'low', 'close', 'active', 'market', 'buyA', 'buy', 'sell'])
  frame1c['price'] = round(frame1c['market'] / frame1c['active'], 8)
  frame1c['sell'] = frame1c['market'] - frame1c['buy']
  frame2c = df(frame1c, columns=['date', 'price', 'market', 'buy', 'sell', 'active', 'delta'])
  frame2c['delta'] = round(frame2c['buy'] - frame2c['sell'], 2)
  frame3c = df(frame2c, columns=['date', 'price', 'market', 'buy', 'sell', 'active', 'delta', '%'])
  frame3c['%'] = round((frame2c['delta'] / grame2c['buy']) * 100, 2)
  return frame1c, frame3c
  fc1, fc3 = base_tabel_of_candles(gc)

def base_tabel_of_trades(gt):
  framet = df(gt, columns=['date', 'price', 'market', 'active', 'sell'])
  framet['sell'] = np.array(framet['market'])
  framet = df(framet.rename(columns={'market': 'buy'}))
  frame1t = df(framet, columns=['date', 'price', 'buy', 'sell'])
  return framet, frame1t
  ft, ft1 = base_tabel_of_trades(gt)

def volume_percent_of_delta_candles(fc3):
  frame4c = df(fc3, columns=['date', 'price', 'market', 'buy', 'sell', 'delta', '%', 'rsi', 'macd', 'ao'])
  frame4c = fc3[fc3['%'] > 0]
  frame5c = df(frame4c, columns=['date', 'buy', 'delta', '%'])
  frame6c = fc3[fc3['%'] > 0]
  frame7c = df(frame6c, columns=['date', 'sell', 'delta', '%'])
  frame8c = df(frame7c, columns=['sell', 'delta', '%'])
  # frame8b['%'] = np.log(frame8b.iloc[:, :])
  return frame4c, frame5c, frame7c, frame8c
  fc4, fc5, fc7, fc8 = volume_percent_of_delta_candles(fc3)

def variables_for_plots_of_volume_candles(fc1, fc4, fc5, fc7, fc8):
  numstr = len(fc1['open'])
  first_date = fc4['date'].iloc[0]
  last_date = fc4['date'].iloc[-1]
  vol_max = round(max(fc1['market']), 2)
  vol_mbuy = round(max(fc4['buy']), 2)
  vol_msell = round(max(fc4['sell']), 2)
  vol_bs = max(vol_mbuy, vol_msell) # макс значение объема (бай/селл)
  vol_aver = round(sum(fc4['market']/2/numstr), 4) # среднее значение бай/селл объемов за период
  delta_buy = round(sum(fc5['delta']) / sum(fc5['buy']) * 100, 2) # delta/buy
  delta_sell = round(sum(fc7['delta']) / sum(fc7['sell']) * 100, 2) # delta/sell
  diff_mbuy = max(fc4['%'])
  diff_msell = max(fc8['%'])
  diff_bs = max(diff_mbuy, diff_msell)
  return numstr, first_date, last_date, vol_max, vol_mbuy, vol_msell, 
  vol_bs, vol_aver, delta_buy, delta_sell, diff_mbuy, diff_msell, diff_bs
  nums, daya, dayz, vmc, vmb, vms, vbs, vav, delb, dels, difb, difs, dibs = variables_for_plots_of_volume_candles(fc1, fc4, fc5, fc7, fc8)

def pivot_volume_price_candles(fc4):
  total1 = fc4.pivot_table(['market'], ['price'], aggfunc='sum')
  return total1
  piv_tab = pivot_volume_price_candles(fc4)

def tabel_of_separated_buy_sell_orders(ft1):
  frame2t = ft1[ft1['buy'] > 0] # выбор значений - бай
  frame3t = df(frame2t, columns=['date', 'price', 'buy', 'order']) # колонка с типом ордера
  frame3t['order'] = np.dtype(frame3t['order'], str()) # формат - текст
  frame3t['order'] = 'buy' # вставить тип ордера
  frame4t = df(frame3t, columns=['date', 'price', 'buy', 'order']) # бай-таблица
  frame5t = ft1[ft1['sell'] < 0] # выбор значений - селл
  frame6t = df(frame5t, columns=['price', 'sell'])
  frame7t = np.abs(frame6t) # убрать знак "-"
  frame7t['date'] = frame5t['date'] # выравнивание фреймов для даты
  frame8t = df(frame7t, columns=['date', 'price', 'sell', 'order']) # селл-таблица
  frame8t['order'] = np.dtype(frame8t['order'], str()) # формат - текст
  frame8t['order'] = 'sell' # вставить тип ордера
  frame9t = frame4t.combine_first(frame8t) # объединить бай и селл таблицы
  frame10t = df(frame9t, columns=['date', 'price', 'buy', 'sell', 'trade', 'order']) # объединенная таблица
  return frame4t, frame8t, frame10t
  ft4, ft8, ft10 = tabel_of_separated_buy_sell_orders(ft1)

def variables_for_plots_trades(ft, ft4, ft8, period=15):
  first = ft['date'].iloc[0] # первая дата периода ордеров
  last = ft['date'].iloc[-1] # последняя дата периода ордеров
  diff = last - first
  diff_minutes = (diff.days * 24 * 60) + (diff.seconds/60)
  tf15 = round(diff_minutes / period, 2) # количество 15-мин периодов
  summa_buy = round(sum(ft4['buy']), 4) # сумма бай-ордеров за период
  ave_buy = round(sum(ft4['buy']) / tf15, 4) # средний размер бай-ордера за 15 мин
  max_buy = round(max(ft4['buy']), 4) # макс размер бай-ордера
  summa_sell = round(sum(ft8['sell']), 4) # сумма селл-ордеров за период
  ave_sell = round(sum(ft8['sell']) / tf15, 4) # средний размер селл-ордера за 15 мин
  max_sell = round(max(ft8['sell']), 4) # макс размер селл-ордера
  abs_max = max(max_buy, max_sell) # абсолютный макс ордера (бай/селл)
  min_ave = min(ave_buy, ave_sell) # средний мин ордер (бай/селл) за 15 мин
  vol_aver = (summa_buy + summa_sell) / 2 # среднее ордеров по объемам (бай/селл)
  aver15 = round((ave_buy + ave_sell) / 2, 4) # средний по 15мин (бай/селл)
  return first, last, ave_buy, max_buy, ave_sell, max_sell, abs_max, min_ave, vol_aver, aver15
  fd, ld, aveb, maxb, aves, maxs, maxabs, minave, vave, a15 = variables_for_plots_trades(ft, ft4, ft8, period=15)

def grands_orders_of_trades(ft10, a15):
  ft10['trade'] = np.where(pd.isnull(ft10['buy']), ft10['sell'], 
  ft10['buy']) # свести в одну колонку значения бай-селл ордеров
  frame11t = df(ft10, columns=['date', 'price', 'buy', 'sell', 'trade', 'order']) # почти финальная таблица
  frame12t = frame11t[frame11t['trade'] > a15] # выбор всех ордеров больше значения 15 мин
  frame13t = df(frame12t, columns=['date', 'price', 'buy', 'sell', 'trade', 'order'])
  return frame11t, frame13t
  ft11, ft13 = grands_orders_of_trades(ft10, a15)
