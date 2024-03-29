import plotly.express as px
import plotly.graph_objects as go
from preprocessing import amount_years
import numpy as np

# The colours for the error bars and the lines connecting them.
marker_color = 'rgba(55, 153, 81, 1)'
line_color = 'rgba(55, 153, 81, 0.4)'


def calc_totals(df):
    """
    Method to generate the minimum, the average and the maximum for the error bars in the plots.
    Args:
        df (df): Pandas dataframe which contains the data of the intervals.
    Returns:
        year_list (List[Int]): List of the years in the correct order.
        sum_begin_int (List[Int]): List of the minimums of the intervals in the correct order.
        sum_middle_int (List[Int]): List of the averages of the intervals in the correct order.
        sum_end_int (List[Int]): List of the maximums of the intervals in the correct order.
    """
    grouped_df = df.groupby(['year'])

    sum_begin_int = np.zeros(amount_years + 1)
    sum_middle_int = np.zeros(amount_years + 1)
    sum_end_int = np.zeros(amount_years + 1)
    year_list = []

    for idx, (year, group) in enumerate(grouped_df):
        year_list.append(str(year))

        for min_spending, max_spending in zip(group['begin_int'], group['end_int']):
            sum_begin_int[idx] += min_spending
            sum_end_int[idx] += max_spending
            sum_middle_int[idx] += (min_spending + max_spending) / 2

    return year_list, sum_begin_int, sum_middle_int, sum_end_int


def create_error_bar_plot(year_list, sum_begin_int, sum_middle_int, sum_end_int, marker_color, line_color):
    """
    Method to a generate a Plotly Error Bar plot.
    Args:
        year_list (List[Int]): List of the years in the correct order.
        sum_begin_int (List[Int]): List of the minimums of the intervals in the correct order.
        sum_middle_int (List[Int]): List of the averages of the intervals in the correct order.
        sum_end_int (List[Int]): List of the maximums of the intervals in the correct order.
        marker_color (Str): Colour for the error bars.
        line_color (Str): Colour for the lines that connect the error bars.
    Returns:
        fig (Figure): Return the newly created explore plot.
    """
    error_plus = sum_end_int - sum_middle_int
    error_minus = sum_middle_int - sum_begin_int

    fig = go.Figure(data=go.Scatter(
        x=year_list,
        y=sum_middle_int,
        marker=dict(color=marker_color),
        line=dict(color=line_color),
        error_y=dict(
            type='data',
            symmetric=False,
            color=marker_color,
            array=error_plus,
            arrayminus=error_minus),
        hovertemplate='Spending: <br>' +
                      'Minimum: %{error_y.arrayminus} €<br>' +
                      'Average: %{y:} €<br>' +
                      'Maximum: %{error_y.array} €' + '<extra></extra>'
    ))

    fig.update_layout(
        template='plotly_white',
        xaxis_title="Year",
        yaxis_title="Total Spending",
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ))
    
    return fig


def explore_country(country_data):
    """
    Method to a generate Plotly Error Bar plot which shows the total spending of a single country,
    with error bars for each year which represent the lobbying cost intervals.
    Args:
        country_data (dataframe): A pandas dataframe that contains all the information from
        the selected country.
    Returns:
        fig (Figure): Return the newly created explore plot for a country.
    """
    year_list, sum_begin_int, sum_middle_int, sum_end_int = calc_totals(country_data)

    fig = create_error_bar_plot(year_list, sum_begin_int, sum_middle_int, sum_end_int, marker_color, line_color)

    return fig


def explore_category(category_data):
    """
    Method to a generate Plotly Error Bar plot which shows the total spending of a single organisation category,
    with error bars for each year which represent the lobbying cost intervals.
    Args:
        category_data (dataframe): A pandas dataframe that contains all the information from
        the selected organisation category.
    Returns:
        fig (Figure): Return the newly created explore plot for an organisation category.
    """
    year_list, sum_begin_int, sum_middle_int, sum_end_int = calc_totals(category_data)

    fig = create_error_bar_plot(year_list, sum_begin_int, sum_middle_int, sum_end_int, marker_color, line_color)

    return fig


def explore_organisation(organisation_data):
    """
    Method to a generate Plotly Error Bar plot which shows the total spending of a single organisation,
    with error bars for each year which represent the lobbying cost intervals.
    Args:
        organisation_data (dataframe): A pandas dataframe that contains all the information from
        the selected organisation.
    Returns:
        fig (Figure): Return the newly created explore plot for a single organisation.
    """
    sum_begin_int = np.array(organisation_data['begin_int'])
    sum_middle_int = np.array((organisation_data['begin_int'] + organisation_data['end_int']) / 2)
    sum_end_int = np.array(organisation_data['end_int'])
    year_list = [str(x) for x in list(organisation_data['year'])]

    fig = create_error_bar_plot(year_list, sum_begin_int, sum_middle_int, sum_end_int, marker_color, line_color)

    return fig
