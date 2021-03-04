import argparse
import streamlit as st

import md_templates
import europe_map
import preprocessing


def run(args):
    print('Running the Imperium app')
    data = preprocessing.preprocess(args.data)

    # Main template
    st.markdown(md_templates.start_template)

    # Sidebar elements
    view_selectbox = st.sidebar.selectbox(
        "What would you like to see?",
        ('Show me the map', 'Categories')
    )

    data_explorer_button = st.sidebar.button('Explore the raw data!')

    if data_explorer_button:
        st.markdown(md_templates.data_explorer_template)
        st.dataframe(data)

    if view_selectbox == 'Show me the map':
        map = europe_map.map_plot()
        st.write(map)
    elif view_selectbox == 'Categories':
        st.markdown(md_templates.categories_template)
        category_selectbox = st.selectbox("Select category", tuple(preprocessing.categories.keys()))
        if category_selectbox in preprocessing.categories.keys():
            print(preprocessing.categories[category_selectbox])
            st.selectbox('Select subcategory', preprocessing.categories[category_selectbox])
        st.markdown(md_templates.compare_categories_template)
        compare_multiselect = st.multiselect('Compare categories', preprocessing.all_categories)


if __name__ == "__main__":
    print('Starting the Imperium app')

    # Starting the parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data', help='The folder containing the data')
    args = parser.parse_args()

    run(args)

    print('Shut down the Imperium app')
