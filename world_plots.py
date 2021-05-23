import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geopy.geocoders import Nominatim

# Initialising the GeoPy geolocator to receive geocodes from a country by name
# Which will be used for zooming to a specific country
geolocator = Nominatim(user_agent="Imperium")


def map_plot(iso3_codes, countries_organisations_amount,countries_list):
    """
    This function will create a new plotly choropleth that displays the number
    of organisations that are lobbying in the different countries.
    :param iso3_codes: A list that contains the iso3 codes for each country.
    :param countries_organisations_amount: A list that contains the number of organisations for each country.
    :param country_name: A list that contains all the countries.
    :return: An new world map.
    """
    d = {'ISO-3': iso3_codes, 'spending': countries_organisations_amount, 'countries': countries_list}
    df = pd.DataFrame(data=d)
    fig = px.choropleth(df,
                        locations='ISO-3',
                        color="spending",
                        scope="world",
                        labels={'spending': 'Amount of organisations'},
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
    This function will zoom on the world map where the user has clicked.
    :param world_map: The current world map.
    :param country_name: The country where the user has clicked.
    :return: An updated world map.
    """
    location = geolocator.geocode(country_name)
    latitude, longitude = location.latitude, location.longitude
    geo = dict(
        projection_scale=2,  # this is kind of like zoom
        center=dict(lat=latitude, lon=longitude),  # this will center on the point
    )
    world_map.update_layout(geo=geo)
    return world_map
    