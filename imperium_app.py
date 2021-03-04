import argparse
import itertools
import pandas as pd
import streamlit as st
import plotly.express as px

from md_templates import *
from preprocessing import preprocess

categories = {
        'Professional consultancies/law firms/self-employed consultants': (
            'Professional consultancies',
            'Law firms',
            'Self-employed consultants'
        ),
        'In-house lobbyists and trade/professional associations': (
            'Companies & groups',
            'Trade and business organisations',
            'Trade unions and professional associations',
            'Other in house lobbyists'
        ),
        'Non-governmental organisations': (
            'Non-governmental organisations, platforms and networks and similar',
        ),
        'Think tanks, research and academic institutions': (
            'Think tanks and research institutions',
            'Academic institutions'
        ),
        'Organisations representing churches and religious communities': (
            'Organisations representing churches and religious communities',
        ),
        'Organisations representing local, regional and municipal authorities, other public or mixed entities, etc.': (
            'Regional structures',
            'Other sub-national public authorities',
            'Transnational associations and networks of public regional or other sub-national authorities',
            'Other public or mixed entities, created by law whose purpose is to act in the public interest'
        )
    }

all_categories = tuple(itertools.chain.from_iterable(categories.items()))


def run(args):
    print('Running the Imperium app')
    data = preprocess(args.data)

    # Main template
    st.markdown(start_template)

    # Sidebar elements
    view_selectbox = st.sidebar.selectbox(
        "What would you like to see?",
        ('Show me the map', 'Categories')
    )

    data_explorer_button = st.sidebar.button('Explore the raw data!')

    if data_explorer_button:
        st.markdown(data_explorer_template)
        st.dataframe(data)

    if view_selectbox == 'Show me the map':
        draw_map()
    elif view_selectbox == 'Categories':
        st.markdown(categories_template)
        category_selectbox = st.selectbox("Select category", tuple(categories.keys()))
        if category_selectbox in categories.keys():
            print(categories[category_selectbox])
            st.selectbox('Select subcategory', categories[category_selectbox])
        st.markdown(compare_categories_template)
        compare_multiselect = st.multiselect('Compare categories', all_categories)


def draw_map():
    d = {'ISO-3': ["ESP", "BEL"], 'spending': ["Apple", "Shell"]}
    df = pd.DataFrame(data=d)
    fig = px.choropleth(df,
                        locations='ISO-3',
                        locationmode="ISO-3",
                        color="spending",
                        scope="europe",
                        labels={'spending': 'Biggest spending'},
                        )
    st.write(fig)


if __name__ == "__main__":
    print('Starting the Imperium app')

    # Starting the parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data', help='The folder containing the data')
    args = parser.parse_args()

    run(args)

    print('Shut down the Imperium app')
