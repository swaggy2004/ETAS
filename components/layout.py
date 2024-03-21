from dash import Dash, html
import components.live_update as live_update
from components import mapview
import imports
import components.frequency_tab as frequency_tab
from components import line_chart


def create_layout(app: Dash) -> imports.dbc.Container:
    return imports.dbc.Container(
        id="main-layout",
        children=[
            html.H1(app.title, className="display-5 mb-4"),
            html.H2("Live Updates", className="text-center h2 fw-lighter mb-3"),
            live_update.render(app),
            html.H2("Frequency of Data",
                    className="text-center h2 fw-lighter mb-3"),
            frequency_tab.render(app),
            line_chart.render(app),
            html.H2("Map View", className="text-center h2 fw-lighter mb-3"),
            mapview.render_map(app),
        ],
    )
