"""Merge bowling for fascism data to map data."""
import os
import pandas as pd
from Desktop.pre_war_copy.base_map import gemeinde_replacements
from Desktop.pre_war_copy.base_map import import_data
from Desktop.pre_war_copy.y_utilities import leftover_analysis

def map_bowling():
    """ Maps bowling data to map. """
    
    base_path = r"C:\Users\Jrxz12\Dropbox\Germany_state"
    
    bowling_names = r"1_Data\Bowling_For_Fascism\Crosswalk_Bowling_Cityid_Cityname.dta"
    
    bowling_data = r"1_Data/Bowling_For_Fascism/Dataset_Bowling_Replication_JPE.dta"
    
    # Import bowling data and map data
    bowling_names, map_df = import_data(base_path, bowling_names)
    
    bowling = pd.read_stata(os.path.join(base_path, bowling_data))
    
    # Merge names with data
    bowling_names["kreis_weimar"][78] =  "RECKLINGHAUSEN S"
    
    bowling_df = bowling.merge(
                                bowling_names,
                                how="inner",
                                on="cityid"
                                )
    
    variables_to_keep_bowling_process = [
                                            "bowling_kreis",
                                            "bowling_kreis_merge",
                                            "city",
                                            "logtaxprop",
                                            "logtaxpers",
                                            "share_prot25",
                                            "cityid",
                                            "pop25",
                                            "clubs_all",
                                            "clubs_nonCivic_pc",
                                            "clubs_civic_pc",
                                            ]
    
    # Prepare map data
    map_df = map_df.copy().rename(columns={
                                    "NAME": "map_kreis",
                                    "STATUS": "map_kreis_type",
                                    "ID": "map_kreisnr",
                                    "RB": "map_rb",
                                    "TYPE": "map_type",
                                    }
    )
    
    map_df["map_kreis_merge"] = map_df["map_kreis"].copy()
    
    bowling_df = bowling_df.copy().rename(columns={"kreis_weimar": "bowling_kreis"})
    
    bowling_df["bowling_kreis_merge"] = bowling_df["bowling_kreis"].copy()
    
    bowling_df = bowling_df.copy().replace(gemeinde_replacements("bowling"))
    
    bowling_df = bowling_df.copy().drop_duplicates(["bowling_kreis_merge"])
    
    bowling_df = bowling_df.copy()[variables_to_keep_bowling_process]
    
    map_key = "map_kreis_merge"
    
    bowling_key = "bowling_kreis_merge"
    
    bowling_mapped, bowling_left_over_df, map_left_over_df = (
                                                                leftover_analysis(
                                                                                    map_key, 
                                                                                    bowling_key, 
                                                                                    map_df, 
                                                                                    bowling_df, 
                                                                                    "cityid"
                                                                                    )
                                                                )
        
    merged_df = (
                    pd.concat([map_left_over_df, bowling_mapped], axis=0)
                    .drop_duplicates(["map_kreisnr"])
    )
    
    output_base_path = r"~/Dropbox/Germany_state/2_Analysis/2_period_data/1_prewar"
    
    # Bowling mapped
    merged_df.to_csv(os.path.join(output_base_path, "bowling_mapped.csv"))
    
    return merged_df

