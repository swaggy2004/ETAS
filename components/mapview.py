from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

token = "e84ee379-3451-4256-a488-7987b44674fd"

fig = px.density_mapbox(center=dict(lat=6.820854124676803, lon=80.03954479062239), zoom=18,
                        mapbox_style="stamen-terrain")

fig.update_layout(mapbox_accesstoken=token)

def render_map(app:Dash) -> dbc.Row:
    return dbc.Row([
        dcc.Graph(figure=fig)
    ])