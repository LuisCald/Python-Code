"""Clean chs data and BEHAVIOR_PROBLEMS_INDEX data and merge them.
"""
import numpy as np
import pandas as pd

from bld.project_paths import project_paths_join as ppj


# ****************************** Clean chs_data.dta. ***************************
# Load chs_data.dta into pandas DataFrame.
df_chs = pd.read_stata(ppj("IN_DATA", "chs_data.dta"))

# Convert 'childid' and 'momid' to integers.
df_chs[["childid", "momid"]] = df_chs[["childid", "momid"]].astype(int)

# Store unique childids in array.
unique_childid_chs = df_chs["childid"].unique()

# Set the index to childid and year.
df_chs = df_chs.set_index(["childid", "year"], drop=False)

# Keep observations from every second year from 1986 to 2010 inclusive.
df_chs = df_chs[df_chs["year"].isin(list(range(1986, 2011, 2)))]


# ************************ Clean BEHAVIOR_PROBLEMS_INDEX.dta. ******************
# Load BEHAVIOR_PROBLEMS_INDEX.dta into pandas DataFrame.
df_bpi = pd.read_stata(ppj("IN_DATA", "BEHAVIOR_PROBLEMS_INDEX.dta"))

# Rename 'C0000100' to 'childid'.
df_bpi = df_bpi.rename(columns={"C0000100": "childid"})

# Convert 'childid' to integers.
df_bpi["childid"] = df_bpi["childid"].astype(int)

# Keep observations which are present in chs_data.
df_bpi = df_bpi[df_bpi["childid"].isin(unique_childid_chs)]

# Replace all negative numbers with np.nan.
# Having a look at the codebook one sees that there are -1, -2, -3 and -7.
df_bpi = df_bpi.replace(to_replace=(-1, -2, -3, -7), value=np.nan)

# Load bpi_variable_info.csv into pandas DataFrame.
df_bpi_variable_info = pd.read_csv(ppj("IN_DATA", "bpi_variable_info.csv"))

# Store nlsy names from the bpi_variable_info.csv in a list.
nlsy_name = df_bpi_variable_info["nlsy_name"].tolist()

# Rename 'C0000100' to 'childid'.
nlsy_name[0] = "childid"

# Keep only variables in BEHAVIOR_PROBLEMS_INDEX.dta which are in bpi_variable_info.csv.
df_bpi = df_bpi[nlsy_name]


# *** BEHAVIOR_PROBLEMS_INDEX.dta in long format: preparation & completion. ****
# Store readable names and survey years from bpi_variable_info.csv in lists.
readable_name = df_bpi_variable_info["readable_name"].tolist()
survey_year = df_bpi_variable_info["survey_year"].tolist()

# Combine readable_name and survey_year into one string with "-" as separator.
readable_name_year = [i + "-" + j for i, j in zip(readable_name, survey_year)]

# Rename 'childid-invariant' to 'childid'.
readable_name_year[0] = "childid"

# Rename variables in BEHAVIOR_PROBLEMS_INDEX.dta to "readable_name-survey_year".
df_bpi.columns = readable_name_year

# Get unique variable names from readable_name.
stubnames = df_bpi_variable_info["readable_name"].unique().tolist()

# Discard time invariant variables.
stubnames = stubnames[3:]

# Generate long format DataFrame for BEHAVIOR_PROBLEMS_INDEX.dta.
df_bpi_long = pd.wide_to_long(df_bpi, stubnames, i="childid", j="year", sep="-")

# Save long format of BEHAVIOR_PROBLEMS_INDEX.dta as csv. in bld/out/data/bpi_long.csv.
df_bpi_long.to_csv(ppj("OUT_DATA", "bpi_long.csv"))


# ************************** Merge chs and bpi_long data. **********************
# Merge chs and bpi_long keeping observations that are present in the chs dataset.
df_chs_bpi_merged = df_chs.join(df_bpi_long)

# Give all variables that appear in both datasets sensible suffixes.
df_chs_bpi_merged.rename(
    columns={
        "momid": "momid_chs",
        "momid-invariant": "momid_bpi",
        "birthoder": "birthorder_chs",
        "birth_order-invariant": "birthorder_bpi",
    },
    inplace=True,
)

