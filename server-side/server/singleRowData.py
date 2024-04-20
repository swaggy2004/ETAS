import pandas as pd
import sqlalchemy
from time import sleep


def __update_view__():
    # Replace with the password you granted the 'python' user
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

    try:
        # Assuming 'created_at' column stores record creation time
        sql = "SELECT * FROM datalogs ORDER BY collectedDate DESC LIMIT 1"
        df = pd.read_sql_query(sql, engine)

        # Process or analyze the DataFrame (df will contain the newest record)
        print(df)

    except (sqlalchemy.exc.OperationalError, pymysql.err.OperationalError) as err:
        print(f"Error connecting to database: {err}")
    except Exception as err:  # Catch other potential exceptions
        print(f"Unexpected error: {err}")
