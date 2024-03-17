from datetime import datetime
from dash import Dash, html
import imports as imports
import dash_core_components as dcc
import pandas as pd

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

current_date = datetime.now().date()

sql = f"SELECT * FROM datalogs WHERE DATE(collectedDate) = '{current_date}'"


df = pd.read_sql(sql, engine)
print(df)