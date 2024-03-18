from datetime import datetime, timedelta
import pandas as pd
import sqlalchemy
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Output, Input
from . import ids


def get_data(val):
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

    if val == "Day":
        current_date = datetime.now().date() - timedelta(days=1)
        sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = '{current_date}'"
    elif val == "Week":
        start_of_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
        end_of_week = start_of_week + timedelta(days=6)
        sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) BETWEEN '{start_of_week}' AND '{end_of_week}'"
    elif val == "Month":
        current_date = datetime.now().date().replace(day=1)
        next_month = current_date.replace(month=current_date.month+1)
        end_of_month = next_month - timedelta(days=1)
        sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) BETWEEN '{current_date}' AND '{end_of_month}'"
    else:
        return None

    # Read data from SQL into DataFrame
    df = pd.read_sql(sql, engine)

    # Convert 'collectedDate' column to datetime
    df['collectedDate'] = pd.to_datetime(df['collectedDate'])

    return df


def process_data(df, frequency):
    if frequency == "Day":
        # Add 'hour' column from 'collectedDate'
        df['hour'] = df['collectedDate'].dt.hour

        # Set 'hour' as index and drop 'collectedDate'
        df.set_index('hour', inplace=True)
        df.drop(columns=['collectedDate'], inplace=True)

        # Calculate hourly average for each hour
        hourly_avg = df.groupby('hour').mean()
        return hourly_avg
    elif frequency == "Week":
        # Add 'day_of_week' column from 'collectedDate'
        df['day_of_week'] = df['collectedDate'].dt.dayofweek

        # Set 'day_of_week' as index and drop 'collectedDate'
        df.set_index('day_of_week', inplace=True)
        df.drop(columns=['collectedDate'], inplace=True)

        # Calculate daily average for each day of the week
        weekly_avg = df.groupby('day_of_week').mean()
        return weekly_avg
    elif frequency == "Month":
        # Set 'collectedDate' as index and drop other columns
        df.set_index('collectedDate', inplace=True)
        df = df.resample('M').mean()  # Resample to get monthly average
        return df
    else:
        return None


def render(app: Dash) -> dbc.Row:
    @app.callback(
        [Output("line-chart-ph", "figure"),
         Output("line-chart-tds", "figure"),
         Output("line-chart-temp", "figure"),
         Output("line-chart-turbidity", "figure")],
        [Input(ids.DATA_FREQUENCY, "value")]
    )
    def show_graph(val) -> list:
        df = get_data(val)
        if df is None:
            # Invalid input
            return [px.line(), px.line(), px.line(), px.line()]

        processed_df = process_data(df, val)

        # Create line charts
        fig1 = px.line(processed_df, x=processed_df.index,
                       y="phValue", title="Hourly Average pH")
        fig2 = px.line(processed_df, x=processed_df.index,
                       y="tdsValue", title="Hourly Average TDS")
        fig3 = px.line(processed_df, x=processed_df.index,
                       y="tempValue", title="Hourly Average Temperature")
        fig4 = px.line(processed_df, x=processed_df.index,
                       y="turbidityValue", title="Hourly Average Turbidity")

        # Update axis labels
        for fig in [fig1, fig2, fig3, fig4]:
            fig.update_layout(xaxis_title="Hour" if val == "Day" else "Day" if val == "Week" else "Month",
                              yaxis_title="pH" if fig == fig1 else "TDS" if fig == fig2 else
                              "Temperature" if fig == fig3 else "Turbidity")

        return fig1, fig2, fig3, fig4

    # Return Dash app layout
    return dbc.Row([
        dcc.Graph(id="line-chart-ph"),
        dcc.Graph(id="line-chart-tds"),
        dcc.Graph(id="line-chart-temp"),
        dcc.Graph(id="line-chart-turbidity")
    ])
