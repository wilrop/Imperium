import pandas as pd
import plotly.express as px


def calc_totals(grouped_df, group_str):
    """
    Method to create a pandas dataframe with all the nessecary data to generate
    the bubble chart plots in the compare_data method bellow.
    Args:
        grouped_df (dataframe): Dataframe which contains the data from the countries,
                            organisations or categories.
        group_str (Str): The selected type for which the data needs to be created 
                    (Country, Organisation or Category).
    Returns:
        Fig (Figure): Returns the correct bubble chart plot.
    """
    results = []
    for _, (by, group) in enumerate(grouped_df):
        if not group.empty:
            for year in range(2012, 2022):
                year_data = group[group['year'] == year]
                if year_data.empty:
                    data = [by, year, 0, 0, 0, 0.00001]
                else:
                    lobbyists = year_data['lobbyists (FTE)'].sum()
                    meetings = year_data['# of meetings'].sum()
                    ep_passes = year_data['EP passes'].sum()
                    mid_point = year_data['end_int'].sum() - year_data['begin_int'].sum()
                    data = [by, year, lobbyists, meetings, ep_passes, mid_point]
                results.append(data)

    columns = [group_str, 'year', 'lobbyists (FTE)', '# of meetings', 'EP passes', 'Approximated spending']
    df = pd.DataFrame(results, columns=columns)
    return df


def compare_data(data, view):
    """
    Method to create a plotly animated bubble chart where the size of the bubble
    represents the approximated spending, the position of the bubble on the x-axis shows
    the number of meetings with the parliamentarians and the y-axis shows the number
    of lobbyists in a single year. The animation shows this plot over multiple years.
    Args:
        data (dataframe): Dataframe which contains the data from the countries,
                            organisations or categories.
        view (Str): The selected type for which the plot needs to be created 
                    (Country, Organisation or Category).
    Returns:
        Fig (Figure): Returns the correct bubble chart plot.
    """
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
                         hover_name=view, animation_group=view, log_x=True, size_max=60, template='plotly_white')
    else:
        size_max = 40
        padding = 0.25
        min_x = result_df['lobbyists (FTE)'].min()
        max_x = result_df['lobbyists (FTE)'].max()
        min_y = result_df['# of meetings'].min()
        max_y = result_df['# of meetings'].max()
        width = abs(max_x - min_x)
        height = abs(max_y - min_y)
        min_x = min_x - padding * width
        max_x = max_x + padding * width
        min_y = min_y - padding * height
        max_y = max_y + padding * height
        fig = px.scatter(result_df, x="lobbyists (FTE)", y="# of meetings", size="Approximated spending",
                         color=view, hover_name=view, animation_frame='year', range_x=[min_x, max_x],
                         range_y=[min_y, max_y], size_max=size_max, template='plotly_white')
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1250
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 3000
    return fig
