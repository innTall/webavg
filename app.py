from flask import Flask, render_template, request, redirect, url_for
from binance.client import Client
import numpy as np
from flaskr.frames import get_candles
from flaskr.frames import get_trades
from flaskr.charts import candlestick_chart
from flaskr.charts import order_chart
from flaskr.charts import simple_chart

client = Client()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def get_dashboard():
  intervals = ['1m', '5m', '15m', '1h', '4h', '1d', '3d', '1w', '1M']
  times = ['1 day ago UTC', '2 days ago UTC', '3 days ago UTC', '5 days ago UTC']
  if request.method == 'POST':
    symbol = request.form['symbol']
    interval = request.form['interval']
    time = request.form['time']
    candles = client.get_klines(symbol=symbol, interval=interval)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    candle_chart = candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    small_chart = simple_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
    (tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
    avs, mas, absma, miav, vav, a15) = get_trades(trades, unit=15, period=15)
    trade_chart = order_chart(tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
    avs, mas, absma, miav, vav, a15)
    return candle_chart
  else:
    symbol = request.args['symbol']
    interval = '1d'
    time = '2 days ago UTC'
    candles = client.get_klines(symbol=symbol, interval=interval)
    (gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums, fd, ld, vma, vmb,
    vms, vbs, vav, dmb, dms, dbs) = get_candles(candles, unit=15)
    candle_chart = candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    small_chart = simple_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu,
    sellu, nums, fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs)
    trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
    (tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
    avs, mas, absma, miav, vav, a15) = get_trades(trades, unit=15, period=15)
    trade_chart = order_chart(tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu, fd, ld, avb, mab,
    avs, mas, absma, miav, vav, a15)
    return render_template('dashboard.html', candle_chart=candle_chart, intervals=intervals,
                           trade_chart=trade_chart, times=times, small_chart=small_chart)
