""" Functions required for cleaning map data

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

def rem_whitespace(string):
    new_string = string.replace(" ", "")
    return new_string

def apply_to_dict(df_dict, list_of_func, variable):
    out = df_dict
    for func in list_of_func:
        for x in list(out.keys()):
            out[x][variable] = out[x][variable].map(lambda y: func(y))
    return out


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
