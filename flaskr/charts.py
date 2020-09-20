from datetime import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame as df
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

def candlestick_chart(candle_data):

  fig = make_subplots(rows=4, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
    print_grid=True,
    specs=[[{'rowspan': 2}],
        [None],
        [{'rowspan': 1}],
        [{'rowspan': 1}]],
    )
  
  data = candle_data
  data = fig.add_trace(
    go.Candlestick(
      x=data['date'],
      open=data['open'],
      high=data['high'],
      low=data['low'],
      close=data['close']
    )
  )

  fig.add_trace(go.Scatter(x=['date'], y=[5, 13], name='volume'), row=3, col=1)
  fig.add_trace(go.Scatter(x=['date'], y=[0.2, 0.8], name='rsi'), row=4, col=1)

  fig.update_layout(xaxis_rangeslider_visible=False,
                  margin=dict(l=0, r=0, t=0, b=0))
  
  graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

# fig.show()
# fig.update_layout(height=600, width=600, title_text="specs examples")
   
# py.image.save_as({'data':data}, 'scatter_plot', format='png')
# py.image.save_as(fig, 'my_plot.png')
