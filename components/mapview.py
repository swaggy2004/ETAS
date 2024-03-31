from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

fig = px.density_mapbox(center=dict(lat=6.820854124676803, lon=80.03954479062239), zoom=18,
                        mapbox_style="stamen-terrain")

def render_map(app:Dash) -> dbc.Row:
    return dbc.Row([
        dcc.Graph(figure=fig)
    ])