from dash import Dash
from layout import create_layout
from callbacks import register_callbacks
from flask import Flask
import dash_bootstrap_components as dbc
import os

# Create Flask server
server = Flask(__name__)

# Function to create a new Dash app
def create_app():
    app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "Fixture Designer"
    app._favicon = "favicon.png"
    app.layout = create_layout(app)
    register_callbacks(app)
    return app

# Initialize the app
app = create_app()

if __name__ == '__main__':
    app.run_server(debug=True)
