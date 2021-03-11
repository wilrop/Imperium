import plotly.express as px
import plotly.graph_objects as go



def explore_country(country_data):
    fig = px.bar(country_data, x='year', y='lobbying costs')
    return fig


def explore_category():
    return 0



#Dummy data
year = [2014,2015,2016,2017]
lobbying_cost_low = [10000,20000,30000,40000]
lobbying_cost_high = [50000,60000,50000,100000]


def explore_business(business_data):
    fig = go.Figure(data=[go.Candlestick(x=year,
                       open=lobbying_cost_low, high=lobbying_cost_high,
                       low=lobbying_cost_low, close=lobbying_cost_high)]
                       )
                       
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig