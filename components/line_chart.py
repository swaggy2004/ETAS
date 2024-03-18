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

    if val == "Daily":
        current_date = datetime.now().date() - timedelta(days=1)
        sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = '{current_date}'"

    elif val == "Weekly":
        end_of_current_week = datetime.now().date(
        ) - timedelta(days=datetime.now().weekday())
        start_of_previous_week = end_of_current_week - timedelta(days=6)
        sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) BETWEEN '{start_of_previous_week}' AND '{end_of_current_week}'"

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
        new_df['day_of_week'] = pd.Categorical(new_df['collectedDate'].dt.day_name(), 
                                            categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                            ordered=True)

        # Set 'day_of_week' as index and drop 'collectedDate'
        new_df.set_index('day_of_week', inplace=True)
        new_df.drop(columns=['collectedDate'], inplace=True)

        # Reindex to ensure Monday is included
        new_df = new_df.reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

        # Calculate daily average for each day of the week
        weekly_avg = new_df.groupby('day_of_week').mean()
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
        fig1 = px.line(processed_df, x=processed_df.index,
                       y="phValue", title=val + " Average pH")
        fig2 = px.line(processed_df, x=processed_df.index,
                       y="tdsValue", title=val + " Average Total Dissolved Solids")
        fig3 = px.line(processed_df, x=processed_df.index,
                       y="tempValue", title=val + "Average Temperature")
        fig4 = px.line(processed_df, x=processed_df.index,
                       y="turbidityValue", title=val + " Average Turbidity")

        # Update axis labels
        for fig in [fig1, fig2, fig3, fig4]:
            if val == "Daily":
                fig.update_layout(xaxis_title="Hour of the Day")
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
        dcc.Graph(id="line-chart-ph"),
        dcc.Graph(id="line-chart-tds"),
        dcc.Graph(id="line-chart-temp"),
        dcc.Graph(id="line-chart-turbidity")
    ])
