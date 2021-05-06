import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def map_plot(iso3_codes, countries_bussines_amount,countries_list):
    d = {'ISO-3': iso3_codes, 'spending': countries_bussines_amount, 'countries': countries_list}
    df = pd.DataFrame(data=d)
    fig = px.choropleth(df,
                        locations='ISO-3',
                        color="spending",
                        scope="world",
                        labels={'spending': 'Amount of companies'},
                        height=600,
                        hover_name=df['countries'],
                        hover_data=['spending'],
                        custom_data=['spending','countries']
                        )

    fig.update_layout(
        title_text='Number of organisations lobbying in the EU',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'))
    fig.update_traces(hovertemplate="<b> %{customdata[1]} </b> : Number of organisations: %{customdata[0]}")
    return fig

def map_plot_click(iso3_codes, countries_bussines_amount,countries_list , iso_selected):
    d = {'ISO-3': iso3_codes, 'spending': countries_bussines_amount, 'countries': countries_list}
    df = pd.DataFrame(data=d)
    df = df.loc[df['ISO-3'] == iso_selected]
    spending = df['spending']
    country = df['countries']
    fig = px.choropleth(df,
                        locations=[iso_selected],
                        color=[1],
                        scope="world",
                        labels={'spending': 'Amount of companies'},
                        height=600,
                        hover_data=['spending'],
                        custom_data=['spending','countries']
                        )

    fig.update_layout(
        title_text='Number of organisations lobbying in the EU',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'))
    fig.update_traces(hovertemplate="<b> %{customdata[1]} </b> : Number of organisations: %{customdata[0]}")
    return fig
