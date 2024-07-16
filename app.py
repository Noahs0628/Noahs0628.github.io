from dash import Dash
from layout import create_layout
from callbacks import register_callbacks
from flask import Flask
import dash_bootstrap_components as dbc
import os
from dash import Dash, DiskcacheManager, CeleryManager

if 'REDIS_URL' in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery
    celery_app = Celery(__name__, broker=os.environ['REDIS_URL'], backend=os.environ['REDIS_URL'])
    background_callback_manager = CeleryManager(celery_app)
else:
    # Diskcache for non-production apps when developing locally
    import diskcache
    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache)

# Create Flask server
server = Flask(__name__)

# Function to create a new Dash app
def create_app():
    app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP], background_callback_manager=background_callback_manager)
    app.title = "Fixture Designer"
    app._favicon = "favicon.png"
    app.layout = create_layout(app)
    register_callbacks(app)
    return app

# Initialize the app
app = create_app()

if __name__ == '__main__':
    app.run_server(debug=True)
