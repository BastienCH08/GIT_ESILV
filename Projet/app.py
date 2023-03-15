import pandas as pd
from dash import Dash, dcc, html
import matplotlib.pyplot as plt
import plotly as plt
import plotly.express as px
import datetime as dt
import time

app = Dash(__name__)
app.title = "Dashboard"


def serve_layout():
   # Dataframe preparation
   df = pd.read_csv("/home/ubuntu/GIT_ESILV/Projet/out.csv", header = None, sep = ';', decimal = ',')
   df.columns = ["Date", "EUR/USD"]
   df["Date"] = pd.to_datetime(df["Date"], format= "%Y/%m/%d %H:%M")
   # Day by day
   day_by_day = pd.DataFrame()
   day_by_day["DailyPrice"] = df.groupby(df["Date"].dt.date)['EUR/USD'].mean()
   day_by_day.index = pd.to_datetime(day_by_day.index, format= "%Y-%m-%d")
   fig2 = px.area(day_by_day["DailyPrice"])
   fig2.update_layout(yaxis_range=[0.999*min(day_by_day["DailyPrice"]),1.001*max(day_by_day["DailyPrice"])])
   fig2.update_layout(template = "plotly_white")
   fig2.update_layout(showlegend = False, yaxis_title="",xaxis_title="")
   fig2.update_traces(line_color = "steelblue")
   daily_summary = df.groupby('Date').mean()   
   # Intraday
   intraday = pd.DataFrame()
   specific_date = pd.to_datetime(df["Date"][df.shape[0] - 1])
   intraday = df.loc[df['Date'].dt.date == specific_date.date()]
   intraday.index = pd.to_datetime(intraday["Date"], format= "%Y-%m-%d %H:%M")
   intraday = intraday.drop("Date", axis = 1)
   fig3 = px.area(intraday["EUR/USD"])
   fig3.update_layout(yaxis_range=[0.999*min(intraday["EUR/USD"]),1.001*max(intraday["EUR/USD"])])
   fig3.update_layout(template = "plotly_white")
   fig3.update_layout(showlegend = False, yaxis_title="",xaxis_title="")
   fig3.update_traces(line_color = "steelblue")
   #previous day
   prev_day = pd.DataFrame()
   yesterday = pd.to_datetime(df["Date"][df.shape[0] - 1-287])
   prev_day = df.loc[df['Date'].dt.date == yesterday]
   prev_day.index = pd.to_datetime(prev_day["Date"], format= "%Y-%m-%d %H:%M")
   prev_day = prev_day.drop("Date", axis = 1)
   mean = round(prev_day["EUR/USD"].mean(),5)
   std = round(prev_day["EUR/USD"].std(),5)
   lower = prev_day["EUR/USD"].min()
   higher = prev_day["EUR/USD"].max()
   close = prev_day["EUR/USD"][-1]
   open = prev_day["EUR/USD"][0]
   return  html.Div(
       style={'fontFamily': 'Helvetica',"textAlign": "center", "color" : "steelblue"},
       children=[
           html.H1 # Title
           (
               children="Dashboard Currency Exchange Rate"
           ),
           html.Hr # Horizontal line
           (
               style={"color" : "steelblue", "background-color" : "steelblue" , "border" : 0, "height" : "2px"}
           ),
           html.Div
           (
               [
                   html.Div
                   (
                       [
                           html.H2 # Paragraph
                           (
                               "Intraday EUR:USD currency rate",
                               style={"align": "top"}
                           ),
                           dcc.Graph # Day by day Graphic
                           (
                               figure= fig3
                           ), 
                       ],
                       style= {'display': 'inline-block', 'verticalAlign': 'top', "width" : "70%"}
                   ),
                   html.Hr
                   (
                       style={"margin-left": "20px","margin-right": "20px",'verticalAlign': 'top',"color" : "steelblue", "background-color" : "steelblue" , "border" : 0,"border-left":"1px" ,"width" : "2px","height": "500px",'display': 'inline-block'}
                   ),
                   html.Div
                   (
                       [
                           html.H2
                           (
                               "Summary of previous day",
                           ),
                           html.Table # Summary
                           (
                               [
                                   html.Tbody
                                   (
                                       [
                                           html.Tr
                                           (
                                               [
                                                   html.Td('Mean'), 
                                                   html.Td(mean)
                                               ],
                                           ),
                                           html.Tr
                                           (
                                               [
                                                   html.Td('StD'), 
                                                   html.Td(std)
                                               ],
                                           ),
                                           html.Tr
                                           (
                                               [
                                                   html.Td('Lower'), 
                                                   html.Td(lower)
                                               ],
                                           ),
                                           html.Tr
                                           (
                                               [
                                                   html.Td('Higher'), 
                                                   html.Td(higher)
                                               ],
                                           ),
                                           html.Tr
                                           (
                                               [
                                                   html.Td('Open'), 
                                                   html.Td(open)
                                               ],
                                           ),
                                           html.Tr
                                           (
                                               [
                                                   html.Td('Close'), 
                                                   html.Td(close)
                                               ],
                                           ),
                                       ],
                                       style={'font_size': '26px',"border": "1px" ,"textAlign" : "left"}
                                   ),
                               ],
                           )
                       ],
                       style= {'display': 'inline-block','verticalAlign': 'top',"width" : "20%", "margin-left" : "10px"}
                   ),  
               ],
           ),
           html.Hr # Horizontal line
           (
               style={"color" : "steelblue", "background-color" : "steelblue" , "border" : 0, "height" : "2px"}
           ),
           html.Div
           (
               [
                   html.H2 # Paragraph
                   (
                        "Daily average EUR:USD currency rate",
                        style={"align": "top"}
                   ),
                   dcc.Graph # Day by day Graphic
                   (
                        figure= fig2
                   ), 
               ],
               style= {'display': 'inline-block', 'verticalAlign': 'top', "width": "100%"}
           ), 
       ]
   )

app.layout = serve_layout

if __name__ == "__main__":
   app.run_server(host = "0.0.0.0", port = 8050)
   time.sleep(60)
