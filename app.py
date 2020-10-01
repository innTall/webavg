from flask import Flask, render_template, request, redirect, url_for
from binance.client import Client
import numpy as np
from flaskr.frames import get_candles
from flaskr.frames import get_trades
from flaskr.charts import candlestick_chart

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
    candles = client.get_klines(symbol=symbol, intervals=intervals)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    candle_chart = candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    return candle_chart
  else:
    symbol = request.args['symbol']
    interval = '1h'
    candles = client.get_klines(symbol=symbol, interval=interval)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    candle_chart = candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    return render_template('dashboard.html', candle_chart=candle_chart, intervals=intervals)
