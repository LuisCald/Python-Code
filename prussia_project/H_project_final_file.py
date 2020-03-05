"""
This file creates a complete dataframe for the nazi data.
Therefore it imports all the files and crosswalks and
glues them together.

I declare lists of variables to be exported first. Whenever a new variable
is added to the processsed datasets its name has to be added to these lists
as well if it should be exported.
 """
import os

import pandas as pd

#The collections of variables for the final nazi dataset
final_variable_collection = [
    "income_tax_per_capita",
    "property_tax_per_capita",
    "total_tax_per_capita",
    "antisemitic_culture_proxy",
    "deportations_per_jewish_inhabitant",
    "deportations_per_jewish_inhabitant39",
    "nazi_share_28",
    "nazi_share_30",
    "nazi_share_32",
    "nazi_share_33",
    "NAME",
    "share_prot25",
    "pog20s",
    "syn33",
    "jews33",
    "c25juden",
    "pog33",
    "ID", #This was changed
    "exposure_prussia",
    "prussia_ind",
    "segment_identifier",
    "NEAR_DIST",
    "NEAR_FID",
    "inc_year",
    "inc_random",
    "long_name",
    "lat",
    "lon",
    "west_ind",
    "west_middle",
    "nap_ind",
    "dist_berlin",
    "logdeport",
    "deptotal",
    "change_jewish_inhabitants_33_39",
    "change_jewish_inhabitants_25_33",
    "change_jewish_inhabitants_25_39",
    "clubs_per_capita",
    "share_listeners31",
    "segment_identifier_alt1",
    "segment_identifier_alt2",
    "RB",
    "c25kath_share",
    "c25juden_share",
    "prot_share",
   "taxable_income_thousands",
   "tot_income_tax_thousands",
   "tot_income_tax_pt",
   "income_tax_pc",
   "local_tax_pc",
   "land_and_building_tax",
   "business_tax",
   "wealth_transfer_tax",
   "land_and_building_taxes_nominal",
   "business_tax_nominal",
   "wealth_transfer_tax_nominal",
   "local_tax_tot_nominal",
   'taxable_income_thousands_nazi',
   'taxable_income_nazi_pt',
   'taxable_income_nazi_pc',
   'income_taxes_collected_thousands_nazi',
   'income_taxes_collected_nazi_pt',
   'income_taxes_collected_pc',
   'elementary_exp_pc',
   'secondary_exp_pc',
   'gen_man_tax_finance_exp_pc',
   'police_exp_pc',
   'school_admin_exp_pc',
   'infrastructure_exp_pc',
   'welfare_exp_pc',
   'health_exp_pc',
   'pop_residential_jan_1937',
   'Beamte37',
   'tot_empl37',
   'tot_immigrants36',
   'tot_imm36_p1000',
   'tot_emigrants36',
   'tot_emi36_p1000',
   'net_migration36',
   'net_migration36p1000',
   'net_migration35p1000',
   'net_migration34p1000',
   'moves_within36',
   'moves_within36p1000'
   ]

final_variable_collection_weimar = []

#The importbase path
bp = r"C:\Users\Jrxz12\Dropbox\Germany_state\2_Analysis\2_period_data\1_prewar"

#All relevant datasets are imported
#there are two diffferent radio datasets that is why we import two frames
radio_df = pd.read_csv(
        os.path.join(
                bp,
                r"radio_processed.csv")
        ).drop(["Unnamed: 0"], axis=1).drop_duplicates(["id"])

radio2_df = pd.read_csv(
        os.path.join(
                bp,
                r"radio2_processed.csv"
                )
        ).drop(["Unnamed: 0"], axis=1).drop_duplicates(["town_id"])

crosswalk_radio_df = pd.read_csv(
        os.path.join(
                bp,
                'merge_map_radio.csv'
                )
        ).drop(["Unnamed: 0"], axis=1)

crosswalk_radio_2_df = pd.read_csv(
        os.path.join(
                bp,
                'merge_kr_tid.csv'
                )
        ).drop(["Unnamed: 0"], axis=1)


pers_processed = "persecution_processed.csv"
persecution_df = (pd.read_csv(os.path.join(
        bp, pers_processed))
        .drop(["Unnamed: 0"], axis=1)
        )

merge_map_pers = "merge_map_persecution.csv"
crosswalk_persecution_1_df = (pd.read_csv(os.path.join(
        bp, merge_map_pers))
        .drop(["_merge", "Unnamed: 0"], axis=1)
        )
# Diese drop geschichten sollten eigentlich davor passieren !

