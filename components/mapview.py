import sqlalchemy
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


def get_data():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

    # SQL query to fetch all records
    sql = "SELECT collectedDate, latitude, longitude, phValue, tdsValue, tempValue, turbidityValue FROM datalogs"

    # Read data from SQL into DataFrame
    df = pd.read_sql(sql, engine)

    # Convert 'collectedDate' column to datetime
    df['collectedDate'] = pd.to_datetime(df['collectedDate'])

    return df


def calculate_purity_index(df, weights={'ph': 0.25, 'turbidity': 0.25, 'temp': 0.25, 'tds': 0.25}):
    # Normalize data
    df_normalized = df.copy()
    for col in ['phValue', 'turbidityValue', 'tempValue', 'tdsValue']:
        df_normalized[col] = (df_normalized[col] - df_normalized[col].min()) / \
            (df_normalized[col].max() - df_normalized[col].min())

    # Calculate purity index
    df['purity_index'] = (df_normalized['phValue'] * weights['ph'] +
                          df_normalized['turbidityValue'] * weights['turbidity'] +
                          df_normalized['tempValue'] * weights['temp'] +
                          df_normalized['tdsValue'] * weights['tds']) / sum(weights.values())

    return df


def render_heatmap(app: Dash):
    # Fetch data
    data = get_data()

    # Drop rows with non-numeric latitude or longitude values
    data = data.dropna(subset=['latitude', 'longitude', 'phValue',
                       'tdsValue', 'tempValue', 'turbidityValue'], how='any')
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

    # Calculate purity index
    data_with_purity = calculate_purity_index(data)

    # Plot heatmap
    fig = px.density_mapbox(data_with_purity,
                            lat='latitude',
                            lon='longitude',
                            z='purity_index',
                            radius=10,
                            center=dict(lat=0, lon=180),
                            zoom=0,
                            mapbox_style="open-street-map",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            opacity=0.6,
                            title="Water Purity Heatmap")

    return fig