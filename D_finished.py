"""
Short description of the way too complicated merge process:

    Merge a df of persecution variables on the
    merge_map_persecution_crosswalk_to_persecution.csv file
    Use kreis_nr or kreis as merge key these are both unique !
    Then we have a file that link the unique kreis name to the merge
    name which could be different depending on
    the level of aggregation.

    Then we groupy the resulting df by nazi_kreis_merge.
    (That is also why the reduce strings functions looks so ugly to ensure
    that there are no duplicated nazi_kreis_merge variables that are
    not the same unit !)
    Thereafter we can glue that to the actual crosswalk that relates
    nazi_merge_names to map merge names by nazi_merge_names !
    Then we can easily connect to the map data !

    Quick explanation we we merge in two steps:
    The first crosswalk specifies which persecution units to aggregate and the
    second one links the aggregated units to map units.
    That procedure is required due to a county reform in the early 30s.

    Manual merges:
    Some crosswalks are still saved in csv files. That was a bad idea but now
    we are stuck with in due to lock in effects.
    What I do is import these files perfroming two left merges with left over
    dataframes to get an other small part of the crosswalk.
    In the end I concatenate these files.
"""
import os

import pandas as pd
import numpy as np

#Global variables
base_path = r"~/Dropbox/Germany_state"
unique_identifier_nazi = "nazi_kreiskey"
unique_id_map = "map_kreisnr"
output_base_path = r"~/Dropbox/Germany_state/2_Analysis/2_period_data/1_prewar"

##################################Import Data###############################
# Persecution Data
persq = r"1_Data/Persecution_perpetuated/Dataset_QJE_Replicate_with_Cities.dta"
persecution_perpetuated_df = pd.read_stata(os.path.join(base_path,persq,))

#Map data
map_df_1932 = pd.read_csv(os.path.join(base_path, gemeinde_1930))

#Import the manual merges I did in csv files
manual_merge_nazi = "6_Code/Manual_Merges_CSV/manual_merges_map_nazi_1.csv"
manual_merge_df_1 = pd.read_csv(os.path.join(base_path, manual_merge_nazi))

manual_merge_nazi2 = "6_Code/Manual_Merges_CSV/manual_merges_map_nazi_2.csv"
manual_merge_df_2 = pd.read_csv(os.path.join(base_path, manual_merge_nazi2))


##################################Define Relevant Functions #################


def reduce_strings(string):
    """
    This function serves to reduce the persecution county names.
    The function mainly removes the brackets after which a more detailed
    reference to the place is made.
    """
    out = string
    if "HALLE" in string:
        out = out
    elif "KOENIGSBERG" in string:
        out = out
    elif "NEUSTADT" in string:
        out = out
    elif " (" in string:
        out = string.split(" (")[0]
    return out


def extend_strings(series_county_names, series_county_types, series_county_types_2):
    """
    This function returns a new series that is represented in a slightly more
    useful manner for our analysis.

    """
    out = pd.Series([0] * len(series_county_names))
    duplication_indication = series_county_names.duplicated(keep=False)
    for x in range(len(series_county_names)):
        if duplication_indication[x] == False:
            out[x] = series_county_names[x]
        elif duplication_indication[x] == True and (
            (series_county_types[x] != "S" and series_county_types[x] != "/")
            or (series_county_types_2[x] == "2")
        ):
            out[x] = series_county_names[x] + " L"
        elif duplication_indication[x] == True and (
            series_county_types[x] == "S" or series_county_types_2[x] == "1"
        ):
            out[x] = series_county_names[x] + " S"
        else:
            out[x] = series_county_names[x]
    return out


def drop_land_stadt(df, col_name):
    """
    This function reduces the city names in the persecution set to match to the
    unidenntified units in the map data  set
    """

    for x in list(df.index):

        if " L" in df[col_name][x]:
            df[col_name][x] = df[col_name][x].replace(" L", "")
        elif " S" in df[col_name][x]:
            df[col_name][x] = df[col_name][x].replace(" S", "")
        else:
            df[col_name][x] = df[col_name][x]
    return df

