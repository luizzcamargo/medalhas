import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

# Load the CSV file
df = pd.read_csv('Summer_olympic_Medals.csv')
# Replace 'United States' with 'United States of America' in the 'Country_Name' column
df['Country_Name'] = df['Country_Name'].replace('United States', 'United States of America')

# Filtre os dados entre 1992 e 2020
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)]

# Create a Dash Application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Necessary for deployment

# App layout
app.layout = dbc.Container([
    html.H1("Dashboard Olímpico - Medalhas de 1992 a 2020", className="text-center my-4"),

    # Gráfico 1 - Mapa
    dbc.Card([
        dbc.CardHeader("Mapa de Medalhas por País"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Tipo de Medalha:"),
                    dcc.Dropdown(
                        id='map-medal-type',
                        options=[
                            {'label': 'Todas Medalhas', 'value': 'Total'},
                            {'label': 'Ouro', 'value': 'Gold'},
                            {'label': 'Prata', 'value': 'Silver'},
                            {'label': 'Bronze', 'value': 'Bronze'}
                        ],
                        value='Total',
                        clearable=False
                    )
                ], md=6),
                dbc.Col([
                    html.Label("Ano:"),
                    dcc.Dropdown(
                        id='map-year',
                        options=[{'label': 'Todos os Anos', 'value': 'all'}] +
                                [{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                        value='all',
                        clearable=False
                    )
                ], md=6)
            ]),
            dcc.Graph(id='map-chart')
        ])
    ], className="mb-4"),

    # Gráfico 2 - Área
    dbc.Card([
        dbc.CardHeader("Top Países por Medalhas"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Tipo de Medalha:"),
                    dcc.Dropdown(
                        id='area-medal-type',
                        options=[
                            {'label': 'Todas Medalhas', 'value': 'Total'},
                            {'label': 'Ouro', 'value': 'Gold'},
                            {'label': 'Prata', 'value': 'Silver'},
                            {'label': 'Bronze', 'value': 'Bronze'}
                        ],
                        value='Total',
                        clearable=False
                    )
                ], md=6),
                dbc.Col([
                    html.Label("Número de Países:"),
                    dcc.Dropdown(
                        id='area-top-n',
                        options=[
                            {'label': 'Top 5', 'value': 5},
                            {'label': 'Top 10', 'value': 10},
                            {'label': 'Top 15', 'value': 15},
                            {'label': 'Top 20', 'value': 20}
                        ],
                        value=10,
                        clearable=False
                    )
                ], md=6)
            ]),
            dcc.Graph(id='area-chart')
        ])
    ], className="mb-4"),

    # Gráfico 3 - Barras
    dbc.Card([
        dbc.CardHeader("Top Países por Medalhas"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Tipo de Medalha:"),
                    dcc.Dropdown(
                        id='bar-medal-type',
                        options=[
                            {'label': 'Todas Medalhas', 'value': 'Total'},
                            {'label': 'Ouro', 'value': 'Gold'},
                            {'label': 'Prata', 'value': 'Silver'},
                            {'label': 'Bronze', 'value': 'Bronze'}
                        ],
                        value='Gold',
                        clearable=False
                    )
                ], md=6),
                dbc.Col([
                    html.Label("Ano:"),
                    dcc.Dropdown(
                        id='bar-year',
                        options=[{'label': 'Todos os Anos', 'value': 'all'}] +
                                [{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                        value='all',
                        clearable=False
                    )
                ], md=6)
            ]),
            dcc.Graph(id='bar-chart')
        ])
    ], className="mb-4"),

    # Gráfico 4 - Pizza (updated with country and year filters)
    dbc.Card([
        dbc.CardHeader("Distribuição de Medalhas por Tipo"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("País:"),
                    dcc.Dropdown(
                        id='pie-country',
                        options=[{'label': country, 'value': country} for country in sorted(df['Country_Name'].unique())],
                        value='United States of America',
                        clearable=False
                    )
                ], md=6),
                dbc.Col([
                    html.Label("Ano:"),
                    dcc.Dropdown(
                        id='pie-year',
                        options=[{'label': 'Todos os Anos', 'value': 'all'}] +
                                [{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
                        value='all',
                        clearable=False
                    )
                ], md=6)
            ]),
            dcc.Graph(id='pie-chart')
        ])
    ], className="mb-4"),

    # Gráfico 5 - Linha (updated with multi-medal type selection)
    dbc.Card([
        dbc.CardHeader("Evolução das Medalhas por Ano"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Tipo de Medalha:"),
                    dcc.Dropdown(
                        id='line-medal-type',
                        options=[
                            {'label': 'Ouro', 'value': 'Gold'},
                            {'label': 'Prata', 'value': 'Silver'},
                            {'label': 'Bronze', 'value': 'Bronze'}
                        ],
                        value=['Gold', 'Silver', 'Bronze'],
                        multi=True
                    )
                ], md=6),
                dbc.Col([
                    html.Label("País:"),
                    dcc.Dropdown(
                        id='line-country',
                        options=[{'label': 'Todos Países', 'value': 'all'}] +
                                [{'label': country, 'value': country} for country in sorted(df['Country_Name'].unique())],
                        value='all',
                        clearable=False
                    )
                ], md=6)
            ]),
            dcc.Graph(id='line-chart')
        ])
    ], className="mb-4")
], fluid=True)

# Callbacks to update graphs

