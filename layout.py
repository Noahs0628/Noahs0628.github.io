from dash import Dash, dash,html, dcc

# Create a list to hold all dropdown components
from keeper import names, dropdowns, AllDDs,tracker,labels
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
        ],
    )
 