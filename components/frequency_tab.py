from dash import Dash, html, dcc
import imports as imports
import components.ids as ids
import dash_bootstrap_components as dbc


def render(app: Dash) -> imports.dbc.Row:
    return imports.dbc.Row(
        className="radio-group justify-content-center align-items-center mb-5 w-50 border border-3 border-danger",
        children=[
            dcc.RadioItems(
                id=ids.DATA_FREQUENCY,
                className="btn-group w-100 p-0",
                inputClassName="btn-check w-100",
                labelClassName="btn btn-primary w-100 fs-4",
                options=[
                    {"label": "Daily", "value": "Daily"},
                    {"label": "Weekly", "value": "Weekly"},
                    {"label": "Monthly", "value": "Monthly"},
                ],
                value="Daily",
            ),
        ]
    )