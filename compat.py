import os
import csv
import shutil
import chardet
directory = r"C:\Users\noahs\Documents\Spot On Lighting\App\data\options"
data_names={}
data_dict = {}
def generate_options()-> dict:
    # Iterate over files in the directory
    for filename in os.listdir(directory):        
        file_name = filename.split('-')[1].split('.')[0]
        file_name_ = filename.split('-')[1].split('_')[0]
        file_path = os.path.join(directory, filename)
        
        # Process files ending with 'options.csv'
        if filename.endswith('options.csv'):
            # Extract file name for tuple name
            dict_key=file_name_
            dict_values={}
            # Read and create tuple from the first column

    # Open the file with the detected encoding
            with open(file_path, mode='r', newline='', encoding='latin-1') as file:
                reader = csv.reader(file, delimiter='\t')
                names=[] 
                for row in reader:                   
                    small_key=row[0].lstrip('\ufeff').strip('ï»¿')
                    dict_values[small_key]=0
                    names.append(small_key)
                    data_dict[file_name_]=dict_values
                names.insert(0,"Select")
        data_names[file_name_] = names
        # Store tuple in the dictionary
        
   
    return data_dict,data_names