from dash import html, dcc, Output, Input
from dash.dependencies import Output, Input
import sqlalchemy
import pandas as pd

# Create SQLAlchemy engine
engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

# Define function to fetch latest data


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


# Define layout for live updates component
layout = html.Div([
    html.H1("Live Updates"),
    html.Div(id="live-update-ph"),
    html.Div(id="live-update-temp"),
    html.Div(id="live-update-turbidity"),
    html.Div(id="live-update-tds"),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Update every 1 second
        n_intervals=0
    )
])

# Define callback to update displayed value


@app.callback(
    [Output("live-update-ph", "children"), Output("live-update-temp", "children"),
     Output("live-update-turbidity", "children"), Output("live-update-tds", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_metrics(n):
    # Fetch latest data
    df = fetch_latest_data()

    if df is not None and not df.empty:
        # Extract the relevant value (e.g., pH value) from the DataFrame
        # Assuming 'phValue' is the column name
        latest_value_ph = df.iloc[0]['phValue']
        latest_value_temp = df.iloc[0]['tempValue']
        latest_value_turbidity = df.iloc[0]['turbidityValue']
        latest_value_tds = df.iloc[0]['tdsValue']

        # Return the latest value as a text string
        return (f"Latest pH value: {latest_value_ph}",
                f"Latest temperature value: {latest_value_temp}",
                f"Latest turbidity value: {latest_value_turbidity}",
                f"Latest TDS value: {latest_value_tds}")
    else:
        return "No data available"
