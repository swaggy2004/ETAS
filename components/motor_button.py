from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
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

        return motor_state

    except Exception as e:
        print("Error fetching latest motor state:", e)
        return None



def render(app: Dash) -> dbc.Row:
    @app.callback(
        Output("motor-switch", "label"),
        Input("motor-switch", "value"),
    )
    def update_motor_switch_label(value: bool) -> str:
        motor_state = fetch_latest_motor_state()
        return "ON" if motor_state else "OFF"

    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    label="On",
                    value=False,
                    className="mx-auto"
                ),
                width="auto",
                className="d-flex justify-content-center align-items-center"
            )
        ],
        className="justify-content-center align-items-center fs-1 mb-3"
    )
