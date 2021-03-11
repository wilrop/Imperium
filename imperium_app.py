import argparse
import streamlit as st

import md_templates
import europe_map
from data_loader import DataLoader


def run(args):
    print('Running the Imperium app')
    data = DataLoader()

    countries = data.get_countries()
    categories = data.get_top_level_categories()
    businesses = data.get_businesses()

    # Main template
    st.markdown(md_templates.start_template)

    # Sidebar elements
    view_selectbox = st.sidebar.selectbox(
        'What would you like to do?',
        ('Show me the map', 'Explore', 'Compare')
    )

    data_explorer_button = st.sidebar.button('Explore the raw data!')

    if data_explorer_button:
        st.markdown(md_templates.data_explorer_template)
        st.dataframe(data)

    if view_selectbox == 'Show me the map':
        _max_width_()
        map = europe_map.map_plot()
        st.write(map)
    elif view_selectbox == 'Explore':
        st.markdown(md_templates.explore_template)

        st.markdown(md_templates.explore_countries_template)
        country = st.selectbox("Select country", countries)
        # TODO: decide on visualisation

        st.markdown(md_templates.explore_categories_template)
        category = st.selectbox("Select category", categories)
        if category in categories:
            st.selectbox('Select subcategory', data.get_low_level_categories(category))
        # TODO: decide on visualisation

        st.markdown(md_templates.explore_businesses_template)
        business = st.selectbox("Select business", businesses)
        # TODO: decide on visualisation

    elif view_selectbox == 'Compare':
        st.markdown(md_templates.compare_template)

        st.markdown(md_templates.compare_countries_template)
        comp_countries = st.multiselect("Select countries", countries)
        # TODO: decide on visualisation

        st.markdown(md_templates.compare_categories_template)
        comp_categories = st.multiselect("Select categories", categories)
        # TODO: decide on visualisation

        st.markdown(md_templates.compare_businesses_template)
        business = st.multiselect("Select businesses", businesses)
        # TODO: decide on visualisation


def _max_width_():  # Streamlit will open plotly graphs in a small window, this will make it fullscreen.
    max_width_str = f"max-width: 2000px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    print('Starting the Imperium app')

    # Starting the parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data', help='The folder containing the data')
    args = parser.parse_args()

    run(args)

    print('Shut down the Imperium app')
