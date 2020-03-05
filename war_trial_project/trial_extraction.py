"""Extracts individual war trials from the pdf/text files."""

import os
import json

import regex as re
import PyPDF2
    
# creating a pdf file object 

def pdf_to_string(pdf):
    """Convert war pdf to long string for searchability.
    
    Args:
        pdf (BufferedReader object): pdf file read in with 'rb' option
    
    Returns:
        pdf_content (string)
        
    """
    pdf = PyPDF2.PdfFileReader(pdf) 
    number_of_pages = pdf.getNumPages()
    pdf_content = ""
    for page_number in range(number_of_pages):
        page = pdf.getPage(page_number)
        pdf_content += page.extractText() 
    
    return pdf_content


def file_processor(path, country):    
    input_base_path = r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\0_original\{}".format(country)
    os.chdir(path)
    list_of_war_files = []
    list_of_war_files.extend(os.listdir(os.path.join(input_base_path, "pre_processed_pdfs")))
    new_war_files = []
    for file in list_of_war_files:
        if file[-3:]=="pdf":
            new_war_file = open(file, 'rb')
            new_war_file = pdf_to_string(new_war_file)
            new_war_files.append(new_war_file)
        elif file[-3:]=="txt":
            with open(file, 'r', encoding="utf8") as file:
                new_war_file = file.read()
                new_war_files.append(new_war_file)
        else:
            break
    if country=="american":
        file_order = [3, 4, 0, 1, 2]
        new_war_files = [new_war_files[i] for i in file_order]
    else:
        pass
    return new_war_files 
              

def export_trial_dict_to_folder(dict_of_regexes, war_files, country):
    trial_list = []
    for war_file_rule, war_file in zip(dict_of_regexes.keys(), war_files):
        for i, rule_content in enumerate(dict_of_regexes[war_file_rule]):
            trial_matches = re.findall(rule_content, war_file)
            trial_list.extend(trial_matches)

    trial_dict = {}
    for i in range(len(trial_list)):
        trial_dict[i] = trial_list[i]
    
    os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\trimmed\{}".format(country))
    for i, trial in enumerate(trial_dict.keys()):
        with open('war_trial{}.txt'.format(i), 'w') as file:
            file.write(json.dumps(trial_dict[trial])) 
    os.chdir("..")


    

   


