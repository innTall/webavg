from datetime import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame as df
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math as m
import json

def candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums,\
 fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs):

  fig = make_subplots(rows=4, cols=1,
    shared_xaxes=True, # связывание осей x
    vertical_spacing=0.02, # интервал по вертикали
    print_grid=True, # текстовое представление Subplot
    specs=[[{'rowspan': 2}],
          [None],
          [{'rowspan': 1}], # ], Create figure with secondary y-axis
          [{'rowspan': 1}], # {'secondary_y': False}
          ] 
  )
  
  data = gc
  data = fig.add_trace(
    go.Candlestick(
      x=data['date'],
      open=data['open'],
      high=data['high'],
      low=data['low'],
      close=data['close']),
      secondary_y=False
  )
  
  data = gc
  data = fig.add_trace(go.Scatter(
        x=data['date'], y=data['buy'], name='volbuy'),
        row=3, col=1
  )     , #, secondary_y=False)
        # ) range=[0, vbs]
  
  data = gc
  data = fig.add_trace(go.Scatter(
        x=data['date'], y=data['sell'], name='volsell'),
        row=3, col=1, #, secondary_y=False
  )
        # ) range=[0, vbs],

  data = gc
  data = fig.add_trace(go.Bar(
        x=data['date'], y=data['%'], name='delta%'), 
        row=3, col=1 #, secondary_y=True
  )

  data = gc
  data = fig.add_trace(go.Scatter(
        x=data['date'], y=data['sell'], name='macd'), row=4, col=1)

  data = gc
  data = fig.add_trace(go.Scatter(
        x=data['date'], y=data['buy'], name='rsi'), row=4, col=1)
  
  fig.update_layout(xaxis_rangeslider_visible=False,
                  margin=dict(l=0, r=0, t=0, b=0))

  graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON
  
  
  #row_heights=[0.6, 0.2, 0.2], # относительная высота строк Subplot
  # Set y-axes titles
  #fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
  #fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

# fig.show()
# fig.update_layout(height=600, width=600, title_text="specs examples")
   
# py.image.save_as({'data':data}, 'scatter_plot', format='png')
# py.image.save_as(fig, 'my_plot.png')
