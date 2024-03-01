from dash import Dash
import dash_bootstrap_components as dbc
import polars as pl

options = pl.scan_parquet("./datasets/poligonos_tratado.parquet")
template_theme1 = "darkly"
url_theme1 = dbc.themes.DARKLY

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(external_stylesheets=[url_theme1,dbc_css], title="Dash Polygon App")
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
server = app.server
