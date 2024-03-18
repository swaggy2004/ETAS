from dash import Dash, html, dcc
import imports as imports
import components.ids as ids
import dash_bootstrap_components as dbc


def render(app: Dash) -> imports.dbc.Row:
    return imports.dbc.Row(
        className="mb-5 text-center",
        children=[
            imports.dbc.Col(
                dcc.RadioItems(
                    id=ids.DATA_FREQUENCY,
                    className="btn-group btn-group-md w-75",
                    inputClassName="btn-check",
                    labelClassName="btn btn-primary fs-4",
                    options=[
                        {"label": "Daily", "value": "Daily"},
                        {"label": "Weekly", "value": "Weekly"},
                        {"label": "Monthly", "value": "Monthly"},
                    ],
                    value="Daily",
                    inline=True,
                ),
                className="radio-group",
            ),
        ]
    )
