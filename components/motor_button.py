from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


def render(app: Dash) -> dbc.Row:
    @app.callback(
        Output("motor-switch", "label"),
        Input("motor-switch", "value"),
    )
    def update_motor_switch_label(value: bool) -> str:
        return "ON" if value else "OFF"
    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    label="On",
                    value=False,
                    className="mx-auto"  # Add this line
                ),
                width="auto",  # Add this line
                className="d-flex justify-content-center align-items-center"  # Add this line
            )
        ],
        className="justify-content-center align-items-center fs-1"
    )
