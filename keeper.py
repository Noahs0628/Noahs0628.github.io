from compat import generate_options
from dash import dash,html, dcc

tracker,names=generate_options()
dropdowns = []
AllDDs=['']
labels=[]
# Iterate over data_dict to create dropdown components
for key, values in names.items():
    dd=f'{key}-dropdown'

    dropdown = dcc.Dropdown(
        id=f'{key}-dropdown',
        options=values,
        value="Select",
        clearable=False,
    )
    
    dropdowns.append(dropdown)
    AllDDs.append(dd)
    labels.append(key)
 