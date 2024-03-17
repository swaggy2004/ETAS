from datetime import datetime
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

current_date = datetime.now().date()

sql = f"SELECT * FROM datalogs WHERE DATE(collectedDate) = '{current_date}'"


df = pd.read_sql(sql, engine)

# Calculate hourly average values
hourly_avg = df.groupby(df['collectedDate'].dt.hour).mean()

# Extract hour from collectedDate and add it as a separate column
hourly_avg['hour'] = hourly_avg.index

# Reorder columns as per requirement
hourly_avg = hourly_avg[['phValue', 'tdsValue',
                         'tempValue', 'turbidityValue', 'hour']]


print(hourly_avg)
