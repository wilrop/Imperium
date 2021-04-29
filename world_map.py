import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def map_plot(iso3_codes, countries_bussines_amount):
    d = {'ISO-3': iso3_codes, 'spending': countries_bussines_amount}
    df = pd.DataFrame(data=d)
    fig = px.choropleth(df,
                        locations='ISO-3',
                        color="spending",
                        scope="world",
                        labels={'spending': 'Amount of companies'},
                        height=600,
                        hover_name=df['spending'],
                        hover_data=['spending'],
                        custom_data=['spending']
                        )

    fig.update_layout(
        title_text='Number of organisations lobbying in the EU',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'))
    fig.update_traces(hovertemplate="Number of organisations: %{customdata}")
    return fig
