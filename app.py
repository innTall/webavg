from flask import Flask, render_template, request, redirect, url_for
from binance.client import Client
# import flaskr.frames
from flaskr.frames import get_candles
from flaskr.frames import get_trades
from flaskr.charts import candlestick_chart
# from flaskr.frames import volume_percent_of_delta_candles
# from flaskr.charts import volume_chart

client = Client()

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def get_dashboard():
  intervals = ['1m', '5m', '15m', '1h', '4h', '1d', '3d', '1w', '1M']
  if request.method == 'POST':
    symbol = request.files['symbol']
    interval = request.form['interval']
    candles = client.get_klines(symbol=symbol, interval=interval)
    candle_data = get_candles(candles)
    candle_chart = candlestick_chart(candle_data)
    return candle_chart
  else:
    symbol = request.args['symbol']
    interval = '1h'
    candles = client.get_klines(symbol=symbol, interval=interval)
    candle_data = get_candles(candles)
    candle_chart = candlestick_chart(candle_data)
    return render_template('dashboard.html', candle_chart=candle_chart, intervals=intervals)