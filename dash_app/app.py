# dash_app/app.py
import dash
from dash import html, dcc

# Initialize the Dash application
app = dash.Dash(__name__, requests_pathname_prefix="/dashboard/")


# Define Dash layout with 4 example graphs
app.layout = html.Div(children=[
     # Navigation Links using html.A to redirect to FastAPI routes
    html.Div([
        html.A('Home', href='/'),  # Redirect to FastAPI's home route
        " | ",
        html.A('Logout', href='/logout')  # Redirect to FastAPI's logout route
    ], style={'marginTop': 20}),
    html.H1(children="Dashboard Example"),
    
    html.Div(children="Welcome to the Dash integrated with FastAPI."),

    dcc.Graph(
        id="example-graph-1",
        figure={
            "data": [
                {"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar", "name": "Example 1"},
                {"x": [1, 2, 3], "y": [2, 4, 5], "type": "bar", "name": "Example 2"},
            ],
            "layout": {"title": "Bar Graph Example"}
        }
    ),

    dcc.Graph(
        id="example-graph-2",
        figure={
            "data": [
                {"x": [1, 2, 3], "y": [10, 15, 13], "type": "line", "name": "Line 1"},
            ],
            "layout": {"title": "Line Graph Example"}
        }
    ),

    dcc.Graph(
        id="example-graph-3",
        figure={
            "data": [
                {"labels": ["A", "B", "C"], "values": [30, 50, 20], "type": "pie"},
            ],
            "layout": {"title": "Pie Chart Example"}
        }
    ),

    dcc.Graph(
        id="example-graph-4",
        figure={
            "data": [
                {"x": [1, 2, 3, 4], "y": [1, 4, 9, 16], "type": "scatter", "mode": "markers", "name": "Scatter"},
            ],
            "layout": {"title": "Scatter Plot Example"}
        }
    )
   
])

# Expose the Flask server to integrate with FastAPI
server = app.server