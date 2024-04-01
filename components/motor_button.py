from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import sqlalchemy
from sqlalchemy.sql import text
import pandas as pd

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')


def fetch_latest_data():
    try:
        # Construct SQL query to select the latest record from the database
        sql = "SELECT motorState FROM datalogs ORDER BY collectedDate DESC LIMIT 1"

        # Execute the SQL query and load result into a DataFrame
        df = pd.read_sql(sql, engine)
        state = df.iloc[0]['motorState']
        print("Fetched state:", state)
        return state

    except Exception as e:
        print("Error fetching latest data:", e)
        return None


def update_data(state):
    try:
        # Construct SQL query to update the record with the latest collectedDate
        sql = text(
            "UPDATE datalogs SET motorState = :state WHERE collectedDate = (SELECT MAX(collectedDate) FROM datalogs)")
        with engine.connect() as conn:
            # Pass parameters as a dictionary
            conn.execute(sql, {"state": state})
            conn.commit()
    except Exception as e:
        print("Error updating data:", e)


def render(app: Dash) -> dbc.Row:
    @app.callback(
        Output("motor-switch", "label"),
        Input("motor-switch", "value"),
    )
    def update_motor_switch_label(value: bool) -> str:
        state = 1 if value else 0
        print("State:", state)
        update_data(state)
        return "ON" if value else "OFF"

    @app.callback(
        Output("motor-switch", "value"),
        Input("interval-component", "n_intervals")
    )
    def update_switch_value(_):
        return fetch_latest_data()

    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    label="On",
                    className="mx-auto"
                ),
                width="auto",
                className="d-flex justify-content-center align-items-center"
            ),
            dcc.Interval(
                id='interval-component',
                interval=3*1000,  # Update every 3 seconds
                n_intervals=0
            ),
        ],
        className="justify-content-center align-items-center fs-1 mb-3"
    )
