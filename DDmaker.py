from Data_setter import generate_options
from dash import dash,html, dcc

tracker,empty_tracker, names=generate_options()
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
<<<<<<< HEAD
=======
        persistence_type='local',
        persistence=True,
>>>>>>> 573b451fd09d2964272e4e380cb858f80b320b34
    )

    dropdowns.append(dropdown)
    AllDDs.append(dd)
    labels.append(key)
