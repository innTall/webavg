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

def candlestick_chart(variables_candles):
  f2c = variables_candles[0]
  mic = variables_candles[3]
  mac = variables_candles[4]
  avc = variables_candles[5]
  buyd = variables_candles[7]
  selld = variables_candles[8]
  buyu = variables_candles[9]
  sellu = variables_candles[10]
  ft = variables_candles[12]
  lt = variables_candles[13]
  averperc = variables_candles[19]

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
  
  x = f2c['date']
  y1 = f2c['open']
  y2 = f2c['high']
  y3 = f2c['low']
  y4 = f2c['close']
  y5 = f2c['buy']
  y6 = f2c['sell']
  y7 = f2c['perc']
  y8 = f2c['ao'] #f2c['ao'] = ta.utils.dropna(f2c['ao'])
  y9 = f2c['rsi'] #f2c['rsi'] = ta.utils.dropna(f2c['rsi'])
    
  f2c = fig.add_trace(
    go.Candlestick(x=x, open=y1, high=y2, low=y3, close=y4, name='candles',
                  line = dict(width=1),
                  increasing = dict(
                    line = dict(color = '#008000', width = 1)
                  ),
                  decreasing = dict(
                    line = dict(color = '#FF0000', width = 1)
                  )), row=1, col=1
  )
  
  f2c = fig.add_trace(go.Line(x=x, y=y5, name='volbuy',
                        line = dict(width = 1, color = '#006400')
                        ), row=3, col=1, secondary_y=False
  )
             
  f2c = fig.add_trace(go.Line(x=x, y=y6, name='volsell',
                        line = dict(width = 1, color = '#FF0000')
                        ), row=3, col=1, secondary_y=False
  )
          
  f2c = fig.add_trace(go.Bar(x=x, y=y7, name='volperc',
                      marker = dict(
                        line = dict(width = 1,
                        color=np.where(y7 > 0, '#1E90FF', '#FF00FF').tolist())
                      )), row=3, col=1, secondary_y=True
  )
  
  f2c = fig.add_trace(go.Bar(x=x, y=y8, name='ao',
                      marker = dict(
                        line=dict(width = 0.8, color = '#228B22')
                      )), row=4, col=1, secondary_y=False
  )

  f2c = fig.add_trace(go.Line(x=x, y=y9, name='rsi',
                        line = dict(width = 0.8, color = '#FF0000')
                        ), row=4, col=1, secondary_y=True
  )
              
  fig.update_layout(xaxis_rangeslider_visible=False,   #line_width=0.6
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  shapes = [
                          dict(name='candles', type='line',
                          xref='paper', yref='y', line_width=0.8,
                          x0=0, x1=1,
                          y0=y,
                          y1=y,
                          line_color='#A9A9A9', line=dict(dash='dot'))
                          for y in [avc, mic, buyd, selld, buyu, sellu, mac]
                  ],
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
 
  graphJSON = json.dumps(f2c, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def order_chart(variables_trades):
  f8t = variables_trades[1]
  fig = make_subplots(rows=3, cols=1,
    shared_xaxes=True, # связывание осей x
    vertical_spacing=0.02, # интервал по вертикали
    print_grid=True, # текстовое представление Subplot   {'rowspan': 2}
    specs=[[{'rowspan': 2}],
          [None],
          [{'secondary_y': True}],
    ]
  )
  
  x = f8t['date']
  x1 = f8t['market']
  y1 = f8t['price']
  y2 = f8t['buy']
  y3 = f8t['sell']

  f8t = fig.add_trace(go.Scatter(x=x, y=y1, name='price',
                        line = dict(width = 1, color = '#006400')
                        ), row=1, col=1, secondary_y=False
  )
             
  f8t = fig.add_trace(go.Scatter(x=x, y=y2, name='buyorder',
                        line = dict(width = 1, color = '#FF0000')
                        ), row=3, col=1, secondary_y=False
  )
          
  f8t = fig.add_trace(go.Bar(x=x, y=y3, name='sellorder',
                      marker = dict(
                        line = dict(width = 1, color = '#6A5ACD')
                      )), row=3, col=1, secondary_y=False
  )

  fig.update_layout(xaxis_rangeslider_visible=False,
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(l=0, r=0, t=0, b=0)
  )
  graphJSON = json.dumps(f8t, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def simple_chart(variables_candles):
  f2c = variables_candles[0]
  mic = variables_candles[3]
  mac = variables_candles[4]
  avc = variables_candles[5]
  buyd = variables_candles[7]
  selld = variables_candles[8]
  buyu = variables_candles[9]
  sellu = variables_candles[10]
  ft = variables_candles[12]
  lt = variables_candles[13]
  
  x = f2c['date']
  y1 = f2c['open']
  y2 = f2c['high']
  y3 = f2c['low']
  y4 = f2c['close']
  
  f2c = go.Figure(go.Candlestick(
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
                  shapes = [
                          dict(name='candles', type='line',
                          xref='paper', yref='y', line_width=0.8,
                          x0=0, x1=1,
                          y0=y,
                          y1=y,
                          line_color='#A9A9A9', line=dict(dash='dot'))
                          for y in [avc, mic, buyd, selld, buyu, sellu, mac]
                  ],
                  margin=dict(l=0, r=0, t=0, b=0))
  )
  graphJSON = json.dumps(f2c, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def candles_time(variables_candles):
  f2c = variables_candles[0]
  
  f2c = go.Figure(go.Table(
    header = dict(values = ['date', 'price', 'buy', 'sell', 'market', 'diff'],
                  line_color='#0000FF',
                  fill_color='#FFFFFF',
                  align=['center'],
                  font=dict(color='#0000FF', size=12)
                  ),
    cells = dict(values = [f2c.date, f2c.price, f2c.buy, f2c.sell, f2c.market],
                line_color='#1E90FF',
                fill_color='#FFFFFF',
                align = ['left', 'center'],
                font = dict(color = '#696969', size = 10)
                ),
    domain = dict(x=[0, 0.5], y=[0, 1]))
  )
  f2c.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(l=0, r=0, t=0, b=0)
  )
  graphJSON = json.dumps(f2c, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def candles_price(variables_candles):
  pivtab1 = variables_candles[1]
  
  pivtab1 = go.Figure(go.Table(
    header = dict(values = ['buy', 'sell', 'market', 'price', 'diff'],
                  line_color='#0000FF',
                  fill_color='#FFFFFF',
                  align=['center'],
                  font=dict(color='#0000FF', size=12)
                  ),
    cells = dict(values = [pivtab1.buy, pivtab1.sell, pivtab1.market],
                line_color='#1E90FF',
                fill_color='#FFFFFF',
                align = ['left', 'center'],
                font = dict(color = '#696969', size = 10)
                ),
    domain = dict(x=[0, 0.5], y=[0, 1]))
  )
  pivtab1.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(l=0, r=0, t=0, b=0)
  )
  graphJSON = json.dumps(pivtab1, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def trades_order(variables_trades):
  f10t = variables_trades[2]
  
  f10t = go.Figure(go.Table(
    header = dict(values = ['date', 'price', 'buy', 'sell', 'market', 'order'],
                  line_color='#0000FF',
                  fill_color='#FFFFFF',
                  align=['center'],
                  font=dict(color='#0000FF', size=12)
                  ),
    cells = dict(values = [f10t.date, f10t.price, f10t.buy, f10t.sell, f10t.market, f10t.order],
                line_color='#1E90FF',
                fill_color='#FFFFFF',
                align = ['left', 'center'],
                font = dict(color = '#696969', size = 10)
                ),
    domain = dict(x=[0, 0.5], y=[0, 1]))
  )
  f10t.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  margin=dict(l=0, r=0, t=0, b=0)
  )
  graphJSON = json.dumps(f10t, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON


'''
shapes=[dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=ft, y0=avc, x1=lt, y1=avc, line_color = '#A9A9A9',
                          line = dict(dash='solid')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=ft, y0=mic, x1=lt, y1=mic, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=ft, y0=buyd, x1=lt, y1=buyd, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=ft, y0=selld, x1=lt, y1=selld, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=ft, y0=buyu, x1=lt, y1=buyu, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=ft, y0=sellu, x1=lt, y1=sellu, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=ft, y0=mac, x1=lt, y1=mac, line_color = '#A9A9A9',
                          line = dict(dash='dot'))],

                      dict(type='line', xref='x1', yref='y7', name='volperc', line_width=0.8,
                          x0=ft, y0=averperc, x1=lt, y1=averperc, line_color='#0000CD',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x', yref='y9', name='rsi', line_width=0.8,
                          x0=ft, y0=30, x1=lt, y1=30, line_color='#0000CD',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x', yref='y9', name='rsi', line_width=0.8,
                          x0=ft, y0=70, x1=lt, y1=70, line_color='#0000CD',
                          line = dict(dash='dot'))],

  
  #row_heights=[0.6, 0.2, 0.2], # относительная высота строк Subplot
  # Set y-axes titles
  #fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
  #fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

# fig.show()
# fig.update_layout(height=600, width=600, title_text="specs examples")
   
# py.image.save_as({'data':data}, 'scatter_plot', format='png')
# py.image.save_as(fig, 'my_plot.png')
'''