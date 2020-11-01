from datetime import datetime
from flask import Flask, jsonify
import numpy as np
import pandas as pd
from pandas import DataFrame as df
from pandas import Series
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import ta
import json

def candlestick_chart(frame1c):
      
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
  
  x = frame1c['date']
  y1 = frame1c['open']
  y2 = frame1c['high']
  y3 = frame1c['low']
  y4 = frame1c['close']
  y5 = frame1c['buy']
  y6 = frame1c['sell']
  y7 = frame1c['perc']
  y8 = frame1c['ao'] #frame1c['ao'] = ta.utils.dropna(frame1c['ao'])
  y9 = frame1c['rsi'] #frame1c['rsi'] = ta.utils.dropna(frame1c['rsi'])
    
  frame1c = fig.add_trace(
    go.Candlestick(x=x, open=y1, high=y2, low=y3, close=y4, name='candles',
                  line = dict(width=1),
                  increasing = dict(
                    line = dict(color = '#008000', width = 1)
                  ),
                  decreasing = dict(
                    line = dict(color = '#FF0000', width = 1)
                  )), row=1, col=1
  )
  
  frame1c = fig.add_trace(go.Line(x=x, y=y5, name='volbuy',
                        line = dict(width = 1, color = '#006400')
                        ), row=3, col=1, secondary_y=False
  )
             
  frame1c = fig.add_trace(go.Line(x=x, y=y6, name='volsell',
                        line = dict(width = 1, color = '#FF0000')
                        ), row=3, col=1, secondary_y=False
  )
          
  frame1c = fig.add_trace(go.Bar(x=x, y=y7, name='volperc',
                      marker = dict(
                        line = dict(width = 1,
                        color=np.where(y7 > 0, '#1E90FF', '#FF00FF').tolist())
                      )), row=3, col=1, secondary_y=True
  )
  
  frame1c = fig.add_trace(go.Bar(x=x, y=y8, name='ao',
                      marker = dict(
                        line=dict(width = 0.8, color = '#228B22')
                      )), row=4, col=1, secondary_y=False
  )

  frame1c = fig.add_trace(go.Line(x=x, y=y9, name='rsi',
                        line = dict(width = 0.8, color = '#FF0000')
                        ), row=4, col=1, secondary_y=True
  )
              
  fig.update_layout(xaxis_rangeslider_visible=False,   #line_width=0.6
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  # shapes = [
                  #         dict(name='candles', type='line',
                  #         xref='paper', yref='y', line_width=0.8,
                  #         x0=0, x1=1,
                  #         y0=y,
                  #         y1=y,
                  #         line_color='#A9A9A9', line=dict(dash='dot'))
                  #         for y in [avc, mic, buyd, selld, buyu, sellu, mac]
                  # ],
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
                  ), margin=dict(l=0, r=0, t=0, b=0)
  )
 
  graphJSON = json.dumps(frame1c, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def order_chart(frame7t):
  
  fig = make_subplots(rows=3, cols=1,
    shared_xaxes=True, # связывание осей x
    vertical_spacing=0.02, # интервал по вертикали
    print_grid=True, # текстовое представление Subplot   {'rowspan': 2}
    specs=[[{'rowspan': 2}],
          [None],
          [{'secondary_y': True}],
    ]
  )
  
  x = frame7t['date']
  x1 = frame7t['market']
  y1 = frame7t['price']
  y2 = frame7t['buy']
  y3 = frame7t['sell']

  frame7t = fig.add_trace(go.Scatter(x=x, y=y1, name='price',
                        line = dict(width = 1, color = '#006400')
                        ), row=1, col=1, secondary_y=False
  )
             
  frame7t = fig.add_trace(go.Scatter(x=x, y=y2, name='buyorder',
                        line = dict(width = 1, color = '#FF0000')
                        ), row=3, col=1, secondary_y=False
  )
          
  frame7t = fig.add_trace(go.Bar(x=x, y=y3, name='sellorder',
                      marker = dict(
                        line = dict(width = 1, color = '#6A5ACD')
                      )), row=3, col=1, secondary_y=False
  )

  fig.update_layout(xaxis_rangeslider_visible=False,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(l=0, r=0, t=0, b=0)
  )
  graphJSON = json.dumps(frame7t, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def simple_chart(frame1c):
    
  x = frame1c['date']
  y1 = frame1c['open']
  y2 = frame1c['high']
  y3 = frame1c['low']
  y4 = frame1c['close']
  
  frame1c = go.Figure(go.Candlestick(
                  x = x, open = y1, high = y2, low = y3, close = y4, name = 'btc',
                  line = dict(width=1),
                  increasing = dict(
                    line = dict(color = '#008000', width = 1)
                  ),
                  decreasing = dict(
                    line = dict(color = '#FF0000', width = 1)
                  )),           
                  layout = go.Layout(xaxis_rangeslider_visible=False,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  # shapes = [
                  #         dict(name='candles', type='line',
                  #         xref='paper', yref='y', line_width=0.8,
                  #         x0=0, x1=1,
                  #         y0=y,
                  #         y1=y,
                  #         line_color='#A9A9A9', line=dict(dash='dot'))
                  #         for y in [avc, mic, buyd, selld, buyu, sellu, mac]
                  #],
                  margin=dict(l=0, r=0, t=0, b=0))
  )
  graphJSON = json.dumps(frame1c, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def candles_time(frame1c):
    
  frame1c = go.Figure(go.Table(
    header = dict(values = ['date', 'price', 'buy', 'sell', 'market', 'diff'],
                  line_color='#0000FF',
                  fill_color='#FFFFFF',
                  align=['center'],
                  font=dict(color='#0000FF', size=12)
                  ),
    cells = dict(values = [frame1c.date, frame1c.price,
                 frame1c.buy, frame1c.sell, frame1c.market],
                line_color='#1E90FF',
                fill_color='#FFFFFF',
                align = ['left', 'center'],
                font = dict(color = '#696969', size = 10)
                ),
    domain = dict(x=[0, 1], y=[0, 1]))
  )
  frame1c.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(l=0, r=0, t=0, b=0)
  )
  graphJSON = json.dumps(frame1c, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def candles_price(total):
    
  total = go.Figure(go.Table(
    header = dict(values = ['buy', 'sell', 'market', 'price', 'diff'],
                  line_color='#0000FF',
                  fill_color='#FFFFFF',
                  align=['center'],
                  font=dict(color='#0000FF', size=12)
                  ),
    cells = dict(values = [total.buy, total.sell, total.market],
                line_color='#1E90FF',
                fill_color='#FFFFFF',
                align = ['left', 'center'],
                font = dict(color = '#696969', size = 10)
                ),
    domain = dict(x=[0, 1], y=[0, 1]))
  )
  total.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(l=0, r=0, t=0, b=0)
  )
  graphJSON = json.dumps(total, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def trades_order(frame10t):
    
  frame10t = go.Figure(go.Table(
    header = dict(values = ['date', 'price', 'buy', 'sell', 'market', 'order'],
                  line_color='#0000FF',
                  fill_color='#FFFFFF',
                  align=['center'],
                  font=dict(color='#0000FF', size=12)
                  ),
    cells = dict(values = [frame10t.date, frame10t.price, frame10t.buy,
                frame10t.sell, frame10t.market, frame10t.order],
                line_color='#1E90FF',
                fill_color='#FFFFFF',
                align = ['left', 'center'],
                font = dict(color = '#696969', size = 10)
                ),
    domain = dict(x=[0, 1], y=[0, 1]))
  )
  frame10t.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(l=0, r=0, t=0, b=0)
  )
  graphJSON = json.dumps(frame10t, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


                      # dict(type='line', xref='x1', yref='y7', name='volperc', line_width=0.8,
                      #     x0=ft, y0=averperc, x1=lt, y1=averperc, line_color='#0000CD',
                      #     line = dict(dash='dot')),
                      #   dict(type='line', xref='x', yref='y9', name='rsi', line_width=0.8,
                      #     x0=ft, y0=30, x1=lt, y1=30, line_color='#0000CD',
                      #     line = dict(dash='dot')),
                      #   dict(type='line', xref='x', yref='y9', name='rsi', line_width=0.8,
                      #     x0=ft, y0=70, x1=lt, y1=70, line_color='#0000CD',
                      #     line = dict(dash='dot'))],

  
  #row_heights=[0.6, 0.2, 0.2], # относительная высота строк Subplot
  # Set y-axes titles
  #fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
  #fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

# fig.show()
# fig.update_layout(height=600, width=600, title_text="specs examples")
   
# py.image.save_as({'data':data}, 'scatter_plot', format='png')
# py.image.save_as(fig, 'my_plot.png')
