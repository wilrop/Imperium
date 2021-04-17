import plotly.express as px
import plotly.graph_objects as go
from preprocessing import amount_years
import numpy as np

marker_color = 'rgba(55, 153, 81, 1)'
line_color = 'rgba(55, 153, 81, 0.4)'

def explore_country(country_data):
    sum_begin_int = [0] * (amount_years + 1)
    sum_middle_int = [0]  * (amount_years + 1)
    sum_end_int = [0]  * (amount_years + 1)
    year_list = []
    yearly = country_data.groupby(['year'])
    
    for idx,(year,group) in enumerate(yearly):
        year_list.append(year)
        for min,max in zip(group['begin_int'], group['end_int']):
            sum_begin_int[idx] += min
            sum_end_int[idx] += max
            sum_middle_int[idx] += (min + max) / 2
    
    sum_begin_int = np.array(sum_begin_int)
    sum_middle_int = np.array(sum_middle_int)
    sum_end_int = np.array(sum_end_int)
    year_list = [str(x) for x in year_list]
    
    fig = go.Figure(data=go.Scatter(
        x=year_list,
        y=sum_middle_int,
        marker=dict(color=marker_color),
        line=dict(color=line_color),
        error_y=dict(
            type='data',
            symmetric=False,
            color=marker_color,
            array=sum_end_int - sum_middle_int,
            arrayminus=sum_middle_int - sum_begin_int)
        ))
    
    return fig


def explore_category(category_data):
    sum_begin_int = [0] * (amount_years + 1)
    sum_middle_int = [0]  * (amount_years + 1)
    sum_end_int = [0]  * (amount_years + 1)
    year_list = []
    yearly = category_data.groupby(['year'])
    
    for idx,(year,group) in enumerate(yearly):
        year_list.append(year)
        for min,max in zip(group['begin_int'],group['end_int']):
            sum_begin_int[idx] += min
            sum_end_int[idx] += max
            sum_middle_int[idx] += (min + max) / 2

    sum_begin_int = np.array(sum_begin_int)
    sum_middle_int = np.array(sum_middle_int)
    sum_end_int = np.array(sum_end_int)
    year_list = [str(x) for x in year_list]
    
    fig = go.Figure(data=go.Scatter(
        x=year_list,
        y=sum_middle_int,
        marker=dict(color=marker_color),
        line=dict(color=line_color),
        error_y=dict(
            type='data',
            symmetric=False,
            color=marker_color,
            array=sum_end_int - sum_middle_int,
            arrayminus=sum_middle_int - sum_begin_int)
        ))
    return fig


def explore_business(business_data):
    sum_begin_int = np.array(business_data['begin_int'])
    sum_middle_int = np.array((business_data['begin_int'] + business_data['end_int']) / 2)
    sum_end_int = np.array(business_data['end_int'])
    year_list = [str(x) for x in list(business_data['year'])]

    fig = go.Figure(data=go.Scatter(
        x=year_list,
        y=sum_middle_int,
        marker=dict(color=marker_color),
        line=dict(color=line_color),
        error_y=dict(
            type='data',
            symmetric=False,
            color=marker_color,
            array=sum_end_int - sum_middle_int,
            arrayminus=sum_middle_int - sum_begin_int)
        ))

    return fig