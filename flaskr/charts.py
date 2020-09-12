from datetime import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame as df
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# from flaskr.frames import base_tabel_of_candles
from flaskr.frames import variables_for_plots_of_volume_candles
import json

def candlestick_chart(frame_c3):

  fig = make_subplots(rows=4, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.02,
    print_grid=True,
    specs=[[{'rowspan': 2}],
        [None],
        [{'rowspan': 1}],
        [{'rowspan': 1}],
    ]
  )
  
  data = fig.add_trace(
    go.Candlestick(
      x=frame_c3['date'],
      open=frame_c3['open'],
      high=frame_c3['high'],
      low=frame_c3['low'],
      close=frame_c3['close'],
    )
  )

  fig.add_trace(go.Scatter(x=frame_c3['date'], y=[5, 13], name='volume'), row=3, col=1)
  fig.add_trace(go.Scatter(x=frame_c3['date'], y=[0.2, 0.8], name='rsi'), row=4, col=1)

  fig.update_layout(xaxis_rangeslider_visible=False)

  graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

# fig.show()
# fig.update_layout(height=600, width=600, title_text="specs examples")
   
# py.image.save_as({'data':data}, 'scatter_plot', format='png')
# py.image.save_as(fig, 'my_plot.png')
