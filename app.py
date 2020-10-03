from flask import Flask, render_template, request, redirect, url_for
from binance.client import Client
import numpy as np
from flaskr.frames import get_candles
from flaskr.frames import get_trades
from flaskr.charts import candlestick_chart
#from flaskr.tabel import tabel

client = Client()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def get_dashboard():
  intervals = ['1m', '5m', '15m', '1h', '4h', '1d', '3d', '1w', '1M']
  if request.method == 'POST':
    symbol = request.form['symbol']
    interval = request.form['interval']
    candles = client.get_klines(symbol=symbol, interval=interval)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    candle_chart = candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    return candle_chart
  else:
    symbol = request.args['symbol']
    interval = '4h'
    candles = client.get_klines(symbol=symbol, interval=interval)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    candle_chart = candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    return render_template('dashboard.html', candle_chart=candle_chart, intervals=intervals)
'''
@app.route('/downblock', methods=['GET', 'POST'])
def get_tabel():
  intervals = ['1m', '5m', '15m', '1h', '4h', '1d', '3d', '1w', '1M']
  if request.method == 'POST':
    symbol = request.form['symbol']
    interval = request.form['interval']
    candles = client.get_klines(symbol=symbol, intervals=intervals)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    tabel_volume = tabel(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    return tabel_volume
  else:
    symbol = request.args['symbol']
    interval = '1h'
    candles = client.get_klines(symbol=symbol, interval=interval)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    tabel_volume = tabel(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    return render_template('downblock.html', tabel_volume=tabel_volume, intervals=intervals)

@app.route('/tradeboard', methods=['GET', 'POST'])
def get_tradeboard():
  times = ['6h', '12h', '24d', '2d', '3d', '4d', '5d' + 'ago UTC']
  if request.method == 'POST':
    symbol = request.form['symbol']
    time = request.form['time']
    trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
    (tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
    avs, mas, absma, miav, vav, a15) = get_trades(trades, unit=15, period=15)
    trade_chart = order_chart(tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
    avs, mas, absma, miav, vav, a15)
    return trade_chart
  else:
    symbol = 'request.args['symbol']'
    time = '1h'
    trades = client.aggregate_trade_iter(symbol=symbol, start_str='2 days ago UTC')
    (tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
    avs, mas, absma, miav, vav, a15) = get_trades(trades, unit=15, period=15)
    trade_chart = order_chart(tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
    avs, mas, absma, miav, vav, a15)
    return render_template('tradeboard.html', trade_chart=trade_chart, times=times)

@app.route('/upright', methods=['GET', 'POST'])
def get_upright():
  intervals = ['1m', '5m', '15m', '1h', '4h', '1d', '3d', '1w', '1M']
  if request.method == 'POST':
    symbol = request.form['symbol']
    interval = request.form['interval']
    candles = client.get_klines(symbol=symbol, intervals=intervals)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    candle_chart = candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    return candle_chart
  else:
    symbol = 'BTCUSDT'
    interval = '1h'
    candles = client.get_klines(symbol=symbol, interval=interval)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    candle_chart = candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    return render_template('upright.html', candle_chart=candle_chart, intervals=intervals)
'''