# Drop 'childid' and 'year' such that we can reset the index.
df_chs_bpi_merged = df_chs_bpi_merged.drop(["childid", "year"], axis=1)

# Set index to 'childid' and 'age'.
df_chs_bpi_merged = df_chs_bpi_merged.reset_index().set_index(["childid", "age"])

# Save merged dataset as csv in bld/out/data/bpi_merged.csv.
df_chs_bpi_merged.to_csv(ppj("OUT_DATA", "bpi_merged.csv"))


# ******** Calculate standardized scores for each subscale of the bpi. *********
# Get unique levels from all subscales.
unique_levels = []
for col in stubnames:
    unique_levels += df_chs_bpi_merged[col].unique().tolist()
unique_levels = pd.Series(unique_levels).unique().tolist()

# Convert categorical to numeric and replace other responses with np.nan.
df_chs_bpi_merged[stubnames] = df_chs_bpi_merged[stubnames].replace(
    to_replace=("NOT TRUE", "Not True", "Not true"), value=0
)

df_chs_bpi_merged[stubnames] = df_chs_bpi_merged[stubnames].replace(
    to_replace=(
        "SOMETIMES TRUE",
        "Sometimes True",
        "Sometimes true",
        "OFTEN TRUE",
        "Often True",
        "Often true",
    ),
    value=1,
)

df_chs_bpi_merged[stubnames] = df_chs_bpi_merged[stubnames].replace(
    to_replace=(
        "NEVER ATTENDED SCHOOL",
        "Never Attended School",
        "Child has never attended school",
    ),
    value=np.nan,
)

# Store all subscales in a list.
subscale_strings = [
    "additional",
    "antisocial",
    "headstrong",
    "hyperactive",
    "dependent",
    "anxiety",
    "peer",
]

for subscale in subscale_strings:
    # Calculate the subscale mean for each observation.
    df_chs_bpi_merged[subscale] = (
        df_chs_bpi_merged.filter(regex="{}".format(subscale))
    ).mean(axis=1)
    # Standardize the score to mean 0 and variance 1 for each age group.
    df_chs_bpi_merged[subscale] = (
        df_chs_bpi_merged[subscale] - df_chs_bpi_merged[subscale].groupby("age").mean()
    ) / df_chs_bpi_merged[subscale].groupby("age").std()

# Save final dataset as csv in bld/out/data/bpi_final.csv.
df_chs_bpi_merged.to_csv(ppj("OUT_DATA", "bpi_final.csv"))

# In case you prefer dictionary to make file wide-to-long
# Creating a dictionary with variables corresponding to a certain year
bpi_year_variable = bpi_info_csv[["survey_year", "nlsy_name"]]
bpi_year_variable["nlsy_name"][0] = "childid"
bpi_dict = defaultdict(list)

# This appends the variables to each year
for year, variable in bpi_year_variable.itertuples(index=False):
    if year == "invariant":
        pass
    else:
        bpi_dict[year].append(variable)

# To actually place rows/content into the variables in the dicitonary
bpi_dict2 = defaultdict(list)

for key, value in bpi_dict.items():
    bpi_dict2[key].append(bpi_data[value])

# Replace names with the readable names
dict_bpi_info_readable_name = dict(zip(bpi_info_csv["nlsy_name"], bpi_info_csv["readable_name"]))

for key, value in bpi_dict2.items():
    bpi_dict2[key][0] = bpi_dict2[key][0].rename(columns=dict_bpi_info_readable_name)

# Add Childid to each dataframe
for year in bpi_dict2.keys():
    bpi_dict2[year][0]["childid"] = bpi_data["childid"]

# Form a final dataset, where we concatenate all dfs for all years
bpi_long = pd.DataFrame()

for key, value in bpi_dict2.items():
    df = pd.DataFrame(value[0]) # Creating dataframes from values
    df.loc[:,'year'] = key  # Adding column called 'year'
    bpi_long = pd.concat([df, bpi_long], 0)
    
# Set index as child_id and year
bpi_long = bpi_long.set_index(["childid","year"]) 
