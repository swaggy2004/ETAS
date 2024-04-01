from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import sqlalchemy
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

def render(app: Dash) -> dbc.Row:
    initial_state = fetch_latest_data()
    @app.callback(
        Output("motor-switch", "label"),
        Input("motor-switch", "value"),
    )
    def update_motor_switch_label(value: bool) -> str:
        return "ON" if value else "OFF"
    
    @app.callback(
        Output("motor-switch", "value"),
        Input("interval-component", "n_intervals"),
    )
    def update_motor_switch_value(n):
        state = fetch_latest_data()
        return int(state)
    return dbc.Row(
        [
            dbc.Col(
                dbc.Switch(
                    id="motor-switch",
                    label="On",
                    value=int(initial_state),
                    className="mx-auto"  # Add this line
                ),
                width="auto",  # Add this line
                className="d-flex justify-content-center align-items-center"  # Add this line
            ),
            dcc.Interval(
                id='interval-component',
                interval=3*1000,  # Update every 1 second
                n_intervals=0
            ),
        ],
        className="justify-content-center align-items-center fs-1 mb-3"
    )
