import plotly.express as px
import plotly.graph_objects as go


def compare_countries(countries_data):
    fig = px.bar(countries_data, x='country head office', y=['begin_int', 'end_int'])
    return fig


def compare_categories(categories_data):
    fig = px.bar(categories_data, x='main_cat', y=['begin_int', 'end_int'])
    return fig


def compare_businesses(businesses_data):
    fig = px.bar(businesses_data, x='organisation name', y=['begin_int', 'end_int'])
    return fig
