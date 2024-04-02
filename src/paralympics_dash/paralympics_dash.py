from dash import Dash, Output, Input, html, dcc
import dash_bootstrap_components as dbc

from figures import line_chart, bar_gender_faceted, create_card, line_chart, bar_gender, scatter_geo

from layout_elements import row_one, row_two, row_three, row_four

external_stylesheets = [dbc.themes.BOOTSTRAP]
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Layout variables are in layout_elements.py

# Figures
map = scatter_geo()
line = line_chart("sports")
bar = bar_gender("winter")

# Layout variables
dropdown = dbc.Select(
    id="type-dropdown",
    options=[
        {"label": "Events", "value": "events"},
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events"
)

checklist = dbc.Checklist(
    options=[
        {"label": "Summer", "value": "summer"},
        {"label": "Winter", "value": "winter"},
    ],
    value=["summer"],
    id="checklist-input",
    inline=True,
)

row_one = html.Div(
    dbc.Row([
        dbc.Col([html.H1("Paralympics Dashboard", id='heading-one'), html.P(
            "Use the charts to help you answer the questions.")
                 ], width=12),
    ]),
)

row_two = dbc.Row([
    dbc.Col(children=[
        dropdown
    ], width=2),
    dbc.Col(children=[
        checklist,
    ], width={"size": 2, "offset": 4}),
], align="start")

row_three = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="line", figure=line),
    ], width=6),
    dbc.Col(children=[
        dcc.Graph(id="bar", figure=bar),
    ], width=6),
], align="start")

row_four = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="map", figure=map)
    ], width=8, align="start"),
    dbc.Col(children=[
        html.Br(),
        html.Div(id='card'),
    ], width=4, align="start"),
])

app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four,
])


@app.callback(
    Output(component_id='line', component_property='figure'),
    Input(component_id='type-dropdown', component_property='value')
)
def update_line_chart(chart_type):
    figure = line_chart(chart_type)
    return figure


@app.callback(
    Output(component_id='bar', component_property='figure'),
    Input(component_id='checklist-input', component_property='value')
)
def update_line_chart(event_type):
    figure = bar_gender_faceted(event_type)
    return figure


@app.callback(
    Output('card', 'children'),
    Input('map', 'hoverData'),
)
def display_card(hover_data):
    if hover_data is not None:
        event_id = hover_data['points'][0]['customdata'][0]
        if event_id is not None:
            return create_card(event_id)


if __name__ == '__main__':
    app.run(debug=True, port=8050)
    # Runs on port 8050 by default, this just shows the parameter to use to change to another port if needed
