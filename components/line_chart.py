from datetime import datetime
import pandas as pd
import sqlalchemy
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Output, Input
from . import ids


def get_data():
    # Create database engine
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

    # Get current date
    current_date = datetime.now().date()

    # SQL query to retrieve data for the current date
    sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = '{current_date}'"

    # Read data from SQL into DataFrame
    df = pd.read_sql(sql, engine)

    # Convert 'collectedDate' column to datetime
    df['collectedDate'] = pd.to_datetime(df['collectedDate'])

    return df


def process_data(df, frequency):
    if frequency == "Daily":
        # Add 'hour' column from 'collectedDate' and drop 'collectedDate'
        df['hour'] = df['collectedDate'].dt.hour
        df.drop(columns=['collectedDate'], inplace=True)

        # Calculate hourly average for each hour
        hourly_avg = df.groupby('hour').mean()
        return hourly_avg
    elif frequency == "Weekly":
        # Add 'day_of_week' column from 'collectedDate' and drop 'collectedDate'
        df['day_of_week'] = df['collectedDate'].dt.dayofweek
        df.drop(columns=['collectedDate'], inplace=True)

        # Calculate daily average for each day of the week
        weekly_avg = df.groupby('day_of_week').mean()
        return weekly_avg
    elif frequency == "Monthly":
        # Calculate monthly average for each month
        monthly_avg = df.groupby(df['collectedDate'].dt.month).mean()
        return monthly_avg


def render(app: Dash) -> dbc.Row:
    @app.callback(
        [Output("line-chart-ph", "figure"),
         Output("line-chart-tds", "figure"),
         Output("line-chart-temp", "figure"),
         Output("line-chart-turbidity", "figure")],
        [Input(ids.DATA_FREQUENCY, "value")]
    )
    def show_graph(val) -> list:
        df = get_data()
        processed_df = process_data(df, val)

        # Reset index to ensure it's numeric or date-like
        processed_df.reset_index(inplace=True)

        # Create line charts
        fig1 = px.line(processed_df, x='index',
                       y="phValue", title="Hourly Average pH")
        fig2 = px.line(processed_df, x='index',
                       y="tdsValue", title="Hourly Average TDS")
        fig3 = px.line(processed_df, x='index',
                       y="tempValue", title="Hourly Average Temperature")
        fig4 = px.line(processed_df, x='index',
                       y="turbidityValue", title="Hourly Average Turbidity")

        return fig1, fig2, fig3, fig4

    # Return Dash app layout
    return dbc.Row([
        dcc.Graph(id="line-chart-ph"),
        dcc.Graph(id="line-chart-tds"),
        dcc.Graph(id="line-chart-temp"),
        dcc.Graph(id="line-chart-turbidity")
    ])
