import pandas as pd
import plotly.express as px


def calc_totals(grouped_df, group_str):
    results = []
    for _, (by, group) in enumerate(grouped_df):
        if not group.empty:
            year_group = group.groupby(['year'])
            for _, (year, year_group) in enumerate(year_group):
                lobbyists = year_group['lobbyists (FTE)'].sum()
                meetings = year_group['# of meetings'].sum()
                ep_passes = year_group['EP passes'].sum()
                mid_point = year_group['end_int'].sum() - year_group['begin_int'].sum()
                results.append([by, str(year), lobbyists, meetings, ep_passes, mid_point])

    columns = [group_str, 'year', 'lobbyists (FTE)', '# of meetings', 'EP passes', 'Approximated spending']
    df = pd.DataFrame(results, columns=columns)
    return df


def compare_data(data, view):
    if view == 'Country':
        data_grouped = data.groupby(['country head office'])
        result_df = calc_totals(data_grouped, 'Country')
    elif view == 'Organisation':
        data_grouped = data.groupby(['organisation name'])
        result_df = calc_totals(data_grouped, 'Organisation')
    else:
        data_grouped = data.groupby(['sub_cat'])
        result_df = calc_totals(data_grouped, 'Category')

    if result_df.empty:
        fig = px.scatter(result_df, x="lobbyists (FTE)", y="# of meetings", size="Approximated spending",
                         hover_name=view, animation_group=view, log_x=True, size_max=60)
    else:
        spacing = 60
        min_x = max(0.1, result_df['lobbyists (FTE)'].min() - spacing*2)
        max_x = result_df['lobbyists (FTE)'].max() + spacing*2
        min_y = result_df['# of meetings'].min() - spacing*2
        max_y = result_df['# of meetings'].max() + spacing*2
        fig = px.scatter(result_df, x="lobbyists (FTE)", y="# of meetings", size="Approximated spending",
                         color=view, hover_name=view, animation_frame='year', animation_group=view, log_x=True,
                         size_max=spacing)

    return fig
