import pandas as pd
import os
import csv
from DDmaker import dropdowns, tracker, names,AllDDs
initial_load=False
directory = r"data"
#updates the values in the working compat tables when any value is changed
def update_options(dd_ID,dd_Value, type):
    #type represents what to do, + means a value represents a deselected value requiring the addition of what was origionally removed
    #- indicated a value was just changed requirng the notation of any incompatible values
    key=dd_ID.split('-')[0]
    for filename in os.listdir(directory):
       
        if key in filename:    
            if ((not filename.endswith('_copy')) and (not filename.endswith('options.csv'))):
                top = filename.split('_')[0]
                
                left = filename.split('_')[1].split('.')[0]
                file_path = os.path.join(directory, filename)
                index = names[key].index(dd_Value)
                if key==top:
                    ifTop(file_path, left, index, type)
                else:
                    ifLeft(file_path, top, index, type)



#handles the case if the changed value is on the top of the compat table
def ifTop(file_path, key, index, type):
    global tracker
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)        
        for row_num, row in enumerate(reader):
            if row_num!=0:                

                if row[index] == '0':  # Corrected: Comparison should be with string '0'
                    tracker[key][row[0]] += type
                    

def ifLeft(file_path, key, index, type):
    global tracker
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        reader=zip(*reader)
        for row_num, row in enumerate(reader):
            if row_num!=0:                

                if row[index] == '0':  # Corrected: Comparison should be with string '0'

                    tracker[key][row[0]] += type

    
def set_options(AllDDs):
    all_new_options = []
    for dd in AllDDs:
            if dd != '':
                option_name = dd.split('-')[0]
                options = [{'label': 'Select', 'value': 'Select'}]    
                for option, value in list(tracker[option_name].items()): 
                        if(value==0):
                            option_={'label': option, 'value': option}
                            options.append(option_)  # Add the cell to the left to options
                        elif option_name in ["Size", "LED" ,"Type", "Driver"]:
                            option_={'label': f"{option} (Not Compatible With Current Selections)", 'value': option, 'disabled': True}
                            options.append(option_)  # Add the cell to the left to options

                all_new_options.append(options)
    return all_new_options

def refresh_options():
    all_options = []
    for dd in AllDDs:
            if dd != '':
                option_name = dd.split('-')[0]
                options = [{'label': 'Select', 'value': 'Select'}]    
                for option, value in list(tracker[option_name].items()):                         
                        option_={'label': option, 'value': option}
                        options.append(option_)  # Add the cell to the left to options
                    
                all_options.append(options)
    return all_options

def save(values,ID):
    file_path = "data/saved/Saved.csv"
    if "Select" in values:
        row = [ID,"Incomplete"] + values
    else:
         row = [ID,"Complete"] + values
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
def empty():
    empty=tracker
    for key, value in empty.items():
        for sub_key in value:
            empty[key][sub_key] = 0
    return empty
         