crosswalk_persecution_2_df = pd.read_csv(
    os.path.join(
        bp,
        "merge_map_persecution_crosswalk_to_persecution.csv",
    )
)


bowling_df = pd.read_csv(
    os.path.join(
        bp, "bowling_processed.csv"
    )
)


crosswalk_bowling_1_df = pd.read_csv(
    os.path.join(
        bp, "merge_map_bowling.csv"
    )
)

crosswalk_bowling_2_df = pd.read_csv(
    os.path.join(
        bp,
        "merge_map_bowling_crosswalk_bowling.csv",
    )
)

# Use the two crosswalks

bowling_intermed_df = (
    crosswalk_bowling_2_df.merge(bowling_df, how="left", on="cityid")
    .groupby(["bowling_kreis_merge"])
    .mean()
    .reset_index()
)

bowling_final_df = crosswalk_bowling_1_df.merge(
    bowling_intermed_df, how="left", on="bowling_kreis_merge"
)

#import digitized data

weimar_dig_df = pd.read_csv(os.path.join(bp,r"weimar_dig_processed.csv"))

nazi_dig_df = pd.read_csv(os.path.join(bp,r"nazi_dig_processed.csv"))

crosswalk_dig_df = pd.read_csv(os.path.join(bp,r"crosswalk_dig.csv"))

#I changed these both to right. The result was no change in observations in
#the regressions
#nor was there a change in the results. Actually, nazi is now 999 observations,
#which is supposed to be correct
nazi_merge_df = crosswalk_dig_df.merge(
        nazi_dig_df,
        on= "Gemeinde",
        how= "right")

weimar_merge_df = crosswalk_dig_df.merge(
        weimar_dig_df,
        on= "Gemeinde",
        how= "left")
#Import the map data

prussia_map_df = pd.read_csv(
    os.path.join(
        bp,
        "prussia_map_df.csv",
    )
)


#####Merge Persecution to crosswalk
# 1. Group by counties in persecution


nazi_intermed_df = (
    crosswalk_persecution_2_df.merge(
        persecution_df,
        how="left",
        left_on="nazi_kreiskey",
        right_on="kreis_nr"
        )
    .groupby(["nazi_kreis_merge"])
    .mean()
    .reset_index()
)
# This is unique since every unique county name carries a unique kreisnr
# One right merge left over that carries no name. Everything else one to one

nazi_full_df = crosswalk_persecution_1_df.merge(
    nazi_intermed_df, how="left", on="nazi_kreis_merge", indicator=True
)
# 34 right and 400 left This is what we obtained in the merge process

radio_intermed_df = crosswalk_radio_df.merge(
        radio_df,
        how= "left",
        on = "id")

radio2_intermed_df = crosswalk_radio_2_df.merge(
        radio2_df,
        how= "left",
        on = "town_id").groupby(["krnr"]).mean()

radio_final_df = radio_intermed_df.merge(
        radio2_intermed_df,
        how="left",
        on="krnr").rename(columns={
                "c25kath_share_y":"c25kath_share",
                "c25juden_share_y":"c25juden_share" })
####Glue this data set to the map

final_pers_df = prussia_map_df.merge(
    nazi_full_df,
    how="left",
    left_on=["NAME", "ID"],
    right_on=["map_kreis", "map_kreisnr"],
)

intermed_df = final_pers_df.merge(
    bowling_final_df,
    how="left",
    left_on=["NAME", "ID"],
    right_on=["map_kreis", "map_kreisnr"],
)
#I changed to right for both
intermed_2_df = intermed_df.merge(
        nazi_merge_df,
        on = ["NAME","ID" ],
        how = "left").rename(columns={"FID_1":"FID","RB_x":"RB"})

final_df = intermed_2_df.merge(
        radio_final_df[["id",
                        "map_kreisnr",
                        "share_listeners31",
                        'c25kath_share',
                        'c25juden_share']],
        how = "left",
        left_on = "ID",
        right_on = "map_kreisnr")[final_variable_collection]


# Still add the bowling data frame !


# Save the dataframe
output_base_path = "~/Dropbox/Germany_state"


final_df.to_csv(
    os.path.join(
        output_base_path, "2_Analysis/2_period_data/1_prewar/final_nazi_df.csv"
    )
)

#Something is weird here that makes the merge messy.
map_weimar_df = prussia_map_df.groupby("NAME").agg("first")


final_weimar_df = map_weimar_df.merge(
        weimar_merge_df,
        on = "NAME",
        how = "left")

final_weimar = "2_Analysis/2_period_data/1_prewar/final_weimar_df.csv"
final_weimar_df.to_csv(os.path.join(output_base_path,final_weimar))
