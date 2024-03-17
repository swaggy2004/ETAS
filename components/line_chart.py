from datetime import datetime
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

current_date = datetime.now().date()
# Select only the required columns from the database
# Select only the required columns from the database
sql = f"SELECT collectedDate, phValue, tdsValue, tempValue, turbidityValue FROM datalogs WHERE DATE(collectedDate) = '{
    current_date}'"

# Read data from the database into a DataFrame
df = pd.read_sql(sql, engine)

# Calculate hourly average values
hourly_avg = df.groupby(df['collectedDate'].dt.hour).mean()

# Extract hour from collectedDate and add it as a separate column
hourly_avg['hour'] = hourly_avg.index

print(hourly_avg)
