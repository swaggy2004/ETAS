from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import sqlalchemy

# Function to retrieve data from the database


def retrieve_data():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')
    sql = "SELECT collectedDate, latitude, longitude, phValue, tdsValue, tempValue, turbidityValue FROM datalogs"
    df = pd.read_sql(sql, engine)
    df['collectedDate'] = pd.to_datetime(df['collectedDate'])
    return df

# Calculate water purity index based on sensor data


def calculate_purity(df):
    # Normalize sensor readings to a scale of 0 to 1
    df['normalized_ph'] = (df['phValue'] - df['phValue'].min()) / \
        (df['phValue'].max() - df['phValue'].min())
    df['normalized_tds'] = (df['tdsValue'] - df['tdsValue'].min()) / \
        (df['tdsValue'].max() - df['tdsValue'].min())
    df['normalized_turbidity'] = (df['turbidityValue'] - df['turbidityValue'].min()) / (
        df['turbidityValue'].max() - df['turbidityValue'].min())
    df['normalized_temp'] = (df['tempValue'] - df['tempValue'].min()) / \
        (df['tempValue'].max() - df['tempValue'].min())

    # Calculate water purity index (weighted average)
    # Adjust the weights based on importance of each factor
    df['purityIndex'] = (df['normalized_ph'] * 0.25 + df['normalized_tds'] * 0.25 +
                         df['normalized_turbidity'] * 0.25 + df['normalized_temp'] * 0.25)

    return df[['collectedDate', 'latitude', 'longitude', 'purityIndex']]

# Function to create the heatmap


def create_heatmap(df):
    # Get the latest longitude and latitude
    latest_location = df[['latitude', 'longitude']].iloc[-1]
    latest_latitude = float(latest_location['latitude'])
    latest_longitude = float(latest_location['longitude'])
    fig = px.density_mapbox(df, lat='latitude', lon='longitude', z='purityIndex',
                            radius=10, center=dict(lat=latest_latitude, lon=latest_longitude),
                            zoom=18, mapbox_style="open-street-map", range_color=[0, 1],
                            color_continuous_scale=px.colors.sequential.Reds)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Function to render the map component


def render_map(app: Dash) -> dbc.Row:
    df = retrieve_data()
    df = calculate_purity(df)
    fig = create_heatmap(df)
    return dbc.Row([
        dcc.Graph(figure=fig),
    ], className="mb-3")

