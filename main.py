# from components.test import setup_callbacks
from components.layout import create_layout
from dash import Dash, html
import imports  # Import the imports module

external_stylesheets = [imports.dbc.themes.MORPH]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "ETAS IOT Dashboard"

app.layout = create_layout(app)

# setup_callbacks(app)

if __name__ == '__main__':
    app.run_server(host="0.0.0.0" ,debug=True)
