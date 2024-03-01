import dash_bootstrap_components as dbc
import polars as pl
from dash import dcc, html, Output, Input
from polygon_app import *
from dash_iconify import DashIconify


layout = dbc.Col([
        dbc.Card([
            dbc.CardImg(src="/assets/logo.svg", top=True,class_name="img"),
            html.H6("Dash Polygon App", className="card-subtitle",style={"text-align":"center"}),
            html.Hr(),
            html.H6("Provide the parameters below to display the map:",
                     className="card-subtitle",style={"text-align":"center"}),
            dbc.CardBody([
                dcc.Dropdown(id="uf-dropdown",
                            className="dbc", placeholder="Select UF",
                            #  options=[{'label':i, 'value':i} for i in uf_options] ,
                            ),
                html.Br(className="dbc",),
                dcc.Dropdown(id="cidade-dropdown",
                            className="dbc", placeholder="Select City",
                            multi=True
                            ),
                html.Br(),
                dbc.Button("Apply", id="filter-btn",color="success", className="dbc")
            ]),
            dbc.CardFooter([
                dcc.Markdown("Developed by *Allan Ribeiro*"),
                dbc.Row([
                    dbc.Col([
                        html.A(children=[
                            DashIconify(icon="ion:logo-github", width=30)
                            ], href="https://github.com/adsribeiro", target="_blank")
                        ]),
                    dbc.Col([
                        html.A(children=[
                            DashIconify(icon="ion:logo-linkedin", width=30)
                            ], href="https://www.linkedin.com/in/allan-ribeiro-22726586", target="_blank")
                        ]),
                    dbc.Col([
                        html.A(children=[
                            DashIconify(icon="ion:logo-instagram", width=30)
                            ], href="https://www.instagram.com/cer_solucoeparaempresas?igsh=ajkxd3NiN2g3dTMy", target="_blank")
                        ]),

                ])
            ]),

        ],class_name=".card",style={"height":"90vh"})
    ],xs=12, sm=12,md=2,lg=2,xl=2)

# Load Dropdown UF
@app.callback(
        Output('uf-dropdown', 'options'),
        Input('uf-store', 'data'),
        prevent_initial_call=False
              )
def load_dropdown_estados(data):
    uf_options = pl.DataFrame(data)
    options = [{'label':i, 'value':i} for i in uf_options.to_series().to_list()]
    return options

# Load Dropdown Cidades
@app.callback(
            Output('cidade-dropdown', 'options'),
            Output('cidade-dropdown', 'value'),
            Input('uf-dropdown', 'value'),
            prevent_initial_call=False
              )
def update_cidades(uf):
    if uf:
        options_cidades = (
        options
        .filter(pl.col("uf")==uf)
        .select(pl.col("municipio").unique())
        .sort("municipio")
        .collect()
        .to_series()
        .to_list()
    ) 
        cidades = sorted([{'label':i, 'value':i} for i in options_cidades], key=lambda d: d['value'])
        return cidades,[]
    else:
        return [],[]


# Enable Filter
@app.callback(
     Output('filter-btn', 'disabled'),
     Input('uf-dropdown', 'value'),
     Input('cidade-dropdown', 'value'),
)
def enable_filter(uf,cidades):
    if not cidades:
        return True
    else:
        False

    