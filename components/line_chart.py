from datetime import datetime
import pandas as pd
import sqlalchemy
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

current_date = datetime.now().date()
sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = '{current_date}'"

df = pd.read_sql(sql, engine)
df['collectedDate'] = pd.to_datetime(df['collectedDate'])
df['hour'] = df['collectedDate'].dt.hour
df.drop(columns=['collectedDate'], inplace=True)
hourly_avg = df.groupby('hour').mean()

fig1 = px.line(hourly_avg, x=hourly_avg.index, y=hourly_avg["phValue"], title="Hourly Average pH")

fig2 = px.line(hourly_avg, x=hourly_avg.index, y=hourly_avg["tdsValue"], title="Hourly Average TDS")

fig3 = px.line(hourly_avg, x=hourly_avg.index,y=hourly_avg["tempValue"], title="Hourly Average Temperature")

fig4 = px.line(hourly_avg, x=hourly_avg.index,y=hourly_avg["turbidityValue"], title="Hourly Average Turbidity")


def render(app: Dash) -> dbc.Row:
    return dbc.Row([
        dcc.Graph(
            id="line-chart-ph",
            figure=fig1
        ),
        dcc.Graph(
            id="line-chart-tds",
            figure=fig2
        ),
        dcc.Graph(
            id="line-chart-temp",
            figure=fig3
        ),
        dcc.Graph(
            id="line-chart-turbidity",
            figure=fig4
        ),
    ],)