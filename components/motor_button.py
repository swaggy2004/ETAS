from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc


def render(app: Dash) -> dbc.Row:
    @app.callback(
        [Output("motor-switch-label", "children"),
         Output("motor-switch", "labelPosition")],
        Input("motor-switch", "value"),
    )
    def toggle_label(switch_value):
        label_text = "ON" if switch_value else "OFF"
        label_position = "end" if switch_value else "start"
        return label_text, label_position

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
                        labelPosition="start",  # Set initial labelPosition to "start"
                    ),
                ],
                width="auto",
                className="d-flex justify-content-center align-items-center",
            )
        ],
        className="justify-content-center align-items-center fs-1",
    )
