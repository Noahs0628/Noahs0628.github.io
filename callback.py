import data_processing as dp
from dash import dash, dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import os
from keeper import names, dropdowns, AllDDs, tracker

previous_values = ["Select"] * len(AllDDs)

def register_callbacks(app):
    # Example callback to update dropdown options and selection
    @app.callback(
        [Output(dd, 'options') for dd in dropdowns],
        [Input(dd, 'value') for dd in dropdowns]
    )
    def update(*values):
        # Identify the dropdown that triggered the callback
        dd_ID = callback_context.triggered[0]['prop_id'].split('.')[0]

        index = AllDDs.index(dd_ID) - 1
        
        # Get the current value of the triggered dropdown
        dd_value = values[index]

        # Get the previous value of the triggered dropdown
        prev_value = previous_values[index]
        
        # Update the previous values list
        previous_values[index] = dd_value
        
        # Update the compatibility tables based on the previous and current value
        if prev_value != "Select":
            dp.update_options(dd_ID, prev_value, +1)
        if dd_value != "Select":
            dp.update_options(dd_ID, dd_value, -1)
        
        # Fetch new options for all dropdowns
        all_new_options = []

        for dd in AllDDs:
            if dd != '':                   
                option_name = dd.split('-')[0]
                options = dp.set_options(option_name)
                all_new_options.append(options)

        return all_new_options
 