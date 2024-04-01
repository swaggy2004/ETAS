from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash.dependencies import Input as DashInput, Output as DashOutput, State, MATCH
import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')


def fetch_latest_motor_state():
    try:
        # Construct SQL query to select the latest record from the database
        sql = "SELECT motorState FROM datalogs ORDER BY collectedDate DESC LIMIT 1"

        # Execute the SQL query and fetch the result
        with engine.connect() as connection:
            result = connection.execute(sql)
            row = result.fetchone()  # Fetch the first (and only) row
            if row:  # Check if a row was fetched
                # Extract motorState value from the first column
                motor_state = row[0]
            else:
                motor_state = None  # Set motor_state to None if no rows were fetched

        return bool(motor_state)

    except Exception as e:
        print("Error fetching latest motor state:", e)
        return None


def render(app: Dash) -> dbc.Row:
    latest_motor_state = fetch_latest_motor_state()

    @app.callback(
        Output("motor-switch", "label"),
        Input("interval-component", "n_intervals")
    )
    def update_motor_switch_label(n_intervals: int) -> str:
        return "ON" if latest_motor_state else "OFF"

    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    label="On",
                    value=latest_motor_state,
                    className="mx-auto"
                ),
                width="auto",
                className="d-flex justify-content-center align-items-center"
            ),
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # in milliseconds
                n_intervals=0
            )
        ],
        className="justify-content-center align-items-center fs-1 mb-3"
    )
