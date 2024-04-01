from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH
import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')


def fetch_latest_motor_state():
    try:
        sql = "SELECT motorState FROM datalogs ORDER BY collectedDate DESC LIMIT 1"
        with engine.connect() as connection:
            result = connection.execute(sql)
            row = result.fetchone()
            if row:
                motor_state = row[0]
            else:
                motor_state = None
            print(motor_state)
        return bool(motor_state)
    except Exception as e:
        print("Error fetching latest motor state:", e)
        return None


def render(app: Dash) -> dbc.Row:
    @app.callback(
        Output("motor-switch", "value"),
        Input("interval-component", "n_intervals")
    )
    def update_motor_switch(n_intervals: int):
        latest_motor_state = fetch_latest_motor_state()
        if latest_motor_state is None:
            return False
        elif latest_motor_state == 1:
            return True
        else:
            return 

    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    value=False,
                    className="mx-auto"
                ),
                width="auto",
                className="d-flex justify-content-center align-items-center"
            ),
            dcc.Interval(
                id='interval-component',
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ],
        className="justify-content-center align-items-center fs-1 mb-3"
    )
