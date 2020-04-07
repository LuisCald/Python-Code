"""Create base map."""
import pandas as pd
import numpy as np
import os


# Constants
BASE_MAP = "admin_units_1930.txt"
MAP_FOR_MERGING = "admin_units_1930_adjusted.csv"

# Definiing paths to import map
base_path = r"~\Dropbox\Germany_state\1_Data"
map_df_1930 = pd.read_csv(os.path.join(base_path, r"{}".format(BASE_MAP)))

# Doubles
map_df_1930["NAME"][27] = "BRAKE L"
map_df_1930["NAME"][53] = "SCHWERIN A"  # "A" is the status
map_df_1930["NAME"][801] = "LAUENBERG (SCH)"



# Changes for bowling
map_df_1930["NAME"][456] = "HALLE (SAALE)"

# Changes for dig
map_df_1930["NAME"][363] = "FRANKFURT/MAIN" 
map_df_1930["NAME"][680] = "FRANKFURT/ODER" 

# Changes for Persection
map_df_1930["NAME"][136] = "BAMBERG CITY"
map_df_1930["NAME"][540] = "ROTENBURG (HESSEN-NASSAU)" 
map_df_1930["NAME"][753] = "MUELHEIM (RUHR)"
map_df_1930["NAME"][370] = "STARGARD (POMMERN)"
map_df_1930["NAME"][745] = "MARIENBERG (DAN)"

# Changes for Radio
map_df_1930["NAME"][197] = "FRIEDBERG 1"
map_df_1930["NAME"][613] = "FRIEDBERG 2"
map_df_1930["NAME"][486] = "MARIENBURG (HIL)"
map_df_1930["NAME"][487] = "NEUSTADT (OPP)"
map_df_1930["NAME"][422] = "NEUSTADT (HAN)"
map_df_1930["NAME"][795] = "OLDENBURG (SCH)"
map_df_1930["NAME"][75] = "OLDENBURG L"

map_df_1930["NAME"][483] = "ROTENBURG (HANNOVER)"
map_df_1930["NAME"][382] = "ROTHENBURG (OBERLAUSITZ)"

map_df_1930["NAME"][395] = "ROSENBERG (O.S)"
map_df_1930["NAME"][750] = "ROSENBERG (WESTPR.)"

# Add S/L to "NAME"
def extend_strings(gemeinde_list, series_county_types, series_county_types_2):
    """
    This function returns a new series that is represented in a slightly more 
    useful manner for our analysis in the map.
     
    """
    out = gemeinde_list
    duplication_indication = gemeinde_list.duplicated(keep=False)
    for i, gemeinde in enumerate(gemeinde_list):
        if duplication_indication[i] == True:
            if series_county_types_2[i] == "1":
                out[i] = gemeinde_list[i] + " L"
            elif series_county_types[i] == "S" or series_county_types_2[i] == "2":
                out[i] = gemeinde_list[i] + " S"
        else:
            pass  
    return out



extend_strings(
                map_df_1930["NAME"],  # Function overwrites this column
                map_df_1930["STATUS"],  # S or L col
                map_df_1930["TYPE"],  # 1 or 2 col
)

# Adding variables to the map
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

