from datetime import datetime
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

current_date = datetime.now().date()
sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = '{
    current_date}'"

df = pd.read_sql(sql, engine)

# Extract hour from collectedDate
df['hour'] = df['collectedDate'].dt.hour

# Group by hour and calculate mean for each hour
hourly_avg = df.groupby('hour').mean()

print(hourly_avg)
