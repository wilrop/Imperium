import pandas as pd
import plotly.express as px


def map_plot():
    d = {'ISO-3': ["ESP", "BEL"], 'spending': ["Apple", "Shell"]}
    df = pd.DataFrame(data=d)
    plot = px.choropleth(df,
                         locations='ISO-3',
                         locationmode="ISO-3",
                         color="spending",
                         scope="europe",
                         labels={'spending': 'Biggest spending'},
                         )

    return plot
