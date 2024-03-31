from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


def render(app: Dash) -> dbc.Row:
    @app.callback(
        Output("motor-switch-label", "children"),
        Input("motor-switch", "value"),
    )
    def toggle_label(switch_value):
        if switch_value:
            return "ON"
        else:
            return "OFF"

    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label(id="motor-switch-label"),
                    dbc.Switch(
                        id="motor-switch",
                        value=False,
                        className="mx-auto",
                        labelClassName="switch-label",
                        labelPosition="start" if not switch_value else "end",
                    ),
                ],
                width="auto",
                className="d-flex justify-content-center align-items-center",
            )
        ],
        className="justify-content-center align-items-center fs-1",
    )
