from dash import Dash, html, dcc
import imports as imports
import components.ids as ids
import dash_bootstrap_components as dbc


def render(app: Dash) -> imports.dbc.Row:
    return imports.dbc.Row(
        className="mb-5 text-center",
        children=[
            imports.dbc.Col(
                html.Div(
                    dcc.RadioItems(
                    id=ids.DATA_FREQUENCY,
                    className="btn-group btn-group-md w-75",
                    inputClassName="btn-check",
                    labelClassName="btn btn-primary fs-4 w-100",
                    options=[
                        {"label": "Daily", "value": "Daily"},
                        {"label": "Weekly", "value": "Weekly"},
                        {"label": "Monthly", "value": "Monthly"},
                    ],
                    value="Daily",
                    inline=True,
                    ),
                    className="d-flex justify-content-center",
                ),
                className="d-flex radio-group text-center",
                xs=12,
            ),
        ]
    )
