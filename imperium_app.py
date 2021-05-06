import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
organisations = data.get_organisations()

# Load necessary data and plot for world map
iso3_codes, countries_business_amount, countries_list = data.get_country_amount_of_organisations()
world_map = world_plot.map_plot(iso3_codes, countries_business_amount, countries_list)

# Load current view
curr_view = 'Country'


# Callback for the worldmap interaction
@app.callback(Output('world-map', 'figure'),
              [Input('world-map', 'clickData')])
def update_map(click_data):
    if click_data is not None:
        country_name = click_data['points'][0]['hovertext']
        iso_code = click_data['points'][0]['location']
        fig = world_plot.map_plot_click(iso3_codes, countries_business_amount, countries_list, iso_code)
    else:
        fig = world_plot.map_plot(iso3_codes, countries_business_amount, countries_list)
    return fig


@app.callback(Output('companies-here', 'children'),
              Output('country-here', 'children'),
              Output('passes-here', 'children'),
              Output('country-here-2', 'children'),
              [Input('countries-dropdown', 'value')])
def update_companies_here(value):
    if value is not None:
        country_data = data.get_countries_data([value])
        company_amount = str(len(country_data))
        ep_amount = str(country_data['EP passes'].sum())
        value = value + " has "
    else:
        company_amount = "No country selected"
        ep_amount = "No country selected"
        value = ""
    return company_amount, value, ep_amount, value


# Callback to update the values in the compare dropdown
@app.callback(Output('explore-plot', 'figure'),
              [Input('countries-dropdown', 'value'),
               Input('organisations-dropdown', 'value'),
               Input('sub-categories-dropdown', 'value')])
def update_explore_dropdown(country, organisation, sub_category):
    ctx = dash.callback_context

    if ctx.triggered:
        dropdown = ctx.triggered[0]['prop_id'].split('.')[0]
        if dropdown == 'countries-dropdown':
            country_data = data.get_countries_data([country])
            country_plot = explorer_plots.explore_country(country_data)
            return country_plot
        elif dropdown == 'organisations-dropdown':
            business_data = data.get_organisations_data([organisation])
            business_plot = explorer_plots.explore_business(business_data)
            return business_plot
        else:
            main_category = subcategory_to_main[sub_category]
            category_data = data.get_sub_categories_data([sub_category])
            category_plot = explorer_plots.explore_category(category_data)
            return category_plot
    else:
        category_data = data.get_countries_data([])  # This data will the always be empty
        category_plot = explorer_plots.explore_category(category_data)
        return category_plot


# Callback for comparer plots
@app.callback(Output('compare-plot', 'figure'),
              [Input('compare-dropdown', 'value')])
def update_compare_plot(items):
    if curr_view == 'Country':
        df = data.get_countries_data(items)
    elif curr_view == 'Category':
        df = data.get_sub_categories_data(items)
    else:
        df = data.get_organisations_data(items)

    fig = comparer_plots.compare_data(df, curr_view)
    return fig


# Callback to update the values in the compare dropdown
@app.callback(Output('compare-dropdown', 'options'),
              Output('compare-dropdown', 'value'),
              [Input('countries-dropdown', 'value'),
               Input('organisations-dropdown', 'value'),
               Input('sub-categories-dropdown', 'value')])
def update_compare_dropdown(country, organisation, sub_category):
    ctx = dash.callback_context

    if ctx.triggered:
        global curr_view
        dropdown = ctx.triggered[0]['prop_id'].split('.')[0]
        if dropdown == 'countries-dropdown':
            curr_view = 'Country'
            return countries, [country]
        elif dropdown == 'organisations-dropdown':
            curr_view = 'Organisation'
            return organisations, [organisation]
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
            dcc.Dropdown(id='organisations-dropdown', options=organisations, optionHeight=60),
        ], className='column')
    ], className='columns is-centered'),
    html.Div([
        html.Div([
            dcc.Graph(id='world-map', figure=world_map)
        ], className='column is-two-thirds'),
        html.Div([
            html.Div([
                html.Div([
                    html.Br(),
                    html.Br(),
                    dcc.Markdown(className='subtitle is-3 center', id='country-here'),
                    dcc.Markdown(className='title is-3 center', id='companies-here'),
                    dcc.Markdown(children=" organisations in our database", className='subtitle is-3 center'),
                ], className='content is-centered')
            ], className='card meta-info'),
            html.Br(),
            html.Div([
                html.Div([
                    html.Br(),
                    html.Br(),
                    dcc.Markdown(className='subtitle is-3 center', id='country-here-2'),
                    dcc.Markdown(className='title is-3 center', id='passes-here'),
                    dcc.Markdown(children=" EP passes", className='subtitle is-3 center'),
                ], className='content is-centered')
            ], className='card meta-info'),
        ], className='column'),
    ], className='columns is-centered'),
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

if __name__ == "__main__":
    app.run_server(debug=True)
