from dash import Dash, html

# Create a list to hold all dropdown components
from DDmaker import dropdowns,labels
# Define the Dash app layout using a list

def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="grid-container",
                children=[
                    html.Div(
                        className="grid-item",
                        children=[
                            labels[i],
                            dropdowns[i],
                        ]
                    ) for i in range(len(dropdowns))
                ]
            ),
            html.Button('Reset', id='reset-button', n_clicks=0),
            html.Div(id='output-container')
        ],
       
    )
