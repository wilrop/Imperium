import streamlit as st
import pandas as pd
import plotly.express as px

d = {'ISO-3': ["ESP", "BEL"], 'spending': ["Apple", "Shell"]}
df = pd.DataFrame(data=d)

def draw_map():

    fig = px.choropleth(df,
    locations='ISO-3', 
    locationmode="ISO-3", 
    color="spending", 
    scope="europe", 
    labels={'spending':'Biggest spending'},
    )
    st.write(fig)





