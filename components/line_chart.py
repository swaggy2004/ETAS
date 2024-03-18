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
    sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = '{
        current_date}'"

    # Read data from SQL into DataFrame
    df = pd.read_sql(sql, engine)

    # Convert 'collectedDate' column to datetime
    df['collectedDate'] = pd.to_datetime(df['collectedDate'])
    df['hour'] = df['collectedDate'].dt.hour

    # Drop 'collectedDate' column
    df.drop(columns=['collectedDate'], inplace=True)

    return df


def process_data(df, frequency):
    if frequency == "Daily":
        # Calculate hourly average
        hourly_avg = df.groupby('hour').mean()
        return hourly_avg
    elif frequency == "Weekly":
        # Calculate daily average
        daily_avg = df.groupby(df.index.date).mean()
        return daily_avg
    elif frequency == "Monthly":
        # Calculate monthly average
        monthly_avg = df.groupby(df.index.month).mean()
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

        # Create line charts
        fig1 = px.line(processed_df, x=processed_df.index,
                       y=processed_df["phValue"], title="Hourly Average pH")
        fig2 = px.line(processed_df, x=processed_df.index,
                       y=processed_df["tdsValue"], title="Hourly Average TDS")
        fig3 = px.line(processed_df, x=processed_df.index,
                       y=processed_df["tempValue"], title="Hourly Average Temperature")
        fig4 = px.line(processed_df, x=processed_df.index,
                       y=processed_df["turbidityValue"], title="Hourly Average Turbidity")

        return fig1, fig2, fig3, fig4

    # Return Dash app layout
    return dbc.Row([
        dcc.Graph(id="line-chart-ph"),
        dcc.Graph(id="line-chart-tds"),
        dcc.Graph(id="line-chart-temp"),
        dcc.Graph(id="line-chart-turbidity")
    ])
