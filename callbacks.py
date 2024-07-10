from dash import dash, Input, Output, callback_context, exceptions
import data_processing as dp
from DDmaker import dropdowns, AllDDs
empty = {
    'Size': {'1.7 x 2.31': 0, '1.85 x 3.0': 0, '2.25 x 3.7': 0, '2.5 x 4.25': 0},
    'Type': {'MO': 0, 'CL': 0, 'WW': 0, 'CX30': 0, 'Custom': 0},
    'LED': {'XOB09': 0, 'XOB14': 0, 'BXRV 1000': 0, 'BXRV 2000': 0, 'XTM19': 0, 'Other': 0},
    'Dimming': {'Phase': 0, '0-10V': 0, 'Dali': 0, 'Casambi': 0, 'Other': 0},
    'Power': {'Integral': 0, 'Remote': 0},
    'Driver': {'cielo': 0, 'magtech': 0, 'solodrive 0-10': 0, 'optotronic': 0, '48V DC': 0, '24V DC': 0},
    'Slope': {'90': 0, 'Custom': 0},
    'Adjustability': {'65 Degrees': 0, '90 Degrees': 0, 'Downlight': 0},
    'Stem': {'1/4 x 1.1': 0, '1/4 x Custom': 0, '3/8 x 1.5': 0, '3/8 x 2': 0, '3/8 x 2.5': 0, '3/8 x 3': 0, '3/8 x Custom': 0},
    'Attachment': {'Standard': 0, 'Jack': 0, 'Track': 0},
    'Cover': {'Drywall Flush': 0, 'Millwork Flush': 0, 'Millwork Overlap': 0, 'OBM 4.5': 0, 'Surface 2.5': 0, 'Surface 2.5 - 90': 0, 'point - class 2': 0, 'track': 0, 'jack': 0},
    'Refractor': {'C13085  spot': 0, 'C13086  medium': 0, 'C13087  wide': 0, 'C13806  white': 0, 'F14738  spot': 0, 'F14739  medium': 0, 'F14740. wide': 0, 'XSA-221 medium': 0, 'XSA-222 wide': 0, 'OJA': 0, '1501-50-15 spot': 0},
    'Accessories': {'solite': 0, 'back-eteched solite': 0, 'linear spread': 0, 'JA 8 Certified': 0, 'Wet Location': 0, 'Accessory Holder': 0},
    'Material': {'Aluminum': 0, 'Brass': 0}
}

previous_values = ["Select"] * len(AllDDs)

def register_callbacks(app):
    @app.callback(
        [Output(dd, 'value') for dd in dropdowns] +
        [Output(dd, 'options', allow_duplicate=True) for dd in dropdowns],
        [Input('reset-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def reset_dropdowns(n_clicks):
        print(empty)
        dp.tracker=empty
        options= dp.refresh_options(AllDDs)
        # Prepare values and options outputs
        values_output = ["Select"] * (len(AllDDs) - 1)
        # Return values and options to update dropdowns
        return values_output + options

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
        if dd_value is not None and prev_value != "Select":
            dp.update_options(dd_ID, prev_value, +1)
        if dd_value is not None and dd_value != "Select":
            dp.update_options(dd_ID, dd_value, -1)

        # Fetch new options for all dropdowns
        options = dp.set_options(AllDDs)

        return options
