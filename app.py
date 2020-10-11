from flask import Flask, render_template, request, redirect, url_for
from binance.client import Client
import numpy as np
import json
from flaskr.frames import get_candles, get_trades
from flaskr.crypto import get_crypto
from flaskr.charts import candlestick_chart, order_chart, simple_chart
from flaskr.charts import candles_time, candles_price, trades_order, dropdown_crypto

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
  variables_candles = get_candles(candles, y_ticks=15)
  candle_chart = candlestick_chart(variables_candles)
  small_chart = simple_chart(variables_candles)
  table_time = candles_time(variables_candles)
  table_price = candles_price(variables_candles)
  trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
  variables_trades = get_trades(trades, y_ticks=15, period=15)
  trade_chart = order_chart(variables_trades)
  table_order = trades_order(variables_trades)
  prices = client.get_all_tickers()
  crypto_bases = get_crypto(prices)
  drop_crypto = dropdown_crypto(crypto_bases)
  return render_template('dashboard.html', candle_chart=candle_chart, intervals=intervals,
                      trade_chart=trade_chart, times=times, small_chart=small_chart,
                      table_time=table_time, table_price=table_price, table_order=table_order,
                      drop_crypto=drop_crypto)

@app.route('/candles', methods=['GET', 'POST'])
def test_candles():
  symbol = request.form['symbol']
  interval = request.form['interval']
  candles = client.get_klines(symbol=symbol, interval=interval)
  variables_candles = get_candles(candles, y_ticks=15)
  candle_chart = candlestick_chart(variables_candles)
  return candle_chart

@app.route('/trades', methods=['GET', 'POST'])
def test_trades():
  symbol = request.form['symbol']
  time = request.form['time']
  trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
  variables_trades = get_trades(trades, y_ticks=15, period=15)
  trade_chart = order_chart(variables_trades)
  return trade_chart

@app.route('/times', methods=['GET', 'POST'])
def test_times():
  symbol = request.form['symbol']
  interval = request.form['interval']
  candles = client.get_klines(symbol=symbol, interval=interval)
  variables_candles = get_candles(candles, y_ticks=15)
  table_time = candles_time(variables_candles)
  return table_time

@app.route('/prices', methods=['GET', 'POST'])
def test_prices():
  symbol = request.form['symbol']
  interval = request.form['interval']
  candles = client.get_klines(symbol=symbol, interval=interval)
  variables_candles = get_candles(candles, y_ticks=15)
  table_price = candles_price(variables_candles)
  return table_price

@app.route('/orderes', methods=['GET', 'POST'])
def test_orderes():
  symbol = request.form['symbol']
  time = request.form['time']
  trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
  variables_trades = get_trades(trades, y_ticks=15, period=15)
  table_order = trades_order(variables_trades)
  return table_order

@app.route('/crypto', methods=['GET', 'POST'])
def test_crypto():
  prices = client.get_all_tickers()
  crypto_bases = get_crypto(prices)
  drop_crypto = dropdown_crypto(crypto_bases)
  return drop_crypto
