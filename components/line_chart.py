from datetime import datetime, timedelta
import pandas as pd
import sqlalchemy
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Output, Input
from . import ids
import numpy as np


def get_data(val):
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

    if val == "Daily":
        current_date = datetime.now().date() - timedelta(days=1)

        sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = '{current_date}'"

    elif val == "Weekly":
        today = datetime.now().date()
        start_of_previous_week = today - timedelta(days=today.weekday() + 7)
        end_of_previous_week = start_of_previous_week + timedelta(days=6)
        sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) BETWEEN '{start_of_previous_week}' AND '{end_of_previous_week}'"

    elif val == "Monthly":
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
    new_df = df.copy()
    if frequency == "Daily":
        # Add 'hour' column from 'collectedDate'
        new_df['hour'] = new_df['collectedDate'].dt.hour

        # Set 'hour' as index and drop 'collectedDate'
        new_df.set_index('hour', inplace=True)
        new_df.drop(columns=['collectedDate'], inplace=True)

        # Calculate hourly average for each hour
        hourly_avg = new_df.groupby('hour').mean()
        return hourly_avg

    elif frequency == "Weekly":
        # Convert 'collectedDate' to day of the week and specify desired order
        new_df['day_of_week'] = pd.Categorical(new_df['collectedDate'].dt.day_name(), categories=[
                                               "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ordered=True)

        # Group by 'day_of_week' and calculate the mean
        weekly_avg = new_df.groupby('day_of_week').mean()

        # Reindex to include all days of the week and fill missing values with NaN
        weekly_avg = weekly_avg.reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=np.nan)

        print(weekly_avg)
        return weekly_avg

    elif frequency == "Monthly":
        # Set 'collectedDate' as index and drop other columns
        new_df.set_index('collectedDate', inplace=True)
        new_df = new_df.resample('M').mean()  # Resample to get monthly average
        return new_df


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
        processed_df = process_data(df, val)

        # Create line charts
        fig1 = px.area(processed_df, x=processed_df.index,
                       y="phValue", title=val + " Average pH", markers="true")
        fig2 = px.area(processed_df, x=processed_df.index,
                       y="tdsValue", title=val + " Average Total Dissolved Solids", markers="true")
        fig3 = px.area(processed_df, x=processed_df.index,
                       y="tempValue", title=val + " Average Temperature", markers="true")
        fig4 = px.area(processed_df, x=processed_df.index,
                       y="turbidityValue", title=val + " Average Turbidity", markers="true")

        fig1.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
        fig2.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
        # Update axis labels
        for fig in [fig1, fig2, fig3, fig4]:
            if val == "Daily":
                fig.update_layout(
                    xaxis_title="Hour of the Day")
            elif val == "Weekly":
                fig.update_layout(xaxis_title="Day of the Week")
            elif val == "Monthly":
                fig.update_layout(xaxis_title="Week of the Month")

            if fig == fig1:
                fig.update_layout(yaxis_title="pH Value")
            elif fig == fig2:
                fig.update_layout(yaxis_title="Total Dissolved Solids Value")
            elif fig == fig3:
                fig.update_layout(yaxis_title="Temperature Value")
            elif fig == fig4:
                fig.update_layout(yaxis_title="Turbidity Value")

        return fig1, fig2, fig3, fig4
    # Return Dash app layout
    return dbc.Row([
        dcc.Graph(id="line-chart-ph", className="mb-3"),
        dcc.Graph(id="line-chart-tds", className="mb-3"),
        dcc.Graph(id="line-chart-temp", className="mb-3"),
        dcc.Graph(id="line-chart-turbidity")
    ], className="mb-5")
