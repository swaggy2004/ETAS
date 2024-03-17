from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import imports
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


def create_card_body(card_title, card_value):
    return [
        imports.dbc.Spinner(color="danger", type="grow", size="sm"),
        html.H5(card_title, className="card-title fs-5 text-center"),
        html.H1(
            # Set id to easily update the value
            id=card_title.lower().replace(" ", "-") + "-value",
            children=card_value,
            className="card-text h1 fw-bold text-center",
        ),
    ]


def render(app: Dash) -> imports.dbc.Row:
    # Define the callback function inside the render function
    @app.callback(
        [
            Output("pH-value", "children"),
            Output("temp-value", "children"),
            Output("tds-value", "children"),
            Output("turbidity-value", "children"),
        ],
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

            return (
                f"{latest_value_ph}",
                f"{latest_value_temp}°C",
                f"{latest_value_tds} ppm",
                f"{latest_value_turbidity} NTU"
            )
        else:
            return "No data available", "No data available", "No data available", "No data available"

    # Define the layout with the updated card values
    return imports.dbc.Row(
        id="live-updates",
        children=[
            imports.dbc.Col(
                imports.dbc.Card(
                    imports.dbc.CardBody(create_card_body("pH", "Loading...")),
                    className="w-100",
                ),
                className="p-3",
            ),
            imports.dbc.Col(
                imports.dbc.Card(
                    imports.dbc.CardBody(create_card_body(
                        "Temperature", "Loading...")),
                    className="w-100",
                ),
                className="p-3",
            ),
            imports.dbc.Col(
                imports.dbc.Card(
                    imports.dbc.CardBody(create_card_body(
                        "Total Dissolved Solids", "Loading...")),
                    className="w-100",
                ),
                className="p-3",
            ),
            imports.dbc.Col(
                imports.dbc.Card(
                    imports.dbc.CardBody(create_card_body(
                        "Turbidity", "Loading...")),
                    className="w-100",
                ),
                className="p-3",
            ),
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # Update every 1 second
                n_intervals=0
            ),
        ],
        className="justify-content-center align-items-center row-cols-1 row-cols-md-2 row-cols-lg-4"
    )
