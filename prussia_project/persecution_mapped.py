"""Mapping Persecution."""
import os
import pandas as pd

from Desktop.pre_war_copy.base_map import gemeinde_replacements
from Desktop.pre_war_copy.base_map import import_data
from Desktop.pre_war_copy.all_var_lists import persecution_vars
from Desktop.pre_war_copy.y_utilities import reduce_strings
from Desktop.pre_war_copy.y_utilities import leftover_analysis


def map_persecution():
    """ Maps persecution data to map. """

    base_path = r"~/Dropbox/Germany_state"
    
    persq = r"1_Data/Persecution_perpetuated/Dataset_QJE_Replicate_with_Cities.dta"
    
    persecution_perpetuated_df, map_df = import_data(base_path, persq)
    
    persecution_perpetuated_df["kreis"][79] = "BAMBERG L"
    
    persecution_perpetuated_df["kreis"][78] = "BAMBERG L"
    
    vars_persecution_process, persecution_agg_rules = persecution_vars()
    
    persecution_perpetuated_df = persecution_perpetuated_df.copy()[vars_persecution_process]
    
     
    #Aggregate on the county level. Sum everything since all absolute quantities. 
    persecution_perpetuated_df = (persecution_perpetuated_df
                                .groupby(["kreis_nr","kreis"])
                                .agg(persecution_agg_rules)
                                .reset_index()
                        )
    
    persecution_perpetuated_df = (
            persecution_perpetuated_df.copy().rename(columns={
                                                "kreis_nr": "nazi_kreiskey", 
                                                "kreis": "nazi_kreis"
                                                }
        )
    )
    
    persecution_perpetuated_df["nazi_kreis_merge"] = persecution_perpetuated_df["nazi_kreis"].copy()
    
    persecution_perpetuated_df = persecution_perpetuated_df.copy().replace(gemeinde_replacements("persecution"))
    
    #Rename stuff
    map_df = map_df.copy().rename(columns={
                                            "NAME": "map_kreis",
                                            "STATUS": "map_kreis_type",
                                            "ID": "map_kreisnr",
                                            "RB": "map_rb",
                                            "TYPE": "map_type",
                                        }
        )
    
    # Create a new column with extended  names
    map_df["map_kreis_merge"] = map_df["map_kreis"].copy()
    
    nazi_df = persecution_perpetuated_df.copy()

    map_key = "map_kreis_merge"
    
    nazi_key = "nazi_kreis_merge"
    
    pers_mapped, nazi_left_over_df, map_left_over_df = (
                                                        leftover_analysis(
                                                                            map_key, 
                                                                            nazi_key, 
                                                                            map_df, 
                                                                            nazi_df, 
                                                                            "nazi_kreiskey"
                                                                            )
                                                        )
    
    # In this case, given the remaining names have the S/L before the parenthesis,
    # we can split first by parenthesis then letter. Taking the left-over, removing L, then merge
    # Duisburg is the only one that has parenthesis before S, but we don't have duisburg
    # in map 
    nazi_left_over_df['nazi_kreis_merge'] = nazi_left_over_df['nazi_kreis_merge'].map(reduce_strings)
    
    leftovers_merged, nazi_left_over_df, map_left_over_df = (
                                                    leftover_analysis(
                                                                        map_key, 
                                                                        nazi_key, 
                                                                        map_left_over_df, 
                                                                        nazi_left_over_df, 
                                                                        "nazi_kreiskey"
                                                                        )
                                                    )
    
    pers_mapped = pd.concat([
                                pers_mapped.copy(), 
                                map_left_over_df, 
                                leftovers_merged], axis=0
        )
    
    
    #Save dataframes 
    output_base_path = r"~/Dropbox/Germany_state/2_Analysis/2_period_data/1_prewar"
    
    # Export persecution combined
    pers_mapped.to_csv(os.path.join(output_base_path, "persecution_mapped.csv"))
    
    return pers_mapped

