import sys
import os

# Add the app directory to the system path
path = '/home/NoahSam28/mysite'
if path not in sys.path:
    sys.path.append(path)

# Set the environment variable for Flask app
os.environ['FLASK_APP'] = 'app'

# Import the Flask server from app.py
from app import server as application

# Optional: Print sys.path for debugging

