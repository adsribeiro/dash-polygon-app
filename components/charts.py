from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

x = [1, 1.5, 2, 2.5,3,3.5]
y = [1,2,3,4,5,6]
fig = px.line(x = x, y=y)

def generate_chart():
   charts =  dbc.Row([
        dbc.Col([dcc.Graph(figure=fig,style={"height":"230px"})],lg=4,),
        dbc.Col([dcc.Graph(figure=fig,style={"height":"230px"})],lg=4,),
        dbc.Col([dcc.Graph(figure=fig,style={"height":"230px"})],lg=4,),
    ], class_name="row g-1")
   return charts