###############################################################################
####################################Set up Nazi Data ##########################
###############################################################################
#Drop duplicated units and clean the raw data of persecution
persecution_perp_merge_df = (
    persecution_perpetuated_df[["kreis_nr", "kreis"]]
    .drop_duplicates(["kreis"])
    .rename(columns={"kreis_nr": "nazi_kreiskey", "kreis": "nazi_kreis"})
)

#Further processing
persecution_perp_merge_df["nazi_kreis_merge"] = persecution_perp_merge_df[
    "nazi_kreis"
].map(reduce_strings)

#Create a crosswalk. This is in additio to the two csv files
persecution_perp_merge_df = persecution_perp_merge_df.replace(
    {
        "nazi_kreis_merge": {
            "ESSEN L": "ESSEN",
            "ESSEN S": "ESSEN",
            "HAMBORN  S": "DUISBURG-HAMBORN",
            "DETMOLD S": "DETMOLD",
            "DETMOLD L ": "DETMOLD",
            "BAMBERG II L": "BAMBERG L",
            "BAMBERG I L ": "BAMBERG L",
            "HOERDE L": "DORTMUND L",
            "HOERDE S": "DORTMUND L",
            "FULDA": "FULDA L",
            "NEUSS S": "NEUSS",
            "HAMM S": "HAMM",
            "HAMM L": "HAMM",
            "KREFELD L": "KEMPEN-KREFELD",
            "KEMPEN": "KEMPEN-KREFELD",
            "KREFELD S": "KREFELD-UERDING",
            "DUESSELDORF L": "DUSSELDORF-METTMANN",
            "DILLENBURG": "DILLKREIS",
            "DESSAU-KOETHEN": "DESSAU",
            "DORTMUND LKR.": "DORTMUND L",
            "GRAFSCHAFT DIEPHOLZ": "DIEPHOLZ",
            "GRAFSCHAFT HOYA": "HOYA",
            "GRAFSCHAFT WERNIGERODE": "WERNIGERODE",
            "HADELN L": "HADELN",
            "HIRSCHBERG S": "HIRSCHBERG",
            "NEUSTRELITZ S": "STRELITZ S",
            "KOENIGSHOFEN": "KOENIGSHOFEN IM GRABFELD",
            "LANDSBERG": "LANDSBERG S",
            "MUENDEN": "MUNDEN",
            "NAUMBURG": "NAUMBURG S",
            "SCHOETMAR": "SCHOETTMAR",
            "WESERMUENDE  S": "WESERMUNDE",
            "GLADBACH-RHEYDT  S": "GLADBACH-RHEYDT",
            "GLADBACH": "GLADBACH-RHEYDT",
            "GREVENBROICH": "GREVENBROICH-NEUSS",
            "SIEGEN": "SIEGEN S",
            "METTMANN": "DUSSELDORF-METTMANN",
            "DUISBURG": "DUISBURG-HAMBORN",
            "GEESTEMUENDE  ": "GEESTEMUNDE",
        }
    }
)

#############################################################################
##################Set up Map Data Frame######################################
############################################################################
#Subset dfs
map_df_1932_merge = map_df_1932[["NAME", "STATUS", "ID", "RB", "TYPE"]]

#Renae stuff
map_df_1932_merge = map_df_1932_merge.rename(
    columns={
        "NAME": "map_kreis",
        "STATUS": "map_kreis_type",
        "ID": "map_kreisnr",
        "RB": "map_rb",
        "TYPE": "map_type",
    }
)

# Create a new column with extended  names
merge_column = extend_strings(
    map_df_1932_merge["map_kreis"],
    map_df_1932_merge["map_kreis_type"],
    map_df_1932_merge["map_type"],
)


#Concat files
map_df_1932_merge = (pd.concat
                     ([map_df_1932_merge, merge_column], axis=1)
                     .rename(columns={0: "map_kreis_merge"})
                     )

