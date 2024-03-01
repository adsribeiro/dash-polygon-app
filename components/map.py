import plotly.express as px
import polars as pl
import geopandas as gpd
import dash_bootstrap_components as dbc
from dash import dcc, Output, Input, State
from polygon_app import *

token = open("./assets/mapbox_token").read() # you will need your own token
config = {"displayModeBar":False}

layout = dbc.Col([
        dbc.Card([
            dcc.Loading(dcc.Graph(id="polygon-map",  style={"height":"90vh"}, config=config, className="dbc"))
        ], class_name=".card")
    ],xs=12, sm=12,md=10,lg=10,xl=10)

@app.callback(
    Output("polygon-map", "figure"),
    Input("filter-btn","n_clicks"),
    State("uf-dropdown","value"),
    State("cidade-dropdown","value"),
    prevent_initial_callbacks=False
)
def update_map(n_clicks,uf, cidades):
    if n_clicks:
        geo_df = (
        options
        .drop_nulls("geometry")
        .with_columns(
            pl.col("status").replace({"Ativo":"Active","Inativo":"Inactive"}).cast(pl.Categorical)
                )
        .filter((pl.col("uf")==uf) & (pl.col("municipio").is_in(cidades)))
        ).collect().rename({"geometry":"polygon"}).to_pandas()
        geo_df['geometry'] = gpd.GeoSeries.from_wkt(geo_df.polygon)
        geo_df = gpd.GeoDataFrame(geo_df)
        lon = geo_df.query('uf == @uf').geometry.centroid.x.mean()
        lat = geo_df.query('uf == @uf').geometry.centroid.y.mean()
        fig = px.choropleth_mapbox(
        geo_df,geojson=geo_df.geometry,
                            locations=geo_df.index,
                            color="status",
                            color_discrete_map={"Inactive": "red","Active": "blue"},
                            category_orders={"status":["Active","Inactive"]},
                            center={"lat":lat, "lon":lon},
                                zoom=8,mapbox_style="dark", opacity=0.2,
                                hover_data={
                                    'id':True,
                                    'nome':True,
                                    'localidade':True,
                                    'municipio':True,
                                    'uf':True,
                                    'area_m2':True,
                                    'data_criacao':True,
                                    'data_lteracao':True,
                                    'status':True})
        fig.update_layout(mapbox_accesstoken=token, margin = dict(t=0, l=0, r=0, b=0),paper_bgcolor = '#73736e',
                            autosize=True,legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01,
                            bgcolor='#4A4A4A', bordercolor="gray",orientation="h",
        borderwidth=2,itemsizing = 'constant'),
        font=dict(size=12, color="white"))
        fig.update_traces(marker_line={'color':'#cfcfc4','width': 1.5})
        return fig
    else:
        fig = px.choropleth_mapbox(
                            center={"lat":-15.793889, "lon":-47.882778},zoom=4,mapbox_style="dark",)
        fig.update_layout(mapbox_accesstoken=token, margin = dict(t=0, l=0, r=0, b=0),paper_bgcolor = '#73736e',
                autosize=True)
        return fig
