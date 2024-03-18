from dash import Dash, html, dcc
import imports as imports
import components.ids as ids
import dash_bootstrap_components as dbc


def render(app: Dash) -> imports.dbc.Row:
    return imports.dbc.Row(
        className="mb-5 border border-2 border-danger px-2",
        children=[
            dcc.RadioItems(
                id=ids.DATA_FREQUENCY,
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-primary fs-4",
                options=[
                    {"label": "Daily", "value": "Daily"},
                    {"label": "Weekly", "value": "Weekly"},
                    {"label": "Monthly", "value": "Monthly"},
                ],
                value="Daily",
            ),
        ]
    )