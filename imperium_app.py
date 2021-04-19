import argparse
import streamlit as st

import md_templates
import world_map
import explorer_plots
import comparer_plots
from data_loader import DataLoader


def run():
    """
    This is the main function that runs our streamlit app.
    :return: /
    """
    data = DataLoader()  # Initialise the data loader.

    countries = data.get_countries()
    categories = data.get_main_categories()
    sub_categories = data.get_sub_categories()
    businesses = data.get_businesses()

    # Main template
    st.markdown(md_templates.start_template)

    # Sidebar elements
    view_selectbox = st.sidebar.selectbox(
        'What would you like to do?',
        ('Show me the map', 'Explore', 'Compare', 'View raw data')
    )

    if view_selectbox == 'Show me the map':
        _max_width_()
        iso3_codes, countries_bussines_amount = data.get_country_amount_of_companies()
        map = world_map.map_plot(iso3_codes, countries_bussines_amount)
        st.write(map, width=5000, height=5000)
    elif view_selectbox == 'Explore':
        st.markdown(md_templates.explore_template)

        st.markdown(md_templates.explore_countries_template)
        country = st.selectbox("Select country", countries)
        country_data = data.get_country_data(country)
        country_plot = explorer_plots.explore_country(country_data)
        st.write(country_plot)

        st.markdown(md_templates.explore_categories_template)
        category = st.selectbox("Select category", categories)
        if category in categories:
            subcategory = st.selectbox('Select subcategory', data.get_sub_categories_for_main(category))
            subcategory_data = data.get_subcategory_data(category, subcategory)
            if not subcategory_data.empty:
                category_plot = explorer_plots.explore_category(subcategory_data)
                st.write(category_plot)

        st.markdown(md_templates.explore_businesses_template)
        business = st.selectbox("Select business", businesses)
        business_data = data.get_business_data(business)
        business_plot = explorer_plots.explore_business(business_data)
        st.write(business_plot)

    elif view_selectbox == 'Compare':
        st.markdown(md_templates.compare_template)

        st.markdown(md_templates.compare_countries_template)
        countries_lst = st.multiselect("Select countries", countries)
        countries_data = data.get_countries_data(countries_lst)
        if not countries_data.empty:
            countries_plot = comparer_plots.compare_countries(countries_data)
            st.write(countries_plot)

        st.markdown(md_templates.compare_categories_template)
        categories_lst = st.multiselect("Select categories", categories)
        categories_data = data.get_categories_data(categories_lst)
        if not categories_data.empty:
            categories_plot = comparer_plots.compare_categories(categories_data)
            st.write(categories_plot)

        st.markdown(md_templates.compare_businesses_template)
        businesses_lst = st.multiselect("Select businesses", businesses)
        businesses_data = data.get_businesses_data(businesses_lst)
        if not businesses_data.empty:
            businesses_plot = comparer_plots.compare_businesses(businesses_data)
            st.write(businesses_plot)

    elif view_selectbox == 'View raw data':
        st.markdown(md_templates.data_explorer_template)
        st.dataframe(data.data)


def _max_width_():
    """
    Streamlit will open plotly graphs in a small window, this will make it fullscreen.
    :return: /
    """
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
    run()
