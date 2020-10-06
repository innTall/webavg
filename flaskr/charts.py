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


def candlestick_chart(var_can):
  gc = var_can[0]
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
  y7 = gc['perc']
  y8 = gc['ao'] #gc['ao'] = ta.utils.dropna(gc['ao'])
  y9 = gc['rsi'] #gc['rsi'] = ta.utils.dropna(gc['rsi'])
    
  gc = fig.add_trace(
    go.Candlestick(x=x, open=y1, high=y2, low=y3, close=y4, name='candles',
                  line = dict(width=1),
                  increasing = dict(
                    line = dict(color = '#008000', width = 1)
                  ),
                  decreasing = dict(
                    line = dict(color = '#FF0000', width = 1)
                  )), row=1, col=1
  )
  
  gc = fig.add_trace(go.Line(x=x, y=y5, name='volbuy',
                        line = dict(width = 1, color = '#006400')
                        ), row=3, col=1, secondary_y=False
  )
             
  gc = fig.add_trace(go.Line(x=x, y=y6, name='volsell',
                        line = dict(width = 1, color = '#FF0000')
                        ), row=3, col=1, secondary_y=False
  )
          
  gc = fig.add_trace(go.Bar(x=x, y=y7, name='delta%',
                      marker = dict(
                        line = dict(width = 1, color = '#6A5ACD')
                      )), row=3, col=1, secondary_y=True
  )
  
  gc = fig.add_trace(go.Bar(x=x, y=y8, name='ao',
                      marker = dict(
                        line=dict(width = 0.8, color = '#228B22')
                      )), row=4, col=1, secondary_y=False
  )

  gc = fig.add_trace(go.Line(x=x, y=y9, name='rsi',
                        line = dict(width = 1, color = '#FF0000')
                      ), row=4, col=1, secondary_y=True
  )
            
  fig.update_layout(xaxis_rangeslider_visible=False,   #line_width=0.6
                  paper_bgcolor='rgba(0,0,0,0)',
                  plot_bgcolor='rgba(0,0,0,0)',
                  shapes=[dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=fd, y0=avc, x1=ld, y1=avc, line_color = '#A9A9A9',
                          line = dict(dash='solid')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=fd, y0=mic, x1=ld, y1=mic, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=fd, y0=buyd, x1=ld, y1=buyd, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=fd, y0=selld, x1=ld, y1=selld, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=fd, y0=buyu, x1=ld, y1=buyu, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=fd, y0=sellu, x1=ld, y1=sellu, line_color = '#A9A9A9',
                          line = dict(dash='dot')),
                        dict(type='line', xref='x1', yref='y1', line_width=0.8,
                          x0=fd, y0=mac, x1=ld, y1=mac, line_color = '#A9A9A9',
                          line = dict(dash='dot'))],
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
 
  graphJSON = json.dumps(gc, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def order_chart(tot2, f8t, f11t, tot3, lp, mit, mat, avt, scat, buyd, selld, buyu, sellu,
fd, ld, avb, mab, avs, mas, absma, miav, vav, a15):

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

def simple_chart(var_can):

  x = gc['date']
  y1 = gc['open']
  y2 = gc['high']
  y3 = gc['low']
  y4 = gc['close']
  
  gc = go.Figure(go.Candlestick(
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
                  margin=dict(l=0, r=0, t=0, b=0))
  )
  graphJSON = json.dumps(gc, cls=plotly.utils.PlotlyJSONEncoder)
  return graphJSON

def timec(gc):

  gc = go.Figure(go.Table(
    header=dict(values=list(gc.columns),
                fill_color='DodgerBlue',
                align='left'),
    cells=dict(values=[gc.date, gc.price, gc.buy, gc.sell, gc.perc],
               fill_color='Gainsboro',
               align='left'))
  )
  json = gc.to_json() 
  return json 
  
def pricec(f8t):

  f8t = go.Figure(go.Table(
    header=dict(values=list(f8t.columns),
                fill_color='DodgerBlue',
                align='left'),
    cells=dict(values=[f8t.price, f8t.buy, f8t.sell],
               fill_color='Gainsboro',
               align='left'))
  )
  json = f8t.to_json() 
  return json 

def ordert(f11t):

  f11t = go.Figure(go.Table(
    header=dict(values=list(f11t.columns),
                fill_color='DodgerBlue',
                align='left'),
    cells=dict(values=[f11t.date, f11t.price, f11t.buy, f11t.sell],
               fill_color='Gainsboro',
               align='left'))
  )
  json = f11t.to_json() 
  return json
  
'''
  var_can = gc, piv, lpc, mic, mac, avc, scac, buyd, selld, buyu, sellu, nums,
  fd, ld, vma, vmb, vms, vbs, vav, dmb, dms, dbs
  
  
  json_table = gc.to_json(orient = 'table')
  return json_table
  
  ["data"],
                   columns=[{"title": str(col)} for col in json.loads(df.to_json(orient="split"))["columns"]])


  gc = fig.add_trace(go.Bar(x=y0, y=x0, name='volprice', orientation='h',
                      marker = dict(
                        line = dict(width = 1, color = '#6A5ACD')
                      )), row=1, col=1, #secondary_x=True
  )

   #dict(type='line', xref='x4', yref='y4', name='rsi', line_width=0.8,
                          #x0=fd, y0=30, x1=ld, y1=30, line_color='#A9A9A9',
                          #line = dict(dash='dot')),
                        #dict(type='line', xref='x4', yref='y4', name='rsi', line_width=0.8,
                          #x0=fd, y0=70, x1=ld, y1=70, line_color='#A9A9A9',
                          #line = dict(dash='dot'))],

  #row_heights=[0.6, 0.2, 0.2], # относительная высота строк Subplot
  # Set y-axes titles
  #fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
  #fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

# fig.show()
# fig.update_layout(height=600, width=600, title_text="specs examples")
   
# py.image.save_as({'data':data}, 'scatter_plot', format='png')
# py.image.save_as(fig, 'my_plot.png')
'''