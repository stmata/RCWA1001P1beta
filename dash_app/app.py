# dash_app/app.py
import dash, requests
from dash import html, dcc

# Initialize the Dash application
app = dash.Dash(__name__, requests_pathname_prefix="/dashboard/")
# External API URL (replace with the actual URL)
EXTERNAL_API_URL = "https://weather1003.azurewebsites.net/info"

 
def get_external_info():
    try:
        response = requests.get(EXTERNAL_API_URL)
        return response.json()  # Convert response to JSON
    except Exception as e:
        return {"date": "N/A", "time": "N/A", "weather": {"city": "Unknown", "temperature": "N/A", "description": "N/A"}}
info = get_external_info()

# Define Dash layout with 4 example graphs
app.layout = html.Div(children=[
    # Display date, time, and weather info at the top of the dashboard
    html.Div([
        html.H3(f"Date: {info['date']}"),
        html.H3(f"Time: {info['time']}"),
        html.H3(f"Weather in {info['weather']['city']}: {info['weather']['temperature']} °C, {info['weather']['description']}"),
    ], style={'marginBottom': 20}),
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