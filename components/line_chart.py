from datetime import datetime
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

current_date = datetime.now().date()
sql = text("SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = :current_date")

df = pd.read_sql(sql, engine, params={'current_date': current_date})

hourly_avg = df.groupby(df['collectedDate'].dt.hour).mean()

# Extract hour from collectedDate and add it as a separate column
hourly_avg['hour'] = hourly_avg.index

print(hourly_avg)
