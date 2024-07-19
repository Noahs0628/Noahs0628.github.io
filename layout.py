import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from DDmaker import dropdowns, labels  # Assuming DDmaker imports are correct

def create_layout(app: dash.Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            dbc.Row(
                className="content-container",
                children=[
                    # Left column for dropdowns (40%)
                    dbc.Col(
                        width=4,
                        children=[
                            html.Div(
                                className="dropdown-item",
                                children=[
                                    labels[i],
                                    dropdowns[i],
                                ]
                            ) for i in range(0, len(dropdowns), 2)
                        ]
                    ),
                    # Center column for dropdowns (40%)
                    dbc.Col(
                        width=4,
                        children=[
                            html.Div(
                                className="dropdown-item",
                                children=[
                                    labels[i],
                                    dropdowns[i],
                                ]
                            ) for i in range(1, len(dropdowns), 2)
                        ]
                    ),
                    # Right column for text input and buttons (20%)
                    dbc.Col(
                        width=4,
                        children=[
                            html.Div(
                                className="text-box",
                                children=[
                                    html.Label("Enter Name:"),
                                    dcc.Input(id='name-input', type='text', className='name-input', placeholder="Add Fixture ID. Ex (A1,B3,F14,... etc)"),
                                ]
                            ),
                            dbc.Popover(
                                className="popover",
                                children=[
                                    dbc.PopoverBody("Please create an ID before saving."),
                                ],
                                id="unnamed",
                                is_open=False,
                                target="name-input",
                                placement="bottom",
                                hide_arrow=True,
                            ),
                            dbc.Popover(
                                className="popover",
                                children=[
                                    dbc.PopoverBody("ID is already in use."),
                                ],
                                id="inuse",
                                is_open=False,
                                target="name-input",
                                placement="bottom",
                                hide_arrow=True,
                            ),
                            dbc.Popover(
                                className="popover",
                                children=[
                                    dbc.PopoverBody("Incomplete... Please finish later."),
                                ],
                                id="notdone",
                                is_open=False,
                                target="name-input",
                                placement="bottom",
                                hide_arrow=True,
                            ),
                            dbc.Button("Clear", id="clear-button", color="danger", className="clear-button"),
                            dbc.Button("Save As",id="save-button", color="success", className="save-button"),
                            html.Div(id="save-as-button"),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        id='grid-container-1',
                                        className='grid-container',
                                        children=[
                                            html.Div(id=f'grid-button-{i}', className='grid-button') for i in range(4)
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        id='grid-container-2',
                                        className='grid-container',
                                        children=[
                                            html.Div(id=f'grid-button-{i}', className='grid-button') for i in range(4, 8)
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        id='grid-container-3',
                                        className='grid-container',
                                        children=[
                                            html.Div(id=f'grid-button-{i}', className='grid-button') for i in range(8, 12)
                                        ]
                                    ),
                                ),
                            ]),
                           html.Div(id="edit-button"),
                           html.Div(id="delete-button"),
                           html.Div(id="cancel-button"),
                           html.Div(id="empty-holder"),
                        ]
                    )
                ]
            ),
            dcc.Input(id='dummy',type='hidden', value='callbackData'),
        ],
    )
