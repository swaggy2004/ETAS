from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import sqlalchemy
import pandas as pd
from sqlalchemy import text

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')


def update_motor_state(motor_state: int):
    try:
        # Construct the SQL query
        sql = text(
            "UPDATE datalogs SET motorState = :motor_state ORDER BY collectedDate DESC LIMIT 1")

        # Execute the SQL query with the parameter value
        with engine.connect() as conn:
            conn.execute(sql, {"motor_state": motor_state})

        print(f"Motor state updated to {motor_state}")
    except Exception as e:
        print("Error updating motor state:", e)


def render(app: Dash) -> dbc.Row:
    def fetch_latest_data():
        try:
            # Refresh the database connection
            engine.dispose()

            # Construct SQL query to select the latest record from the database
            sql = "SELECT * FROM datalogs ORDER BY collectedDate DESC LIMIT 1"

            # Execute the SQL query and load result into a DataFrame
            with engine.connect() as conn:
                df = pd.read_sql(sql, conn)

            return df
        except Exception as e:
            print("Error fetching latest data:", e)
            return None

    @app.callback(
        Output("motor-switch", "value"),
        Input("motor-switch", "value"),
    )
    def update_motor_switch_value(switch_value: bool) -> bool:
        # Fetch the latest data from the database
        latest_data = fetch_latest_data()

        # If there is data available, check the motorState value
        if not latest_data.empty:
            motor_state = latest_data['motorState'].iloc[0]
            if motor_state == 1:
                # If motorState is 1, set the switch to True (ON)
                switch_value = True
            else:
                # If motorState is 0, set the switch to False (OFF)
                switch_value = False
        else:
            # If no data is available, set the switch to False (OFF) as a default
            switch_value = False

        # Update the motorState value in the database
        motor_state = int(switch_value)
        update_motor_state(motor_state)

        return switch_value

    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    label="On",
                    value=False,
                    className="mx-auto",
                ),
                width="auto",
                className="d-flex justify-content-center align-items-center",
            )
        ],
        className="justify-content-center align-items-center fs-1 mb-3",
    )
