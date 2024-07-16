from dash import Input, Output, html,State, ctx, callback_context
from dash.exceptions import PreventUpdate
import data_processing as dp
from DDmaker import dropdowns, AllDDs,labels
import dash_bootstrap_components as dbc
import csv
import time
initial_load=True
empty = dp.empty()
temp_tracker=empty
savable=False
values = ["Select"] * (len(AllDDs)-1)
backup_values=values
skip_timeout=False
backup_saved=False
def register_callbacks(app):
   
   
    #####################################################
    #updates options after a value has been chosed/changed
    @app.callback(
        [Output(dd, 'options') for dd in dropdowns],
        [Input(dd, 'value') for dd in dropdowns]
    )
    def update(*args):
        global values
        # find which dd triggerd callback
        dd_ID = callback_context.triggered[0]['prop_id'].split('.')[0]
        index = AllDDs.index(dd_ID) - 1

        # Get the current value of the triggered dropdown
        dd_value = args[index]

        # Get the previous value of the triggered dropdown
        prev_value = values[index]

        # Update the previous values list
        values[index] = dd_value

        # Update the compatibility tables based on the previous and current value
        if dd_value is not None and prev_value != "Select":
            #undo any changes previous option did
            dp.update_options(dd_ID, prev_value, +1)
        if dd_value is not None and dd_value != "Select":
            #make changes for current selection
            dp.update_options(dd_ID, dd_value, -1)

        # get new options for all dropdowns
        options = dp.set_options(AllDDs)

        return options
    
    
    #####################################################
    #Deterimine if selections are savable/Throw popover if needed
    @app.callback(
        [Output("unnamed", "is_open",allow_duplicate=True),
        Output("inuse", "is_open",allow_duplicate=True),
        Output("notdone", "is_open",allow_duplicate=True),
        [Input('save-button', 'n_clicks')]],
        [State('name-input', 'value')],

        prevent_initial_call=True
    )

    def check_name(click, value):
        global initial_load
        #if initial load do nthg
        if initial_load==True:
            return False,False,False  
        global savable, values,skip_timeout
        #used to skip function closing popovers if not necessary
        skip_timeout=False
        #assume not savable, will change if it is
        savable = False
        #if unnamed return that popover
        if value is None or value == "":     
            return [True,False,False]
        
        with open("data/saved/Saved.csv", mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                #prevent save if name is alr in use, throw popover
                if row[0] == value:  
                    return [False,True,False]
        
        #techinically savable atp
        savable = True
        #However, throw "incomplete" popover if not complete
        if "Select" in values:
            return [False,False,True]
        #if complete there will be no popover->skip the timeout function to close them
        skip_timeout=True
        return [False,False,False]
    
    
    #####################################################
    #Clear options/name box when clear or save(if possible) is pressed
    @app.callback(
        Output('name-input', 'value'),
        [Output(dd, 'value', allow_duplicate=True) for dd in dropdowns] +
        [Output(dd, 'options', allow_duplicate=True) for dd in dropdowns],
        [
            Input('clear-button', 'n_clicks'),
            Input('save-button', 'n_clicks'),
        ],
        [
            State('name-input', 'value'),
        ],
        prevent_initial_call=True
    )
    def reset_save(clear_clicks, save_clicks, name_input_value):
        #imports if the current selections can be saved
        global savable,values
        # leave if not savable
        if ctx.triggered[0]['prop_id'].split('.')[0] == 'save-button' and not savable:
            raise PreventUpdate
        
        # save if savable
        if ctx.triggered[0]['prop_id'].split('.')[0] == 'save-button' and savable:
            # Implement your save logic here
            dp.save(values, name_input_value)

        # resets tracker and options/values, atp savable==true or clear==true
        dp.tracker = dp.empty()
        options = dp.refresh_options()
        values = ["Select"] * len(dropdowns)
        savable=False
        return "", *values, *options
    
    
    #####################################################
    #Turns off the popover, couldn't find a less intrusive way :/
    @app.callback(
        [Output("unnamed", "is_open"),
        Output("inuse", "is_open"),
        Output("notdone", "is_open"),],
        [Input('save-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def turnoff(click):
        global skip_timeout
        if ~skip_timeout:    
            time.sleep(2)
        return [False,False,False]
    
    
    #####################################################
    #add/change grid buttons in some way depending on what button was pressed 
    @app.callback(
        [
            Output(f'grid-button-{i}', "children") for i in range(8)
        ] ,
        [
            [Input(f'grid-button-{i}', "n_clicks") for i in range(8)],
            Input('cancel-button', "n_clicks"),
            Input('save-button', 'n_clicks'),
        ],

    )
    def grid_buttons(grid_clicks, cancel_clicks, save_clicks):
            global backup_values,backup_saved,temp_tracker
            #get id of what triggered CB
            triggered_component=ctx.triggered[0]['prop_id'].split('.')[0]
            class_names=[0]*8
            buttons=[]
            #if a grid button was selected highlight that button
            if "grid-button" in triggered_component:
                index=int(triggered_component.split("button-")[1])
                class_names[index]=1
                #if cycling through saved, only save work in progress
                if not backup_saved:   
                    backup_values=values
                    temp_tracker=dp.tracker
                    backup_saved=True
            file_path = "data/saved/Saved.csv"
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)        
                row_num=-1
                for row_num, row in enumerate(reader):
                    if class_names[row_num]==0:
                        i=dbc.Button(row[0],id=row[0],class_name=row[1])
                        
                    else:
                        i=dbc.Button(row[0],id=row[0],class_name="selectedbutton")
                    buttons.append(i)
                for a in range((row_num+1),8):
                    buttons.append(html.Div())
            #shows all grid buttons, highlights one selected if applicable
            return buttons
    
    
    #####################################################
    #Show/hide cancel/edit buttons
    @app.callback(
        [
            Output('clear-button','disabled'),
            Output('save-button','disabled'),
            Output('save-as-button','children'),
            Output("edit-button", "children"),
            Output("delete-button", "children"),
            Output("cancel-button", "children"),
        ],
        [
            [Input(f'grid-button-{i}', "n_clicks") for i in range(8)],
            Input('cancel-button', "n_clicks"),
            Input('save-button', 'n_clicks'),
            Input('edit-button', 'n_clicks'),
        ],

    )
    def update_buttons(grid_clicks, cancel_clicks, save_clicks, edit_click ):
            global skip_timeout,initial_load
            #get triggered ID and return proper buttons
            triggered_component=ctx.triggered[0]['prop_id'].split('.')[0]
            if "grid-button" in triggered_component:
                return [
                        True,True,
                        html.Div(),
                        dbc.Button("Edit", color="secondary", className="edit-button"),
                        html.Div(),
                        dbc.Button("Cancel", color="grey", className="cancel-button")]
            
            
            if triggered_component=="edit-button":
                return [
                        False,False,
                        dbc.Button("Save As",  color="success", className="save-button"),
                        html.Div(),
                        html.Div(),
                        dbc.Button("Cancel", color="grey", className="cancel-button")]
            
            else: 
                initial_load=False
                return [False,False, html.Div(), html.Div(),html.Div(),html.Div()]   
    
    
    #####################################################
    #Show grid button values when clicked
    @app.callback(       
        [Output(dd, 'options', allow_duplicate=True) for dd in dropdowns],
        [Output(dd, 'value', allow_duplicate=True) for dd in dropdowns],
        [Output(dd, 'disabled', allow_duplicate=True) for dd in dropdowns],
        [Input(f'grid-button-{i}', "n_clicks") for i in range(8)],
        Input('cancel-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def grid_button_value(*args):
        global values, backup_saved, backup_values, temp_tracker
        #get id
        triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]
        disabled = [True] * (len(AllDDs) - 1)
        #if cancel button return the work in progess values/options
        if triggered_component == "cancel-button":
            #reset tracker to the back up and reset backup saved var
            dp.tracker = temp_tracker
            values = backup_values
            backup_saved = False
            #enable buttons
            disabled = [False] * (len(AllDDs) - 1)
        else:
            dp.tracker =dp.empty()
            class_names = [0] * 8
            index = int(triggered_component.split("button-")[1])
            class_names[index] = 1
            file_path = "data/saved/Saved.csv"
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)        
                row_num = -1
                for row_num, row in enumerate(reader):
                    if class_names[row_num] == 1:
                        #set values to saved data
                        values = row[2:]
                        
        i = 0
        for dd in labels:
            dp.update_options(dd, values[i], -1)
            i += 1
            
        options = dp.refresh_options()
        # Ensure options, values, and disabled are iterables and return them correctly
        return [*options, *values, *disabled]

