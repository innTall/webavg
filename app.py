from flask import Flask, render_template, request, redirect, url_for, jsonify
from binance.client import Client
import numpy as np
import json
from flaskr.frames import get_candles, get_trades
from flaskr.charts import candlestick_chart, order_chart, simple_chart
#from flaskr.charts import timec
#from flaskr.charts import pricec
#from flaskr.charts import ordert

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
    var_can = get_candles(candles, y_ticks=15)
    candle_chart = candlestick_chart(var_can)
    small_chart = simple_chart(var_can)
    trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
    var_trad = get_trades(trades, y_ticks=15, period=15)
    trade_chart = order_chart(var_trad)
    return candle_chart
  else:
    symbol = request.args['symbol']
    interval = '1d'
    time = '2 days ago UTC'
    candles = client.get_klines(symbol=symbol, interval=interval)
    var_can = get_candles(candles, y_ticks=15)
    candle_chart = candlestick_chart(var_can)
    small_chart = simple_chart(var_can)
    trades = client.aggregate_trade_iter(symbol=symbol, start_str=time)
    var_trad = get_trades(trades, y_ticks=15, period=15)
    trade_chart = order_chart(var_trad)
    return render_template('dashboard.html', candle_chart=candle_chart, intervals=intervals,
                      trade_chart=trade_chart, times=times, small_chart=small_chart)
    '''
    jsonfiles = json.loads(df.to_json(orient='records'))
    return render_template('index.html', ctrsuccess=jsonfiles)
    
    table_time = timec(var_can(0))
    table_price = pricec(var_trad(1))
    table_order = ordert(var_trad(2))
    table_time=table_time, table_price=table_price, table_order=table_order

    return jsonify(table_price=json.loads(gc.to_json(orient='values'))['data'],
                  columns=[{'title': str(col)}
                  for col in json.loads(
                    gc.to_json(orient='values'))["columns"]])
    return jsonify(table_price=json.loads(piv.to_json(orient='values'))['data'],
                  columns=[{'title': str(col)}
                  for col in json.loads(
                    piv.to_json(orient='values'))["columns"]])                
    return jsonify(table_order=json.loads(f11t.to_json(orient='values'))['data'],
                  columns=[{'title': str(col)}
                  for col in json.loads(
                    f11t.to_json(orient='values'))["columns"]])
'''



