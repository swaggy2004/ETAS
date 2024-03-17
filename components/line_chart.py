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

# Extract hour from collectedDate
df['hour'] = df['collectedDate'].dt.hour
df.drop(columns=['collectedDate'], inplace=True)
hourly_avg = df.groupby('hour').mean()

fig = px.line(hourly_avg, x=hourly_avg.index,
              y=hourly_avg["phValue"], title="Hourly Average")

def render(app:Dash) -> dbc.Row:
    return dbc.Row(
        fig.show()
        # dcc.Graph(
        #     id="line-chart",
        #     figure={
        #         "data": [
        #             {
        #                 "x": hourly_avg.index,
        #                 "y": hourly_avg["phValue"],
        #                 "type": "line",
        #                 "name": "pH",
        #             },
        #             {
        #                 "x": hourly_avg.index,
        #                 "y": hourly_avg["tdsValue"],
        #                 "type": "line",
        #                 "name": "TDS",
        #             },
        #             {
        #                 "x": hourly_avg.index,
        #                 "y": hourly_avg["tempValue"],
        #                 "type": "line",
        #                 "name": "Temperature",
        #             },
        #             {
        #                 "x": hourly_avg.index,
        #                 "y": hourly_avg["turbidityValue"],
        #                 "type": "line",
        #                 "name": "Turbidity",
        #             },
        #         ],
        #         "layout": {
        #             "title": "Hourly Average",
        #             "xaxis": {"title": "Hour"},
        #             "yaxis": {"title": "Value"},
        #         },
        #     },
        # )
    )