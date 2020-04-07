
"""
Functions required for cleaning map data 
"""
import numpy as np
import pandas as pd


def fix_encoding_bug(string):
    new_string = (
        string.replace("Ã", "ss")
        .replace("Ã¼", "ue")
        .replace("Ã¶", "oe")
        .replace("Ã¤", "ae")
    )
    return new_string


def umlaut_rem(string):
    new_string = (
        string.replace("ö", "oe")
        .replace("ä", "ae")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )
    return new_string


def import_func(path):
    if path[-3:] == "dta":
        out = pd.read_stata(path, encoding="latin1")
    if path[-5:] == "z.csv":

        out = pd.read_csv(path, 
                          sep=",",
                          encoding = "latin1", 
                          index_col=None
                          )
        
    elif path[-3:] == "csv":

        out = pd.read_csv(path, 
                          sep=";",
                          encoding = "latin1", 
                          index_col=None
                          )
    
    else:
        out = pd.read_csv(path, sep=" ",encoding = "latin1", index_col=None)
    return out


def hyphen_rem(string):
    new_string = string.replace("-", "")
    return new_string


def a_rem(string):
    new_string = string.replace(" a", "")
    return new_string


def rem_whitespace(string):
    new_string = string.replace(" ", "")
    return new_string


def col_rem(df, name):
    for x in range(len(df)):
        if df[name][x] == "b":
            df[name][x] = df[name][x - 1]
        if df[name][x] == "c":
            df[name][x] = df[name][x - 2]
    return df


def merge_func(df, name):
    """
    This function deals with tables where one unit has more than one row!
    """
    df["duplicated"] = df.duplicated(["Gemeinde"])
    if df["duplicated"].sum() == 0:
        new_df = df
    else:
        df_1 = df.loc[df["duplicated"] == 0]
        df = df.loc[df["duplicated"] == 1]
        df["duplicated_2"] = df.duplicated(["Gemeinde"])
        df_2 = df.loc[df["duplicated_2"] == 0]
        if df["duplicated_2"].sum() == 0:
            new_df = df_1.merge(df_2, on="Gemeinde", how="left")
        else:
            df_3 = df.loc[df["duplicated_2"] == 1]
            df_merge_1 = df_1.merge(df_2, on="Gemeinde", how="left")
            new_df = df_merge_1.merge(df_3, on="Gemeinde", how="left")
    return new_df


def apply_to_dict(df_dict, list_of_func, variable):
    out = df_dict
    for func in list_of_func:
        for x in list(out.keys()):
            out[x][variable] = out[x][variable].map(lambda y: func(y))
    return out

def rename_cols(df):
    df_out = df.copy().rename(columns = {"City":"Gemeinde"})
    return df_out

def drop_empty_rows(df):
    df_im = df.dropna(subset=["Gemeinde"]).reset_index()
    df_out = df_im.copy()[~(df_im["Gemeinde"].str.contains("Grupp"))].reset_index()
    return df_out

def rm_numbers(string):
    list_numbers = list(range(10))
    list_numbers = [str(x) for x in list_numbers]
    string = string.lstrip()
    if (
     ((string[0]) in list_numbers)
     and ((string[1]) in list_numbers)
     and ((string[2]) in list_numbers)
     ):
        out = string[3:]
    elif (
     ((string[0]) in list_numbers)
     and ((string[1]) in list_numbers)
     ):
        out = string[2:]
    elif (((string[0]) in list_numbers)):
        out = string[1:]
    else:
        out = string
        
    return out 
    
def string_to_numeric(variable):
     new_variable = string.replace("-", "9999")
     new_variable = pd.to_numeric(new_variable.str.replace(",","."))
     new_variable = new_variable.replace(9999, np.NaN)
     return new_variable


def reduce_strings(string):
    """
    This function serves to reduce the persecution county names. 
    The function mainly removes the brackets after which a more detailed 
    reference to the place is made. 
    """
    out = string
    if " (" in string:
        out = string.split(" (")[0]
        if " L" in out:
            out = out.split(" L")[0]
        else:
            pass
        
    elif " L" in out:
        out = out.split(" L")[0]
    
    else:
        pass
    
    return out


def leftover_analysis(merge_key_map, merge_key_data, map_df, source_df, source_id):
    """Get leftover data."""
    
    merged_df = map_df.merge(
                                source_df,
                                how="inner",
                                left_on=merge_key_map,
                                right_on=merge_key_data,
                                indicator=True,
                            )
    
    # Get leftover
    map_merged_list = list(merged_df["map_kreisnr"])
    
    map_left_over_df = (map_df
                        .loc[~map_df["map_kreisnr"]
                        .isin(map_merged_list)]
                        )
    
    
    data_merged_list = list(merged_df[source_id])
    
    data_left_over_df = (source_df
                          .loc[~source_df[source_id]
                          .isin(data_merged_list)]
                          )
    
    return merged_df, data_left_over_df, map_left_over_df
    