from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine('mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

def fetch_latest_data():
    try:
        # Construct SQL query to select the latest record from the database
        sql = "SELECT * FROM datalogs ORDER BY collectedDate DESC LIMIT 1"
        # Execute the SQL query and load result into a DataFrame
        df = pd.read_sql(sql, engine)
        print(df);
        return df
    except Exception as e:
        print("Error fetching latest data:", e)
        return None

def render(app: Dash) -> dbc.Row:
    @app.callback(
        Output("motor-switch", "value"),
        Input("motor-switch", "n_clicks"),
    )
    def update_motor_switch_value(n_clicks: int) -> bool:
        # Fetch the latest data from the database
        latest_data = fetch_latest_data()

        # If there is data available, check the motorState value
        if not latest_data.empty:
            motor_state = latest_data['motorState'].iloc[0]
            if motor_state == 1:
                # If motorState is 1, set the switch to True (ON)
                return True
            else:
                # If motorState is 0, set the switch to False (OFF)
                return False
        else:
            # If no data is available, set the switch to False (OFF) as a default
            return False

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