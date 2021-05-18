import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim


def map_plot(iso3_codes, countries_bussines_amount,countries_list):
    d = {'ISO-3': iso3_codes, 'spending': countries_bussines_amount, 'countries': countries_list}
    df = pd.DataFrame(data=d)
    fig = px.choropleth(df,
                        locations='ISO-3',
                        color="spending",
                        scope="world",
                        labels={'spending': 'Amount of companies'},
                        height=500,
                        hover_name=df['countries'],
                        hover_data=['spending'],
                        custom_data=['spending','countries']
                        )

    fig.update_layout(
        title_text='Number of organisations lobbying in the EU',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'))
    fig.update_traces(hovertemplate="<b> %{customdata[1]} </b> : Number of organisations: %{customdata[0]}")
    return fig


def zoom_world_map(world_map, country_name):
    """
    This function will zoom on where the user has clicked.
    :param world_map: The current world map.
    :param country_name: The country where the user has clicked.
    :return: An updated world map.
    """
    geolocator = Nominatim(user_agent="Imperium")
    location = geolocator.geocode(country_name)
    latitude, longitude = location.latitude, location.longitude
    geo = dict(
        projection_scale=2,  # this is kind of like zoom
        center=dict(lat=latitude, lon=longitude),  # this will center on the point
    )
    world_map.update_layout(geo=geo)
    return world_map


def map_plot_click(iso3_codes, countries_bussines_amount,countries_list , iso_selected):
    d = {'ISO-3': iso3_codes, 'spending': countries_bussines_amount, 'countries': countries_list}
    df = pd.DataFrame(data=d)
    df = df.loc[df['ISO-3'] == iso_selected]
    spending = df['spending']
    country = df['countries']
    fig = px.choropleth(df,
                        locations=[iso_selected],
                        color=[1],
                        scope="world",
                        labels={'spending': 'Amount of companies'},
                        height=500,
                        hover_data=['spending'],
                        custom_data=['spending','countries']
                        )

    fig.update_layout(
        title_text='Number of organisations lobbying in the EU',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'))
    fig.update_traces(hovertemplate="<b> %{customdata[1]} </b> : Number of organisations: %{customdata[0]}")
    return fig
