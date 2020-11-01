from flask import Flask, render_template, request, redirect, url_for
from binance.client import Client
import numpy as np
from flaskr.candles import (get_database_candles, get_table_basic_can,
      get_pivot_table_price, get_price_base_params, get_scale_percent,
      get_volume_base_params)
from flaskr.trades import (get_trades, base_table_trades, table_buy_sell,
      price_trade_params, scale_perc_trade, time_trade_params,
      volume_trades_params, tables_max_trades)
from flaskr.pairs import get_pairs
from flaskr.charts import (candlestick_chart, order_chart, simple_chart,
      candles_time, candles_price, trades_order)

client = Client()

app = Flask(__name__)

intervals = ['1m', '5m', '15m', '1h', '4h', '1d', '3d', '1w', '1M']
times = ['1 day ago UTC', '2 days ago UTC', '3 days ago UTC', '5 days ago UTC']

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def get_dashboard():
  symbol = request.args['symbol']
  interval = '1d'
  time = '2 days ago UTC'
  candles = client.get_klines(symbol=symbol, interval=interval)
  frame_candles = get_database_candles(candles)
  frame1c = get_table_basic_can(frame_candles)
  candle_chart = candlestick_chart(frame1c)
  small_chart = simple_chart(frame1c)
  table_time = candles_time(frame1c)
  total = get_pivot_table_price(frame1c)
  table_price = candles_price(total)
  trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
  frame_trades = get_trades(trades)
  frame2t = base_table_trades(frame_trades)
  frame7t = table_buy_sell(frame2t)
  trade_chart = order_chart(frame7t)
  sum_15m = time_trade_params(frame7t, period=15)
  volume_trades = volume_trades_params(frame7t, sum_15m)
  frame10t = tables_max_trades(frame7t, volume_trades)
  table_order = trades_order(frame10t)
  prices = client.get_all_tickers()
  btc, eth, bnb, usdt = get_pairs(prices)
  return render_template('dashboard.html', candle_chart=candle_chart,
          intervals=intervals, trade_chart=trade_chart, times=times,
          small_chart=small_chart, table_time=table_time,
          table_price=table_price, table_order=table_order, btc=btc, eth=eth,
          bnb=bnb, usdt=usdt)
  
@app.route('/candles', methods=['GET', 'POST'])
def test_candles():
  symbol = request.form['symbol']
  interval = request.form['interval']
  candles = client.get_klines(symbol=symbol, interval=interval)
  frame_candles = get_database_candles(candles)
  frame1c = get_table_basic_can(frame_candles)
  candle_chart = candlestick_chart(frame1c)
  return candle_chart

@app.route('/trades', methods=['GET', 'POST'])
def test_trades():
  symbol = request.form['symbol']
  time = request.form['time']
  trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
  frame_trades = get_trades(trades)
  frame2t = base_table_trades(frame_trades)
  frame7t = table_buy_sell(frame2t)
  trade_chart = order_chart(frame7t)
  return trade_chart

@app.route('/times', methods=['GET', 'POST'])
def test_times():
  symbol = request.form['symbol']
  interval = request.form['interval']
  candles = client.get_klines(symbol=symbol, interval=interval)
  frame_candles = get_database_candles(candles)
  frame1c = get_table_basic_can(frame_candles)
  table_time = candles_time(frame1c)
  return table_time

@app.route('/prices', methods=['GET', 'POST'])
def test_prices():
  symbol = request.form['symbol']
  interval = request.form['interval']
  candles = client.get_klines(symbol=symbol, interval=interval)
  frame_candles = get_database_candles(candles)
  total = get_pivot_table_price(frame_candles)
  table_price = candles_price(total)
  return table_price

@app.route('/orderes', methods=['GET', 'POST'])
def test_orderes():
  symbol = request.form['symbol']
  time = request.form['time']
  trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
  frame_trades = get_trades(trades)
  frame2t = base_table_trades(frame_trades)
  frame7t = table_buy_sell(frame2t)
  sum_15m = time_trade_params(frame7t, period=15)
  volume_trades = volume_trades_params(frame7t, sum_15m)
  frame10t = tables_max_trades(frame7t, volume_trades)
  table_order = trades_order(frame10t)
  return table_order

