import os
import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

df1 = pd.read_csv("all_states_1.csv")


# Define locations dictionary
location1 = df1[['State', 'Latitude', 'Longitude']]
list_locations = location1.set_index('State')[['Latitude', 'Longitude']].T.to_dict('dict')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H3('Monitoring and Evaluation', style={"margin-bottom": "0px", 'color': 'white'}),
                        html.H5('NPCU Dashboard', style={"margin-top": "0px", 'color': 'white'}),
                    ],
                    className="six column",
                    id="title"
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"}
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            'Select Year:',
                            className='fix_label',
                            style={'color': 'white', 'margin-left': '1%'}
                        ),
                        dcc.Slider(
                            id='select_year',
                            included=False,
                            updatemode='drag',
                            tooltip={'always_visible': True},
                            min=2022,
                            max=2025,
                            step=1,
                            value=2023,
                            marks={str(yr): str(yr) for yr in range(2022, 2025, 1)},
                            className='dcc_compon'
                        ),
                    ],
                    className="create_container twelve columns",
                )
            ],
            className="row flex-display",
        ),
        html.Div([
            html.Div([
                html.Div(id='text1'),
            ],
                className="create_container three columns",
            ),

            html.Div([
                html.Div(id='text2'),
            ],
                className="create_container three columns",
            ),

            html.Div([
                html.Div(id='text3'),
            ],
                className="create_container three columns",
            ),

            html.Div([
                html.Div(id='text4'),
            ],
                className="create_container three columns",
            ),
        ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P('Select State:', className='fix_label', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='State_dropdown',
                            multi=True,
                            clearable=False,
                            disabled=False,
                            style={'display': True},
                            value=['ADAMAWA'],
                            placeholder='Select State',
                            options=[{'label': 'All States', 'value': 'All States'}] + [{'label': c, 'value': c} for c
                                                                                        in df1['State'].unique()],
                        ),

                        html.P('Select Quarter:', className='fix_label', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='qtr_dropdown',
                            multi=False,
                            clearable=False,
                            disabled=False,
                            style={'display': True},
                            value='Q1',
                            placeholder='Select Quarter',
                            options=[{'label': c, 'value': c} for c in df1['Quarter'].unique()],
                        ),

                        html.P('Select PDO Indicator:', className='fix_label', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='pdo_dropdown',
                            multi=False,
                            clearable=True,
                            disabled=False,
                            style={'display': True},
                            value='Number of public senior secondary schools that benefit from one or more project interventions',
                            placeholder='Select PDO Indicator',
                            options=[{'label': i, 'value': i} for i in
                                     df1[df1['component'] == 'PDO Indicators']['indicator'].unique()]
                        ),

                        html.P('Select Component 1 Indicator:', className='fix_label', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='comp1_dropdown',
                            multi=False,
                            clearable=True,
                            disabled=False,
                            style={'display': True},
                            value='Number of public JSS and SS schools that received at least one of the School Improvement Grants made available under the project that is both (a) managed by the SBMC based on the School Improvement Plan, and (b) has taken into account feedback from the community and all stakeholders into the school activities',
                            placeholder='Select Component 1 Indicator',
                            options=[{'label': i, 'value': i} for i in
                                     df1[df1['component'] == 'Component 1 Indicators']['indicator'].unique()]
                        ),

                        html.P('Select Component 2 Indicator:', className='fix_label', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='comp2_dropdown',
                            multi=False,
                            clearable=True,
                            disabled=False,
                            style={'display': True},
                            value='Number of girls (a) meeting the eligibility criteria and (b) continuing their education in SS2 or SS3',
                            placeholder='Select Component 2 Indicator',
                            options=[{'label': i, 'value': i} for i in
                                     df1[df1['component'] == 'Component 2 Indicators']['indicator'].unique()]
                        ),

                        html.P('Select Component 3 Indicator:', className='fix_label', style={'color': 'white'}),
                        dcc.Dropdown(
                            id='comp3_dropdown',
                            multi=False,
                            clearable=True,
                            disabled=False,
                            style={'display': True},
                            value='Number of schools implementing awareness programs on climate change',
                            placeholder='Select Component 3 Indicator',
                            options=[{'label': i, 'value': i} for i in
                                     df1[df1['component'] == 'Component 3 Indicators']['indicator'].unique()]
                        ),

                    ],
                    className="create_container twelve columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='bar_graph_pdo'),
                    ],
                    className="create_container six columns",
                ),
                html.Div(
                    [
                        dcc.Graph(id='bar_graph_comp1'),
                    ],
                    className="create_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id='bar_graph_comp2'),
                    ],
                    className="create_container six columns",
                ),
                html.Div(
                    [
                        dcc.Graph(id='bar_graph_comp3'),
                    ],
                    className="create_container six columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


def generate_bar_chart(df_component, indicator_name, state_dropdown, colors):
    return [
        go.Bar(
            x=['All States'] if 'All States' in state_dropdown else df_component['State'],
            y=[df_component['baseline_summed_data'].sum()] if 'All States' in state_dropdown else df_component[
                'baseline_consolidated_data'],
            text=[df_component['baseline_summed_data'].sum()] if 'All States' in state_dropdown else df_component[
                'baseline_consolidated_data'],
            texttemplate='%{text:.2s}',
            textposition='auto',
            name=f'{indicator_name} Baseline',
            marker=dict(color=colors['Baseline']),
            hoverinfo='text',
            hovertext=[
                f'<b>State</b>: {"All States" if "All States" in state_dropdown else state}<br>'
                f'<b>Baseline</b>: {baseline:,.0f}<br>'
                for state, baseline in zip(['All States'] if 'All States' in state_dropdown else df_component['State'],
                                           [df_component[
                                                'baseline_summed_data'].sum()] if 'All States' in state_dropdown else
                                           df_component['baseline_consolidated_data'])
            ]
        ),
        go.Bar(
            x=['All States'] if 'All States' in state_dropdown else df_component['State'],
            y=[df_component['actual_summed_data'].sum()] if 'All States' in state_dropdown else df_component[
                'actual_consolidated_data'],
            text=[df_component['actual_summed_data'].sum()] if 'All States' in state_dropdown else df_component[
                'actual_consolidated_data'],
            texttemplate='%{text:.2s}',
            textposition='auto',
            name=f'{indicator_name} Actual',
            marker=dict(color=colors['Actual']),
            hoverinfo='text',
            hovertext=[
                f'<b>State</b>: {"All States" if "All States" in state_dropdown else state}<br>'
                f'<b>Actual</b>: {actual:,.0f}<br>'
                for state, actual in zip(['All States'] if 'All States' in state_dropdown else df_component['State'], [
                    df_component['actual_summed_data'].sum()] if 'All States' in state_dropdown else df_component[
                    'actual_consolidated_data'])
            ]
        ),
        go.Bar(
            x=['All States'] if 'All States' in state_dropdown else df_component['State'],
            y=[df_component['Target_summed_data'].sum()] if 'All States' in state_dropdown else df_component[
                'Target_consolidated_data'],
            text=[df_component['Target_summed_data'].sum()] if 'All States' in state_dropdown else df_component[
                'Target_consolidated_data'],
            texttemplate='%{text:.2s}',
            textposition='auto',
            name=f'{indicator_name} Target',
            marker=dict(color=colors['Target']),
            hoverinfo='text',
            hovertext=[
                f'<b>State</b>: {"All States" if "All States" in state_dropdown else state}<br>'
                f'<b>Target</b>: {target:,.0f}<br>'
                for state, target in zip(['All States'] if 'All States' in state_dropdown else df_component['State'], [
                    df_component['Target_summed_data'].sum()] if 'All States' in state_dropdown else df_component[
                    'Target_consolidated_data'])
            ]
        )
    ]


@app.callback(
    [Output('bar_graph_pdo', 'figure'),
     Output('bar_graph_comp1', 'figure'),
     Output('bar_graph_comp2', 'figure'),
     Output('bar_graph_comp3', 'figure')],
    [Input('State_dropdown', 'value'),
     Input('qtr_dropdown', 'value'),
     Input('pdo_dropdown', 'value'),
     Input('comp1_dropdown', 'value'),
     Input('comp2_dropdown', 'value'),
     Input('comp3_dropdown', 'value')]
)
def update_bar_charts(state_dropdown, qtr_dropdown, pdo_dropdown, comp1_dropdown, comp2_dropdown, comp3_dropdown):
    df_filtered = df1[(df1['Quarter'] == qtr_dropdown)]
    if 'All States' not in state_dropdown:
        df_filtered = df_filtered[df_filtered['State'].isin(state_dropdown)]

    colors_pdo = {
        'Baseline': '#FF5733',
        'Actual': '#33FF57',
        'Target': '#3357FF'
    }

    colors_comp1 = {
        'Baseline': '#FF8C00',
        'Actual': '#ADFF2F',
        'Target': '#1E90FF'
    }

    colors_comp2 = {
        'Baseline': '#FF4500',
        'Actual': '#7CFC00',
        'Target': '#0000FF'
    }

    colors_comp3 = {
        'Baseline': '#FF6347',
        'Actual': '#32CD32',
        'Target': '#4682B4'
    }

    data_pdo, data_comp1, data_comp2, data_comp3 = [], [], [], []

    if pdo_dropdown:
        df_component = df_filtered[df_filtered['indicator'] == pdo_dropdown]
        data_pdo = generate_bar_chart(df_component, 'PDO', state_dropdown, colors_pdo)

    if comp1_dropdown:
        df_component = df_filtered[df_filtered['indicator'] == comp1_dropdown]
        data_comp1 = generate_bar_chart(df_component, 'Component 1', state_dropdown, colors_comp1)

    if comp2_dropdown:
        df_component = df_filtered[df_filtered['indicator'] == comp2_dropdown]
        data_comp2 = generate_bar_chart(df_component, 'Component 2', state_dropdown, colors_comp2)

    if comp3_dropdown:
        df_component = df_filtered[df_filtered['indicator'] == comp3_dropdown]
        data_comp3 = generate_bar_chart(df_component, 'Component 3', state_dropdown, colors_comp3)

    layout = go.Layout(
        barmode='group',
        plot_bgcolor='#010915',
        paper_bgcolor='#010915',
        titlefont={
            'color': 'white',
            'size': 20
        },
        hovermode='x',
        xaxis=dict(
            title='<b>State</b>',
            color='white',
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='white',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='white'
            )
        ),
        yaxis=dict(
            title='<b>Value</b>',
            color='white',
            showline=True,
            showgrid=True,
            showticklabels=True,
            linecolor='white',
            linewidth=2,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='white'
            )
        ),
        legend={
            'orientation': 'h',
            'bgcolor': '#010915',
            'xanchor': 'center',
            'x': 0.5,
            'y': -0.3
        },
        font=dict(
            family='sans-serif',
            size=12,
            color='white'
        )
    )

    return (
        {'data': data_pdo, 'layout': layout},
        {'data': data_comp1, 'layout': layout},
        {'data': data_comp2, 'layout': layout},
        {'data': data_comp3, 'layout': layout}
    )


