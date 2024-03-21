from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


def render(app: Dash) -> dbc.Row:
    return dbc.Row([
        dbc.Switch(
            id="motor-switch",
            label="On",
            value=False,
        ),
    ],
        className="text-center fs-2"
)
