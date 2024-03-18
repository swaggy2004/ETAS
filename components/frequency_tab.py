from dash import Dash, html, dcc
import imports as imports
import components.ids as ids
import dash_bootstrap_components as dbc


def render(app: Dash) -> imports.dbc.Row:
    return imports.dbc.Row(
        className="mb-5 px-0 px-md-2 justify-content-center align-items-center",
        children=[
            dcc.RadioItems(
                id=ids.DATA_FREQUENCY,
                className="btn-group p-0 w-md-75 w-100",
                inputClassName="btn-check",
                labelClassName="btn btn-primary fs-5 fs-md-4",
                options=[
                    {"label": "Daily", "value": "Daily"},
                    {"label": "Weekly", "value": "Weekly"},
                    {"label": "Monthly", "value": "Monthly"},
                ],
                value="Daily",
            ),
        ]
    )