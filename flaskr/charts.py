import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

def candlestick_chart(frame_c3):
  data = go.Figure(
    data=[go.Candlestick(
      x=frame_c3['date'],
      open=frame_c3['open'],
      high=frame_c3['high'],
      low=frame_c3['low'],
      close=frame_c3['close']
    )]
  )
  graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON
