from dash import Dash, html, dcc
import imports
from dash.dependencies import Output, Input
import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')


def fetch_latest_data():
    try:
        # Construct SQL query to select the latest record from the database
        sql = "SELECT * FROM datalogs ORDER BY collectedDate DESC LIMIT 1"

        # Execute the SQL query and load result into a DataFrame
        df = pd.read_sql(sql, engine)

        return df

    except Exception as e:
        print("Error fetching latest data:", e)
        return None


def make_card(card_title, card_value):
    card = imports.dbc.Card(
        imports.dbc.CardBody(
            [
                html.H5(card_title, className="card-title fs-5 text-center"),
                html.H1(
                    card_value,
                    className="card-text h1 fw-bold text-center",
                ),
            ]
        ),
        className="w-100"
    )
    return card


def render(app: Dash) -> imports.dbc.Row:
    @app.callback(
        Output("pH", "children"),
        Output("temp", "children"),
        Output("tds", "children"),
        Output("turbidity", "children"),
        Input("interval-component", "n_intervals"),
    )
    def update_metrics(n):
        # Fetch latest data
        df = fetch_latest_data()

        if df is not None and not df.empty:
            # Extract the relevant values from the DataFrame
            latest_value_ph = df.iloc[0]['phValue']
            latest_value_temp = df.iloc[0]['tempValue']
            latest_value_turbidity = df.iloc[0]['turbidityValue']
            latest_value_tds = df.iloc[0]['tdsValue']

            # Create updated card components
            ph_card = make_card("pH", f"{latest_value_ph}")
            temp_card = make_card("Temperature", f"{latest_value_temp}°C")
            turbidity_card = make_card(
                "Turbidity", f"{latest_value_turbidity} NTU")
            tds_card = make_card("Total Dissolved Solids",
                                 f"{latest_value_tds} ppm")

            return ph_card, temp_card, tds_card, turbidity_card
        else:
            return "No data available"

    return imports.dbc.Row(
        id="live-updates",
        children=[
            imports.dbc.Col(
                id="pH",
                className="",
            ),
            imports.dbc.Col(
                id="temp",
                className="",
            ),
            imports.dbc.Col(
                id="tds",
                className="",
            ),
            imports.dbc.Col(
                id="turbidity",
                className="",
            ),
            dcc.Interval(
                id='interval-component',
                interval=3*1000,  # Update every 1 second
                n_intervals=0
            ),
        ],
        className="justify-content-center align-items-center row-cols-1 row-cols-md-2 row-cols-lg-4 mb-5 p-0"
    )
