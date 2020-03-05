import os
import json

import regex as re
import pandas as pd
import numpy as np
import PyPDF2

from collections import defaultdict
from fuzzywuzzy import fuzz

os.chdir(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder")
import preprocess_pdfs 
from trial_extraction import file_processor
from trial_extraction import pdf_to_string
from trial_extraction import export_trial_dict_to_folder
from extract_snippets import extract_info
from extract_snippets import extract_info2
from extract_snippets import analysis
from functions_metadata import file_writer

from regex_dict import *
from search_snippets import snippet_and_best_guess_dict
from search_snippets import british_snippet_and_best_guess_dict

from create_output import trial_dataframe

# To test your new dictionary because you changed a rule, just import regex_dict and search_snippets
# Then run from snippet_dict onward (approximately line 49)

pdf1 = "us_military_reports_1_25.pdf"
pdf2 = "us_military_trial_reports_26_48.pdf"

# british pdfs
british_pdf1 = "british_military_trial_reports_2_48.pdf"
british_pdf2 = "british_military_trial_reports_49_103.pdf"
british_pdf3 = "british_military_trial_reports_319_415.pdf"
british_pdf4 = "british_military_trial_reports_416_470.pdf"
british_pdf5 = "british_military_trial_reports_471_476.pdf"
british_pdf6 = "british_military_trial_reports_477_524.pdf"

paths_dict = {
    "to_process_pdf_american" : r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\0_original\american\pre_processed_pdfs",
    "to_process_pdf_british" : r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\0_original\british\pre_processed_pdfs",
    "save_ind_trials_american" : r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\trimmed\american",
    "save_ind_trials_british" : r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\trimmed\british"
    }

# Only for 2 pdfs, since the other files could not be read with PyPDF2
# US
preprocess_pdfs.pre_process_pdf(0, 33, pdf1, 1, "american", second_set=True, lb2=628, ub2=3568)    
preprocess_pdfs.pre_process_pdf(0, 12, pdf2, 2, "american", second_set=True, lb2=17, ub2=20)    

#British      
pages_to_delete = list(range(0, 12))
pages_to_delete.extend(list(range(877, 902)))
pages_to_delete.extend(list(range(1550, 2755)))
preprocess_pdfs.pre_process_pdf2(pages_to_delete, british_pdf1, 3, "british")      
  
pages_to_delete2 = list(range(0, 318))
pages_to_delete2.extend(list(range(805, 812)))
pages_to_delete2.extend(list(range(1151, 1163)))
pages_to_delete2.extend(list(range(1168, 1200)))
pages_to_delete2.extend(list(range(1306, 2630)))     
preprocess_pdfs.pre_process_pdf2(pages_to_delete2, british_pdf2, 4, "british")      
# preprocess_pdfs.pre_process_pdf(0, 14, british_pdf3, 5, "british", second_set=False)      
# preprocess_pdfs.pre_process_pdf(0, 13, british_pdf4, 6, "british", second_set=False)      
# preprocess_pdfs.pre_process_pdf(0, 12, british_pdf5, 7, "british", second_set=False)      
# preprocess_pdfs.pre_process_pdf(0, 10, british_pdf6, 8, "british", second_set=False)      

# Import war files
american_war_files = file_processor(paths_dict["to_process_pdf_american"], "american")
british_war_files = file_processor(paths_dict["to_process_pdf_british"], "british")

# Create .txt files of each trial and store in specified folder
export_trial_dict_to_folder(dict_of_regexes["american"], american_war_files, "american")
export_trial_dict_to_folder(dict_of_regexes["british"], british_war_files, "british")

# Write in the .txt files to create trial dictionary
american_trial_dict = file_writer(paths_dict["save_ind_trials_american"], "american")
british_trial_dict = file_writer(paths_dict["save_ind_trials_british"], "british")

# Extract from trial_dict
snippet_dict, best_guess_dict = snippet_and_best_guess_dict(american_trial_dict, snippet_rules_dict, bestguess_rules_dict)
british_snippet_dict, british_best_guess_dict = british_snippet_and_best_guess_dict(british_trial_dict, snippet_rules_dict_british, bestguess_rules_dict_british)

# Analysis of missing
analysis(best_guess_dict)
analysis(snippet_dict)

analysis(british_best_guess_dict)
analysis(british_snippet_dict)

# Extract one-pagers, [\s\S]*?(?:Date of Receipt|To whom sent|Date sent|Purport)
regex = r"((?:MILITARY\W+(?:\w+\W+){0,6}CRIMINALS)\s+(?:\S+\s*){2000})"
british_one_pagers = []
for i, war_file in enumerate(british_war_files):
    one_pagers = re.findall(regex, british_war_files[i])
    british_one_pagers.append(one_pagers)






# Create dataframe of snippet and of best guesses 
trial_snippet_df = trial_dataframe(snippet_dict, best_guess_dict=False)
best_guess_df = trial_dataframe(best_guess_dict, best_guess_dict=True)