@app.route('/pairs', methods=['GET', 'POST'])
def test_pairs():
  prices = client.get_all_tickers()
  btc, eth, bnb, usdt = get_pairs(prices)
  return btc, eth, bnb, usdt

# from flask import Flask, render_template, request, redirect, url_for
# from binance.client import Client
# import numpy as np
# from flaskr.pairs import get_pairs
# from flaskr.frames import get_candles, get_trades
# from flaskr.charts import candlestick_chart, order_chart, simple_chart
# from flaskr.charts import candles_time, candles_price, trades_order

# client = Client()

# app = Flask(__name__)

# intervals = ['1m', '5m', '15m', '1h', '4h', '1d', '3d', '1w', '1M']
# times = ['1 day ago UTC', '2 days ago UTC', '3 days ago UTC', '5 days ago UTC']

# @app.route('/')
# def index():
#   return render_template('index.html')

# @app.route('/dashboard', methods=['GET', 'POST'])
# def get_dashboard():
#   symbol = request.args['symbol']
#   interval = '1d'
#   time = '2 days ago UTC'
#   candles = client.get_klines(symbol=symbol, interval=interval)
#   variables_candles = get_candles(candles, y_ticks=15)
#   candle_chart = candlestick_chart(variables_candles)
#   small_chart = simple_chart(variables_candles)
#   table_time = candles_time(variables_candles)
#   table_price = candles_price(variables_candles)
#   trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
#   variables_trades = get_trades(trades, y_ticks=15, period=15)
#   trade_chart = order_chart(variables_trades)
#   table_order = trades_order(variables_trades)
#   prices = client.get_all_tickers()
#   btc, eth, bnb, usdt = get_pairs(prices)
#   return render_template('dashboard.html', candle_chart=candle_chart,
#         intervals=intervals, trade_chart=trade_chart, times=times,
#   small_chart=small_chart, table_time=table_time, table_price=table_price,
#   table_order=table_order, btc=btc, eth=eth, bnb=bnb, usdt=usdt)
  
# @app.route('/candles', methods=['GET', 'POST'])
# def test_candles():
#   symbol = request.form['symbol']
#   interval = request.form['interval']
#   candles = client.get_klines(symbol=symbol, interval=interval)
#   variables_candles = get_candles(candles, y_ticks=15)
#   candle_chart = candlestick_chart(variables_candles)
#   return candle_chart

# @app.route('/trades', methods=['GET', 'POST'])
# def test_trades():
#   symbol = request.form['symbol']
#   time = request.form['time']
#   trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
#   variables_trades = get_trades(trades, y_ticks=15, period=15)
#   trade_chart = order_chart(variables_trades)
#   return trade_chart

# @app.route('/times', methods=['GET', 'POST'])
# def test_times():
#   symbol = request.form['symbol']
#   interval = request.form['interval']
#   candles = client.get_klines(symbol=symbol, interval=interval)
#   variables_candles = get_candles(candles, y_ticks=15)
#   table_time = candles_time(variables_candles)
#   return table_time

# @app.route('/prices', methods=['GET', 'POST'])
# def test_prices():
#   symbol = request.form['symbol']
#   interval = request.form['interval']
#   candles = client.get_klines(symbol=symbol, interval=interval)
#   variables_candles = get_candles(candles, y_ticks=15)
#   table_price = candles_price(variables_candles)
#   return table_price

# @app.route('/orderes', methods=['GET', 'POST'])
# def test_orderes():
#   symbol = request.form['symbol']
#   time = request.form['time']
#   trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
#   variables_trades = get_trades(trades, y_ticks=15, period=15)
#   table_order = trades_order(variables_trades)
#   return table_order

# @app.route('/pairs', methods=['GET', 'POST'])
# def test_pairs():
#   prices = client.get_all_tickers()
#   btc, eth, bnb, usdt = get_pairs(prices)
#   return btc, eth, bnb, usdt