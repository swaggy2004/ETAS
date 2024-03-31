from dash import Dash, html
import components.live_update as live_update
from components import mapview
import imports
import components.frequency_tab as frequency_tab
from components import line_chart
from components import motor_button


def create_layout(app: Dash) -> imports.dbc.Container:
    return imports.dbc.Container(
        id="main-layout",
        children=[
            html.H1(app.title, className="display-1 text-center mb-1 mt-5"),
            html.H4("(Enviro Track Aqua Shield)",
                    className="text-center fw-lighter mb-5"),
            html.H2("Motor Control", className="text-center h2 fw-lighter mb-3"),
            motor_button.render(app),
            html.H2("Live Updates", className="text-center h2 fw-lighter mb-3"),
            live_update.render(app),
            html.H2("Frequency of Data",
                    className="text-center h2 fw-lighter mb-3"),
            frequency_tab.render(app),
            line_chart.render(app),
            html.H2("Purity Map View", className="text-center h2 fw-lighter"),
            mapview.render_map(app),
        ],
    )