###################Specify Merge data frames ##############################
nazi_df = persecution_perp_merge_df
map_df = map_df_1932_merge

###############################################################################
###########################First Manual Merge            ######################
###############################################################################
manual_merge_df_step_1 = map_df.merge(
        manual_merge_df_1,
        how="inner",
        on="map_kreisnr"
        )
merged_df_1 = nazi_df.merge(
        manual_merge_df_step_1,
        how="inner",
        on="nazi_kreiskey"
        )


###############################################################################
#################Get left over data############################################
###############################################################################
map_merged_list = list(merged_df_1[unique_id_map])
map_left_over_df = (map_df
                    .loc[~map_df[unique_id_map]
                    .isin(map_merged_list)]
                    )

nazi_merged_list = list(merged_df_1[unique_identifier_nazi])
nazi_left_over_df = (nazi_df
                     .loc[~nazi_df[unique_identifier_nazi]
                     .isin(nazi_merged_list)]
                     )

###################Specify Merge data frames ##############################
nazi_df = nazi_left_over_df.drop_duplicates(["nazi_kreis_merge"])
map_df = map_left_over_df

###########################Specify Merge Paramters#############################
merge_key_nazi = "nazi_kreis_merge"
merge_key_map = "map_kreis_merge"

##########################Merge Process########################################
# First merge porcess
merged_df_2 = map_df.merge(
    nazi_df,
    how="inner",
    left_on=merge_key_map,
    right_on=merge_key_nazi,
    indicator=True).drop_duplicates(unique_id_map)

merge_summary_series = merged_df_2["_merge"].value_counts()

#######################Get left over data frames ##############################
map_merged_list = list(merged_df_2[unique_id_map])
map_left_over_df = (map_df
                    .loc[~map_df[unique_id_map]
                    .isin(map_merged_list)]
                    )

nazi_merged_list = list(merged_df_2[unique_identifier_nazi])
nazi_left_over_df = (nazi_df
                     .loc[~nazi_df[unique_identifier_nazi]
                     .isin(nazi_merged_list)]
                     )


###############################################################################
###########   Manual Merge 2                  #################################
###############################################################################
###################Specify Merge data frames ##################################
nazi_df = nazi_left_over_df
map_df = map_left_over_df

###############################################################################
###########################First Manual Merge            ######################
###############################################################################
manual_merge_df_step_1 = map_df.merge(
        manual_merge_df_2,
        how="inner",
        on="map_kreisnr"
        )

merged_df_4 = nazi_df.merge(
        manual_merge_df_step_1,
        how="inner",
        on="nazi_kreiskey"
        )

###############################################################################
######################Get left over values#####################################
###############################################################################
map_merged_list = list(merged_df_4[unique_id_map])
map_left_over_df = (map_left_over_df
                    .loc[~map_df[unique_id_map]
                    .isin(map_merged_list)]
                    )

nazi_merged_list = list(merged_df_4[unique_identifier_nazi])
nazi_left_over_df = (nazi_df
                     .loc[~nazi_df[unique_identifier_nazi]
                     .isin(nazi_merged_list)]
                     .drop_duplicates(["nazi_kreis_merge"], keep=False)
                     )


###############################################################################
##########################create data set######################################
###############################################################################
#crosswalk map
final_merged_df = pd.concat(
    [merged_df_1, merged_df_2, merged_df_4, map_left_over_df], axis=0
).drop_duplicates([unique_id_map])

#aggregation crosswalk
crosswalk_nazi_data = persecution_perp_merge_df[
    ["nazi_kreis_merge", "nazi_kreiskey"]
]

#Save dataframes
merge_map_persecution = "merge_map_persecution.csv"
final_merged_df.to_csv(os.path.join(output_base_path, merge_map_persecution))
# This can be used to map the nazi data to the crosswalk file
crosswalk_nazi_data.to_csv(
    os.path.join(output_base_path,
                 "merge_map_persecution_crosswalk_to_persecution.csv"
                 )
)
