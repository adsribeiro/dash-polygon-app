from dash import Dash, Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import polars as pl
from components import map, sidebar
from polygon_app import *


# Data Ingestion
uf_options = (
        options
        .filter(pl.col("uf")!="TR")
        .select(pl.col("uf").cast(pl.Utf8).unique())
        .sort("uf")
        .collect()
        .to_dicts()
)

# Layout
app.layout = dbc.Container([
    dcc.Store(id="uf-store", data=uf_options),
dbc.Row([
    sidebar.layout,
    map.layout

])
], fluid=True, style={"padding":"10px"})


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8080", debug=False)