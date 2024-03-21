from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


def render(app: Dash) -> dbc.Row:
    return dbc.Row([
        dbc.Checklist(
            options=[{"Pump": "On", "value": 0},],
            value=0,
            id="motor-button",
            switch=True
        )
    ])
