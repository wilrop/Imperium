import plotly.express as px
import plotly.graph_objects as go
from preprocessing import amount_years



def explore_country(country_data):
    sum_begin_int = [0] * (amount_years + 1)
    sum_end_int = [0]  * (amount_years + 1)
    year_list = []
    yearly = country_data.groupby(['year'])
    

    for idx,(year,group) in enumerate(yearly):
        year_list.append(year)
        for min,max in zip(group['begin_int'],group['end_int']):
            sum_begin_int[idx] += min
            sum_end_int[idx] += max
    
    fig = go.Figure(data=[go.Candlestick(x=year_list,
                       open=sum_begin_int, high=sum_end_int,
                       low=sum_begin_int, close=sum_end_int)]
                       )
                       
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig


def explore_category(category_data):
    print(category_data)
    sum_begin_int = [0] * (amount_years + 1)
    sum_end_int = [0]  * (amount_years + 1)
    year_list = []
    yearly = category_data.groupby(['year'])
    

    for idx,(year,group) in enumerate(yearly):
        year_list.append(year)
        for min,max in zip(group['begin_int'],group['end_int']):
            sum_begin_int[idx] += min
            sum_end_int[idx] += max
    
    fig = go.Figure(data=[go.Candlestick(x=year_list,
                       open=sum_begin_int, high=sum_end_int,
                       low=sum_begin_int, close=sum_end_int)]
                       )
                       
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

def explore_business(business_data):
    fig = go.Figure(data=[go.Candlestick(x=business_data['year'],
                       open=business_data['begin_int'], high=business_data['end_int'],
                       low=business_data['begin_int'], close=business_data['end_int'])]
                       )
                       
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig