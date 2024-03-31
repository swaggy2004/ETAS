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
        label_position = "right" if switch_value else "left"
        return label_text, label_position

    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label(id="motor-switch-label"),
                    dcc.Switch(
                        id="motor-switch",
                        value=False,
                        className="mx-auto",
                        labelClassName="switch-label",
                        labelPosition="left",  # Set initial labelPosition to "left"
                    ),
                ],
                width="auto",
                className="d-flex justify-content-center align-items-center",
            )
        ],
        className="justify-content-center align-items-center fs-1",
    )
