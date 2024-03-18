from dash import Dash, html, dcc
import imports as imports
import components.ids as ids
import dash_bootstrap_components as dbc


def render(app: Dash) -> imports.dbc.Row:
    return imports.dbc.Row(
        className="mb-5 text-center border border-2 border-dark",
        children=[
            imports.dbc.Col(
                dcc.RadioItems(
                    id=ids.DATA_FREQUENCY,
                    className="btn-group border border-2 border-success",
                    inputClassName="btn-check border border-2 border-black",
                    labelClassName="btn btn-primary fs-4 border border-2 border-danger",
                    options=[
                        {"label": "Daily", "value": "Daily"},
                        {"label": "Weekly", "value": "Weekly"},
                        {"label": "Monthly", "value": "Monthly"},
                    ],
                    value="Daily",
                    inline=True,
                ),
                className="radio-group border border-2 border-danger w-50",
            ),
        ]
    )
