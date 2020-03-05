"""Form dictionaries containing trial .txt content. Amalgamate the dicts
to form a long list of trials that can be used to extract info using regex.

"""
import os
from collections import defaultdict


def file_writer(path, country):
    """Generates a dictionary with trial # as key, trial content as value.
    
    Args:
        path (string): The last parent folder where the file belongs
        number (non-negative integer): refers to the folder location in the 
        list of folders 
        country (string): either american or british
    Returns: 
        trial_text_dict (dict)
        
    
    """
    input_base_path = r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\trimmed"
    list_of_war_files = []
    list_of_war_files.extend(os.listdir(os.path.join(input_base_path, country)))
    os.chdir(path)
    trial_text_dict = defaultdict(list)
    for i, file in enumerate(list_of_war_files):
        with open(file, "r") as file:
            trial_text_dict[i].append(file.read())
    
    return trial_text_dict 


    os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder")