"""Map radio to map."""
import os
import pandas as pd

from Desktop.pre_war_copy.base_map import gemeinde_replacements
from Desktop.pre_war_copy.base_map import import_data
from Desktop.pre_war_copy.all_var_lists import radio_vars
from Desktop.pre_war_copy.y_utilities import leftover_analysis

def map_radio():
    """Merge radio data to map."""
        
    base_path = r"~/Dropbox/Germany_state"
    
    files = {
                "radio_regions": r"1_Data/Radio_and_Nazis/Germany_Media_Replication_Regions.dta",
                "radio_towns": r"1_Data/Radio_and_Nazis/Germany_Media_Replication_Towns.dta",
                "crosswalk_df": r"1_Data/Radio_and_Nazis/krnr_town_ids.dta",
                "crosswalk2_df": r"1_Data/Radio_and_Nazis/ids_with_krnrs_names_and_idnames.dta"            
                }
    
    source_data_dict, map_data_raw_df_2 = import_data(base_path, files)
    
    radio_raw_data_df = source_data_dict["source_data_0"]
    
    radio2_raw_data_df = source_data_dict["source_data_1"].dropna()
    
    crosswalk_df = source_data_dict["source_data_2"]
    
    crosswalk_2_df = source_data_dict["source_data_3"]
    
    radio_ss = radio_raw_data_df[["id", "ss", "lis_share", "year"]]
    
    radio_ss32 = (
                    radio_ss[radio_ss["year"]=="n32n"]
                    .rename(columns={
                                        "ss": "ss32",
                                        "lis_share": "lis_share32"
                                        }).drop("year", axis=1)
                    )
                    
    radio_ss33 = (
                    radio_ss[radio_ss["year"]=="n333"]
                    .rename(columns={
                                        "ss": "ss33",
                                        "lis_share": "lis_share33"
                                        }).drop("year", axis=1)
                    )
                    
    radio_ss = radio_ss32.merge(radio_ss33, how="inner", on="id")
    
    
    radio_df = radio_raw_data_df[radio_raw_data_df.columns.difference(["ss", "lis_share", "year"])].drop_duplicates(["id"])
    
    radio_df = radio_df.merge(radio_ss, how="inner", on="id")
    
    radio_merge_df = radio_df.groupby("id").mean().reset_index()
    
    # merge, drop nans for "krnr"
    merge_df = radio_merge_df.merge(
            crosswalk_2_df, 
            how="inner", on="id").drop([588, 589])
    
    
    ##########################################Prepare radio data set###############
    radio_df_merge = merge_df.rename(
        columns={"idname": "radio_kreis_merge", "name": "radio_kreis"}
    )
    
    # To merge with map properly. 
    radio_df_merge["radio_kreis"][953] = "FRIEDBERG L1"
    
    radio_df_merge["radio_kreis"][965] = "FRIEDBERG L2"
    
    radio_df_merge["radio_kreis"][215] = "HIRSCHBERG K"
    
    radio_df_merge["radio_kreis"][584] = "NEUSTADT L"
    
    radio_df_merge["radio_kreis"][293] = "OLDENBURG K"
    
    radio_df_merge["radio_kreis"][572] = "ROTTENBURG ROTTENBURG AN DER LAABER"
    
    # Drop duplicates of radio kreis, they contain same values in the columns
    radio_df_merge = radio_df_merge.drop_duplicates("radio_kreis")
    
    radio_df_merge = radio_df_merge.replace(gemeinde_replacements("radio"))
    
    radio_df_merge = radio_df_merge.drop_duplicates("radio_kreis")
    
    map_df_merge = map_data_raw_df_2.copy()    
    
    map_df_merge = map_df_merge.rename(
                                        columns={
                                            "NAME": "map_kreis",
                                            "STATUS": "map_kreis_type",
                                            "ID": "map_kreisnr",
                                            "RB": "map_rb",
                                            "TYPE": "map_type",
                                        }
                                        )
    
    map_df_merge["map_kreis_merge"] = map_df_merge["map_kreis"].copy() 
    
    #########################Specify merge data frames#############################
    map_df = map_df_merge.copy()
    
    radio_df = radio_df_merge.copy()
    
    merge_key_map = "map_kreis_merge"
    
    merge_key_radio = "radio_kreis"
    
    merged_df_2, radio_left_over_df, map_left_over_df = (
                                                            leftover_analysis(
                                                                                merge_key_map, 
                                                                                merge_key_radio, 
                                                                                map_df, 
                                                                                radio_df, 
                                                                                "id"
                                                                                )
                                                            )
    
    # Removing parenthesis/L unnecessary here, since they're already removed
    leftovers_merged, radio_left_over_df, map_left_over_df = (
                                                                leftover_analysis(
                                                                                    merge_key_map, 
                                                                                    "radio_kreis_merge", 
                                                                                    map_left_over_df, 
                                                                                    radio_left_over_df, 
                                                                                    "id"
                                                                                    )
                                                                )
    
    merged_df = pd.concat([
                            merged_df_2, 
                            map_left_over_df,
                            leftovers_merged], axis=0
                            ).drop_duplicates(["map_kreisnr"])
    
    # Here, I am looking for rows which have the same kreis and values. These are 
    # sincerely duplicates
    dup = (crosswalk_df.duplicated(["kreis", "n206pop"]))  # The mask
    
    crosswalk_df_dict = {
                            "town_id": "first",
                            "n206pop": "sum",
                            "n245pop": "sum",
                            "n333pop": "sum"
                            }
    
    crosswalk_df = crosswalk_df[~dup].groupby(["krnr", "kreis"]).agg(crosswalk_df_dict).reset_index()
    
    # radio2 only has town_id
    final2_df = crosswalk_df.merge(radio2_raw_data_df,
                                   how= "left",
                                   on = "town_id") 
    
    final2_df["krnr"][176] = 34  # Johannisburg has wrong krnr
    final2_df["krnr"][566] = 1190  # Johannisburg has wrong krnr
    
    # merge final2_df with merged_df. len of map
    radio_combined = merged_df.merge(
                                        final2_df,
                                        how="left",
                                        on="krnr"
                                        )
    
    variables_to_keep_radio_process = radio_vars()
    
    radio_combined = radio_combined.copy()[variables_to_keep_radio_process]
    
    output_base_path = r"~/Dropbox/Germany_state/2_Analysis/2_period_data/1_prewar"
    
    radio_combined.to_csv(os.path.join(output_base_path, "radio_mapped.csv"))
    
    return radio_combined
