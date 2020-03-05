"""
This file compiles the map data.
We have several datasets that contain important information.
These include distance measures, segment identifiers and indicators.
This script creates one coherent dataset out of all these.
"""
import os

import pandas as pd
import numpy as np

#define relevant functions
def prussia_ind(string):
    if string == "/":
        return 0
    else:
        return 1

#Import path
import_base_path =  "~/Dropbox/Germany_state"

#This is the map csv that contains information about expansion and randomness
exp = "2_Analysis/1_merged_gis_data/1_prewar/map_1930_merged_to_expansion.csv"
prussia_map_import_df = pd.read_csv(os.path.join(import_base_path, exp))

#This file contains information about the distance to the boundary
dist_boundary = "2_Analysis/3_distance_data/1_prewar/1930_dist_to_boundary.txt"
prussia_rd_df = pd.read_csv(os.path.join(import_base_path, dist_boundary))

#This file contains infomration about lattitude and longitude
lat_lon = "2_Analysis/1_merged_gis_data/1_prewar/map_1930_ll.csv"
prussia_ll_df = pd.read_csv(os.path.join(import_base_path, lat_lon))

#This file contains information about segment identifiers
segment_identifier = "2_Analysis/2_period_data/1_prewar/map_boundary_segments_restricted.csv"
map_bs_df = (pd.read_csv(os.path.join(
        import_base_path, segment_identifier))
    .rename(columns = {"NEAR_FID":"segment_identifier"})
    )

#This file contains information about other segment identifiers
s="2_Analysis/2_period_data/1_prewar/map_boundary_segments_restricted_alt1.csv"
map_bs_new_1_df = (pd.read_csv(os.path.join(
        import_base_path, s))
    .rename(columns = {"NEAR_FID":"segment_identifier_alt1"})
    )

#This file contains information about other segment identifiers
c="2_Analysis/2_period_data/1_prewar/map_boundary_segments_restricted_alt2.csv"
map_bs_new_2_df = (pd.read_csv(os.path.join(
        import_base_path,c))
    .rename(columns = {"NEAR_FID":"segment_identifier_alt2"})
    )

#This file contains information about distance to berlin
prussia_berlin_df = pd.read_csv \
    (os.path.join(import_base_path ,
                  "2_Analysis/2_period_data/1_prewar/map_dis_to_berlin.csv"
                  )
    ).rename(
    columns = {"NEAR_DIST":"dist_berlin"}
    )


#Specify fixed effects dicts
#Inidcator for the eastern parts
dict_rb_region = {
    "POT":0,
    "BER":0,
    "FRA":0,
    "KOS":0,
    "MAG":0,
    "ERF":0,
    "STE":0,
    "GUM":0,
    "KON":0,
    "MAR":0,
    "MIN":1,
    "ARN":1,
    "DUS":1,
    "MER":0,
    "MUN":1,
    "OSN":1,
    "AUR":1,
    "DAN":0,
    "SMU":0,
    "POS":0,
    "LIE":0,
    "BRE":0,
    "OPP":0,
    "KOL":1,
    "KOB":1,
    "TRI":1,
    "AAC":1,
    "STR":0,
    "SIG":1,
    "KAS":1,
    "SCH":1,
    "LUN":1,
    "STA":1,
    "HIL":1,
    "HAN":1,
    "WIE":1,
    "/":np.nan
}

#We merge everything together step by step. We only keep relevant variables
prussia_intermediate_1_df = prussia_map_import_df.merge(
    prussia_rd_df[["NEAR_DIST",'NEAR_FID' ,'ID']],
    #prussia_rd_df[['NEAR_DIST' ,'NEAR_FID' ,'ID']],
    how='left',
    on = 'ID'
)

prussia_intermediate_2_df = prussia_intermediate_1_df.merge(
    prussia_ll_df[['lat' ,'lon' ,'ID']],
    how='left',
    on = 'ID'
)


prussia_intermediate_3_df = prussia_intermediate_2_df.merge(
    prussia_berlin_df[["ID","dist_berlin"]],
    how="left",
    on = "ID"
)
#final_df = prussia_intermediate_3_df.merge(
#                        map_bs_df[["segment_identifier","ID"]],
#                        how= "left",
#                        on = "ID")

prussia_intermediate_4_df = prussia_intermediate_3_df.merge(
        map_bs_df[["segment_identifier","ID"]],
        how= "left",
        on = "ID"
        )


prussia_intermediate_5_df = prussia_intermediate_4_df.merge(
        map_bs_new_1_df[["segment_identifier_alt1","ID"]],
        how= "left",
        on = "ID"
        )

final_df = prussia_intermediate_5_df.merge(
        map_bs_new_2_df[["segment_identifier_alt2","ID"]],
        how= "left",
        on = "ID"
        )

#We create an indicator for Prussia
final_df["prussia_ind"] = final_df["RB"].map(prussia_ind)

#We delete counties that have zeros years of  beeing Prussia and have
#a prussia indicator equal to one. (These units seem to be wrong)
filter_prussia = (final_df['inc_year' ] == 0) & (final_df["prussia_ind" ] == 1)
final_df = final_df[~filter_prussia]

#We remap the incorporation year and create other useful historic inidcators
final_df["inc_year"] = final_df["inc_year"].replace({0 :1871})
final_df["exposure_prussia"] = final_df["inc_year"].map(lambda x: 1871 - x  )
final_df["west_ind"] = final_df["RB"].replace(dict_rb_region)
napoleon_filter = (final_df["inc_year"] == 1815) & (final_df["west_ind" ] == 1)
final_df["nap_ind"] = napoleon_filter.map(lambda x: int(x))
old_west_filter = (final_df["inc_year"] <= 1815) & (final_df["west_ind" ] == 1)
final_df["old_west_ind"] =old_west_filter.map(lambda x: float(x))
final_df["west_middle"] = final_df["old_west_ind"] +final_df["west_ind"]

#####Save data
output_path = "~/Dropbox/Germany_state/2_Analysis/2_period_data/1_prewar"
final_df.to_csv(os.path.join(output_path, "prussia_map_df.csv"))
