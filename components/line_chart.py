from dash import Dash, html, dcc
import imports
import plotly.express as px
from . import ids
import pandas as pd
import sqlalchemy
from datetime import datetime, timedelta

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')


def fetch_today_data():
    try:
        # Get today's date
        today = datetime.now().date()

        # Construct SQL query to select today's records from the database
        sql = f"SELECT * FROM datalogs WHERE DATE(collectedDate) = '{today}'"

        # Execute the SQL query and load result into a DataFrame
        df = pd.read_sql(sql, engine)

        return df

    except Exception as e:
        print("Error fetching today's data:", e)
        return None


def calculate_hourly_average(df):
    if df is None or df.empty:
        return None

    # Convert collectedDate to datetime object
    df['collectedDate'] = pd.to_datetime(df['collectedDate'])

    # Extract hour from collectedDate
    df['hour'] = df['collectedDate'].dt.hour

    # Calculate hourly average pH value
    hourly_avg = df.groupby('hour')['phValue'].mean().reset_index()

    return hourly_avg

def update_graph(n):
    # Fetch today's data from the database
    today_data = fetch_today_data()

    if today_data is None or today_data.empty:
        # If no data available, return an empty graph
        fig = px.line()
    else:
        # Calculate hourly average pH value
        hourly_avg = calculate_hourly_average(today_data)

        if hourly_avg is None or hourly_avg.empty:
            # If no hourly average available, return an empty graph
            fig = px.line()
        else:
            # Plot hourly average pH value
            fig = px.line(hourly_avg, x='hour', y='phValue')

    # Update X and Y axis labels
    fig.update_layout(xaxis_title="Hours", yaxis_title="pH Value")

    return fig