# Gráfico 1 - Mapa
@app.callback(
    Output('map-chart', 'figure'),
    Input('map-medal-type', 'value'),
    Input('map-year', 'value')
)
def update_map(medal_type, year):
    if medal_type == 'Total':
        df['Medal_Count'] = df['Gold'] + df['Silver'] + df['Bronze']
    else:
        df['Medal_Count'] = df[medal_type]

    if year != 'all':
        df_filtered = df[df['Year'] == year]
    else:
        df_filtered = df.copy()

    df_country_medals = df_filtered.groupby('Country_Name')['Medal_Count'].sum().reset_index()

    fig = px.choropleth(
        df_country_medals,
        locations='Country_Name',
        locationmode='country names',
        color='Medal_Count',
        hover_name='Country_Name',
        color_continuous_scale=px.colors.sequential.YlOrRd,
        title=f'Distribuição de Medalhas {"em " + str(year) if year != "all" else "de 1992 a 2020"}'
    )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    return fig

# Gráfico 2 - Área
@app.callback(
    Output('area-chart', 'figure'),
    Input('area-medal-type', 'value'),
    Input('area-top-n', 'value')
)
def update_area(medal_type, top_n):
    if medal_type == 'Total':
        df['Medal_Count'] = df['Gold'] + df['Silver'] + df['Bronze']
    else:
        df['Medal_Count'] = df[medal_type]

    df_country_medals = df.groupby('Country_Name')['Medal_Count'].sum().reset_index()
    top_countries = df_country_medals.nlargest(top_n, 'Medal_Count')['Country_Name']

    df_countries = df.groupby(['Country_Name', 'Year'])['Medal_Count'].sum().reset_index()
    df_top_countries = df_countries[df_countries['Country_Name'].isin(top_countries)]

    fig = px.area(
        df_top_countries,
        x="Year",
        y="Medal_Count",
        color="Country_Name",
        title=f'Top {top_n} Países por medalhas de {medal_type if medal_type != "Total" else "todas as medalhas"}'
    )
    return fig

# Gráfico 3 - Barras
@app.callback(
    Output('bar-chart', 'figure'),
    Input('bar-medal-type', 'value'),
    Input('bar-year', 'value')
)
def update_bar(medal_type, year):
    if medal_type == 'Total':
        df['Medal_Count'] = df['Gold'] + df['Silver'] + df['Bronze']
    else:
        df['Medal_Count'] = df[medal_type]

    if year != 'all':
        df_filtered = df[df['Year'] == year]
    else:
        df_filtered = df.copy()

    df_top_countries = df_filtered.groupby('Country_Name')['Medal_Count'].sum().nlargest(10).reset_index()

    # Choose appropriate color based on medal type
    color_map = {
        'Gold': 'gold',
        'Silver': 'silver',
        'Bronze': 'peru',
        'Total': 'royalblue'
    }

    fig = px.bar(
        df_top_countries,
        x='Country_Name',
        y='Medal_Count',
        color_discrete_sequence=[color_map.get(medal_type, 'gold')],
        title=f'Top 10 Países com mais medalhas de {medal_type.lower() if medal_type != "Total" else "todas"} {"em " + str(year) if year != "all" else "de 1992 a 2020"}'
    )
    return fig

# Gráfico 4 - Pizza (updated callback)
@app.callback(
    Output('pie-chart', 'figure'),
    Input('pie-country', 'value'),
    Input('pie-year', 'value')
)
def update_pie(country, year):
    # Filter for the selected country
    df_country = df[df['Country_Name'] == country]

    # Filter for the selected year if not 'all'
    if year != 'all':
        df_country = df_country[df_country['Year'] == year]

    # Prepare data for pie chart (medals by type)
    medal_data = {
        'Medal_Type': ['Ouro', 'Prata', 'Bronze'],
        'Count': [
            df_country['Gold'].sum(),
            df_country['Silver'].sum(),
            df_country['Bronze'].sum()
        ]
    }
    df_pie = pd.DataFrame(medal_data)

    fig = px.pie(
        df_pie,
        names='Medal_Type',
        values='Count',
        title=f'Distribuição de medalhas por tipo para {country}' + (f' em {year}' if year != 'all' else ' (todos os anos)'),
        color='Medal_Type',
        color_discrete_map={'Ouro': 'gold', 'Prata': 'silver', 'Bronze': 'peru'}
    )
    return fig

# Gráfico 5 - Linha (updated callback)
@app.callback(
    Output('line-chart', 'figure'),
    Input('line-medal-type', 'value'),
    Input('line-country', 'value')
)
def update_line(medal_types, country):
    # Prepare data based on selected medal types
    dfs = []

    for medal_type in medal_types:
        temp_df = df.copy()
        temp_df['Medal_Count'] = temp_df[medal_type]

        if country == 'all':
            temp_df = temp_df.groupby('Year')['Medal_Count'].sum().reset_index()
        else:
            temp_df = temp_df[temp_df['Country_Name'] == country].groupby('Year')['Medal_Count'].sum().reset_index()

        temp_df['Medal_Type'] = medal_type
        dfs.append(temp_df)

    if not dfs:
        return px.line(title="Selecione pelo menos um tipo de medalha")

    df_line = pd.concat(dfs)

    # Define colors for each medal type
    color_map = {
        'Gold': 'gold',
        'Silver': 'silver',
        'Bronze': 'peru'
    }

    fig = px.line(
        df_line,
        x='Year',
        y='Medal_Count',
        color='Medal_Type',
        title=f'Evolução de medalhas para {"todos países" if country == "all" else country}',
        markers=True,
        color_discrete_map=color_map
    )

    fig.update_traces(line=dict(width=3))
    fig.update_layout(legend_title_text='Tipo de Medalha')
    return fig

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

def create_app():
    return app.server

if __name__ == '__main__':
    app.run(debug=True)
