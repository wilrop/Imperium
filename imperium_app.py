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

external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css']

app = dash.Dash(__name__, title="Imperium: Looking at the EU",
                external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
data = DataLoader()  # Initialise the data loader.

# Load static data
countries = data.get_countries()
categories = data.get_main_categories()
sub_categories = data.get_sub_categories()
organisations = data.get_organisations()

# Load necessary data and plot for world map
iso3_codes, countries_business_amount, countries_list = data.get_country_amount_of_organisations()
world_map = world_plot.map_plot(
    iso3_codes, countries_business_amount, countries_list)

# Load current view
curr_view = 'Country'


def aboutpage():
    layout = html.Div([
        nav,
        about
    ], style={'backgroundColor': '$light'})
    return layout


def homepage():
    layout = html.Div([
        nav,
        body
    ], style={'backgroundColor': '$light'})
    return layout


@app.callback(Output('info-here', 'children'),
              Output('info-here-2', 'children'),
              Output('country-here-3', 'children'),
              [Input('countries-dropdown', 'value'),
               Input('organisations-dropdown', 'value'),
               Input('sub-categories-dropdown', 'value')])
def update_companies_here(country, organisation, sub_category):
    info_here = "**" + "No criteria selected" + "**"
    info_here_2 = "**" + "No criteria selected" + "**"
    country_here = "**" + "No criteria selected" + "**"
    if country is not None:
        country_data = data.get_countries_data([country])
        company_amount = str(len(country_data))
        ep_amount = str(country_data['EP passes'].sum())
        info_here = "**" + country + "**" + " has " + ep_amount + " EP Passes"
        info_here_2 = "**" + country + "**" + " has " + \
            company_amount + " organisations in our database"
        country_here = country
    elif organisation is not None:
        country_here = organisation
        business_data = data.get_organisations_data([organisation])
        ep_passes = 0
        lobbyist = 0
        for row in business_data.itertuples(index=False):
            ep_passes += row[business_data.columns.get_loc('EP passes')]
            lobbyist += row[business_data.columns.get_loc('lobbyists (FTE)')]
        info_here = "**" + organisation + "**" + \
            " has " + str(ep_passes) + " EP Passes"
        info_here_2 = "**" + organisation + "**" + \
            " has " + str(lobbyist) + " lobbyists"
    elif sub_category is not None:
        country_here = sub_category
        business_data = data.get_sub_categories_data([sub_category])
        nr_organisations = str(len(business_data))
        ep_passes = str(business_data['EP passes'].sum())
        info_here = "There are " + nr_organisations + \
            " **" + sub_category + "**" + " in our database"
        info_here_2 = "**" + sub_category + "**" + " has " + ep_passes + " EP Passes"

    return info_here, info_here_2, country_here


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
            category_data = data.get_sub_categories_data([sub_category])
            category_plot = explorer_plots.explore_category(category_data)
            return category_plot
    else:
        category_data = data.get_countries_data(
            [])  # This data will the always be empty
        category_plot = explorer_plots.explore_category(category_data)
        return category_plot


@app.callback(Output('countries-dropdown', 'value'),
              Output('organisations-dropdown', 'value'),
              Output('sub-categories-dropdown', 'value'),
              Output('world-map', 'clickData'),
              [Input('countries-dropdown', 'value'),
               Input('organisations-dropdown', 'value'),
               Input('sub-categories-dropdown', 'value'),
               Input('world-map', 'clickData')])
def clear_other_dropdowns(country, organisation, sub_category, click_data):
    if click_data is not None:
        country_name = click_data['points'][0]['hovertext']
        return str(country_name), None, None, None
    else:
        ctx = dash.callback_context

        if ctx.triggered:
            dropdown = ctx.triggered[0]['prop_id'].split('.')[0]
            if dropdown == 'countries-dropdown':
                return country, None, None, None
            elif dropdown == 'organisations-dropdown':
                return None, organisation, None, None
            else:
                return None, None, sub_category, None
        else:
            return country, None, None, None


# Callback for compare country plot
@app.callback(Output('compare-countries-plot', 'figure'),
              [Input('compare-countries-dropdown', 'value')])
def update_compare_countries_plot(selected_countries):
    df = data.get_countries_data(selected_countries)
    fig = comparer_plots.compare_data(df, 'Country')
    return fig

# Callback for compare category plot


@app.callback(Output('compare-categories-plot', 'figure'),
              [Input('compare-categories-dropdown', 'value')])
def update_compare_categories_plot(selected_categories):
    df = data.get_sub_categories_data(selected_categories)
    fig = comparer_plots.compare_data(df, 'Category')
    return fig

# Callback for compare organisation plot


@app.callback(Output('compare-organisations-plot', 'figure'),
              [Input('compare-organisations-dropdown', 'value')])
def update_compare_organisations_plot(selected_organisations):
    df = data.get_organisations_data(selected_organisations)
    fig = comparer_plots.compare_data(df, 'Organisation')
    return fig


# Callback to update the values in the compare dropdown
@app.callback(Output('compare-tabs', 'value'),
              [Input('countries-dropdown', 'value'),
               Input('organisations-dropdown', 'value'),
               Input('sub-categories-dropdown', 'value')])
def update_compare_dropdown(country, organisation, sub_category):
    ctx = dash.callback_context

    if ctx.triggered:
        dropdown = ctx.triggered[0]['prop_id'].split('.')[0]
        if dropdown == 'countries-dropdown':
            return 'tab-country'
        elif dropdown == 'organisations-dropdown':
            return 'tab-organisation'
        else:
            return 'tab-category'
    else:
        return 'tab-country'


# App layout


nav = html.Nav([
    html.Div([
        html.A([
            dcc.Markdown(children="IMPERIUM", className='title is-5 center'),

        ], className="navbar-item")

    ], className="navbar-brand"),
    html.Div([
        html.Div([
            html.A([
                "Home"

            ], className="navbar-item", href="/home"),
            html.A([
                "About"

            ], className="navbar-item", id="about", href="/about")

        ], className="navbar-start")
    ], className="navbar-menu")

], className="navbar is-light has-shadow")
body = html.Div([
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.Div([
                dcc.Markdown(children='Filter by Country',
                             className='title is-6 center'),
                dcc.Dropdown(id='countries-dropdown',
                             options=countries, style={'margin-left': '5px'}),
            ], className='column is-one-third'),
            html.Div([
                dcc.Markdown(children='Filter by Category',
                             className='title is-6 center'),
                dcc.Dropdown(id='sub-categories-dropdown',
                             options=sub_categories)
            ], className='column'),
            html.Div([
                dcc.Markdown(children='Filter by Organisation',
                             className='title is-6 center'),
                dcc.Dropdown(id='organisations-dropdown', options=organisations, optionHeight=60,
                             style={'margin-right': '5px'}),
            ], className='column')
        ], className='columns is-centered')

    ], className='card'),
    html.Br(),
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='world-map', figure=world_map)

            ], className='card'),
        ], className='column is-two-thirds'),
        html.Div([
            html.Div([
                html.Div([
                    html.Br(),
                    html.Br(),
                    dcc.Markdown(className='subtitle is-3 center',
                                 id='info-here'),
                ], className='content is-centered')
            ], className='card meta-info'),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div([
                    html.Br(),
                    html.Br(),
                    dcc.Markdown(className='subtitle is-3 center',
                                 id='info-here-2'),
                ], className='content is-centered')
            ], className='card meta-info'),
        ], className='column'),
    ], className='columns is-centered'),
    html.Div([
        html.Div([
            html.Div([
                dcc.Markdown(children='You are looking at ', className='subtitle is-4 center',
                             style={'border-radius': '60px'}),
                dcc.Markdown(className='title is-4 center',
                             id='country-here-3'),
                dcc.Graph(id='explore-plot')
            ], className='column is-half'),
            html.Div([
                # dcc.Markdown(children='Add more items to compare their lobbying practices over time!',
                #             className='subtitle is-4 center', style={'border-radius': '60px'}),
                dcc.Tabs(id='compare-tabs', value='tab-country', children=[
                    dcc.Tab(label='Compare countries', value='tab-country', children=[
                        dcc.Dropdown(id='compare-countries-dropdown', options=countries, multi=True,
                                     style={'margin-right': '5px'}),
                        dcc.Graph(id='compare-countries-plot')
                    ]),
                    dcc.Tab(label='Compare categories', value='tab-category',  children=[
                        dcc.Dropdown(id='compare-categories-dropdown', options=sub_categories, multi=True,
                                     style={'margin-right': '5px'}),
                        dcc.Graph(id='compare-categories-plot')
                    ]),
                    dcc.Tab(label='Compare organisations', value='tab-organisation', children=[
                        dcc.Dropdown(id='compare-organisations-dropdown', options=organisations, multi=True,
                                     persistence=True, style={'margin-right': '5px'}, persistence_type='local'),
                        dcc.Graph(id='compare-organisations-plot')
                    ])
                ]),
            ], className='column')
        ], className='columns'),
    ], className='card')
], className='container is-fluid', id="home")


about = html.Div([html.Div([
    html.Br(),
    html.Div([html.Div([
        dcc.Markdown('''
## About
Imperium is a data visualisation app that serves investigative journalists and concerned citizens with the knowledge they require and deserve. For too long we have had no idea what goes on in Brussels. Imperium aims to change that.
##### Information about the data:
 * We have included employees spending 5% or more of their time engaged in relevant activities under the 25% band.

#### Created by Willem Ropke, Sofyan Ajridi and Thomas Vaeyens
''')


    ], className="content is-normal")])
], className="container")])


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home':
        return homepage()
    elif pathname == '/about':
        return aboutpage()
    else:
        return homepage()


app.head = [
    html.Link(
        href='/assets/logo2.jpg',
        rel='icon'
    ),
]

if __name__ == "__main__":
    app.run_server(debug=True)
