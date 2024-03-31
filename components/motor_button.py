from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


def render(app: Dash) -> dbc.Row:
    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    label="On",
                    value=False,
                    className="mx-auto"
                ),
                width="auto",
                className="d-flex justify-content-center align-items-center"
            )
        ],
        className="justify-content-center align-items-center fs-1"
    )
