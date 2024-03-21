from dash import Dash, html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import imports
import plotly.express as px

fig = px.density_mapbox(center=dict(lat=6.820854124676803, lon=80.03954479062239), zoom=18,
                        mapbox_style="open-street-map")

def render_map(app:Dash) -> imports.dbc.Row:
    return imports.dbc.Row([
        dcc.Graph(figure=fig)
    ])