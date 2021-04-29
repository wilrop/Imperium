import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def calc_totals(grouped_df, group_str):
    results = []
    for idx, (by, group) in enumerate(grouped_df):
        lobbyists = group['lobbyists (FTE)'].sum()
        meetings = group['# of meetings'].sum()
        ep_passes = group['EP passes'].sum()
        mid_point = group['end_int'].sum() - group['begin_int'].sum()
        results.append([by, lobbyists, meetings, ep_passes, mid_point])

    columns = [group_str, 'lobbyists (FTE)', '# of meetings', 'EP passes', 'Approximated spending']
    df = pd.DataFrame(results, columns=columns)
    return df


def compare_countries(countries_data):
    countries_data_grouped = countries_data.groupby(['country head office'])
    result_df = calc_totals(countries_data_grouped, 'Country')
    if result_df.empty:
        fig = px.scatter(result_df, x="lobbyists (FTE)", y="# of meetings", size="Approximated spending",
                         hover_name="Country", log_x=True, size_max=60)
    else:
        fig = px.scatter(result_df, x="lobbyists (FTE)", y="# of meetings", size="Approximated spending",
                         color="Country", hover_name="Country", log_x=True, size_max=60)
    return fig


def compare_categories(categories_data):
    categories_data_grouped = categories_data.groupby(['main_cat'])
    result_df = calc_totals(categories_data_grouped, 'Category')

    fig = px.scatter(result_df, x="lobbyists (FTE)", y="# of meetings", size="Approximated spending",
                     color="Category", hover_name="Category", log_x=True, size_max=60)
    return fig


def compare_businesses(businesses_data):
    businesses_data_grouped = businesses_data.groupby(['organisation name'])
    result_df = calc_totals(businesses_data_grouped, 'Business')

    fig = px.scatter(result_df, x="lobbyists (FTE)", y="# of meetings", size="Approximated spending",
                     color="Business", hover_name="Business", log_x=True, size_max=60)
    return fig