# We merge everything together step by step. We only keep relevant variables 
prussia_intermediate_1_df = prussia_map_import_df.merge(
    prussia_rd_df[["NEAR_DIST",'NEAR_FID' ,'ID']],
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
def prussia_ind(string):
    if string == "/":
        return 0
    else:
        return 1
    
    
final_df["prussia_ind"] = final_df["RB"].map(prussia_ind)

# Correct false inc_year 
RB_dict = {"ARN": 1815, "KAS": 1866, "MER": 1815, "SCH": 1866, "STE": 1720}
for RB, year in RB_dict.items():    
    final_df_mask = (final_df['inc_year'] == 0) & (final_df['RB'] == RB)
    final_df["inc_year"][final_df_mask] = year

#We remap the incorporation year and create other useful historic inidcators 
final_df["inc_year"] = final_df["inc_year"].replace({0: 1871})
final_df["exposure_prussia"] = final_df["inc_year"].map(lambda x: 1871 - x  )

final_df["west_ind"] = final_df["RB"].replace(dict_rb_region)
napoleon_filter = (final_df["inc_year"] == 1815) & (final_df["west_ind" ] == 1)
final_df["nap_ind"] = napoleon_filter.map(lambda x: int(x))
old_west_filter = (final_df["inc_year"] <= 1815) & (final_df["west_ind" ] == 1)
final_df["old_west_ind"] =old_west_filter.map(lambda x: float(x))
final_df["west_middle"] = final_df["old_west_ind"] +final_df["west_ind"]

# Export to csv to be used in the crosswalks
final_df = final_df[final_df.columns.difference([
                                                    "FID",
                                                    "AREA",
                                                    "PERIMETER",
                                                    "LAND",
                                                    "NAME",
                                                    "STATUS",
                                                    "ID",
                                                    "RB",
                                                    "TYPE"
                                                    ]
    )
    ]
info_with_map = map_df_1930.merge(
                                    final_df,
                                    how="inner",
                                    left_on="FID",
                                    right_on="FID_1"
                                    )
output_base_path = r"~\Dropbox\Germany_state\1_Data"

info_with_map.to_csv((os.path.join(output_base_path, MAP_FOR_MERGING)))

###############################################################################
"""Maintain replacements for each source data."""

def gemeinde_replacements(source):
    if source== "bowling":
        gemeinde_dict =     {
            
            "bowling_kreis_merge": {
                                    "AMMERLAND": "WESTERSTEDE",
                                    "BAMBERG": "BAMBERG CITY",
                                    "BONN": "BONN S",
                                    "GELSENKIRCHEN-BUER": "GELSENKIRCHEN",
                                    "CALBE": "KALBE",
                                    "CELLE": "CELLE S",
                                    "EMDEN": "EMDEN S",
                                    "ERFURT": "ERFURT S",
                                    "GOETTINGEN": "GOTTINGEN S",
                                    "GUBEN": "GUBEN S",
                                    "HALBERSTADT": "HALBERSTADT S",
                                    "HANAU": "HANAU S",
                                    "HANNOVER": "HANNOVER S",
                                    "HERFORD": "HERFORD S",
                                    "HILDESHEIM": "HILDESHEIM S",
                                    "ISERLOHN": "ISERLOHN S",
                                    "KOBLENZ": "KOBLENZ S",
                                    "KOELN": "KOLN S",
                                    "MARBURG": "MARBURG S",
                                    "MERSEBURG": "MERSEBURG S",
                                    "NAUMBURG": "NAUMBURG S",
                                    "SIEGEN": "SIEGEN S",
                                    "STENDAL": "STENDAL S",
                                    "TRIER": "TRIER S",
                                    "ZEITZ": "ZEITZ S",
                                    "WEISSENFELS": "WEISSENFELS S",
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
                                    "FRIEDBERG": "FRIEDBERG 2",
                                    "RHEYDT": "GLADBACH-RHEYDT",
                                    
                                    "DUESSELDORF": "DUSSELDORF",
                                    "BUER": "GELSENKIRCHEN",
                                    "FRANKENTHAL": "FRANKENTHAL (PFALZ)",
                                    "GRAFSCHAFT SCHAUMBURG": "SCHAUMBURG",
                                    "HAMBURG": "HANSESTADT HAMBURG",
                                    "JUELICH": "JULICH",
                                    "Karlsruhe": "KARLSRUHE",
                                    "LUEBECK": "HANSESTADT LUEBECK",
                                    "LUENEBURG": "LUNEBURG S",
                                    "MARIENBERG": "MARIENBERG (DAN)",
                                    "MUENSTER": "MUNSTER S",
                                    "NEUSTADT (HARDT)": "NEUSTADT AN DER HAARDT",
                                    "OSNABRUECK": "OSNABRUCK S",
                                    "Recklinghausen": "RECKLINGHAUSEN S",
                                    "ROTHENBURG": "ROTHENBURG (OBERLAUSITZ)",
                                    "UECKERMUENDE": "UCKERMUNDE",
                                    "UELZEN": "ULZEN",
                                    "WEIDEN": "WEIDEN IN DER OBERPFALZ",
                                    "COTTBUS": "KOTTBUS S",
                                    "NEUSTRELITZ": "STRELITZ",
                                    "HALLE ": "HAALE (SAALE)",
                                    "MUELHEIM A.D.R.": "MUELHEIM (RUHR)",
                                    "MUELHEIM": "MULHEIM",
                                    "FRANKFURT ODER": "FRANKFURT/ODER"
                                }
            }
    elif source== "dig":
        gemeinde_dict = {
                        "BAMBERG": "BAMBERG CITY",
                        "BREMEN":"HANSESTADT BREMEN",
                        "COTTBUS":"KOTTBUS",
                        "Cotbus": "KOTTBUS",
                        "GRUNBERG":"GRUENBERG",
                        "FRANKFURT/M":"FRANKFURT/MAIN",
                        "FRANKFURT/M.":"FRANKFURT/MAIN",
                        "FRANKFURT_ODER":"FRANKFURT/ODER",                    
                        "HAMBURG":"HANSESTADT HAMBURG",
                        "Hellbronn":"HEILBRONN",
                        "Harb.-Wilhelmsb.":"HARBUG-WILHELMSBURG",
                        "Ofenbach":"OFFENBACH",
                        "Muechen": "MUENCHEN",
                        "KIRCHHAIN":"KIRCHHEIN",
                        "KOTHEN":"KOETHEN",
                        "LORRACH": "LOERRACH",
                        "LUDWIGSHAFEN":"LUDWIGSHAFEN AM RHEIN",
                        "LUBECK":"HANSESTADT LUEBECK",
                        "LUDENSCHEIDT":"LUDENSCHEID",
                        "MARIENBURG": "MARIENBURG (DAN)",
                        "MEERSBURG":"MERSEBURG",
                        "MORS":"MOERS",
                        "MULHEIM": "MUELHEIM (RUHR)",
                        "NEURUPPIN": "BRANDENBURG",
                        "NORDHORN": "LINGEN",                    
                        "OBERHAUSENB":"OBERHAUSEN",                    
                        "RUSTRINGEN":"RUESTRINGEN",
                        "SCHWELM": "ENNEPE-RUHR",
                        "SCHWENNING": "VILLINGEN",
                        "STARGARD": "STARGARD (POMMERN)",
                        "TUBINGEN": "TUEBINGEN",                    
                        "WALD":"SIGMARINGEN",
                        "KREFELD-URDINGEN":"KREFELD-UERDING",
                        "AU":"AUE",
                        "GOPPINGEN":"GOEPPINGEN",
                        "BADKREUZN":"KREUZNACH",
                        "BUR":"BUREN",
                        "CRIMMITSCH":"CRIMMITSCHAU", 
                        "DELMENH":"DELMENHORST",
                        "DOBELN":"DOEBELN",
                        "FRANKENTHAL":"FRANKENTHAL (PFALZ)",
                        "Kaoserslautern": "Kaiserslautern",                    
                        # necessary since these KEEP the ae, oe, au
                        "FURTH":"FUERTH",
                        "HILDESEIM":"HILDESHEIM",
                        "KAOSERSLAUTERN": "KAISERSLAUTERN",
                        "MUNCHEN": "MUENCHEN S",
                        "NEUSTADT.H.": "NEUSTADT AN DER HAARDT",
                        "NURNBERG":"NUERNBERG",
                        "QUDLINBURG":"QUEDLINBURG",
                        "RAITBOR": "RATIBOR",
                        "PLAUN":"PLAUEN",
                        "SCHONEBERG": "SCHOENBERG",
                        "WURZBURG":"WUERZBURG",
                        "ZWEIBRUCKEN": "ZWEIBRUECKEN",
                        "Halle": "HALLE (SAALE)"
                     }
            
    elif source=="persecution":
        gemeinde_dict = {
            
            "nazi_kreis_merge": {
                                    "ACHIM (-30.9.32)": "ACHIM",
                                    "ALTONA  S": "ALTONA",
                                    "ALZENAU (UNTERFRANKEN)": "ALZENAU",
                                    "ANGERMUENDE": "ANGERMUNDE",
                                    "APOLDA  S": "APOLDA",
                                    "ASCHENDORF (-3O.9.32)/A.": "ASCHENDORF",
                                    "BERLIN-MITTE BA 1": "BERLIN",
                                    "BERSENBRUECK": "BERSENBRUCK", 
                                    "BEUTHEN S": "BEUTHEN",
                                    "BLECKEDE (-30.9.32)": "BLECKEDE",
                                    "BLOMBERG S (-31.3.32)": "BLOMBERG",
                                    "BOCHOLT    S": "BOCHOLT",
                                    "BOCHUM S": "BOCHUM",
                                    "BOTTROP   S": "BOTTROP",
                                    "BREMEN S": "HANSESTADT BREMEN",
                                    "HAMBURG MIT HAFEN  S": "HANSESTADT HAMBURG",
                                    "BUEREN": "BUREN",
                                    "BUETOW": "BUTOW",
                                    "CALBE": "KALBE",
                                    "CAMMIN": "KAMMIN",
                                    "CASTROP-RAUXEL  S (1.4.28-)": "CASTROP-RAUXEL",          
                                    "CLEVE": "KLEVE",
                                    "COCHEM": "KOCHEM",
                                    "COESFELD": "KOESFELD",
                                    "COSEL": "KOSEL",
                                    "COTTBUS S": "KOTTBUS L",
                                    "CUXHAVEN  S": "CUXHAVEN",
                                    "DESSAU-KOETHEN": "KOETHEN",
                                    "DESSAU (-31.12.31)/DESSA": "DESSAU",
                                    "DETMOLD L  (1.4.32-)": "DETMOLD",
                                    "DUEREN": "DUREN",
                                    "DILLENBURG": "DILLKREIS",
                                    "DILLINGEN (DONAU) L": "DILLINGEN AN DER DONAU L",
                                    "DORTMUND S": "DORTMUND",
                                    "METTMANN (-31.7.29)": "DUSSELDORF-METTMANN",
                                    "DUESSELDORF S": "DUSSELDORF",
                                    "DORTMUND LKR.": "DORTMUND L",  # for consistency, not necessary
                                    "EBERSWALDE     S": "EBERSWALDE",
                                    "EISLEBEN  S": "EISLEBEN",
                                    "ENNEPE-RUHRKREIS": "ENNEPE-RUHR",
                                    "ESSEN S": "ESSEN",
                                    "FORST (LAUSITZ)  S": "FORST",
                                    # "FRANKENTHAL L": "FRANKENTHAL (PFALZ) L",
                                    "FRANKENTHAL S": "FRANKENTHAL (PFALZ) S",
                                    "FRANKFURT   S": "FRANKFURT/MAIN",
                                    "FRANKFURT (ODER)  S": "FRANKFURT/ODER", 
                                    "FRITZLAR (-30.9.32)/F.-H": "FRITZLAR",
                                    "FUERSTENBERG S (-14.1.3": "FUERSTENBERG",
                                    "FULDA S (1.4.27-)": "FULDA S",
                                    "GEESTEMUENDE   (-30.9.32)": "GEESTEMUNDE",
                                    "GEILENKIRCHEN (-9.8.33)/GEILENK.-HEINSBE": "GEILENKIRCHEN",
                                    "GELSENKIRCHEN  S": "GELSENKIRCHEN",
                                    "GEMUENDEN": "GEMUENDEN AM MAIN",
                                    "GERSFELD (-30.9.32)": "GERSFELD",
                                    "GLADBACH-RHEYDT  S": "GLADBACH-RHEYDT",
                                    "GLADBACH": "GLADBACH-RHEYDT",
                                    "GLADBECK   S": "GLADBECK",
                                    "GLEIWITZ S": "GLEIWITZ",
                                    "GOETTINGEN L": "GOTTINGEN L",
                                    "GOETTINGEN S": "GOTTINGEN S",
                                    "GRAFSCHAFT BENTHEIM": "BENTHEIM",
                                    "GRAFSCHAFT DIEPHOLZ (KREIS DIEPHOLZ)": "DIEPHOLZ",
                                    "GRAFSCHAFT HOYA (KREIS HOYA)": "HOYA",
                                    "GRAFSCHAFT WERNIGERODE (": "WERNIGERODE",
                                    "GRAFSCHAFT SCHAUMBURG": "SCHAUMBURG",
                                    "GRAFSCHAFT HOHENSTEIN": "HOHENSTEIN",
                                    "GREVENBROICH": "GREVENBROICH-NEUSS",
                                    "GROSS GERAU": "GROSS-GERAU",
                                    "HADELN L": "HADELN",
                                    "HAGEN S": "HAGEN",
                                    "HALLE (SAALE)  S": "HALLE (SAALE)",  # Moritz function has bug
                                    "HAMBORN  S (-31.7.29)": "DUISBURG-HAMBORN",
                                    "HAMELN S": "HAMELN",
                                    "HAMM S": "HAMM",
                                    "HARBURG-WILHELMSBURG  S (1.7.27-)": "HARBUG-WILHELMSBURG",
                                    "HERNE   S": "HERNE",
                                    "HERRSCHAFT SCHMALKALDEN  (-24 SCHMALKALD": "SCHMALKALDEN",
                                    "HINDENBURG (O.S) (1.1.27)": "HINDENBURG",
                                    "HIRSCHBERG S": "HIRSCHBERG",
                                    "HOECHSTADT (AISCH)": "HOECHSTADT AN DER AISCH",
                                    "HOEXTER": "HOXTER",
                                    "HOFHEIM (UNTERFRANKEN)": "HOFHEIM IN UNTERFRANKEN",
                                    "HUENFELD": "HUNFELD",
                                    "JUELICH": "JULICH",
                                    "JUETERBOG-LUCKENWALDE": "JUTERBOG-LUCKENWALDE",
                                    "KEMPTEN S": "KEMPTEN (ALLGAEU) S",
                                    "KIEL  S": "KIEL",
                                    "KIRCHHAIN (-30.9.32)": "KIRCHHAIN",
                                    "KISSINGEN S  (BAD)": "BAD KISSINGEN S",
                                    "KISSINGEN L": "BAD KISSINGEN L",
                                    "KOELN S": "KOLN S",  
                                    "KOELN L": "KOLN L",  
                                    "KOENIGSBERG (PR) S": "KONIGSBERG S",
                                    # "KOENIGSBERG (NEUMARK)": "KONIGSBERG S",
                                    "KOENIGSHOFEN (I.GRABFELD)": "KOENIGSHOFEN IM GRABFELD",
                                    "KOLBERG S": "KOLBERG",
                                    "KOESLIN L": "KOSLIN L",
                                    "KOESLIN S": "KOSLIN S",
                                    "KREFELD S (-31.7.29)": "KREFELD-UERDING",
                                    "LANDAU (PFALZ) S": "LANDAU IN DER PFALZ S",
                                    "LANDAU (PFALZ) L": "LANDAU IN DER PFALZ L",
                                    "LANDSBERG (WARTHE) S": "LANDSBERG S",
                                    "LAUENBURG (POMMERN)": "LAUENBURG",
                                    "LEOBSCHUETZ": "LEOBSCHUTZ",
                                    "LOHR": "LOHR AM MAIN",
                                    "LUDWIGSHAFEN (RHEIN) L": "LUDWIGSHAFEN AM RHEIN L",
                                    "LUDWIGSHAFEN (RHEIN) S": "LUDWIGSHAFEN AM RHEIN S",
                                    "LUENEBURG S": "LUNEBURG S",
                                    "LUEBBECKE": "LUBBECKE",
                                    "LUEBBEN": "LUBBEN",
                                    "LUEBECK S": "HANSESTADT LUEBECK",
                                    "LUEDINGHAUSEN": "LUDINGHAUSEN",
                                    "MAGDEBURG  S": "MAGDEBURG",
                                    "MARBURG": "MARBURG S",
                                    
                                    "MUELHEIM (RUHR)  S": "MUELHEIM (RUHR)",
                                    "MUEHLHAUSEN S": "MUHLHAUSEN S", 
                                    "MUEHLHAUSEN L": "MUHLHAUSEN L",
                                    "MUENDEN": "MUNDEN",
                                    "MUENSTER L": "MUNSTER L",
                                    "MUENSTER S": "MUNSTER S",
                                    "NAMSLAU (=NAMSLAU-REST)": "NAMSLAU",
                                    "NAUMBURG (SAALE) S": "NAUMBURG S",
                                    "NETZEKREIS": "NETZE",
                                    "NEUMARKT (OBERPFALZ) S": "NEUMARKT IN DER OBERPFALZ S",
                                    "NEUMARKT (OBERPFALZ) L": "NEUMARKT IN DER OBERPFALZ L",
                                    "NEUMUENSTER  S": "NEUMUNSTER",
                                    "NEUSS S": "NEUSS",
                                    "NEUSTADT (AISCH)": "NEUSTADT AN DER AISCH",
                                    "NEUSTADT (HARDT) L": "NEUSTADT AN DER HAARDT L",
                                    "NEUSTADT (HARDT) S": "NEUSTADT AN DER HAARDT S",
                                    "NEUSTADT (SAALE)": "NEUSTADT AN DER SAALE",
                                    "NEUSTADT (WALDNAAB)": "NEUSTADT AN DER WALDNAAB",
                                    
                                    "NORDHAUSEN  S": "NORDHAUSEN",
                                    'OBERHAUSEN  S': "OBERHAUSEN",
                                    "OBERNBURG": "OBERNBURG AM MAIN",
                                    "OELS": "OLS",
                                    "OLDENBURG (OLDENBURG) S": "OLDENBURG (OLDENBURG)",
                                    "OLDENBURG": "OLDENBURG (SCH)",
                                    "OLETZKO (-33/TREUBURG)": "OLETZKO",
                                    "OPPELN S": "OPPELN S",
                                    "OSNABRUECK S": "OSNABRUCK S", 
                                    "OSTERODE (HARZ)": "OSTERODE AM HARZ",
                                    "POTSDAM  S": "POTSDAM",
                                    "RATHENOW  S": "RATHENOW",
                                    "RHEINBACH (-30.9.32)": "RHEINBACH",
                                    "ROESSEL": "ROSSEL",
                                    "ROTHENBURG (TAUBER) S": "ROTHENBURG OB DER TAUBER S",
                                    "SCHLUECHTERN": "SCHLUCHTERN",
                                    "SCHOETMAR (VERW.-AMT)  (-31.3.32)": "SCHOETTMAR",
                                    "SCHWERIN (WARTHE)": "SCHWERIN",
                                    "SOLINGEN S": "SOLINGEN",
                                    "STADTHAGEN S (-31.3.34)": "STADTHAGEN S",
                                    "STALLUPOENEN": "STALLUPONEN",
                                    "STARGARD (POMMERN) S": "STARGARD (POMMERN)",
                                    "STETTIN  S": "STETTIN",
                                    "STOLZENAU (-30.9.32)  N.": "STOLZENAU",
                                    "STRALSUND  S": "STRALSUND",
                                    "TILSIT S": "TILSIT",
                                    "UECKERMUENDE": "UCKERMUNDE",
                                    "UELZEN": "ULZEN",
                                    "WALDENBURG (SCHLESIEN) S": "WALDENBURG S",
                                    "WATTENSCHEID  S (1.8.29-)": "WATTENSCHEID",
                                    "WEIDEN    S": "WEIDEN IN DER OBERPFALZ",
                                    "WEISSENBURG (BAYERN) L": "WEISSENBURG IN BAYERN L",
                                    "WESERMUENDE  S": "WESERMUNDE",
                                    "WIEDENBRUECK": "WIEDENBRUCK",
                                    "WIESBADEN S": "WIESBADEN",
                                    "WILHELMSHAVEN  S": "WILHELMSHAVEN",
                                    "WITTENBERGE  S": "WITTENBERG S",
                                    "ZEITZ S": "ZEITZ L",
                                    "BAMBERG S": "BAMBERG CITY",
                                }
        }
            
    elif source=="radio":
        gemeinde_dict =     {
        
            "radio_kreis": {
                                "AIBLING": "BAD AIBLING",
                                "ACHIM (-30.9.32)": "ACHIM",
                                "ADENAU (-30.9.32)": "ADENAU",
                                "ALTONA  S": "ALTONA",
                                "ALZENAU (UNTERFRANKEN)": "ALZENAU",
                                "ANGERMUENDE": "ANGERMUNDE",
                                "APOLDA  S": "APOLDA",
                                "ASCHENDORF (-3O.9.32)/A.": "ASCHENDORF",
                                "ASCHENDORF-HUEMMLING": "HUMMLING",
                                "ASCHERSLEBEN  S": "ASCHERSLEBEN",
                                "AUE     S": "AUE",
                                "BAMBERG S": "BAMBERG CITY",
                                "BERLIN-MITTE BA 1": "BERLIN",
                                "BERSENBRUECK": "BERSENBRUCK", 
                                "BEUTHEN S": "BEUTHEN",
                                "BEUTHEN-TARNOWITZ (1.1.27-)": "BEUTHEN-TARNOWITZ",
                                "BLECKEDE (-30.9.32)": "BLECKEDE",
                                "BLOMBERG S (-31.3.32)": "BLOMBERG",
                                "BLUMENTHAL (-30.9.32)": "BLUMENTHAL",
                                "BOCHOLT    S": "BOCHOLT",
                                "BOCHUM S": "BOCHUM",
                                "BOLKENHAIN (-30.9.32)": "BOLKENHAIN",
                                "BORDESHOLM (-30.9.32)": "BORDESHOLM",
                                "BOTTROP   S": "BOTTROP",
                                "BRAKE (-14.5.33)": "BRAKE L",
                                "BRANDENBURG A. H.   S": "BRANDENBURG",
                                "BREMEN S": "HANSESTADT BREMEN",
                                "BREMERHAVEN  S": "BREMERHAVEN",
                                "BREMERVOERDE": "BREMERVORDE",
                                "BUBLITZ (-30.9.32)": "BUBLITZ",
                                "BUEREN": "BUREN",
                                "BUETOW": "BUTOW",
                                "BUECKEBURG S (-31.3.34)": "BUECKEBURG S",
                                "BURG B. M.     S": "BURG",
                                "HAMBURG MIT HAFEN  S": "HANSESTADT HAMBURG",
                                "CALAU": "KALAU",
                                "CALBE": "KALBE",
                                "CAMMIN": "KAMMIN",
                                "CASTROP-RAUXEL  S (1.4.28-)": "CASTROP-RAUXEL",          
                                "CLEVE": "KLEVE",
                                "COCHEM": "KOCHEM",
                                "COESFELD": "KOESFELD",
                                "COSEL": "KOSEL",
                                "COTTBUS S": "KOTTBUS S",
                                "COTTBUS L": "KOTTBUS L",
                                "CRIMMITSCHAU  S": "CRIMMITSCHAU",
                                "CUXHAVEN  S": "CUXHAVEN",
                                "DESSAU-KOETHEN": "KOETHEN",
                                "DESSAU (-31.12.31)/DESSA": "DESSAU",
                                "DETMOLD L  (1.4.32-)": "DETMOLD",
                                "DELMENHORST L (-14.5.33)": "DELMENHORST L",
                                "DUEREN": "DUREN",
                                "DILLINGEN (DONAU) L": "DILLINGEN AN DER DONAU L",
                                "DILLINGEN (DONAU) S": "DILLINGEN AN DER DONAU S",
                                "DORTMUND S": "DORTMUND",
                                "METTMANN (-31.7.29)": "DUSSELDORF-METTMANN",
                                "DUESSELDORF S": "DUSSELDORF",
                                "DORTMUND LKR.": "DORTMUND L",  # for consistency, not necessary
                                "EBERSWALDE     S": "EBERSWALDE",
                                "ECKERNFOERDE": "ECKERNFORDE",
                                "EISLEBEN  S": "EISLEBEN",
                                "ELSFLETH (-14.5.33)": "ELSFLETH",
                                "EMDEN L (-30.9.32)": "EMDEN L",            
                                "ENNEPE-RUHRKREIS": "ENNEPE-RUHR",
                                "ERFURT L (-30.9.32)": "ERFURT L",
                                "ESCHENBACH (OBERPFALZ)": "ESCHENBACH IN DER OBERPFALZ",
                                "ESSEN S": "ESSEN",
                                "FELDBERG S (-14.1.34)": "FELDBERG",
                                "FORST (LAUSITZ)  S": "FORST",
                                "FRANKENTHAL L": "FRANKENTHAL (PFALZ) L",
                                "FRANKENTHAL S": "FRANKENTHAL (PFALZ) S",
                                "FRANKFURT   S": "FRANKFURT/MAIN",
                                "FRANKFURT (ODER)  S": "FRANKFURT/ODER", 
                                "FREITAL S": "FREITAL",
                                "FRIEDEBERG (NEUMARK)": "FRIEDEBERG",
                                "FRIEDLAND S (-14.1.34)": "FRIEDLAND", 
                                "FRIESOYTHE (-14.5.33)": "FRIESOYTHE",
                                "FRITZLAR (-30.9.32)/F.-H": "FRITZLAR",
                                "FUERSTENBERG S (-14.1.3": "FUERSTENBERG",            
                                "FULDA L": "FULDA S",  # Moritz function has bug
                                "FULDA S (1.4.27-)": "FULDA S",  # Moritz function has bug
                                "GEESTEMUENDE   (-30.9.32)": "GEESTEMUNDE",         
                                "GEILENKIRCHEN (-9.8.33)/GEILENK.-HEINSBERG": "GEILENKIRCHEN",          
                                "GELSENKIRCHEN  S": "GELSENKIRCHEN",      
                                "GEMUENDEN": "GEMUENDEN AM MAIN",
                                "GERSFELD (-30.9.32)": "GERSFELD",           
                                "GLADBACH-RHEYDT  S": "GLADBACH-RHEYDT",
                                "GLADBACH": "GLADBACH-RHEYDT",
                                "GLADBECK   S": "GLADBECK",          
                                "GLEIWITZ S": "GLEIWITZ",          
                                "GOETTINGEN L": "GOTTINGEN L",
                                "GOETTINGEN S": "GOTTINGEN S",
                                "GOERLITZ L": "GORLITZ L",
                                "GOERLITZ S": "GORLITZ S",
                                "GOLDBERG-HAYNAU (-30.9.32)": "GOLDBERG-HAINAU",
                                "GRAFSCHAFT BENTHEIM": "BENTHEIM",
                                "GRAFSCHAFT DIEPHOLZ (KREIS DIEPHOLZ)": "DIEPHOLZ",
                                "GRAFSCHAFT HOYA (KREIS HOYA)": "HOYA",
                                "GRAFSCHAFT WERNIGERODE (": "WERNIGERODE",
                                "GRAFSCHAFT SCHAUMBURG": "SCHAUMBURG",
                                "GRAFSCHAFT HOHENSTEIN": "HOHENSTEIN",
                                "GREVESMUEHLEN (-14.1.34)": "GREVESMUEHLEN",
                                "GRIESBACH": "GRIESBACH IM ROTTAL",
                                "GROSS GERAU": "GROSS-GERAU",
                                "GRUENBERG S": "GRUNBERG S",
                                "GRUENBERG L": "GRUNBERG L",
                                "GUMMERSBACH (-30.9.32)/R": "GUMMERSBACH",
                                "HADELN L": "HADELN",
                                "HAGEN L (-31.7.29)": "HADELN",             
                                "HAGEN S": "HAGEN",
                                "HALBERSTADT L (-30.9.32)": "HALBERSTADT L",         
                                "HALLE (SAALE)  S": "HALLE (SAALE)",  
                                "HALLE (WESTFALEN)": "HALLE",         
                                "HAMBORN  S (-31.7.29)": "DUISBURG-HAMBORN",
                                "HAMELN S": "HAMELN",
                                "HAMM S": "HAMM",
                                "HARBURG-WILHELMSBURG  S (1.7.27-)": "HARBUG-WILHELMSBURG",
                                "HERNE   S": "HERNE",
                                "HERRSCHAFT SCHMALKALDEN  (-24 SCHMALKALDEN)": "SCHMALKALDEN",
                                "HINDENBURG S": "HINDENBURG",
                                "HIRSCHBERG S": "HIRSCHBERG",
                                "HIRSCHBERG L": "HIRSCHBERG IM RIESENGEBIRGE", 
                                "HOECHSTADT (AISCH)": "HOECHSTADT AN DER AISCH",
                                "HOEXTER": "HOXTER",
                                "HOFHEIM (UNTERFRANKEN)": "HOFHEIM IN UNTERFRANKEN",
                                "HOMBERG (-30.9.32)": "HOMBERG", 
                                "HUENFELD": "HUNFELD",
                                "HUEMMLING (-30.9.32)": "HUMMLING",
                                "IBURG (-30.9.32)": "IBURG",
                                "ILFELD (-30.9.32)": "ILFELD",
                                "ISENHAGEN (-30.9.32)": "ISENHAGEN",
                                "JENA  S": "JENA",
                                "JEVER L (-14.5.33)": "JEVER L",
                                "JEVER S (-30.4.33)": "JEVER S",
                                "JORK (-30.9.32)": "JORK",
                                "JUELICH": "JULICH",
                                "JUETERBOG-LUCKENWALDE": "JUTERBOG-LUCKENWALDE",
                                "KEHDINGEN (-30.9.32)": "KEHDINGEN",
                                "KEMPTEN S": "KEMPTEN (ALLGAEU) S",
                                "KEMPTEN L": "KEMPTEN (ALLGAEU) L",
                                "KIEL  S": "KIEL",
                                "KIRCHHAIN (-30.9.32)": "KIRCHHAIN",
                                "KISSINGEN S  (BAD)": "BAD KISSINGEN S",
                                "KISSINGEN L": "BAD KISSINGEN L",
                                "KOELN L": "KOLN L",
                                "KOELN S": "KOLN S",
                                "KOENIGSBERG (NEUMARK)": "KONIGSBERG",
                                "KOENIGSBERG (PR) L": "KONIGSBERG L",
                                "KOENIGSBERG (PR) S": "KONIGSBERG S",
                                "KOENIGSHOFEN (I.GRABFELD)": "KOENIGSHOFEN IM GRABFELD",
                                "KOLBERG S": "KOLBERG",
                                "KOESLIN L": "KOSLIN L",
                                "KOESLIN S": "KOSLIN S",
                                "KOETHEN (-31.12.31)": "KOETHEN",
                                "KOLBERG S": "KOLBERG",
                                "KOLBERG-KOERLIN": "KOLBERG-KORLIN",
                                "KREFELD-UERDINGEN  S (RHEIN": "KREFELD-UERDING",
                                "KRUMBACH": "KRUMBACH (SCHWABEN)",
                                "LANDAU (PFALZ) S": "LANDAU IN DER PFALZ S",
                                "LANDAU (PFALZ) L": "LANDAU IN DER PFALZ L",
                                "LANDAU A.D.ISAR": "LANDAU AN DER ISAR",
                                "LAUENBURG (POMMERN)": "LAUENBURG",
                                "LEOBSCHUETZ": "LEOBSCHUTZ",
                                "LINDEN (-30.9.32)": "LINDEN",
                                "LIPPERODE-CAPPEL A (-31.3.28)": "LIPPERODE-CAPPEL",
                                "LOETZEN": "LOTZEN",
                                "LOEWENBERG": "LOWENBERG",
                                "LOHR": "LOHR AM MAIN",
                                "LUDWIGSHAFEN (RHEIN) L": "LUDWIGSHAFEN AM RHEIN L",
                                "LUDWIGSHAFEN (RHEIN) S": "LUDWIGSHAFEN AM RHEIN S",
                                "LUENEBURG S": "LUNEBURG S",
                                "LUENEBURG L": "LUNEBURG L",
                                "LUEBBECKE": "LUBBECKE",
                                "LUEBEN": "LUBEN",
                                "LUEBBEN": "LUBBEN",
                                "LUEBECK S": "HANSESTADT LUEBECK",
                                "LUECHOW (-30.9.32)": "LUCHOW",
                                "LUEDENSCHEID  S": "LUDENSCHEID",
                                "LUEDINGHAUSEN": "LUDINGHAUSEN",
                                "LUENEBURG L": "LUNEBURG L",
                                "LUENEBURG S": "LUNEBURG S",
                                "LUENEN  S (1.4.28-)": "LUNEN",
                                "MAGDEBURG  S": "MAGDEBURG",
                                "MAIN-TAUNUSKREIS (1.4.28": "MAIN-TAUNUS-KREIS",
                                "MANSFELDER GEBIRGSKREIS": "MANSFELDER GEBIRGSKR",
                                "MARBURG S (1.4.29-)": "MARBURG S",
                                "MARIENBURG (WESTPR.)": "MARIENBURG (DAN)",
                                "MARIENBURG I. HANN.": "MARIENBURG (HIL)",
                                "MARKT OBERDORF": "MARKTOBERDORF",
                                "MARKTREDWITZ  S": "MARKTREDWITZ",
                                "MEERANE    S": "MEERANE",
                                "MEISENHEIM (-30.9.32)": "MEISENHEIM",
                                "MERZIG-WADERN (REST) (1920  MERZIG)": "MERZIG-WADERN",
                                "METTMANN (-31.7.29)": "DUSSELDORF-METTMANN",
                                "MIROW S (-14.1.34)": "MIROW",
                                "MITTWEIDA S": "MITTWEIDA",
                                "MUEHLDORF": "MUEHLDORF AM  INN",
                                "MUEHLHAUSEN S": "MUHLHAUSEN S", 
                                "MUEHLHAUSEN L": "MUHLHAUSEN L",
                                "MUELHEIM (RHEIN) (-30.9.": "MULHEIM",
                                "MUELHEIM (RUHR)  S": "MUELHEIM (RUHR)",
                                "MUENDEN": "MUNDEN",
                                "MUENSTER L": "MUNSTER L",
                                "MUENSTER S": "MUNSTER S",
                                "MUENSTERBERG (-30.9.32)": "MUNSTERBERG",
                                "NAMSLAU (=NAMSLAU-REST)": "NAMSLAU",
                                "NAUMBURG (SAALE) S": "NAUMBURG S",
                                "NAUMBURG (SAALE) L (-30.": "NAUMBURG L",
                                "NETZEKREIS": "NETZE",
                                "NEUBRANDENBURG  S": "NEUBRANDENBURG",
                                "NEUBURG (DONAU) L": "NEUBURG AN DER DONAU L",
                                "NEUBURG (DONAU) S": "NEUBURG AN DER DONAU S",
                                "NEUHAUS A. D. OSTE": "NEUHAUS",
                                "NEUMARKT (SCHLESIEN)": "NEUMARKT",
                                "NEUMARKT (OBERPFALZ) S": "NEUMARKT IN DER OBERPFALZ S",
                                "NEUMARKT (OBERPFALZ) L": "NEUMARKT IN DER OBERPFALZ L",
                                "NEUMUENSTER  S": "NEUMUNSTER",
                                "NEUNBURG (V.WALD)": "NEUNBURG VORM WALD",
                                "NEURODE (-30.9.32)": "NEURODE",
                                "NEUSS S": "NEUSS",
                                "NEUSTADT (AISCH)": "NEUSTADT AN DER AISCH",
                                "NEUSTADT (B.COBURG)  S": "NEUSTADT BEI COBURG",
                                "NEUSTADT (HARDT) L": "NEUSTADT AN DER HAARDT L",
                                "NEUSTADT (HARDT) S": "NEUSTADT AN DER HAARDT S",
                                "NEUSTADT (O.S)": "NEUSTADT (OPP)",
                                "NEUSTADT (A. RUEBENBERGE)": "NEUSTADT (HAN)",
                                "NEUSTADT (SAALE)": "NEUSTADT AN DER SAALE",
                                "NEUSTADT (WALDNAAB)": "NEUSTADT AN DER WALDNAAB",
                                "NEUSTRELITZ S": "STRELITZ S",
                                "NIMPTSCH (-30.9.32)": "NIMPTSCH",
                                "NORDHAUSEN  S": "NORDHAUSEN",
                                'OBERHAUSEN  S': "OBERHAUSEN",
                                "OBERNBURG": "OBERNBURG AM MAIN",
                                "OELS": "OLS",
                                "OLDENBURG (OLDENBURG) S": "OLDENBURG (OLDENBURG)",
                                "OLDENBURG (OLDENBURG) L": "OLDENBURG L",
                                "OLDENBURG": "OLDENBURG (SCH)",
                                "OLETZKO (-33/TREUBURG)": "OLETZKO",
                                "OSTERODE (HARZ)": "OSTERODE AM HARZ",
                                "OSTERODE I. OSTPR.": "OSTERODE",
                                "OSNABRUECK L": "OSNABRUCK L",
                                "OSNABRUECK S": "OSNABRUCK S",
                                "PFAFFENHOFEN A.D.ILM": "PFAFFENHOFEN AN DER ILM",
                                "PLOEN": "PLON",
                                "POTSDAM  S": "POTSDAM",
                                "PRUEM": "PRUM",
                                "RATHENOW  S": "RATHENOW",
                                "REICHENBACH   S": "REICHENBACH",
                                "REICHENBACH": "REICHENBACH (EULENGEBIRGE)",
                                "REMSCHEID  S": "REMSCHEID",
                                "RHEIN-WUPPER-KREIS (=SOLINGEN-LENNEP)": "SOLINGEN-LENNEP",
                                "RHEYDT  S": "GLADBACH-RHEYDT",
                                "RHEINBACH (-30.9.32)": "RHEINBACH",
                                "RIESA S": "RIESA",
                                "RODACH (B.COBURG)  S": "RODACH BEI COBURG",
                                "ROESSEL": "ROSSEL",
                                "ROSENHEIM  L": "ROSENHEIM L",
                                "ROTHENBURG (TAUBER) S": "ROTHENBURG OB DER TAUBER S",
                                "ROTHENBURG (TAUBER) L": "ROTHENBURG OB DER TAUBER L",
                                "RUEGEN": "RUGEN",
                                "RUESTRINGEN  S": "RUESTRINGEN",
                                "SAGAN (-30.9.32)": "SAGAN",
                                "SCHIVELBEIN (-30.9.32)": "SCHIVELBEIN",
                                "SCHLUECHTERN": "SCHLUCHTERN",
                                "SCHNEIDEMUEHL  S": "SCHNEIDEMUHL",
                                "SCHOENAU (-30.9.32)": "SCHONAU",
                                "SCHOENBERG S (-14.1.34)": "SCHOENBERG S",
                                "SCHOETMAR (VERW.-AMT)  (-31.3.32)": "SCHOETTMAR",
                                "SCHWANDORF (BAYERN)  S": "SCHWANDORF",
                                "SCHWERIN (WARTHE)": "SCHWERIN",
                                "SELB  S": "SELB",
                                "SOLINGEN S": "SOLINGEN",
                                "SPREMBERG (LAUSITZ)": "SPREMBERG",
                                "ST WENDEL-BAUMHOLDER (1930- \"(REST)\")": "ST. WENDEL-BAUMHOLDER",
                                "STARGARD S (-14.1.34)": "STARGARD (POMMERN)",
                                "STADTHAGEN S (-31.3.34)": "STADTHAGEN S",
                                "STALLUPOENEN": "STALLUPONEN",
                                "STEINAU (-30.9.32)": "STEINAU",
                                "STETTIN  S": "STETTIN",
                                "STOLZENAU (-30.9.32)  N.": "STOLZENAU",
                                "STRELITZ L (-14.1.34)": "STRELITZ L",
                                "STRELITZ S (-30.9.31)": "STRELITZ S",
                                "STRIEGAU (-30.9.32)": "STRIEGAU",
                                "STRALSUND  S": "STRALSUND",
                                "SUED TONDERN": "SUDTONDERN",
                                "SUEDERDITHMARSCHEN": "SUDERDITHMARSCHEN",
                                "SULINGEN (-30.9.32)": "SULINGEN",
                                "SYKE (-30.9.32)": "SYKE",
                                "TEUSCHNITZ (-31.5.31)": "TEUSCHNITZ",
                                "TILSIT S": "TILSIT",
                                "TILSIT  L": "TILSIT",
                                "UECKERMUENDE": "UCKERMUNDE",
                                "UELZEN": "ULZEN",
                                "UNNA (-16.10.30 HAMM L)": "UNNA",
                                "USLAR (-30.9.32)": "USLAR",
                                "VAIHINGEN (1928- VAHINGEN-ENZ)": "VAIHINGEN",
                                "VAREL L (-14.5.33)": "VAREL L",
                                "VAREL S (-14.5.33)": "VAREL S",
                                "VIERSEN    S": "VIERSEN",
                                "WALDBROEL (-30.9.32)": "WALDBROL",
                                "WALDENBURG (SCHLESIEN) S": "WALDENBURG S",
                                "WALDENBURG (SCHLESIEN) L": "WALDENBURG L",
                                "WANDSBEK  S": "WANDSBEK",
                                "WANNE-EICKEL  S": "WANNE-EICKEL",
                                "WASSERBURG (INN)": "WASSERBURG AM INN",
                                "WATTENSCHEID  S (1.8.29-)": "WATTENSCHEID",
                                "WEIDEN    S": "WEIDEN IN DER OBERPFALZ",
                                "WEISSENBURG (BAYERN) L": "WEISSENBURG IN BAYERN L",
                                "WEISSENBURG (BAYERN) S": "WEISSENBURG IN BAYERN S",
                                "WERDAU L (-28.2.33)": "WERDAU L",
                                "WESENBERG S (-14.1.34)": "WESENBERG S",
                                "WESENBERG S": "WESENBERG",
                                "WESERMUENDE  S": "WESERMUNDE",
                                "WESTERBURG (-30.9.32)": "WESTERBURG",
                                "WESTERSTEDE (-14.5.33)": "WESTERSTEDE",
                                "WIEDENBRUECK": "WIEDENBRUCK",
                                "WIESBADEN S": "WIESBADEN",
                                "WILDESHAUSEN (-14.5.33)": "WILDESHAUSEN",
                                "WILHELMSHAVEN  S": "WILHELMSHAVEN",
                                "WINSEN (-30.9.32)": "WINSEN",
                                "WIPPERFUERTH (-30.9.32)": "WIPPERFURTH",
                                "WITTEN  S": "WITTEN",
                                "WITTENBERG L": "WITTENBERG",
                                "WITTENBERGE  S": "WITTENBERGE",
                                "WOLDEGK S (-14.1.34)": "WOLDEGK",
                                "WUPPERTAL  S": "WUPPERTAL",
                                "WURZEN  S": "WURZEN",
                                "ZELLA-MEHLIS  S": "ZELLA-MEHLIS",
                                "ZEVEN (-30.9.32)": "ZEVEN",
                                "ZIEGENRUECK": "ZIEGENRUCK",
                                "ZUELLICHAU-SCHWIEBUS": "ZULLICHAU-SCHWIEBUS",
                                "HARBURG L": "HARBURG"
                                
                            }
                        }
    else:
        raise Exception("Specified data source, {}, is incorrect.".format(source))
    
    return gemeinde_dict

###############################################################################
"""Functions to simplify crosswalk formation."""


def import_data(base_path, files):
    """ Import map data and source data.
    
    Args:
        base_path (str): This is a raw string of the base path. Should be 
            consistent across crosswalks.
        files (str or dict of str): If the data source is one file, then only
            specify a raw string. If multiple files are imported, make a 
            dictionary. 
            
            Example:
                files = {
                    source_data1: r"1_Data\some_data_source.dta",
                    source_data2: r"1_Data\another_data_source.csv"}

    """
    map_data = pd.read_csv(os.path.join(base_path, r"1_Data\admin_units_1930_adjusted.csv"))
    if type(files) is str:
        if files[-3:]=="csv":
            source_data = pd.read_csv(os.path.join(base_path, files))
        elif files[-3:]=="dta":
            source_data = pd.read_stata(os.path.join(base_path, files))
        else:
            raise Exception("File extension unacceptable. Only .dta and .csv.")
    
    elif type(files) is dict:
        source_data = {}
        for i, data in enumerate(files):
            if files[data][-3:]=="csv":
                source_data["source_data_{}".format(i)] = pd.read_csv(os.path.join(base_path, files[data]))
            elif files[data][-3:]=="dta":
                source_data["source_data_{}".format(i)] = pd.read_stata(os.path.join(base_path, files[data]))
            else:
                raise Exception("File extension unacceptable. Only .dta and .csv.")
    
    return source_data, map_data