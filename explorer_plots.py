import plotly.express as px
import plotly.graph_objects as go



def explore_country(country_data):
    fig = px.bar(country_data, x='year', y='lobbying costs')
    return fig


def explore_category():
    return 0

def explore_business(business_data):
    fig = go.Figure(data=[go.Candlestick(x=business_data['year'],
                       open=business_data['begin_int'], high=business_data['end_int'],
                       low=business_data['begin_int'], close=business_data['end_int'])]
                       )
                       
    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig