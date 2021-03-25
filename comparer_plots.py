import plotly.express as px
import plotly.graph_objects as go


def explore_country(country_data):
    fig = px.bar(country_data, x='year', y='lobbying costs')
    return fig


def explore_category():
    return 0


def compare_businesses(businesses_data):
    fig = px.bar(businesses_data, x='organisation name', y=['begin_int', 'end_int'])
    return fig