@app.callback(
    [Output('text1', 'children'),
     Output('text2', 'children'),
     Output('text3', 'children'),
     Output('text4', 'children')],
    [Input('State_dropdown', 'value'),
     Input('qtr_dropdown', 'value'),
     Input('pdo_dropdown', 'value'),
     Input('comp1_dropdown', 'value'),
     Input('comp2_dropdown', 'value'),
     Input('comp3_dropdown', 'value')]
)
def update_texts(State_dropdown, qtr_dropdown, pdo_dropdown, comp1_dropdown, comp2_dropdown, comp3_dropdown):
    if 'All States' in State_dropdown:
        df_filtered = df1[(df1['Quarter'] == qtr_dropdown)]
    else:
        df_filtered = df1[(df1['Quarter'] == qtr_dropdown) &
                          (df1['State'].isin(State_dropdown))]

    baseline_value = 0
    actual_value = 0
    target_value = 0

    if pdo_dropdown:
        df_component = df_filtered[df_filtered['indicator'] == pdo_dropdown]
        baseline_value += df_component['baseline_summed_data'].sum() if 'All States' in State_dropdown else \
        df_component['baseline_consolidated_data'].sum()
        actual_value += df_component['actual_summed_data'].sum() if 'All States' in State_dropdown else df_component[
            'actual_consolidated_data'].sum()
        target_value += df_component['Target_summed_data'].sum() if 'All States' in State_dropdown else df_component[
            'Target_consolidated_data'].sum()

    if comp1_dropdown:
        df_component = df_filtered[df_filtered['indicator'] == comp1_dropdown]
        baseline_value += df_component['baseline_summed_data'].sum() if 'All States' in State_dropdown else \
        df_component['baseline_consolidated_data'].sum()
        actual_value += df_component['actual_summed_data'].sum() if 'All States' in State_dropdown else df_component[
            'actual_consolidated_data'].sum()
        target_value += df_component['Target_summed_data'].sum() if 'All States' in State_dropdown else df_component[
            'Target_consolidated_data'].sum()

    if comp2_dropdown:
        df_component = df_filtered[df_filtered['indicator'] == comp2_dropdown]
        baseline_value += df_component['baseline_summed_data'].sum() if 'All States' in State_dropdown else \
        df_component['baseline_consolidated_data'].sum()
        actual_value += df_component['actual_summed_data'].sum() if 'All States' in State_dropdown else df_component[
            'actual_consolidated_data'].sum()
        target_value += df_component['Target_summed_data'].sum() if 'All States' in State_dropdown else df_component[
            'Target_consolidated_data'].sum()

    if comp3_dropdown:
        df_component = df_filtered[df_filtered['indicator'] == comp3_dropdown]
        baseline_value += df_component['baseline_summed_data'].sum() if 'All States' in State_dropdown else \
        df_component['baseline_consolidated_data'].sum()
        actual_value += df_component['actual_summed_data'].sum() if 'All States' in State_dropdown else df_component[
            'actual_consolidated_data'].sum()
        target_value += df_component['Target_summed_data'].sum() if 'All States' in State_dropdown else df_component[
            'Target_consolidated_data'].sum()

    achieved_value = (actual_value / target_value) * 100 if target_value != 0 else 0

    color = 'red' if achieved_value < 50 else 'green'

    return [
        [
            html.H6(children='Baseline', style={'textAlign': 'left', 'color': 'white'}),
            html.P(f'{baseline_value:,.0f}', style={'textAlign': 'center', 'color': '#3065C9', 'fontSize': 30}),
        ],
        [
            html.H6(children='Actual', style={'textAlign': 'left', 'color': 'white'}),
            html.P(f'{actual_value:,.0f}', style={'textAlign': 'center', 'color': '#3065C9', 'fontSize': 30}),
        ],
        [
            html.H6(children='Target', style={'textAlign': 'left', 'color': 'white'}),
            html.P(f'{target_value:,.0f}', style={'textAlign': 'center', 'color': '#3065C9', 'fontSize': 30}),
        ],
        [
            html.H6(children='Achieved', style={'textAlign': 'left', 'color': 'white'}),
            html.P(f'{achieved_value:,.2f}%', style={'textAlign': 'center', 'color': color, 'fontSize': 30}),
        ]
    ]


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, port=7023)

