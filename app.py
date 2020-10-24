from flask import Flask, render_template, request, redirect, url_for
from binance.client import Client
import numpy as np
import json
from flaskr.frames import get_candles, get_trades, get_cryptos
from flaskr.charts import candlestick_chart, order_chart, simple_chart
from flaskr.charts import candles_time, candles_price, trades_order

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
  btcx, ethx, bnbx, usdtx = get_cryptos(prices)
  return render_template('dashboard.html', candle_chart=candle_chart, intervals=intervals,
                      trade_chart=trade_chart, times=times, small_chart=small_chart,
                      table_time=table_time, table_price=table_price, table_order=table_order,
                      btcx=btcx, ethx=ethx, bnbx=bnbx, usdtx=usdtx)
  
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

@app.route('/cryptos', methods=['GET', 'POST'])
def test_cryptos():
  prices = client.get_all_tickers()
  btcx, ethx, bnbx, usdtx = get_cryptos(prices)
  return btcx, ethx, bnbx, usdtx
  # list(btcx)
  # list(ethx)
  # list(bnbx)
  # list(usdtx)
  # print(btcx, ethx, bnbx, usdtx)

  # btcx = ['ETHBTC', 'LTCBTC', 'BNBBTC', 'NEOBTC', 'BCCBTC', 'GASBTC', 'HSRBTC', 'MCOBTC',
  #         'WTCBTC', 'LRCBTC', 'QTUMBTC', 'YOYOBTC', 'OMGBTC', 'ZRXBTC', 'STRATBTC', 'SNGLSBTC',
  #         'BQXBTC', 'KNCBTC', 'FUNBTC', 'SNMBTC', 'IOTABTC', 'LINKBTC', 'XVGBTC', 'SALTBTC',
  #         'MDABTC', 'MTLBTC', 'SUBBTC', 'EOSBTC', 'SNTBTC', 'ETCBTC', 'MTHBTC', 'ENGBTC', 'DNTBTC'
  #         'ZECBTC', 'BNTBTC', 'ASTBTC', 'DASHBTC', 'OAXBTC', 'ICNBTC', 'BTGBTC', 'EVXBTC', 'REQBTC',
  #         'VIBBTC', 'TRXBTC', 'POWRBTC', 'ARKBTC', 'XRPBTC', 'MODBTC', 'ENJBTC', 'STORJBTC',
  #         'VENBTC', 'KMDBTC', 'RCNBTC', 'NULSBTC', 'RDNBTC', 'XMRBTC', 'DLTBTC', 'AMBBTC',
  #         'BATBTC', 'BCPTBTC', 'ARNBTC', 'GVTBTC', 'CDTBTC', 'GXSBTC', 'POEBTC', 'QSPBTC',
  #         'BTSBTC', 'XZCBTC', 'LSKBTC', 'TNTBTC', 'FUELBTC', 'MANABTC', 'BCDBTC', 'DGDBTC',
  #         'ADXBTC', 'ADABTC', 'PPTBTC', 'CMTBTC', 'XLMBTC', 'CNDBTC', 'LENDBTC', 'WABIBTC',
  #         'TNBBTC', 'WAVESBTC', 'GTOBTC', 'ICXBTC', 'OSTBTC', 'ELFBTC', 'AIONBTC', 'NEBLBTC',
  #         'BRDBTC', 'EDOBTC', 'WINGSBTC', 'NAVBTC', 'LUNBTC', 'TRIGBTC', 'APPCBTC', 'VIBEBTC',
  #         'RLCBTC', 'INSBTC', 'PIVXBTC', 'IOSTBTC', 'CHATBTC', 'STEEMBTC', 'NANOBTC', 'VIABTC',
  #         'BLZBTC', 'AEBTC', 'RPXBTC', 'NCASHBTC', 'POABTC', 'ZILBTC', 'ONTBTC', 'STORMBTC',
  #         'XEMBTC', 'WANBTC', 'WPRBTC', 'QLCBTC', 'SYSBTC', 'GRSBTC', 'CLOAKBTC', 'GNTBTC',
  #         'LOOMBTC', 'BCNBTC', 'REPBTC', 'TUSDBTC', 'ZENBTC', 'SKYBTC', 'CVCBTC', 'THETABTC',
  #         'IOTXBTC', 'QKCBTC', 'AGIBTC', 'NXSBTC', 'DATABTC', 'SCBTC', 'NPXSBTC', 'KEYBTC',
  #         'NASBTC', 'MFTBTC', 'DENTBTC', 'ARDRBTC', 'HOTBTC', 'VETBTC', 'DOCKBTC', 'POLYBTC',
  #         'PHXBTC', 'HCBTC', 'GOBTC', 'PAXBTC', 'RVNBTC', 'DCRBTC', 'MITHBTC', 'BCHABCBTC',
  #         'BCHSVBTC', 'RENBTC', 'BTTBTC', 'ONGBTC', 'FETBTC', 'CELRBTC', 'MATICBTC', 'ATOMBTC',
  #         'PHBBTC', 'TFUELBTC', 'ONEBTC', 'FTMBTC', 'BTCBBTC', 'ALGOBTC', 'ERDBTC', 'DOGEBTC',
  #         'DUSKBTC', 'ANKRBTC', 'WINBTC', 'COSBTC', 'COCOSBTC', 'TOMOBTC', 'PERLBTC', 'CHZBTC',
  #         'BANDBTC', 'BEAMBTC', 'XTZBTC', 'HBARBTC', 'NKNBTC', 'STXBTC', 'KAVABTC', 'ARPABTC',
  #         'CTXCBTC', 'BCHBTC', 'TROYBTC', 'VITEBTC', 'FTTBTC', 'OGNBTC', 'DREPBTC', 'TCTBTC',
  #         'WRXBTC', 'LTOBTC', 'MBLBTC', 'COTIBTC', 'STPTBTC', 'SOLBTC', 'CTSIBTC', 'HIVEBTC',
  #         'CHRBTC', 'MDTBTC', 'STMXBTC', 'PNTBTC', 'DGBBTC', 'COMPBTC', 'SXPBTC', 'SNXBTC',
  #         'IRISBTC', 'MKRBTC', 'DAIBTC', 'RUNEBTC', 'FIOBTC', 'AVABTC', 'BALBTC', 'YFIBTC',
  #         'JSTBTC', 'SRMBTC', 'ANTBTC', 'CRVBTC', 'SANDBTC', 'OCEANBTC', 'NMRBTC', 'DOTBTC',
  #         'LUNABTC', 'IDEXBTC', 'RSRBTC', 'PAXGBTC', 'WNXMBTC', 'TRBBTC', 'BZRXBTC', 'WBTCBTC',
  #         'SUSHIBTC', 'YFIIBTC', 'KSMBTC', 'EGLDBTC', 'DIABTC', 'UMABTC', 'BELBTC', 'WINGBTC',
  #         'UNIBTC', 'NBSBTC', 'OXTBTC', 'SUNBTC', 'AVAXBTC', 'HNTBTC', 'FLMBTC', 'SCRTBTC',
  #         'ORNBTC', 'UTKBTC', 'XVSBTC', 'ALPHABTC', 'VIDTBTC', 'AAVEBTC', 'NEARBTC', 'FILBTC',
  #         'INJBTC']
  # ethx = ['QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH', 'BNBETH', 'OAXETH', 'DNTETH', 'MCOETH',
  #         'ICNETH', 'WTCETH', 'LRCETH', 'OMGETH', 'ZRXETH', 'STRATETH', 'SNGLSETH', 'BQXETH',
  #         'KNCETH', 'FUNETH', 'SNMETH', 'NEOETH', 'IOTAETH', 'LINKETH', 'XVGETH', 'SALTETH',
  #         'MDAETH', 'MTLETH', 'SUBETH', 'ETCETH', 'MTHETH', 'ENGETH', 'ZECETH', 'ASTETH',
  #         'DASHETH', 'BTGETH', 'EVXETH', 'REQETH', 'VIBETH', 'HSRETH', 'TRXETH', 'POWRETH',
  #         'ARKETH', 'YOYOETH', 'XRPETH', 'MODETH', 'ENJETH', 'STORJETH', 'VENETH', 'KMDETH',
  #         'RCNETH', 'NULSETH', 'RDNETH', 'XMRETH', 'DLTETH', 'AMBETH', 'BCCETH', 'BATETH',
  #         'BCPTETH', 'ARNETH', 'GVTETH', 'CDTETH', 'GXSETH', 'POEETH', 'QSPETH', 'BTSETH',
  #         'XZCETH', 'LSKETH', 'TNTETH', 'FUELETH', 'MANAETH', 'BCDETH', 'DGDETH', 'ADXETH',
  #         'ADAETH', 'PPTETH', 'CMTETH', 'XLMETH', 'CNDETH', 'LENDETH', 'WABIETH', 'LTCETH',
  #         'TNBETH', 'WAVESETH', 'GTOETH', 'ICXETH', 'OSTETH', 'ELFETH', 'AIONETH', 'NEBLETH',
  #         'BRDETH', 'EDOETH', 'WINGSETH', 'NAVETH', 'LUNETH', 'TRIGETH', 'APPCETH', 'VIBEETH',
  #         'RLCETH', 'INSETH', 'PIVXETH', 'IOSTETH', 'CHATETH', 'STEEMETH', 'NANOETH', 'VIAETH',
  #         'BLZETH', 'AEETH', 'RPXETH', 'NCASHETH', 'POAETH', 'ZILETH', 'ONTETH', 'STORMETH',
  #         'XEMETH', 'WANETH', 'WPRETH', 'QLCETH', 'SYSETH', 'GRSETH', 'CLOAKETH', 'GNTETH',
  #         'LOOMETH', 'BCNETH', 'REPETH', 'TUSDETH', 'ZENETH', 'SKYETH', 'CVCETH', 'THETAETH',
  #         'IOTXETH', 'QKCETH', 'AGIETH', 'NXSETH', 'DATAETH', 'SCETH', 'NPXSETH', 'KEYETH',
  #         'NASETH', 'MFTETH', 'DENTETH', 'ARDRETH', 'HOTETH', 'VETETH', 'DOCKETH', 'PHXETH',
  #         'HCETH', 'PAXETH', 'STMXETH', 'WBTCETH', 'SCRTETH', 'AAVEETH']
  # bnbx = ['VENBNB', 'YOYOBNB', 'POWRBNB', 'NULSBNB', 'RCNBNB', 'RDNBNB', 'DLTBNB', 'WTCBNB',
  #         'AMBBNB', 'BCCBNB', 'BATBNB', 'BCPTBNB', 'NEOBNB', 'QSPBNB', 'BTSBNB', 'XZCBNB',
  #         'LSKBNB', 'IOTABNB', 'ADXBNB', 'CMTBNB', 'XLMBNB', 'CNDBNB', 'WABIBNB', 'LTCBNB',
  #         'WAVESBNB', 'GTOBNB', 'ICXBNB', 'OSTBNB', 'AIONBNB', 'NEBLBNB', 'BRDBNB', 'MCOBNB',
  #         'NAVBNB', 'TRIGBNB', 'APPCBNB', 'RLCBNB', 'PIVXBNB', 'STEEMBNB', 'NANOBNB', 'VIABNB',
  #         'BLZBNB', 'AEBNB', 'RPXBNB', 'NCASHBNB', 'POABNB', 'ZILBNB', 'ONTBNB', 'STORMBNB',
  #         'QTUMBNB', 'XEMBNB', 'WANBNB', 'SYSBNB', 'QLCBNB', 'ADABNB', 'GNTBNB', 'LOOMBNB',
  #         'BCNBNB', 'REPBNB', 'TUSDBNB', 'ZENBNB', 'SKYBNB', 'EOSBNB', 'CVCBNB', 'THETABNB',
  #         'XRPBNB', 'AGIBNB', 'NXSBNB', 'ENJBNB', 'TRXBNB', 'ETCBNB', 'SCBNB', 'NASBNB',
  #         'MFTBNB', 'ARDRBNB', 'VETBNB', 'POLYBNB', 'PHXBNB', 'GOBNB', 'PAXBNB', 'RVNBNB',
  #         'DCRBNB', 'USDCBNB', 'MITHBNB', 'RENBNB', 'BTTBNB', 'ONGBNB', 'HOTBNB', 'ZRXBNB',
  #         'FETBNB', 'XMRBNB', 'ZECBNB', 'IOSTBNB', 'CELRBNB', 'DASHBNB', 'OMGBNB', 'MATICBNB',
  #         'ATOMBNB', 'PHBBNB', 'TFUELBNB', 'ONEBNB', 'FTMBNB', 'ALGOBNB', 'ERDBNB', 'DOGEBNB',
  #         'DUSKBNB', 'ANKRBNB', 'WINBNB', 'COSBNB', 'COCOSBNB', 'TOMOBNB', 'PERLBNB', 'CHZBNB',
  #         'BANDBNB', 'BEAMBNB', 'XTZBNB', 'HBARBNB', 'NKNBNB', 'STXBNB', 'KAVABNB', 'ARPABNB',
  #         'CTXCBNB', 'BCHBNB', 'TROYBNB', 'VITEBNB', 'FTTBNB', 'OGNBNB', 'DREPBNB', 'TCTBNB',
  #         'WRXBNB', 'LTOBNB', 'STRATBNB', 'MBLBNB', 'COTIBNB', 'STPTBNB', 'SOLBNB', 'CTSIBNB',
  #         'HIVEBNB', 'CHRBNB', 'MDTBNB', 'STMXBNB', 'IQBNB', 'DGBBNB', 'COMPBNB', 'SXPBNB',
  #         'SNXBNB', 'VTHOBNB', 'IRISBNB', 'MKRBNB', 'DAIBNB', 'RUNEBNB', 'FIOBNB', 'AVABNB',
  #         'BALBNB', 'YFIBNB', 'JSTBNB', 'SRMBNB', 'ANTBNB', 'CRVBNB', 'SANDBNB', 'OCEANBNB',
  #         'NMRBNB', 'DOTBNB', 'LUNABNB', 'RSRBNB', 'PAXGBNB', 'WNXMBNB', 'TRBBNB', 'BZRXBNB',
  #         'SUSHIBNB', 'YFIIBNB', 'KSMBNB', 'EGLDBNB', 'DIABNB', 'BELBNB', 'WINGBNB', 'SWRVBNB',
  #         'CREAMBNB', 'UNIBNB', 'AVAXBNB', 'BAKEBNB', 'BURGERBNB', 'FLMBNB', 'CAKEBNB',
  #         'SPARTABNB', 'XVSBNB', 'ALPHABNB', 'AAVEBNB', 'NEARBNB', 'FILBNB', 'INJBNB']
  # usdtx = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'BCCUSDT', 'NEOUSDT', 'LTCUSDT', 'QTUMUSDT',
  #         'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'TUSDUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT',
  #         'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'VENUSDT', 'NULSUSDT', 'VETUSDT', 'PAXUSDT',
  #         'BCHABCUSDT', 'BCHSVUSDT', 'USDCUSDT', 'LINKUSDT', 'WAVESUSDT', 'BTTUSDT', 'USDSUSDT',
  #         'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT', 'ZECUSDT',
  #         'IOSTUSDT', 'CELRUSDT', 'DASHUSDT', 'NANOUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT',
  #         'MITHUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT',
  #         'USDSBUSDT', 'GTOUSDT', 'ERDUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT',
  #         'COSUSDT', 'NPXSUSDT', 'COCOSUSDT', 'MTLUSDT', 'TOMOUSDT', 'PERLUSDT', 'DENTUSDT',
  #         'MFTUSDT', 'KEYUSDT', 'STORMUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT',
  #         'CHZUSDT', 'BANDUSDT', 'BUSDUSDT', 'BEAMUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT',
  #         'HCUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT',
  #         'RLCUSDT', 'MCOUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'FTTUSDT',
  #         'EURUSDT', 'OGNUSDT', 'DREPUSDT', 'BULLUSDT', 'BEARUSDT', 'ETHBULLUSDT', 'ETHBEARUSDT',
  #         'TCTUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'EOSBULLUSDT',
  #         'EOSBEARUSDT', 'XRPBULLUSDT', 'XRPBEARUSDT', 'STRATUSDT', 'AIONUSDT', 'MBLUSDT',
  #         'COTIUSDT', 'BNBBULLUSDT', 'BNBBEARUSDT', 'STPTUSDT', 'WTCUSDT', 'DATAUSDT', 'XZCUSDT',
  #         'SOLUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT', 'BTCUPUSDT', 'BTCDOWNUSDT', 'GXSUSDT',
  #         'ARDRUSDT', 'LENDUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'REPUSDT', 'LRCUSDT',
  #         'PNTUSDT', 'COMPUSDT', 'BKRWUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'ETHUPUSDT',
  #         'ETHDOWNUSDT', 'ADAUPUSDT', 'ADADOWNUSDT', 'LINKUPUSDT', 'LINKDOWNUSDT', 'VTHOUSDT',
  #         'DGBUSDT', 'GBPUSDT', 'SXPUSDT', 'MKRUSDT', 'DAIUSDT', 'DCRUSDT', 'STORJUSDT',
  #         'BNBUPUSDT', 'BNBDOWNUSDT', 'XTZUPUSDT', 'XTZDOWNUSDT', 'MANAUSDT', 'AUDUSDT',
  #         'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'SRMUSDT',
  #         'ANTUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT',
  #         'RSRUSDT', 'PAXGUSDT', 'WNXMUSDT', 'TRBUSDT', 'BZRXUSDT', 'SUSHIUSDT', 'YFIIUSDT',
  #         'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMAUSDT', 'EOSUPUSDT',
  #         'EOSDOWNUSDT', 'TRXUPUSDT', 'TRXDOWNUSDT', 'XRPUPUSDT', 'XRPDOWNUSDT', 'DOTUPUSDT',
  #         'DOTDOWNUSDT', 'BELUSDT', 'WINGUSDT', 'LTCUPUSDT', 'LTCDOWNUSDT', 'UNIUSDT', 'NBSUSDT',
  #         'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'HNTUSDT', 'FLMUSDT', 'UNIUPUSDT', 'UNIDOWNUSDT',
  #         'ORNUSDT', 'UTKUSDT', 'XVSUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'SXPUPUSDT',
  #         'SXPDOWNUSDT', 'FILUSDT', 'FILUPUSDT', 'FILDOWNUSDT', 'YFIUPUSDT', 'YFIDOWNUSDT',
  #         'INJUSDT']
