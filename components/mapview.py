import sqlalchemy
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


def get_data():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://python:python123!@localhost:3306/ETAS_IOT')

    # SQL query to fetch all records
    sql = "SELECT collectedDate, longitude, latitude, phValue, tdsValue, tempValue, turbidityValue FROM datalogs"

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


def render_map(app: dash.Dash) -> dbc.Row:
    # Fetch data
    data = get_data()

    # Calculate purity index
    data_with_purity = calculate_purity_index(data)

    # Plot map
    fig = px.scatter_mapbox(data_with_purity,
                            lat="latitude",
                            lon="longitude",
                            color="purity_index",
                            color_continuous_scale=px.colors.sequential.Viridis,
                            size_max=15,
                            zoom=10,
                            hover_data={"purity_index": True})

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(title="Water Purity Map")

    # Return the map as a Dash component
    return dbc.Row([
        dcc.Graph(figure=fig)
    ])
