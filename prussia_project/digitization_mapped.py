"""Mapping digitization."""
import os 
import pandas as pd

from Desktop.pre_war_copy.base_map import gemeinde_replacements
from Desktop.pre_war_copy.base_map import import_data
from Desktop.pre_war_copy.all_var_lists import weimar_initial_vars
from Desktop.pre_war_copy.all_var_lists import nazi_initial_vars
from Desktop.pre_war_copy.y_utilities import leftover_analysis

# Import data
def map_digitization():
    """ Maps digitized data to map. """

    base_path =  r"C:\Users\Jrxz12\Dropbox\Germany_state"
    
    dig_file = r"2_Analysis\2_period_data\1_prewar\merge_key_dig.csv"
    
    dig_df, map_df = import_data(base_path, dig_file)
    
    
    #We create a new column and apply changes such that it merges with the map units
    dig_df["gemeinde_merge"] = (
            dig_df["Gemeinde"]
            .copy().map(lambda x: x.upper())
            .map(lambda x: x.replace("UE","U"))
            .map(lambda x: x.replace("OE","O"))
            .map(lambda x: x.replace("AE","A"))
            )
    
    map_df = map_df.copy().rename(columns={
                                            "NAME": "map_kreis",
                                            "STATUS": "map_kreis_type",
                                            "ID": "map_kreisnr",
                                            "RB": "map_rb",
                                            "TYPE": "map_type",
                                        }
        )
    map_df["map_kreis_merge"] = map_df["map_kreis"].copy()
        
    # Add S to some Gemeinde to properly merge. 
    dig_df = dig_df.copy().drop_duplicates("Gemeinde")
    
    dig_df = dig_df.replace({"gemeinde_merge":gemeinde_replacements("dig")})
    
    
    # Trying to add "S" to "gemeinde_merge" in dig_df if it appears in map
    for i, value in enumerate(dig_df["gemeinde_merge"]):
        if value + " S" in map_df["map_kreis_merge"].values:
            dig_df["gemeinde_merge"][i] = value + " S" 
    
    #merge procedure (it said raw before)
    map_key = "map_kreis_merge"
    
    dig_key = "gemeinde_merge"
    
    merged_df, dig_left_over_df, map_left_over_df = (
                                                        leftover_analysis(
                                                                            map_key, 
                                                                            dig_key, 
                                                                            map_df, 
                                                                            dig_df, 
                                                                            dig_key
                                                                            )
                                                        )
    
    merged_df = merged_df.groupby("gemeinde_merge").first().reset_index()
    
    merged_df = pd.concat([merged_df, map_left_over_df], axis=0)
    
    # Reading weimar. Merge to merged_df 
    import_base_path = r"~\Dropbox\Germany_state\2_Analysis\2_period_data\1_prewar"
    
    dig_weimar_df = (pd.read_csv(os.path.join(import_base_path,"weimar_dig.csv"))
        .rename(columns = {"Unnamed: 0":"Gemeinde"})
        )
    
    variables_to_keep_weimar_dig_process = weimar_initial_vars()
    
    dig_weimar_df = dig_weimar_df.copy()[variables_to_keep_weimar_dig_process]
    
    weimar_mapped = merged_df.merge(
                                        dig_weimar_df,
                                        how="left",
                                        on="Gemeinde"
                                        )
    
    # Reading nazi. Merge to merged_df
    dig_nazi_df = (pd.read_csv(os.path.join(import_base_path,"nazi_dig.csv"))
        .rename(columns = {"Unnamed: 0":"Gemeinde"})
        )
    
    variables_to_keep_nazi_dig_process = nazi_initial_vars()
    
    dig_nazi_df = dig_nazi_df.copy()[variables_to_keep_nazi_dig_process]
    
    nazi_mapped = merged_df.merge(
                                        dig_nazi_df,
                                        how="left",
                                        on="Gemeinde"
                                        )
    
    weimar_mapped.to_csv(os.path.join(base_path,"2_Analysis/2_period_data/1_prewar/weimar_mapped.csv"))
    
    nazi_mapped.to_csv(os.path.join(base_path,"2_Analysis/2_period_data/1_prewar/nazi_mapped.csv"))
    
    return nazi_mapped, weimar_mapped
