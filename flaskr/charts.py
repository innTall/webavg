from datetime import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame as df
from pandas import Series
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import ta
import math as m
import json

def candlestick_chart(gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums,
fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs):

  fig = make_subplots(rows=4, cols=1,
    shared_xaxes=True, # связывание осей x
    vertical_spacing=0.02, # интервал по вертикали
    print_grid=True, # текстовое представление Subplot   {'rowspan': 2}
    specs=[[{'rowspan': 2}],
          [None],
          [{'secondary_y': True}],
          [{'secondary_y': True}]
    ]
  )
  
  x = gc['date']
  y1 = gc['open']
  y2 = gc['high']
  y3 = gc['low']
  y4 = gc['close']
  y5 = gc['buy']
  y6 = gc['sell']
  y7 = gc['%']
  y8 = gc['ao'] #gc['ao'] = ta.utils.dropna(gc['ao'])
  y9 = gc['rsi'] #gc['rsi'] = ta.utils.dropna(gc['rsi'])
    
  gc = fig.add_trace(
    go.Candlestick(
      x=x,
      open=y1,
      high=y2,
      low=y3,
      close=y4
    )
  )
  
  gc = fig.add_trace(go.Scatter(
        x=x, y=y5, name='volbuy'), row=3, col=1, secondary_y=False)
         
  gc = fig.add_trace(go.Scatter(
        x=x, y=y6, name='volsell'), row=3, col=1, secondary_y=False)
          
  gc = fig.add_trace(go.Bar(
        x=x, y=y7, name='delta%'), row=3, col=1, secondary_y=True)
  
  gc = fig.add_trace(go.Scatter(
        x=x, y=y8, name='ao'), row=4, col=1, secondary_y=False)
  
  gc = fig.add_trace(go.Scatter(
        x=x, y=y9, name='rsi'), row=4, col=1, secondary_y=True)

  fig.update_layout(xaxis_rangeslider_visible=False,
                  xaxis = dict(
                    showgrid = False,
                    showline = False,
                    showticklabels = False,
                    gridwidth = 1
                  ),
                  yaxis = dict(
                    showgrid = False,
                    showline = True,
                    gridcolor = '#bdbdbd',
                    gridwidth = 1,
                    tickfont = dict(
                      family = 'Old Standard TT, serif',
                      size = 10,
                      color = 'blue'
                    )
                  ),
                  margin=dict(l=0, r=0, t=0, b=0))
 
  graphJSON = json.dumps(gc, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

  

  #row_heights=[0.6, 0.2, 0.2], # относительная высота строк Subplot
  # Set y-axes titles
  #fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
  #fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

# fig.show()
# fig.update_layout(height=600, width=600, title_text="specs examples")
   
# py.image.save_as({'data':data}, 'scatter_plot', format='png')
# py.image.save_as(fig, 'my_plot.png')
