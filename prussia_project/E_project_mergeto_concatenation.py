import os
import pandas as pd

#base_path = r'C:\Users\Moritz.Mendel\Dropbox\Germany_state\1_Data\Radio_and_Nazis'

base_path = r"~/Dropbox/Germany_state/1_Data"

radio_regions = "Radio_and_Nazis/Germany_Media_Replication_Regions.dta"
radio_raw_data_df = pd.read_stata(os.path.join(base_path, radio_regions))

radio_towns = "Radio_and_Nazis/Germany_Media_Replication_Towns.dta"
radio2_raw_data_df = pd.read_stata(os.path.join(base_path, radio_towns))

crosswalk_df = pd.read_stata(
    os.path.join(base_path, "Radio_and_Nazis/krnr_town_ids.dta")
)

crosswalk_file = "Radio_and_Nazis/ids_with_krnrs_names_and_idnames.dta"
crosswalk_2_df = pd.read_stata(
    os.path.join(base_path, crosswalk_file)
)

map_data_raw_df = pd.read_csv(os.path.join(base_path, "admin_units_1932.txt"))

gemeinde_1930 = "admin_units_1930.txt"
map_data_raw_df_2 = pd.read_csv(os.path.join(base_path, gemeinde_1930))

#####################Unique ident##############################################


###############################################################################
###################Define relevant functions###################################
###############################################################################


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


###############################################################################
#######################Data Prep###############################################
###############################################################################

radio_merge_df = pd.DataFrame(
        {"id": radio_raw_data_df.drop_duplicates(["id"])["id"]})

###############################################################################
#######################Merge to ID#############################################
###############################################################################

merge_df = radio_merge_df.merge(
        crosswalk_2_df,
        how="outer", on="id").drop([1183, 1184])


##########################################Prepare radio data set###############


radio_df_merge = merge_df.rename(
    columns={"idname": "radio_kreis_merge", "name": "radio_kreis"}
)

radio_df_merge = radio_df_merge.replace(
    {
        "radio_kreis_merge": {
            "TARNOWITZ": "BEUTHEN-TARNOWITZ",
            "HAMBORN": "DUISBURG-HAMBORN",
            "DUISBURG": "DUISBURG-HAMBORN",
            "HATTINGEN": "ENNEPE-RUHR",
            "GLADBACH": "GLADBACH-RHEYDT",
            "HARBURG": "HARBUG-WILHELMSBURG",
            "ZABRZE": "HINDENBURG",
            "COETHEN": "KOETHEN",
            "KREFELD": "KREFELD-UERDING",
            "METTMANN": "DUSSELDORF-METTMANN",
            "MUNCHEN GLADBACH": "GLADBACH-RHEYDT",
            "REICHENBACH": "REICHENBACH (EULENGEBIRGE)",
            "RHEYDT": "GLADBACH-RHEYDT",
            "GREVENBROICH": "GREVENBROICH-NEUSS",
            "BUER": "GELSENKIRCHEN",
            "BAMBERG II": "BAMBERG L",
        }
    }
)


#####################Unique ident##############################################
unique_identifier_map = "map_kreisnr"

unique_identifier_radio = "id"


###############################################################################
###################Prepare the map data set####################################
###############################################################################


map_df_merge = map_data_raw_df_2[["NAME", "STATUS", "ID", "RB", "TYPE"]]
# Add a shortname column to the map_data


map_df_merge = map_df_merge.rename(
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
    map_df_merge["map_kreis"],
    map_df_merge["map_kreis_type"],
    map_df_merge["map_type"]
)


map_df_merge = pd.concat([map_df_merge, merge_column], axis=1).rename(
    columns={0: "map_kreis_merge"}
)


#########################Specify merge data frames#############################
map_df = map_df_merge

radio_df = radio_df_merge


##############################################Merge keys#######################

merge_key_map = "map_kreis_merge"

merge_key_radio = "radio_kreis"

###############################################################################
#######################First Merge Process#####################################
###############################################################################
merged_df_2 = map_df.merge(
    radio_df,
    how="inner",
    left_on=merge_key_map,
    right_on=merge_key_radio,
    indicator=True,
)

##############################Sort put unique matches on the left side ########


merge_summary_series = merged_df_2["_merge"].value_counts()


########################Get left over data ####################################

map_merged_list = list(merged_df_2[unique_identifier_map])
map_left_over_df = (map_df
                    .loc[~map_df[unique_identifier_map]
                    .isin(map_merged_list)]
                    )


radio_merged_list = list(merged_df_2[unique_identifier_radio])
radio_left_over_df = (radio_df
                      .loc[~radio_df[unique_identifier_radio]
                      .isin(radio_merged_list)]
                      )


####################################2nd Merge Ṕrep#############################


#########################Specify merge data frames#############################
map_df = map_left_over_df

radio_df = radio_left_over_df.drop_duplicates(["radio_kreis_merge"])


##############################################Merge keys#######################

merge_key_map = "map_kreis"

merge_key_radio = "radio_kreis_merge"


###############################################################################
#######################First Merge Process#####################################
###############################################################################
merged_df_3 = map_df.merge(
    radio_df,
    how="inner",
    left_on=merge_key_map,
    right_on=merge_key_radio,
    indicator=True,
)

##############################Sort put unique matches on the left side ########


merge_summary_series = merged_df_3["_merge"].value_counts()


###############################################################################
##########################Get left over data###################################
###############################################################################


map_merged_list = list(merged_df_3[unique_identifier_map])
map_left_over_df = (map_df
                    .loc[~map_df[unique_identifier_map]
                    .isin(map_merged_list)]
                    )


radio_merged_list = list(merged_df_3[unique_identifier_radio])
radio_left_over_df = (radio_df
                      .loc[~radio_df[unique_identifier_radio]
                      .isin(radio_merged_list)]
                      )


###############################################################################
###########################cOMPOSE FULL DATASET################################
###############################################################################


merged_df = pd.concat(
    [merged_df_2, merged_df_3, map_left_over_df], axis=0
).drop_duplicates([unique_identifier_map])

####create a crosswalk between town id and krnr
final2_df = crosswalk_df.merge(radio2_raw_data_df,
                               how= "left",
                               on = "town_id")

output_base_path = r"~/Dropbox/Germany_state/2_Analysis/2_period_data/1_prewar"

merged_df.to_csv(os.path.join(output_base_path, "merge_map_radio.csv"))
final2_df.to_csv(os.path.join(output_base_path, "merge_kr_tid.csv"))
