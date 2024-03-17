from dash import Dash, html
import components.test as test
import imports  # Import the imports module
# Import the frequency_tab module
import components.frequency_tab as frequency_tab
# from components import line_chart  # Import the line_chart module


def create_layout(app: Dash) -> imports.dbc.Container:
    return imports.dbc.Container(
        id="main-layout",
        children=[
            html.H1(app.title),
            imports.dcb.Row([
                html.H2("Live Updates", className="text-center h2 fw-semibold"),
                imports.dbc.Spinner(color="danger", type="grow", size="sm"),
            ]),
            test.render(app),
            html.H2("Frequency of Data"),
            frequency_tab.render(app),
            # line_chart.render(app),
        ],
    )
