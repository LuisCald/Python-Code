""" Create datasets containing information extracted from snippets.
    Row index indicates the number of trial. 
    Save dataset as .csv and .xlsx files.

"""

import os
import regex as re
import pandas as pd


# Create datasets


def trial_dataframe(snippet_dict, best_guess_dict=False):
    
    snippet_df = pd.DataFrame()
    for i, snippet in enumerate(snippet_dict.keys()):
        df = pd.DataFrame.from_dict(snippet_dict[snippet], orient="index")
        df.columns = (["{}".format(snippet) + str(i) for i in range(1, (len(df.columns) + 1))])
        snippet_df = pd.concat([df, snippet_df], axis=1)
    snippet_df["trial_number"] = snippet_df.index
    snippet_df = pd.wide_to_long(snippet_df, stubnames=snippet_dict.keys(), i=['trial_number'], j='person_number')
    snippet_df = snippet_df.dropna(how="all")

    if best_guess_dict:
        snippet_df.to_csv(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\final\dataset.csv", sep=",")
        snippet_df.to_excel(r'C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\final\dataset.xlsx')
    else:        
        snippet_df.to_csv(r"C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\final\dataset_snippets.csv", sep=",")
        snippet_df.to_excel(r'C:\Users\Jrxz12\Dropbox\Germany_state\war_crime_folder\final\dataset_snippets.xlsx')

    return snippet_df

# Drop if names are kinda the same with fuzzy matching
# iguanas = print(fuzz.ratio("the apple is red".split(), "the apple is".split()))




