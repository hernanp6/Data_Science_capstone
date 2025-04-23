# Import required libraries
import dash
import pandas as pd
from dash import html, dcc, callback, Output, Input
import plotly.express as px


# Read the airline data into pandas dataframe

import requests
from io import StringIO

# URL of the CSV file
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv'
response = requests.get(url)
spacex_df = pd.read_csv(StringIO(response.text))
# Filter the dataframe where 'Launch Site' equals 1
filtered_df = spacex_df[spacex_df['class'] == 1]
max_payload = filtered_df['Payload Mass (kg)'].max()
min_payload = filtered_df['Payload Mass (kg)'].min()

#max_payload = spacex_df['Payload Mass (kg)'].max()
#min_payload = spacex_df['Payload Mass (kg)'].min()

#spacex_df = pd.read_csv(response)



# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                    html.Label("SpaceX Launch Site"),
                                    dcc.Dropdown(
                                         id='site-dropdown',
                                         options=[{'label': 'All sites', 'value': 'All sites'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
                                         value='All sites',  # Set 'All sites' as the default value
                                         placeholder="Select a Launch Site Here"
                                        ),
                                    ]),
                                html.Div(id='dropdown-output'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(figure={},id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                 min=0, max=10000, step=1000,
                                                 marks={0: '0',
                                                        10000: '10000'},
                                                 value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    
    if entered_site == 'All sites':
        # Count the occurrences of each launch site
        #filtered_df = spacex_df[spacex_df['class'] == 1]
        launch_site_counts = filtered_df['Launch Site'].value_counts()
        fig = px.pie(launch_site_counts, 
                     values=launch_site_counts.values, 
                     names=launch_site_counts.index, 
                     title='successful launches count for all sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        # Count the occurrences of each launch site
        #launch_site_counts = filtered_df['Launch Site'].value_counts()
        #fig = plt.pie(launch_site_counts, vlabels=launch_site_counts.index, autopct='%1.1f%%', startangle=90, 
        #title='title')
        filtered_df1 = spacex_df[spacex_df['class'] == 1]
        filtered_df1['Launch Site'] = filtered_df1['Launch Site'].apply(lambda x: 'Other' if x != entered_site else entered_site)
        launch_site_counts1 = filtered_df1['Launch Site'].value_counts()
        fig = px.pie(launch_site_counts1, 
                     values=launch_site_counts1.values, 
                     names=launch_site_counts1.index, 
                     title= f'successful launches count for the site {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
              Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_chart(selected_site, selected_range):
    
    if selected_site == 'All sites':
        filtered_all_sites = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_range[0]) & (spacex_df['Payload Mass (kg)'] <= selected_range[1])]
        fig = px.scatter(filtered_all_sites, 
                 x='Payload Mass (kg)', 
                 y='class', 
                 color='Booster Version Category',  # This will create different series based on Booster Version Category
                 title="SpaceX Scatter Plot: Payload Mass vs Class for all launch sites")

        return fig
    else:
        filtered_Launch_Site = spacex_df[spacex_df['Launch Site'] == selected_site]
        filtered_Launch_Site = filtered_Launch_Site[(filtered_Launch_Site['Payload Mass (kg)'] >= selected_range[0]) & (filtered_Launch_Site['Payload Mass (kg)'] <= selected_range[1])]
        fig = px.scatter(filtered_Launch_Site, 
                 x='Payload Mass (kg)', 
                 y='class', 
                 color='Booster Version Category',  # This will create different series based on Booster Version Category
                 title= f"SpaceX Scatter Plot: Payload Mass vs Class for the launch site {selected_site}")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()