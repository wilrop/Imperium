import plotly.express as px
import plotly.graph_objects as go
from preprocessing import amount_years
import numpy as np

marker_color = 'rgba(55, 153, 81, 1)'
line_color = 'rgba(55, 153, 81, 0.4)'


def calc_totals(df):
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


def explore_country(country_data):
    '''
        hovertemplate='MIN: %{error_y.arrayminus}<br>' +
               'MIDDLE: %{y:}<br>' + 
               'MAX: %{error_y.array}'
    '''
    # '<extra></extra>'
    year_list, sum_begin_int, sum_middle_int, sum_end_int = calc_totals(country_data)

    error_plus = sum_end_int - sum_middle_int
    error_minus = sum_middle_int - sum_begin_int

    print([sum_begin_int.tolist(), sum_end_int.tolist()])

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
        customdata = [sum_begin_int.tolist(), sum_end_int.tolist()],
        hovertemplate='MIN: %{customdata[0]}<br>' +
               'MIDDLE: %{y:}<br>' + 
               'MAX: %{customdata[1]}',
    ))

    fig.update_layout(
        template='plotly_white',
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ))

    return fig


def explore_category(category_data):
    year_list, sum_begin_int, sum_middle_int, sum_end_int = calc_totals(category_data)

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
            arrayminus=error_minus)
    ))

    fig.update_layout(
        template='plotly_white',
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ))

    return fig


def explore_business(business_data):
    sum_begin_int = np.array(business_data['begin_int'])
    sum_middle_int = np.array((business_data['begin_int'] + business_data['end_int']) / 2)
    sum_end_int = np.array(business_data['end_int'])
    year_list = [str(x) for x in list(business_data['year'])]

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
            arrayminus=error_minus)
    ))

    fig.update_layout(
        template='plotly_white',
    xaxis=dict(
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ))

    return fig
