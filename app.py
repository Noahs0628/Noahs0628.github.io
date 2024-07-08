from dash import Dash, dash,html, dcc
from layout import create_layout
from compat import generate_options
from callback import register_callbacks

app = dash.Dash(__name__)
app.title="Fixture Designer"
app._favicon = ("favicon.png")
app.layout = create_layout(app)
      
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True) 