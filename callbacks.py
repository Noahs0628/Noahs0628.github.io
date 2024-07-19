import csv
import time
from dash import Dash, html, Input, Output, State, ctx, callback_context
import dash_bootstrap_components as dbc
import data_processing as dp
from DDmaker import dropdowns, AllDDs, labels
########################
#READ ME
#
# IK IT IS MUCH LESS EFFICIENT TO SORT BY INPUTS RATHER THAN OUTPUTS
# WILL FIX LTR
# TOO HARD TO PLAN OUT IF GROUPING BY OUTPUTS, EASIER TO TRANSLATE AFTER

########################
# File path for saved data
file_path = "data/saved/Saved.csv"

# Initialize global variables
#
#
#current stuff
values = ["Select"] * (len(AllDDs) - 1)
current_options = {}

#backup values
temp_tracker = dp.empty()
backup_options=current_options
backup_values = values
backup_name = ""
backup_saved = False
#other
button_num=-1
editMode=False
def register_callbacks(app):
   #loads buttons
    @app.callback(
        [Output(f'grid-button-{i}', "children") for i in range(12)]+
        [
            Output('clear-button', 'disabled'),
            Output('save-button', 'disabled'),
            Output('save-as-button', 'children'),
            Output("edit-button", "children"),
            Output("delete-button", "children"),
            Output("cancel-button", "children"),
        ],
        [Input('dummy', 'value')]
    )
    #loads buttons
    def load_buttons(dummy):
        buttons = []
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            row_num = -1
            for row_num, row in enumerate(reader):
                buttons.append(dbc.Button(row[0], id=row[0], className=row[1]))
            for a in range((row_num + 1), 12):
                buttons.append(html.Div())
        return buttons+[False, False, html.Div(), html.Div(), html.Div(), html.Div()]
    #updates tracker after value is changed
    @app.callback(
        [Output(dd, 'options') for dd in dropdowns],
        [Input(dd, 'value') for dd in dropdowns]
    )
    def update(*args):
        global values, current_options
        dd_ID = callback_context.triggered[0]['prop_id'].split('.')[0]
        index = AllDDs.index(dd_ID) - 1
        #find which dropdown triggered CB
        dd_value = args[index]
        prev_value = values[index]
        #update values with new value
        values[index] = dd_value
        #undo any changes to tracker prev value did
        #update options based on new value
        if dd_value is not None and prev_value != "Select":
            dp.update_options(dd_ID, prev_value, +1)
        if dd_value is not None and dd_value != "Select":
            dp.update_options(dd_ID, dd_value, -1)
        #update options
        options = dp.set_options(AllDDs)
        current_options = options
        return options
    
        
    #save mega callback
    @app.callback(
        [
            Output("unnamed", "is_open", allow_duplicate=True),
            Output("inuse", "is_open", allow_duplicate=True),
            Output("notdone", "is_open", allow_duplicate=True),
            Output('name-input', 'value', allow_duplicate=True),
            *[Output(dd, 'value', allow_duplicate=True) for dd in dropdowns],
            *[Output(dd, 'options', allow_duplicate=True) for dd in dropdowns],
            *[Output(f'grid-button-{i}', "children", allow_duplicate=True) for i in range(12)],
            Output('clear-button', 'disabled', allow_duplicate=True),
            Output('save-button', 'disabled', allow_duplicate=True),
            Output('save-as-button', 'children', allow_duplicate=True),
            Output("edit-button", "children", allow_duplicate=True),
            Output("delete-button", "children", allow_duplicate=True),
            Output("cancel-button", "children", allow_duplicate=True),
        ],
        [
            Input("save-button", "n_clicks"),
            Input("save-as-button", "n_clicks"),
            Input('dummy','value'),
        ],
        [State("name-input", 'value')],
        prevent_initial_call=True
    )
    def save_button(save1, save2,dummy, name):
        global skip_timeout, values, current_options,backup_saved,backup_name,button_num,editMode
        #initialize return variables
        popovers = [False, False, False]
        buttons = []
        options = []
        new_name = ""
        skip_timeout=False
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        #if no name throw popover at end
        if not name:
            popovers = [True, False, False]
        else:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == name:
                        #if save button (not save-as) was 
                        #pressed & the name is already used throw popover at end
                        if trigger == "save-button":
                            popovers = [False, True, False]
                        break
        #if no popovers are thrown this name can be saved
        if popovers==[False, False, False]:        
            #if incomplete throw popover but save anyway
            if "Select" in values:
                popovers = [False, False, True]
            if trigger == "save-button":
                dp.save(values, name)
            else:
                dp.override(values, name, button_num)
            #if doing so reset everything
            if editMode:
                dp.tracker=temp_tracker
                options=backup_options
                values=backup_values
                new_name=backup_name    
            else:
                dp.tracker = dp.empty()
                options = dp.refresh_options()
                values = ["Select"] * len(dropdowns)
                new_name = ""
            backup_saved=False
            editMode=False
            
        else:
            #if not savable keep current stuff (values remain unchanged)
            options = current_options
            new_name = name
        #show all buttons
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            row_num = -1
            for row_num, row in enumerate(reader):
                buttons.append(dbc.Button(row[0], id=row[0], className=row[1]))
            for i in range(row_num + 1, 12):
                buttons.append(html.Div())

        if not editMode:
            return (
                popovers +
                [new_name] +
                values +
                options +
                buttons +
                [False, False, html.Div(), html.Div(), html.Div(), html.Div()]
            )
        else:
            return (
                popovers +
                [new_name] +
                values +
                options +
                buttons +
                [False, False] +
                [dbc.Button("Save", color="success", className="save-button")] +
                [html.Div()] +
                [html.Div()] +
                [dbc.Button("Cancel", color="grey", className="cancel-button")]
            )
    #turns off popovers if they're being shown
    @app.callback(
        [
            Output("unnamed", "is_open", allow_duplicate=True),
            Output("inuse", "is_open", allow_duplicate=True),
            Output("notdone", "is_open", allow_duplicate=True),
        ],
        [
            Input('save-button', 'n_clicks'),
            Input('save-as-button', 'n_clicks')
        ],
        prevent_initial_call=True
    )
    def turnoff(*clicks):
        global skip_timeout
        if not skip_timeout:
            time.sleep(2)
        return [False, False, False]
    #grid button mega callback
    @app.callback(
        [
        *[Output(f'grid-button-{i}', "children", allow_duplicate=True) for i in range(12)],
        *[Output(dd, 'disabled', allow_duplicate=True) for dd in dropdowns],
        *[Output(dd, 'value', allow_duplicate=True) for dd in dropdowns],
        Output('clear-button', 'disabled', allow_duplicate=True),
        Output('save-button', 'disabled', allow_duplicate=True),
        Output('save-as-button', 'children', allow_duplicate=True),
        Output("edit-button", "children", allow_duplicate=True),
        Output("delete-button", "children", allow_duplicate=True),
        Output("cancel-button", "children", allow_duplicate=True),
        Output('name-input', 'value', allow_duplicate=True),
        ],
        [[Input(f'grid-button-{i}', 'n_clicks') for i in range(12)]],
        [State('name-input', 'value')],
        prevent_initial_call=True
    )
    def grid_button(clicks, name):
        global backup_name, backup_saved, backup_values, temp_tracker,values,current_options,backup_options,button_num
        #initialize return vars
        buttons = []
        new_name = ""
        #disable all DDs when cycling
        disable=[True] * (len(AllDDs) - 1)
        #figure out which button was pressed
        triggered_component = ctx.triggered[0]['prop_id'].split('.')[0]
        class_names = [0] * 12
        index = int(triggered_component.split("button-")[1])
        button_num=index
        print(button_num)
        class_names[index] = 1
        #if first button pressed when cycling save values
        #otherwise ignore
        if backup_saved==False:   
            backup_values = values
            backup_options=current_options
            temp_tracker = dp.tracker
            backup_name = name
            if backup_name is None:
                backup_name=""
            backup_saved = True
        #update buttons to show highlight whichever is selected
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            row_num = -1
            for row_num, row in enumerate(reader):
                if class_names[row_num] == 0:
                    buttons.append(dbc.Button(row[0], id=row[0], className=row[1]))
                else:
                    #for selected button get name and values to display
                    buttons.append(dbc.Button(row[0], id=row[0], className="selectedbutton"))
                    new_name = row[0]
                    new_vals=row[2:]
                    values=new_vals
            for i in range(row_num + 1, 12):
                buttons.append(html.Div())

        return (
            buttons+
            disable+
            [*new_vals]+
            [True, True]+
            [html.Div(),
            dbc.Button("Edit", color="secondary", className="edit-button"),
            dbc.Button("Delete Fixture", color="grey", className="delete-button"),
            dbc.Button("Cancel", color="grey", className="cancel-button"),
            new_name]            
        )
    #delete button
    @app.callback(
        *[Output(f'grid-button-{i}', "children", allow_duplicate=True) for i in range(12)],
        Output('clear-button', 'disabled', allow_duplicate=True),
        Output('save-button', 'disabled', allow_duplicate=True),
        Output('save-as-button', 'children', allow_duplicate=True),
        Output("edit-button", "children", allow_duplicate=True),
        Output("delete-button", "children", allow_duplicate=True),
        Output("cancel-button", "children", allow_duplicate=True),
        Output('name-input', 'value', allow_duplicate=True),
        *[Output(dd, 'options', allow_duplicate=True) for dd in dropdowns],
        *[Output(dd, 'value', allow_duplicate=True) for dd in dropdowns],
        *[Output(dd, 'disabled', allow_duplicate=True) for dd in dropdowns],
    
        [Input('delete-button', 'n_clicks')],
        prevent_initial_call=True
    )

    def delete(click):
        global backup_saved, backup_name, editMode, values, current_options, button_num
        
        # Read the existing data from the file
        with open(file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
        
        # Filter out the row to be deleted
        new_rows = [row for row_num, row in enumerate(rows) if row_num != button_num]

        # Write the updated data back to the file
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(new_rows)
        
        buttons = []
        disabled = [False] * (len(AllDDs) - 1)
        
        # Reset buttons so none are highlighted
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            row_num = -1
            for row_num, row in enumerate(reader):
                buttons.append(dbc.Button(row[0], id=row[0], className=row[1]))
            for a in range(row_num + 1, 12):
                buttons.append(html.Div())
        
        # Reset values and options
        dp.tracker = temp_tracker
        current_options = backup_options
        values = backup_values
        backup_saved = False
        editMode = False

        return (
            buttons + 
            [False, False, html.Div(), html.Div(), html.Div(), html.Div(), backup_name] +
            [*backup_options] +  # Include saved options
            [*backup_values] +   # Include saved values
            disabled
        )
        
    #cancel button mega callback
    @app.callback(
        *[Output(f'grid-button-{i}', "children", allow_duplicate=True) for i in range(12)],
        Output('clear-button', 'disabled', allow_duplicate=True),
        Output('save-button', 'disabled', allow_duplicate=True),
        Output('save-as-button', 'children', allow_duplicate=True),
        Output("edit-button", "children", allow_duplicate=True),
        Output("delete-button", "children", allow_duplicate=True),
        Output("cancel-button", "children", allow_duplicate=True),
        Output('name-input', 'value', allow_duplicate=True),
        *[Output(dd, 'options', allow_duplicate=True) for dd in dropdowns],
        *[Output(dd, 'value', allow_duplicate=True) for dd in dropdowns],
        *[Output(dd, 'disabled', allow_duplicate=True) for dd in dropdowns],
    
        [Input('cancel-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def cancel(click):
        global backup_saved,backup_name,editMode,values,backup_name,current_options
        buttons = []
        disabled = [False] * (len(AllDDs) - 1)
        #reset buttons so none are highlighted
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            row_num = -1
            for row_num, row in enumerate(reader):
                buttons.append(dbc.Button(row[0], id=row[0], className=row[1]))
            for a in range(row_num + 1, 12):
                buttons.append(html.Div())
        #values return to value when saved
        dp.tracker = temp_tracker
        current_options=backup_options
        values=backup_values
        backup_saved = False
        editMode=False

        return (
            buttons + 
            [False, False, html.Div(), html.Div(), html.Div(), html.Div(), backup_name]+
            [*backup_options]+ #saved from starting to cycle
            [*backup_values] + #this too
            disabled)
    #clear button mega callback
    @app.callback(
        Output('name-input', 'value', allow_duplicate=True),
        *[Output(dd, 'value', allow_duplicate=True) for dd in dropdowns],
        *[Output(dd, 'options', allow_duplicate=True) for dd in dropdowns],
        [Input('clear-button', 'n_clicks')],
        [State('name-input', 'value')],
        prevent_initial_call=True
    )
    def clear(click,name):
        global current_options,values
        #clear everythig and update necessary globals
        dp.tracker = dp.empty()
        options = dp.refresh_options()
        current_options=options
        new_vals = ["Select"] * len(dropdowns)
        values=new_vals
        return [""]+ [*new_vals]+ [*options]
    #edit button mega callbacl
    @app.callback(
        Output('clear-button', 'disabled', allow_duplicate=True),
        Output('save-button', 'disabled', allow_duplicate=True),
        Output('save-as-button', 'children', allow_duplicate=True),
        Output("edit-button", "children", allow_duplicate=True),
        Output("delete-button", "children", allow_duplicate=True),
        Output("cancel-button", "children", allow_duplicate=True),
        *[Output(dd, 'disabled', allow_duplicate=True) for dd in dropdowns],
        *[ Output(f'grid-button-{i}', "children", allow_duplicate=True) for i in range(12)],
        *[Output(dd, 'value', allow_duplicate=True) for dd in dropdowns],
        *[Output(dd, 'options', allow_duplicate=True) for dd in dropdowns],
        [Input('edit-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def edit(click):
        global editMode,values,current_options
        #for selected grid's labels update tracker and options, done here to reduce processing
        dp.tracker=dp.empty()
        for i in range(len(AllDDs)-1):
            print()
            dd_ID = labels[i]+"-"
            dd_value= values[i]
            dp.update_options(dd_ID, dd_value, -1)
        #update options
        options = dp.set_options(AllDDs)
        current_options = options        
        editMode=True
        divs=[html.Div()] * 12
        disable=[False] * (len(AllDDs) - 1)
        return ([False, False]+
                [dbc.Button("Save", color="success", className="save-button")]+
                [html.Div()]+
                [html.Div()]+
                [dbc.Button("Cancel", color="grey", className="cancel-button")]+
                disable+
                divs+
                [*values]+
                [*options]
                )

