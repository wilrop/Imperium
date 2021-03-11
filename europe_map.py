import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



def map_plot():
    d = {'ISO-3': ["ESP", "BEL"], 'spending': ["Apple", "Shell"]}
    df = pd.DataFrame(data=d)
    fig = px.choropleth(df,
                         locations='ISO-3',
                         locationmode="ISO-3",
                         color="spending",
                         scope="europe",
                         labels={'spending': 'Biggest spending'},
                         width=1000,
                         height=1000
                         )


    

    return fig
