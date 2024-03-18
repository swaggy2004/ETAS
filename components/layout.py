from dash import Dash, html
import components.live_update as live_update
import imports  
import components.frequency_tab as frequency_tab
from components import line_chart  

def create_layout(app: Dash) -> imports.dbc.Container:
    return imports.dbc.Container(
        id="main-layout",
        children=[
            html.H1(app.title),
            html.H2("Live Updates", className="text-center h2 fw-semibold"),
            live_update.render(app),
            html.H2("Frequency of Data"),
            frequency_tab.render(app),
            html.BR(),
            frequency_tab.render1(app),
            line_chart.render(app),
        ],
    )
