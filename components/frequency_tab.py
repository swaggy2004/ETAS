from dash import Dash, html, dcc
import imports as imports
import components.ids as ids
import dash_bootstrap_components as dbc


def render(app: Dash) -> imports.dbc.Row:
    return imports.dbc.Row(
        className="radio-group justify-content-center align-items-center mb-5",
        children=[
            dcc.RadioItems(
                id=ids.DATA_FREQUENCY,
                className="btn-group",
                inputClassName="btn-check",
                labelClassName="btn btn-primary",
                options=[
                    {"label": "Daily", "value": "Daily"},
                    {"label": "Weekly", "value": "Weekly"},
                    {"label": "Monthly", "value": "Monthly"},
                ],
                value="Daily",
            ),
        ]
    )

# def render1(app: Dash) -> imports.dbc.Row:
#     return imports.dbc.Row([
#         dbc.ButtonGroup(
#             [
#                 dbc.Button(
#                     "Daily",
#                     id=ids.DATA_FREQUENCY + "-daily",
#                     n_clicks=0,
#                     class_name="w-100 fs-5",
#                 ),
#                 dbc.Button(
#                     "Weekly",
#                     id=ids.DATA_FREQUENCY + "-weekly",
#                     n_clicks=0,
#                     class_name="w-100 fs-5",
#                 ),
#                 dbc.Button(
#                     "Monthly",
#                     id=ids.DATA_FREQUENCY + "-monthly",
#                     n_clicks=0,
#                     class_name="w-100 fs-5",
#                 ),
#             ],
#             id=ids.DATA_FREQUENCY,
#             className="p-0",
#         )
#     ],
#         className="justify-content-center align-items-center row-cols-1 row-cols-md-3 row-cols-lg-3 w-100"
#     )

# def render(app: Dash) -> imports.dbc.Row:
#     frequency = ["Daily", "Weekly", "Monthly"]
#     return imports.dbc.Row(
#         children=[
#             dcc.RadioItems(
#                 id=ids.DATA_FREQUENCY,
#                 options=[
#                     {"label": fq, "value": fq} for fq in frequency,
#                 ],
#                 value="Daily",
#                 className="btn-group btn-group-lg",
#             )
#         ]
#     )
