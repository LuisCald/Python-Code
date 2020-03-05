import os
import pandas as pd
import numpy as np

#Secify the path for importing variables
import_base_path =  r"C:\Users\Jrxz12\Dropbox\Germany_state"

#Specify a list of variables that we want to keep
#1.Merge variables 2. unique dig 3. unique map 4. map aggregate
variables_crosswalk = ["gemeinde_merge","Gemeinde", "ID","NAME"]

#Define unique idnetifiers
unique_id_map = "ID"
unique_identifier_dig = "Gemeinde"

#Import the raw map

map_raw_df = pd.read_csv(os.path.join(import_base_path, gemeinde_1930))

#Import the all gemeinde names file. This file contains all the unique Gemeinde
#names for both weimar and Nazi from the digitilization effort.

unique_dig_gemeinde = r"2_Analysis\2_period_data\1_prewar\merge_key_dig.csv"
dig_raw_df = pd.read_csv(os.path.join(import_base_path, unique_dig_gemeinde))

#I copy the df to avoid pandas problems
dig_df = dig_raw_df.copy()

#We create a new column and apply changes such that it merges with the map 
#units
dig_df["gemeinde_merge"] = (
        dig_raw_df["Gemeinde"]
        .copy().map(lambda x: x.upper())
        .map(lambda x: x.replace("UE","U"))
        .map(lambda x: x.replace("OE","O"))
        .map(lambda x: x.replace("AE","A"))
        )

#Specify name mapping
renaming_dict = {
    "BREMEN":"HANSESTADT BREMEN",
    "COTTBUS":"KOTTBUS",
    "Cotbus": "KOTTBUS",
    "GRUNBERG":"GRUENBERG",
    "FRANKFURT/M":"FRANKFURT/MAIN",
    "FRANKFURT/M.":"FRANKFURT/MAIN",
    "FRANKFURT_ODER":"FRANKFURT/ODER",
    "FURTH":"FUERTH",
    "HAMBURG":"HANSESTADT HAMBURG",
    "Hellbronn":"HEILBRONN",
    "Harb.-Wilhelmsb.":"WILHELMSBURG",
    "Ofenbach":"OFFENBACH",
    "Muechen": "MUENCHEN",
    "HILDESCHEIM":"HILDESEIM",
    "KIRCHHAIN":"KIRCHHEIN",
    "KOTHEN":"KOETHEN",
    "HILDESCHEIM":"HILDESEIM",
    "LUDWIGSHAFEN":"LUDWIGSHAFEN AM RHEIN",
    "LUBECK":"HANSESTADT LUEBECK",
    "LUDENSCHEIDT":"LUDENSCHEID",
    "MEERSBURG":"MERSEBURG",
    "MORS":"MOERS",
    "NURNBERG":"NUERNBERG",
    "Neustadt.H.":"NEUSTADT",
    "OBERHAUSENB":"OBERHAUSEN",
    "PLAUN":"PLAUEN",
    "QUDLINBURG":"QUEDLINBURG",
    "Quedlimburg":"QUEDLINBURG",
    "RUSTRINGEN":"RUESTRINGEN",
    "WALD":"WALDMUENCHEN",
    "WURZBURG":"WUERZBURG",
    "KREFELD-URDINGEN":"KREFELD-UERDING",
    "AU":"AUE",
    "GOPPINGEN":"GOEPPINGEN",
    "BADKREUZN":"KREUZNACH",
    "BUR":"BUREN",
    "CRIMMITSCH":"CRIMMITSCHAU",
    "DELMENH":"DELMENHORST",
    "DOBELN":"DOEBELN",
    "FRANKENTHAL":"FRANKENTHAL (PFALZ)",




                 }

#apply the dict
dig_df= dig_df.replace({"gemeinde_merge":renaming_dict})

#Process Map. Only keep variables that are relavent to the crosswalk.
map_df = map_raw_df[["NAME","ID"]]
map_df["name_merge"] = map_df["NAME"].copy()

#create a variable for aggregatioon purposes
map_df["name_merge"][363] = "FRANKFURT/MAIN"
map_df["name_merge"][680] = "FRANKFURT/ODER"

#We groupy by the map on the gemeinde level
map_merge_df = map_df.groupby("name_merge").agg({"ID":"first",
                                                  "NAME":"first"})

#merge procedure (it said raw before)
merged_df = map_merge_df.merge(dig_df,
                             how = "inner",
                             left_on = "name_merge",
                             right_on = "gemeinde_merge",
                             indicator = True )
summary_df = merged_df["_merge"].value_counts()

#Get left over frames
#Get the list of all merged units
map_merged_list = list(merged_df[unique_id_map])
#Get the all the names of units that are not merged
map_left_over_df = (map_merge_df
    .loc[~map_merge_df[unique_id_map]
    .isin(map_merged_list)])

#Do the same thing for the other dataset
dig_merged_list = list(merged_df[unique_identifier_dig])
dig_left_over_df = dig_df.loc[
    ~dig_df[unique_identifier_dig].isin(dig_merged_list)
]

#Save the crosswalk
crosswlk = "2_Analysis/2_period_data/1_prewar/crosswalk_dig.csv"
merged_df[variables_crosswalk].to_csv(os.path.join(import_base_path, crosswlk))
