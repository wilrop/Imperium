import argparse
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px

import md_templates
import world_map as world_plot
import explorer_plots
import comparer_plots
from data_loader import DataLoader
from preprocessing import subcategory_to_main


external_stylesheets = ['https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
data = DataLoader()  # Initialise the data loader.

# Load static data
countries = data.get_countries()
categories = data.get_main_categories()
sub_categories = data.get_sub_categories()
businesses = data.get_businesses()

# Load necessary data and plot for world map
iso3_codes, countries_business_amount,countries_list = data.get_country_amount_of_companies()
world_map = world_plot.map_plot(iso3_codes, countries_business_amount,countries_list)


# Load current view
curr_view = 'Country'

@app.callback(Output('world-map', 'figure'),
              [Input('world-map', 'clickData')])
def update_map(click_data):
    if click_data != None:
        country_name = click_data['points'][0]['hovertext']
        iso_code = click_data['points'][0]['location']
        fig = world_plot.map_plot_click(iso3_codes, countries_business_amount,countries_list,iso_code)
    else:
        fig = world_plot.map_plot(iso3_codes, countries_business_amount,countries_list)
    return fig

# Callback to update the values in the compare dropdown
@app.callback(Output('explore-plot', 'figure'),
              [Input('countries-dropdown', 'value'),
               Input('businesses-dropdown', 'value'),
               Input('sub-categories-dropdown', 'value')])
def update_explore_dropdown(country, business, sub_category):
    ctx = dash.callback_context

    if ctx.triggered:
        dropdown = ctx.triggered[0]['prop_id'].split('.')[0]
        if dropdown == 'countries-dropdown':
            country_data = data.get_country_data(country)
            country_plot = explorer_plots.explore_country(country_data)
            return country_plot
        elif dropdown == 'businesses-dropdown':
            business_data = data.get_business_data(business)
            business_plot = explorer_plots.explore_business(business_data)
            return business_plot
        else:
            main_category = subcategory_to_main[sub_category]
            category_data = data.get_subcategory_data(main_category, sub_category)
            category_plot = explorer_plots.explore_category(category_data)
            return category_plot
    else:
        category_data = data.get_country_data(None)  # This data will the always be empty
        category_plot = explorer_plots.explore_category(category_data)
        return category_plot


'''# Callback for country explorer plots
@app.callback(dash.dependencies.Output('country-explore-plot', 'figure'),
              [dash.dependencies.Input('countries-dropdown-explore', 'value')])
def update_country_explorer(country):
    country_data = data.get_country_data(country)
    country_plot = explorer_plots.explore_country(country_data)
    return country_plot


# Callback for updating main category
@app.callback(dash.dependencies.Output('sub-categories-dropdown-explore', 'options'),
              [dash.dependencies.Input('main-categories-dropdown-explore', 'value')])
def update_main_category(category):
    if not category:
        raise PreventUpdate
    sub_categories = data.get_sub_categories_for_main(category)
    return sub_categories


# Callback for category explorer plots
@app.callback(dash.dependencies.Output('category-explore-plot', 'figure'),
              [dash.dependencies.Input('main-categories-dropdown-explore', 'value'),
               dash.dependencies.Input('sub-categories-dropdown-explore', 'value')])
def update_category_explorer(main_category, sub_category):
    if not (main_category and sub_category):
        category_data = data.get_country_data(None)  # This data will the always be empty
        category_plot = explorer_plots.explore_category(category_data)
        return category_plot
    else:
        category_data = data.get_subcategory_data(main_category, sub_category)
        category_plot = explorer_plots.explore_category(category_data)
        return category_plot


# Callback for business explorer plots
@app.callback(dash.dependencies.Output('business-explore-plot', 'figure'),
              [dash.dependencies.Input('businesses-dropdown-explore', 'value')])
def update_business_explorer(business):
    business_data = data.get_business_data(business)
    business_plot = explorer_plots.explore_business(business_data)
    return business_plot


# Callback for country comparer plots
@app.callback(dash.dependencies.Output('countries-compare-plot', 'figure'),
              [dash.dependencies.Input('countries-dropdown-compare', 'value')])
def update_country_comparer(countries):
    countries_data = data.get_countries_data(countries)
    countries_plot = comparer_plots.compare_countries(countries_data)
    return countries_plot

'''

# Callback for comparer plots
@app.callback(Output('compare-plot', 'figure'),
              [Input('compare-dropdown', 'value')])
def update_compare_plot(items):
    if curr_view == 'Country':
        df = data.get_countries_data(items)
    elif curr_view == 'Category':
        df = data.get_sub_categories_data(items)
    else:
        df = data.get_businesses_data(items)

    fig = comparer_plots.compare_data(df, curr_view)
    return fig


# Callback to update the values in the compare dropdown
@app.callback(Output('compare-dropdown', 'options'),
              Output('compare-dropdown', 'value'),
              [Input('countries-dropdown', 'value'),
               Input('businesses-dropdown', 'value'),
               Input('sub-categories-dropdown', 'value')])
def update_compare_dropdown(country, business, sub_category):
    ctx = dash.callback_context

    if ctx.triggered:
        global curr_view
        dropdown = ctx.triggered[0]['prop_id'].split('.')[0]
        if dropdown == 'countries-dropdown':
            curr_view = 'Country'
            return countries, [country]
        elif dropdown == 'businesses-dropdown':
            curr_view = 'Business'
            return businesses, [business]
        else:
            curr_view = 'Category'
            return sub_categories, [sub_category]
    else:
        return countries, []


# App layout
app.layout = html.Div([
    dcc.Markdown(children=md_templates.start_template),
    html.Div([
        html.Div([
            dcc.Dropdown(id='countries-dropdown', options=countries),
        ], className='column is-one-third'),
        html.Div([
            dcc.Dropdown(id='sub-categories-dropdown', options=sub_categories)
        ], className='column'),
        html.Div([
            dcc.Dropdown(id='businesses-dropdown', options=businesses, optionHeight=60),
        ], className='column')
    ], className='columns'),
    html.Div([
        html.Div([
            dcc.Graph(id='world-map', figure=world_map)
        ], className='column is-two-thirds'),
        html.Div([
            html.Div([
                dcc.Markdown(children='There are X companies here', className='center')
            ], className='card meta-info'),
            html.Div([
                dcc.Markdown(children='They spend between X and Y amount of money', className='center')
            ], className='card meta-info')
        ], className='column'),
    ], className='columns'),
    html.Div([
        html.Div([
            dcc.Markdown(children='You are looking at X')
        ], className='column is-half'),
        html.Div([
            dcc.Dropdown(id='compare-dropdown', options=countries, multi=True),
        ], className='column')
    ], className='columns'),
    html.Div([
        html.Div([
            dcc.Graph(id='explore-plot')
            # dcc.Graph(id='explore-plot')
        ], className='column is-half'),
        html.Div([
            dcc.Graph(id='compare-plot')
        ], className='column')
    ], className='columns')
], className='container is-fluid')


'''# App layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Markdown(children=md_templates.start_template, className='title is-6'),
                        dcc.Graph(id='world-map', figure=world_map)
                    ], className='content')
                ], className='card-content')
            ], className='card')
        ], className='column is-two-thirds'),
        html.Div([
             html.Div([
                html.Div([
                    html.Div([

                        dcc.Markdown(children=md_templates.explore_template,className='title is-6'),
                        dcc.Markdown(children=md_templates.explore_countries_template),
                        dcc.Dropdown(id='countries-dropdown-explore',options=countries),
                        dcc.Graph(id='country-explore-plot')

                    ],className='content')
                ],className='card-content')
            ],className='card')
        ],className='column'),
    ],className='columns'),

    html.Div([
        html.Div([
             html.Div([
                html.Div([
                    html.Div([

                        dcc.Markdown(children=md_templates.explore_categories_template,className='title is-6'),
                        dcc.Markdown(children=md_templates.explore_categories_template),
                        dcc.Dropdown(id='main-categories-dropdown-explore', options=categories),
                        dcc.Dropdown(id='sub-categories-dropdown-explore'),
                        dcc.Graph(id='category-explore-plot')

                    ],className='content')
                ],className='card-content')
            ],className='card')
        ],className='column'),
        html.Div([
             html.Div([
                html.Div([
                    html.Div([

                        dcc.Markdown(children=md_templates.explore_businesses_template,className='title is-6'),
                        dcc.Dropdown(id='businesses-dropdown-explore',options=businesses),
                        dcc.Graph(id='business-explore-plot')

                    ],className='content')
                ],className='card-content')
            ],className='card')
        ],className='column'),
        html.Div([
             html.Div([
                html.Div([
                    html.Div([
                        
                        dcc.Markdown(children=md_templates.compare_countries_template,className='title is-6'),
                        dcc.Markdown(children=md_templates.compare_countries_template),
                        dcc.Dropdown(id='countries-dropdown-compare',options=countries,multi=True),
                        dcc.Graph(id='countries-compare-plot')

                    ],className='content')
                ],className='card-content')
            ],className='card')
        ],className='column'),
    ],className='columns'),

],className="container is-fluid")'''

'''
app.layout = html.Div([
        html.Div([
            html.Div([
                    html.Div([
                    dcc.Graph(
                        id='world-map',
                        figure=world_map)
                        ],className='card-content')
                ],className='card'),
            ],className='column is-narrow'),
        html.Div([html.Div([
            dcc.Markdown(children=md_templates.compare_template),
                html.Div([
                    dcc.Markdown(children=md_templates.compare_countries_template),
                    dcc.Dropdown(
                        id='countries-dropdown-compare',
                        options=countries,
                        multi=True
                    ),
                    dcc.Graph(id='countries-compare-plot')
        ])],className='card')],className='column')
    ,
    html.Div([
        dcc.Markdown(children=md_templates.explore_template),
        html.Div([
            dcc.Markdown(children=md_templates.explore_countries_template),
            dcc.Dropdown(
                id='countries-dropdown-explore',
                options=countries
            ),
            dcc.Graph(id='country-explore-plot')
        ]),
        html.Div([
            dcc.Markdown(children=md_templates.explore_categories_template),
            dcc.Dropdown(
                id='main-categories-dropdown-explore',
                options=categories
            ),
            dcc.Dropdown(
                id='sub-categories-dropdown-explore',
            ),
            dcc.Graph(id='category-explore-plot')
        ]),
        html.Div([
            dcc.Markdown(children=md_templates.explore_businesses_template),
            dcc.Dropdown(
                id='businesses-dropdown-explore',
                options=businesses
            ),
            dcc.Graph(id='business-explore-plot')
        ]),
    ]),
    html.Div([
        dcc.Markdown(children=md_templates.compare_template),
        html.Div([
            dcc.Markdown(children=md_templates.compare_countries_template),
            dcc.Dropdown(
                id='countries-dropdown-compare-test',
                options=countries,
                multi=True
            ),
            dcc.Graph(id='countries-compare-plot-test')
        ]),
    ])

],className='columns is-multiline is-centered')
'''
'''

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
        st.dataframe(data.data)'''


'''def _max_width_():
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
    )'''


if __name__ == "__main__":
    app.run_server(debug=True)
