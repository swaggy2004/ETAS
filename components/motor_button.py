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
        return state

    except Exception as e:
        print("Error fetching latest data:", e)
        return None
    

def update_data(state):
    try:
        sql = text(f"UPDATE datalogs SET motorState = {state} ORDER BY collectedDate DESC LIMIT 1;")
        with engine.connect() as conn:
            conn.execute(sql)
    except Exception as e:
        print("Error: ", e)


def render(app: Dash) -> dbc.Row:
    global_state = fetch_latest_data()
    @app.callback(
        Output("motor-switch", "label"),
        Input("motor-switch", "value"),
    )
    def update_motor_switch_label(value: bool) -> str:
        if value:
            state = 1
        else:
            state = 0
        print(state)
        global_state = state
        update_data(state)
        return "ON" if value else "OFF"
    
    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    label="On",
                    value=global_state,
                    className="mx-auto"  # Add this line
                ),
                width="auto",  # Add this line
                className="d-flex justify-content-center align-items-center"  # Add this line
            ),
        ],
        className="justify-content-center align-items-center fs-1 mb-3"
    )
