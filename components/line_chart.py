from datetime import datetime
import pandas as pd
import sqlalchemy
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
from dash.dependencies import Output, Input
import ids

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

# Extract hour from collectedDate
df['hour'] = df['collectedDate'].dt.hour

# Drop 'collectedDate' column
df.drop(columns=['collectedDate'], inplace=True)

# Calculate hourly average
hourly_avg = df.groupby('hour').mean()

# Define function to render Dash app layout


def render(app: Dash) -> dbc.Row:
    @app.callback(
        [Output("line-chart-ph", "figure"),
         Output("line-chart-tds", "figure"),
         Output("line-chart-temp", "figure"),
         Output("line-chart-turbidity", "figure")],
        [Input(ids.DATA_FREQUENCY, "value")]
    )
    def show_graph(val) -> list:
        if val == "Daily":
            # Calculate hourly average again if needed
            hourly_avg = df.groupby('hour').mean()

            # Create line charts
            fig1 = px.line(hourly_avg, x=hourly_avg.index,
                        y=hourly_avg["phValue"], title="Hourly Average pH")
            fig2 = px.line(hourly_avg, x=hourly_avg.index,
                        y=hourly_avg["tdsValue"], title="Hourly Average TDS")
            fig3 = px.line(hourly_avg, x=hourly_avg.index,
                        y=hourly_avg["tempValue"], title="Hourly Average Temperature")
            fig4 = px.line(hourly_avg, x=hourly_avg.index,
                        y=hourly_avg["turbidityValue"], title="Hourly Average Turbidity")

        elif val == "Weekly":
            # Calculate daily average
            daily_avg = df.groupby(df.index.date).mean()

            # Create line charts
            fig1 = px.line(daily_avg, x=daily_avg.index,
                           y=daily_avg["phValue"], title="Daily Average pH")
            fig2 = px.line(daily_avg, x=daily_avg.index,
                           y=daily_avg["tdsValue"], title="Daily Average TDS")
            fig3 = px.line(daily_avg, x=daily_avg.index,
                           y=daily_avg["tempValue"], title="Daily Average Temperature")
            fig4 = px.line(daily_avg, x=daily_avg.index,
                           y=daily_avg["turbidityValue"], title="Daily Average Turbidity")

        elif val == "Monthly":
            # Calculate monthly average
            monthly_avg = df.groupby(df.index.month).mean()

            # Create line charts
            fig1 = px.line(monthly_avg, x=monthly_avg.index,
                           y=monthly_avg["phValue"], title="Monthly Average pH")
            fig2 = px.line(monthly_avg, x=monthly_avg.index,
                           y=monthly_avg["tdsValue"], title="Monthly Average TDS")
            fig3 = px.line(monthly_avg, x=monthly_avg.index,
                           y=monthly_avg["tempValue"], title="Monthly Average Temperature")
            fig4 = px.line(monthly_avg, x=monthly_avg.index,
                           y=monthly_avg["turbidityValue"], title="Monthly Average Turbidity")

        return fig1, fig2, fig3, fig4

    # Return Dash app layout
    return dbc.Row([
        dcc.Graph(id="line-chart-ph"),
        dcc.Graph(id="line-chart-tds"),
        dcc.Graph(id="line-chart-temp"),
        dcc.Graph(id="line-chart-turbidity")
    ])
