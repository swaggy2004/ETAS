from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import zscore
import sqlalchemy
# Function to retrieve data from the SQL database


def retrieve_data():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')
    sql = "SELECT collectedDate, latitude, longitude, phValue, tdsValue, tempValue, turbidityValue FROM datalogs"
    df = pd.read_sql(sql, engine)
    df['collectedDate'] = pd.to_datetime(df['collectedDate'])

    # Convert latitude and longitude columns to numeric with non-numeric values as NaN
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    return df

# Function to normalize the sensor data using Z-score normalization


def normalize_data(df):
    df['phValue_norm'] = zscore(df['phValue'])
    df['tdsValue_norm'] = zscore(df['tdsValue'])
    df['turbidityValue_norm'] = zscore(df['turbidityValue'])
    df['tempValue_norm'] = zscore(df['tempValue'])
    return df

# Function to calculate the water purity index with weighting


def calculate_water_purity_index(row, weights):
    ph_score = row['phValue_norm']
    tds_score = row['tdsValue_norm']
    turbidity_score = row['turbidityValue_norm']
    temp_score = row['tempValue_norm']
    return (ph_score * weights['ph'] +
            tds_score * weights['tds'] +
            turbidity_score * weights['turbidity'] +
            temp_score * weights['temperature'])


# Retrieve data from the SQL database
df = retrieve_data()

# Normalize the sensor data
df = normalize_data(df)

# Define the weights for each variable
weights = {
    'ph': 0.4,
    'tds': 0.2,
    'turbidity': 0.3,
    'temperature': 0.1
}

# Calculate the water purity index with weighting
df['water_purity_index'] = df.apply(
    calculate_water_purity_index, weights=weights, axis=1)


def render_map(app: Dash) -> dbc.Row:
    # Create the Plotly scatter mapbox trace
    trace = go.Scattermapbox(
        lat=df['latitude'],
        lon=df['longitude'],
        mode='markers',
        marker=dict(
            size=10,
            color=df['water_purity_index'],
            colorscale='Viridis',
            cmin=-3,
            cmax=3,
            colorbar=dict(
                title='Water Purity Index'
            )
        )
    )

    # Create the map layout
    layout = go.Layout(
        mapbox=dict(
            bearing=0,
            center=dict(
                lat=df['latitude'].mean(),
                lon=df['longitude'].mean()
            ),
            pitch=0,
            zoom=8,
            style='open-street-map'
        ),
        autosize=True
    )

    fig = go.Figure(data=[trace], layout=layout)

    return dbc.Row([
        dcc.Graph(figure=fig)
    ])
