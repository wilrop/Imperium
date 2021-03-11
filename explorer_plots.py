import plotly.express as px


def explore_country(country_data):
    fig = px.bar(country_data, x='year', y='lobbying costs')
    return fig


def explore_category():
    return 0


def explore_business(business_data):
    fig = px.bar(business_data, x='year', y='lobbying costs')
    return fig