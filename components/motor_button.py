from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import sqlalchemy
import pandas as pd

# Database connection
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


def update_motor_state(value):
    int(value)
    try:
        with engine.connect() as connection:
            connection.execute(
                "UPDATE datalogs SET motorState = %s ORDER BY collectedDate DESC LIMIT 1;", (value,))
    except Exception as e:
        print("Error updating motor state:", e)



def render(app: Dash) -> dbc.Row:
    # Initial fetching of data
    latest_data = fetch_latest_data()
    initial_motor_state = latest_data['motorState'].iloc[0] if latest_data is not None and len(
        latest_data) > 0 else 0

    @app.callback(
        Output("motor-switch", "label"),
        Input("motor-switch", "value"),
    )
    def update_motor_switch_label(value: bool) -> str:
        return "ON" if value else "OFF"

    @app.callback(
        Output("motor-switch", "value"),
        Input("switch-label", "children"),
    )
    def update_motor_state_and_switch(label: str) -> bool:
        # Update motor state in the database based on switch label
        value = 1 if label == "ON" else 0
        update_motor_state(value)
        # Return the new value for the switch
        return value

    return dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Switch(
                        id="motor-switch",
                        # Set initial label based on fetched data
                        label="ON" if initial_motor_state else "OFF",
                        # Set initial value based on fetched data
                        value=bool(initial_motor_state),
                        className="mx-auto"  # Add this line
                    ),
                    html.Div(id="switch-label", style={"display": "none"},
                             children="ON" if initial_motor_state else "OFF")
                ],
                width="auto",  # Add this line
                className="d-flex justify-content-center align-items-center"  # Add this line
            )
        ],
        className="justify-content-center align-items-center fs-1 mb-3"
    )
