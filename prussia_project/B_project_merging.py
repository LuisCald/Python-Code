import os
import pandas as pd
import numpy as np

base_path = r"C:\Users\Jrxz12\Dropbox\Germany_state"
gemeinde_1930 = r"1_Data\admin_units_1930.txt"
map_raw_data_df = pd.read_csv(os.path.join(base_path, gemeinde_1930))

bowling = r"1_Data\Bowling_For_Fascism\Crosswalk_Bowling_Cityid_Cityname.dta"
bowling_raw_data_df = pd.read_stata(os.path.join(base_path, bowling))

###############################Prepare Map Data###############################
map_data_merge_df = map_raw_data_df.rename(
    columns={
        "NAME": "map_kreis",
        "STATUS": "map_kreis_type",
        "ID": "map_kreisnr",
        "RB": "map_rb",
        "TYPE": "map_type",
    }
)
#Setting up merge column and renaming rows
map_data_merge_df["map_kreis_merge"] = map_data_merge_df["map_kreis"]
map_data_merge_df["map_kreis_merge"][753] = "MUELHEIM A.D.R."
map_data_merge_df["map_kreis_merge"][662] = "MUELHEIM"
map_data_merge_df["map_kreis_merge"][456] = "HAALE (SAALE)"
map_data_merge_df["map_kreis_merge"][363] = "FRANKFURT ODER"


unique_id_map = "map_kreisnr"
###############################Prepare Bowling Data############################


bowling_merge_df = bowling_raw_data_df.rename(
    columns={"kreis_weimar": "bowling_kreis"}
)

unique_identifier_bowling = "cityid"

#Setting up merge column
bowling_merge_df["bowling_kreis_merge"] = bowling_merge_df["bowling_kreis"]


bowling_merge_df = bowling_merge_df.replace(
    {
        "bowling_kreis_merge": {
            "GELSENKIRCHEN-BUER": "GELSENKIRCHEN",
            "CALBE": "KALBE",
            "ANGERMUENDE": "ANGERMUNDE",
            "ENNEPE-RUHRKREIS": "ENNEPE-RUHR",
            "GLADBACH": "GLADBACH-RHEYDT",
            "BREMEN": "HANSESTADT BREMEN",
            "CALAU": "KALAU",
            "CLEVE": "KLEVE",
            "DESSAU-KOETHEN": "DESSAU",
            "KREFELD-UERDINGEN": "KREFELD-UERDING",
            "DUESSELDORF-METTMANN": "DUSSELDORF-METTMANN",
            "DUEREN": "DUREN",
            "RHEYDT": "GLADBACH-RHEYDT",
            "DUESSELDORF": "DUSSELDORF",
            "BUER": "GELSENKIRCHEN",
            "FRANKENTHAL": "FRANKENTHAL (PFALZ)",
            "GOETTINGEN": "GOTTINGEN",
            "GRAFSCHAFT SCHAUMBURG": "SCHAUMBURG",
            "HAMBURG": "HANSESTADT HAMBURG",
            "JUELICH": "JULICH",
            "KOELN": "KOLN",
            "Karlsruhe": "KARLSRUHE",
            "LUEBECK": "HANSESTADT LUEBECK",
            "LUENEBURG": "LUNEBURG",
            "MUENSTER": "MUNSTER",
            "NEUSTADT (HARDT)": "NEUSTADT AN DER HAARDT",
            "OSNABRUECK": "OSNABRUCK",
            "Recklinghausen": "RECKLINGHAUSEN",
            "UECKERMUENDE": "UCKERMUNDE",
            "UELZEN": "ULZEN",
            "WEIDEN": "WEIDEN IN DER OBERPFALZ",
            "COTTBUS": "KOTTBUS",
            "NEUSTRELITZ": "STRELITZ",
            "HALLE ": "HAALE (SAALE)",
        }
    }
)


###############Specify Merge Dataframes#######################################

bowling_df = bowling_merge_df.drop_duplicates(["bowling_kreis_merge"])

map_df = map_data_merge_df


###############################################################################
#########################First Merge Process###################################
###############################################################################


merged_df_1 = map_df.merge(
                            bowling_df,
                            how="inner",
                            left_on="map_kreis_merge",
                            right_on="bowling_kreis_merge",
                            indicator=True,
                            )

merge_summary_series = merged_df_1["_merge"].value_counts()


###############################################################################
###################Get left over values########################################
###############################################################################


map_merged_list = list(merged_df_1[unique_id_map])


map_left_over = map_df.loc[~map_df[unique_id_map].isin(map_merged_list)]


bowling_merged_list = list(merged_df_1[unique_identifier_bowling])

bowling_left_over_df = bowling_df.loc[
    ~bowling_df[unique_identifier_bowling].isin(bowling_merged_list)
]


###############################################################################
#########################Create Full Merge#####################################
###############################################################################

# This gets the left over from the map df and then we merge to the inner-merged
# df
merged_df = pd.concat(
        [map_left_over, merged_df_1], axis=0).drop_duplicates([unique_id_map])

#That is the question whether we should do this ?
#Ultimately we should run this on the
###############################################################################
#############################save dataframe####################################
###############################################################################


output_base_path = r"~/Dropbox/Germany_state/2_Analysis/2_period_data/1_prewar"


merged_df.to_csv(os.path.join(output_base_path, "merge_map_bowling.csv"))

bowling_merge_df[["cityid", "bowling_kreis_merge"]].to_csv(
    os.path.join(output_base_path, "merge_map_bowling_crosswalk_bowling.csv")
)
