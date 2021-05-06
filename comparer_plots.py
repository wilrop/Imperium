import pandas as pd
import plotly.express as px


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
                         hover_name="Country", log_x=True, size_max=60)
    else:
        fig = px.scatter(result_df, x="lobbyists (FTE)", y="# of meetings", size="Approximated spending",
                     color=view, hover_name=view, log_x=True, size_max=60)

    return fig
