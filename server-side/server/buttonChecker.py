import sqlalchemy
import pandas as pd

engine = sqlalchemy.create_engine(
    'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

def state_checker(newState):
    try:
        # Construct SQL query to select the latest record from the database
        sql = "SELECT motorState FROM datalogs ORDER BY collectedDate DESC LIMIT 1 OFFSET 1;"

        # Execute the SQL query and load result into a DataFrame
        df = pd.read_sql(sql, engine)
        state = df.iloc[0]['motorState']
        if (state == newState):
            return newState
        else:
            return state
        
    except Exception as e:
        print("Error fetching latest data:", e)
        return None
