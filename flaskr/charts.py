import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from frames import gc

def candlestick_chart(gc):
  data = go.Figure(
    data=[go.Candlestick(
      x=gc['date'],
      open=gc['open'],
      high=gc['high'],
      low=gc['low'],
      close=gc['close']
    )]
  )
  graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON
