# -*- coding: utf-8 -*-
"""
Quick architecture for cleaning postwar data
"""
#If the gemeinde error ever appears,
#it is the csv/excel file most likely, in particular, spacing

import os


import numpy as np
import pandas as pd

#importing functions from utils_00 file
from utils_00 import(
    fix_encoding_bug,
    umlaut_rem,
    import_func,
    hyphen_rem,
    a_rem,
    rem_whitespace,
    col_rem,
    merge_func,
    apply_to_dict,
    rename_cols,
    drop_empty_rows,
    rm_numbers
    )

input_base_path= r"C:\Users\Jrxz12\Dropbox\Germany_state\1_Data\prewar"

#Get a list of all files in the prewar diretory
#creating the list of files using the os utility package.
list_of_files = os.listdir(os.path.join(input_base_path, "prewar_dig"))

dict_new_names= {
    "Bielefel":"Bielefeld",
    "Bochun":"Bochum",
    "Botrop":"Bottrop",
    "Brandenburh":"Brandenburg",
    "Bremen":"HANSESTADT BREMEN",
    "Castr.-Rauxel":"Castrop-Rauxel",
    "Chenitz":"Chemnitz",
    "Duesselldorf":"Duesseldorf",
    "Frankfurt/M-":"Frankfurt/M",
    "Frankfurt/O":"Frankfurt_Oder",
    "Frankfurt/O-":"Frankfurt_Oder",
    "Freiberg":"Freiburg",
    "Gelsekirchen":"Gelsenkirchen",
    "Gelsenk--Buer-":"Gelsenkirchen",
    "Gruenbg./S.":"Gruenberg",
    "Halberstadt":"Halberstaedt",
    "Harb-Wilhelmsb-":"Wilhelmsburg",
    "Harb.-Wilhelmsbg.":"Wilhelmsburg",
    "Harb.-Wilhelmsbg":"Wilhelmsburg",
    "Harb.-Wilhlbg.":"Wilhelmsburg",
    "Harb.-Wilhelmsburg":"Wilhelmsburg",
    "Harb.-Wilhbg":"Wilhelmsburg",
    "Hirschbg.i.R.":"Hirschberg",
    "Harb.Wilhelmsb":"Wilhelmsburg",
    "Harbg-Wilhelmsbg":"Wilhelmsburg",
    "Hrbg.-Wilhbg":"Wilhelmsburg",
    "Harbg.-Wilhbg":"Wilhelmsburg",
    "Harb.-Wilhelmsb.":"Wilhelmsburg",
    "Heilbron":"Heilbronn",
    "Hildescheim":"Hildeseim",
    "Hildesheim":"Hildeseim",
    "Hindernburg":"Hindenburg",
    "Insterberg":"Insterburg",
    "Iserholn":"Iserlohn",
    "Kamp-Lintf":"Kamp-Lintfort",
    "Kref.-Uerdgb":"Krefeld-Uerdingen",
    "Kref.-Uerdg":"Krefeld-Uerdingen",
    "Kref.-Uerdingen":"Krefeld-Uerdingen",
    "M--Gladbach":"Gladbach-Rheydt",
    "Gldb.-Rheydtb":"Gladbach-Rheydt",
    "Magdenburg":"Magdeburg",
    "Mersburg":"Meersburg",
    "Merseburg":"Meersburg",
    "Muelhausen/Th":"Muehlhausen/Th",
    "Naumbg.a.S.":"Naumberg",
    "Oberhause":"Oberhausenb",
    "Oberhausen":"Oberhausenb",
    "Oddenbach":"Offenbach",
    "Ofenbach":"Offenbach",
    "Pforzeim":"Pforzheim",
    "Pforzhelm":"Pforzheim",
    "Postdam":"Potsdam",
    "Recklinghaus":"Recklinghausen",
    "Recklinghs":"Recklinghausen",
    "Reichenb./V":"Reichenbach",
    "Schneidem":"Schneidemuehl",
    "Stargrd/P":"Stargard",
    "Stolp/Pom":"Stolp",
    "Straslung":"Stralsund",
    "Trief":"Trier",
    "Wanne-Eiekel":"Wanne-Eickel",
    "WanneâEickel":"Wanne-Eickel",
    "Wilhelmshv":"Wilhelmshaven",
    "Wuppertalb":"Wuppertal",
    "Duisb.-Hambb":"Duisburg-Hamborn",
    "Duisburg":"Duisburg-Hamborn",
    "Rheydt":"Gladbach-Rheydt",
    "Muchen":"Muenchen",
    "Hamborn":"Duisburg-Hamborn",
    "M.-Gladbach":"Gladbach-Rheydt",
    "Aschaffenbg":"Aschaffenburg",
    "Braunschw.":"Braunschweig",
    "Bg.Gladb.":"Gladbach-Rheydt",
    "Castop-Rauxel":"Castrop-Rauxel",
    "Frankfurt/M.":"Frankfurt/M",
    "Frankfurt/O.":"Frankfurt_Oder",
    "bElberfelt":"Elberfeld",
    "bHamborn": "Duisburg-Hamborn",
    "bSterkrade":"Sterkrade",
    "Aaschen":"Aachen",
    "B.Godesbg.":"Bad Godesberg",
    "Hrbg.-Wilhbg.":"Wilhelmsburg",
    }



# Import all indivdual datasets. Remember, give spyder time for any updates
# made outside spyder.
# This uses the import_func created from utils_00
dict_of_dfs_import = {
    x: import_func(os.path.join(input_base_path, "prewar_dig", x))
    for x in list_of_files
}

immigration_columns = [
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

def _cleaning_missing(variable_name):
    """ For converting '.' to np.nan, then
    object to to_numeric
    """
    new_var = variable_name.replace(".", np.nan)
    new_var = pd.to_numeric(new_var)
    return new_var

def _comma_to_dot(variable_name):
    """ For converting ',' to '.', then
    object to to_numeric
    """
    new_var = variable_name.str.replace(",", ".")
    new_var = pd.to_numeric(new_var)
    return new_var

def _dash_to_nan(variable_name):
    """ For converting ',' to '.', then
    object to to_numeric
    """
    new_var = variable_name.replace("-", np.nan)
    new_var = pd.to_numeric(new_var)
    return new_var

a= '1937_immigration_real.csv'
for column in immigration_columns:
    dict_of_dfs_import[a][column] = (
            _cleaning_missing(dict_of_dfs_import[a][column])
            )

nonlocal_columns = [
    'deaths_local_p1000',
    'foreign_deaths_p1000',
    'local_deaths_1yearp100',
    'nonlocal_deaths_1yearp100'
    ]

b='1931_nonlocal_localstuff.csv'
for column in nonlocal_columns:
    dict_of_dfs_import[b][column] = (
            _comma_to_dot(dict_of_dfs_import[b][column])
            )

#    dict_of_dfs_import[b][column] = (
#       pd.to_numeric(dict_of_dfs_import[b][column]
#       .str.replace(",","."))
#       )


c= '1929_death_summary_foreign.csv'
dict_of_dfs_import[c]['tot_foreign_baby_deaths']= (
        pd.to_numeric(dict_of_dfs_import[c]['tot_foreign_baby_deaths']
        .replace("-",np.nan))
        )
dict_of_dfs_import[c]['tot_foreign_deaths_percent']= (
        pd.to_numeric(dict_of_dfs_import[c]['tot_foreign_deaths_percent']
        .str.replace(",",".")
        .replace("-",np.nan))
        )

d= '1929_education_training_pc.csv'
dict_of_dfs_import[d]['exp_education_training_pc']= (
        pd.to_numeric(dict_of_dfs_import[d]['exp_education_training_pc']
        .str.replace(",","."))
        )

e= '1929_marriage_birth_summary_foreign.csv'
f= 'total_livebirths_foreigners'
dict_of_dfs_import[e][f]= (
        pd.to_numeric(dict_of_dfs_import[e][f])
        )

g= 'total_livebirths_foreigners_percent'
dict_of_dfs_import[e][g]= (
        pd.to_numeric(dict_of_dfs_import[e][g]
        .str.replace(",","."))
        )
dict_of_dfs_import[e]['tot_stillborns_foreigners']= (
        pd.to_numeric(dict_of_dfs_import[e]['tot_stillborns_foreigners']
        .replace("-",np.nan))
        )

h= 'tot_stillborns_foreigners_percent'
dict_of_dfs_import[e][h]= (
        pd.to_numeric(dict_of_dfs_import[e][h]
        .str.replace(",",".")
        .replace("-",np.nan))
        )
i= '1930_population.csv'
dict_of_dfs_import[i]['population1930']= (
        pd.to_numeric(dict_of_dfs_import[i]['population1930']
         .str.replace(",","."))
        )

j= '1931_accomodation.csv'
dict_of_dfs_import[j]['accomodated_persons_atlarge']= (
        pd.to_numeric(dict_of_dfs_import[j]['accomodated_persons_atlarge']
        .replace(".",np.nan))
        )

k= '1931_accomodation.csv'
dict_of_dfs_import[k]['accomodated_minors']= (
        pd.to_numeric(dict_of_dfs_import[k]['accomodated_minors']
        .replace("-",np.nan))
        )
war_col= [
    'war_dependents',
    'war_dep_percent'
    ]

l= '1931_benefit_receivers.csv'
for column in war_col:
    dict_of_dfs_import[l][column] = (
            pd.to_numeric(dict_of_dfs_import[l][column]
            .replace("-",np.nan))
            )
war_column2 = [
        'exp_war_dependents',
        'exp_war_dependents_percent',
        'exp_socialpensioners',
        'exp_socialpensioners_percent',
        'exp_smallpensioners',
        'exp_smallpensioners_percent',
        'exp_otherbenefit receivers',
        'exp_otherbenefit receivers_percent',
        'exp_weekly_care',
        'exp_weekly_care_percent'
        ]

t= '1931_benefit_receivers_exp.csv'
for column in war_column2:
    dict_of_dfs_import[t][column] = (
            pd.to_numeric(dict_of_dfs_import[t][column]
            .replace("-",np.nan))
            )

u= '1931_expenditure_youthaid.csv'
dict_of_dfs_import[u]['exp_nursing'] = (
        pd.to_numeric(dict_of_dfs_import[u]['exp_nursing']
        .replace("-",np.nan))
        )

Beamte_str_columns = [
        'Lifetime_Beamte',
        'Part_time_Beamte',
        'Fireable_Beamte',
        'scientific_beamte',
        'angestellte_pension',
        'angestellte_Nopension',
        'trainee_beamte',
        'tot_Beamte'
        ]

for column in Beamte_str_columns:
    dict_of_dfs_import['1929_Beamte_a.csv'][column] = (
            pd.to_numeric(dict_of_dfs_import['1929_Beamte_a.csv'][column]
            .replace("-", np.nan))
            )

    dict_of_dfs_import['1929_Beamte_b.csv'][column] = (
            pd.to_numeric(dict_of_dfs_import['1929_Beamte_b.csv'][column]
            .replace("-", np.nan))
            )

dict_of_dfs_import['1929_Beamte_b.csv']['gemeinde_back_up'] = (
        dict_of_dfs_import['1929_Beamte_b.csv']['Gemeinde']
        .replace('b', np.nan)
        .ffill()
        )

condition_a = dict_of_dfs_import['1929_Beamte_b.csv']['Gemeinde'].str.len()>1
dict_of_dfs_import['1929_Beamte_a.csv'] = (
        dict_of_dfs_import['1929_Beamte_b.csv'][condition_a]
        .drop('gemeinde_back_up', axis=1)
        )

condition_b = dict_of_dfs_import['1929_Beamte_b.csv']['Gemeinde'].str.len()==1

dict_of_dfs_import['1929_Beamte_b.csv']= (
        dict_of_dfs_import['1929_Beamte_b.csv'][condition_b]
        .drop('Gemeinde', axis=1)
        .rename(columns={'gemeinde_back_up': 'Gemeinde'})
        )


#When taking the sum over SPECIFIC columns, a list must be made in order to
#take the appropriate row sum. The row sum will skip over strings naturally.
columns_beamte_a =[
        'Lifetime_Beamte',
        'Part_time_Beamte',
        ]

columns_beamte_b =[
        'Lifetime_Beamte',
        'Part_time_Beamte',
        ]

dict_of_dfs_import['1929_Beamte_a.csv']['Total_beamte_a']= (
        dict_of_dfs_import['1929_Beamte_a.csv'][columns_beamte_a]
        .sum(axis=1, skipna=True)
        )

dict_of_dfs_import['1929_Beamte_b.csv']['Total_beamte_b']= (
        dict_of_dfs_import['1929_Beamte_b.csv'][columns_beamte_b]
        .sum(axis=1, skipna=True)
        )



dict_of_dfs_import['1929_Beamte_a.csv']= (
        dict_of_dfs_import['1929_Beamte_a.csv']
        .rename(columns={
                "Lifetime_Beamte":"Lifetime_Beamte_a",
                "Part_time_Beamte":"Part_time_Beamte_a",
                "Fireable_Beamte":"Fireable_Beamte_a",
                "scientific_beamte":"scientific_beamte_a",
                'angestellte_pension':'angestellte_pension_a',
                'angestellte_Nopension':'angestellte_Nopension_a',
                "trainee_beamte":"trainee_beamte_a",
                "tot_Beamte":"tot_empl_a"
                })
        )

dict_of_dfs_import['1929_Beamte_b.csv']= (
        dict_of_dfs_import['1929_Beamte_b.csv']
        .rename(columns={
                "Lifetime_Beamte":"Lifetime_Beamte_b",
                "Part_time_Beamte":"Part_time_Beamte_b",
                "Fireable_Beamte":"Fireable_Beamte_b",
                "scientific_beamte":"scientific_beamte_b",
                'angestellte_pension':'angestellte_pension_b',
                'angestellte_Nopension':'angestellte_Nopension_b',
                'trainee_beamte':'trainee_beamte_b',
                "tot_Beamte":"tot_empl_b"
                })
        )

#drop irrelevant column names (sometimes, empty columns are imported)
dict_of_dfs_col= {
        x: dict_of_dfs_import[x]
        .drop(columns = [
        x for x in list(dict_of_dfs_import[x].columns) if "Unnamed" in x ])
        for x in dict_of_dfs_import.keys()
        }

#Drop unnecessary rows
_dict_of_dfs_prelim= {
        x: drop_empty_rows(rename_cols(dict_of_dfs_col[x]))
        for x in dict_of_dfs_import.keys()
}

#Try to remove all hyphen values
dict_of_dfs_prelim = {
         x: _dict_of_dfs_prelim[x]
        .replace("-",np.nan)
        .replace(",",".") for x in _dict_of_dfs_prelim.keys()
}


# Make some name changes to the Gemeinde names
for x in list(dict_of_dfs_prelim.keys()):
    print(x)
    dict_of_dfs_prelim[x]["Gemeinde"] = (
        dict_of_dfs_prelim[x]["Gemeinde"]
        .map(lambda y: rm_numbers(y))
        .map(lambda y: fix_encoding_bug(y))
        .map(lambda y: a_rem(y))
        .map(lambda y: rem_whitespace(y))
        .map(lambda y: umlaut_rem(y))
        .map(lambda y: y.replace("*","")
        )
    )
columns_emp_exp= list(dict_of_dfs_prelim['1929_employment_1.csv'].columns)
columns_emp_not= [
               "index",
               "Gemeinde",
               "level_0",
               "tot_empl",
               "tot_female_empl"
               ]
columns_emp_to_process= list(set(columns_emp_exp) - set(columns_emp_not))
for column in columns_emp_to_process:
    dict_of_dfs_prelim['1929_employment_1.csv'][column] = (
            pd.to_numeric(
            dict_of_dfs_prelim['1929_employment_1.csv'][column]
            )
    )

dict_of_dfs_prelim['1929_employment_1.csv']['tot_female_empl']= (
        dict_of_dfs_prelim['1929_employment_1.csv']['tot_female_empl']
        .replace("-",np.nan)
        )


dict_of_dfs_prelim['1929_employment_1.csv']= (
        dict_of_dfs_prelim['1929_employment_1.csv']
        .drop("tot_female_empl", axis=1)
        )
nazi_exp = [
        'elementary_exp_pc',
        'secondary_exp_pc',
        'gen_man_tax_finance_exp_pc',
        'police_exp_pc',
        'school_admin_exp_pc',
        'infrastructure_exp_pc',
        'welfare_exp_pc',
        'health_exp_pc'
        ]

v= '1936_local_expenditures.csv'
for column in nazi_exp:
    dict_of_dfs_prelim[v][column]= (
            pd.to_numeric(dict_of_dfs_prelim[v][column]
            .str.replace(",","."))
            )



#These are the employee categories
empl_columns = [
        "Police_admin",
        "School_admin",
        'civil_engineering_man',
        "fleet_management",
        "park_garden_man",
        "fire_management",
        "other_education_officials",
        ]
w = '1929_employment_nominal.csv'
for column in empl_columns:
    dict_of_dfs_prelim[w][column] = (
            pd.to_numeric(dict_of_dfs_prelim[w][column]))

x= '1929_health_welfare_exp_pc.csv'
dict_of_dfs_prelim[x]['exp_health_pc']= (
        pd.to_numeric(
                dict_of_dfs_prelim[x]['exp_health_pc']
                .str.replace(",","."))
        )


dict_of_dfs_prelim[x]['exp_welfare_pc']= (
        pd.to_numeric(
                dict_of_dfs_prelim[x]['exp_welfare_pc']
                .str.replace(",","."))
        )

y= '1929_general_and_infrastructure__exp_pc.csv'
dict_of_dfs_prelim[y]['General_admin_exp_pc']= (
        pd.to_numeric(
                dict_of_dfs_prelim[y]['General_admin_exp_pc']
                .str.replace(",","."))
        )

dict_of_dfs_prelim[y]['infrastructure_exp_pc']= (
        pd.to_numeric(
                dict_of_dfs_prelim[y]['infrastructure_exp_pc']
                .str.replace(",","."))
        )

dict_of_dfs_prelim['1929_exp_pc_alot.csv']= (
        dict_of_dfs_prelim['1929_exp_pc_alot.csv']
        .drop(["exp_cemeteries_funeral_services_pc",
               "exp_cemeteries_funeral_services_1000RM",
               'exp_property_management_1000RM',
               'exp_property_management_pc'],
        axis=1)
        )

columns_exp= list(dict_of_dfs_prelim['1929_exp_pc_alot.csv'].columns)
columns_not= [
        "index",
        "Gemeinde",
        "level_0",
        "exp_trade_schools_1000RM",
        "exp_primary_education_1000RM",
        "exp_welfare_including_youth_1000RM",
        "exp_youth_wellbeing_1000RM"
        ]

columns_to_process = list(set(columns_exp) - set(columns_not))


for column in columns_to_process:
    dict_of_dfs_prelim['1929_exp_pc_alot.csv'][column] = (
            dict_of_dfs_prelim['1929_exp_pc_alot.csv'][column]
            .str
            .replace("-","999999")
            )

    dict_of_dfs_prelim['1929_exp_pc_alot.csv'][column]= (
            pd.to_numeric(dict_of_dfs_prelim['1929_exp_pc_alot.csv'][column]
            .str
            .replace(",","."))
            )

    dict_of_dfs_prelim['1929_exp_pc_alot.csv'][column]= (
            dict_of_dfs_prelim['1929_exp_pc_alot.csv'][column]
            .replace(999999,np.NaN)
            )
aa= '1937_population.csv'
dict_of_dfs_prelim[aa]['pop_1933_1000s']= (
        pd.to_numeric(
                dict_of_dfs_prelim[aa]['pop_residential_june_1933']
                .str.replace(",","."))
        )
# Apply the renaming dict
for files in list(dict_of_dfs_prelim.keys()):
    dict_of_dfs_prelim[files]= (
            dict_of_dfs_prelim[files]
            .replace({"Gemeinde": dict_new_names})
            )

#We rename one column due to csv delimiter issues (line 349)
bb= '1937_national_tax.csv'
dict_of_dfs_prelim[bb]["income_tax_pc"]= (
        pd.to_numeric(dict_of_dfs_prelim[bb]["income_tax_pc"]
        .str.replace(",","."))
        )

cc= '1937_local_tax_categories_2_pc.csv'
dict_of_dfs_prelim[cc]= (
        dict_of_dfs_prelim[cc]
        .rename(columns={"local_tax_pc,,,,,,,,,,":"local_tax_pc"})
        )

dict_of_dfs_prelim[cc]["local_tax_pc"]= (
        pd.to_numeric(
                dict_of_dfs_prelim[cc]["local_tax_pc"]
                .str[:-1]
                .str.replace(",,,,,,,,,","9999")
                .str.replace(",","."))
                .replace(9999,np.NaN)
        )
dict_of_dfs_prelim['1931_population.csv']['pop_residential_june_1933']= (
        pd.to_numeric(
        dict_of_dfs_prelim['1931_population.csv']['pop_residential_june_1933']
        .str.replace(",","."))
        )*1000


tax_columns= [
        'land_and_building_tax',
        'business_tax',
        'wealth_transfer_tax'
        ]

for column in tax_columns:
    dict_of_dfs_prelim[cc][column]= (
        pd.to_numeric(dict_of_dfs_prelim[cc][column]
        .str.replace(",","."))
        )

dd= '1937_local_tax_2_nominalz.csv'
dict_of_dfs_prelim[dd]["wealth_transfer_tax_nominal"]= (
        pd.to_numeric(
                dict_of_dfs_prelim[dd]["wealth_transfer_tax_nominal"]
                .str.replace("-","9999"))
                .replace(9999,np.NaN)
        )


ee= '1937_taxable_income_versus_collected.csv'
dict_of_dfs_prelim[ee]["income_taxes_collected_pc"] = (
        pd.to_numeric(dict_of_dfs_prelim[ee]["income_taxes_collected_pc"]
        .str.replace(",","."))
        )

dict_of_dfs_prelim[ee]= (
        dict_of_dfs_prelim[ee]
        .rename(columns= {
                "taxable_income_thousands_nazi_pc":"taxable_income_nazi_pc"})
        )

tot_tax_columns= ['percent_tot_tax_exempt','tot_tax_exempt']

ff= '1931_amount_of_people_taxed_untaxed_exempted.csv'
for column in tot_tax_columns:
    dict_of_dfs_prelim[ff][column]= (
        pd.to_numeric(
                dict_of_dfs_prelim[ff][column]
                .str.replace("-","9999")
                .str.replace(",","."))
                .replace(9999,np.NaN)
        )

tot_tax_col_2= ['percent_tot_taxed','percent_tot_untaxed']
for column in tot_tax_col_2:
    dict_of_dfs_prelim[ff][column]= (
        pd.to_numeric(dict_of_dfs_prelim[ff][column]
        .str.replace(",","."))
        )

gg= '1929_police_construction.csv'
dict_of_dfs_prelim[gg]['tot_exp_police_pc']= (
        pd.to_numeric(dict_of_dfs_prelim[gg]['tot_exp_police_pc']
        .str.replace(",","."))
        )

hh= '1929_facilities_expense_pc.csv'
dict_of_dfs_prelim[hh]['exp_healthcare_1000RM']= (
        pd.to_numeric(dict_of_dfs_prelim[hh]['exp_healthcare_1000RM'])
        )

ii= '1937_population.csv'
dict_of_dfs_prelim[ii]['pop_residential_jan_1937']= (
        pd.to_numeric(dict_of_dfs_prelim[ii]['pop_residential_jan_1937']
        .str.replace(",","."))
        )
#Aggreagte to the Gemeinde Level


dict_of_dfs= {
        x:dict_of_dfs_prelim[x]
        .groupby("Gemeinde")
        .sum(min_count= 1)
        .reset_index() for x in list_of_files
        }

#Get Gemeinde names
dict_of_years_final_merge= {
    x: dict_of_dfs[x]
    .iloc[:, 0]
    .to_frame(name="Gemeinde")
    for x in dict_of_dfs.keys()
    }

# Put these together for merging purposes
all_gemeinde_names= (
        pd.concat([dict_of_years_final_merge[x] for x in dict_of_dfs.keys() ])
        .drop_duplicates()
        )

#Set Gemeinde as index for the concatenation procedure
dict_of_times_df = {
        "weimar": ([dict_of_dfs[x].set_index("Gemeinde")
        for x in dict_of_dfs.keys() if any(y in x for y in ["10", "29","30","31"])]),

        "nazi" : ([dict_of_dfs[x].set_index("Gemeinde")
        for x in dict_of_dfs.keys() if any( y in x for y in ["37","35","36"])])
        }



#Concat weimar anzi period to get the full datframes
dict_final_df = {
    x:pd.concat(dict_of_times_df[x],axis = 1) for x in dict_of_times_df.keys()}

#Save all the dataframes
export_base_path = r"~\Dropbox\Germany_state\2_Analysis\2_period_data\1_prewar"
all_gemeinde_names.to_csv(os.path.join(export_base_path,"merge_key_dig.csv"))

ik= "{}_dig.csv"
for x in ["weimar", "nazi"]:
    dict_final_df[x].to_csv(os.path.join(export_base_path, ik.format(x)))



def _find_variable(var_name_to_find):
    """ Find the dataset that contains variable var_name_to_find"""
    if dict_of_dfs_import:

        for dataset in dict_of_dfs_import:
            if var_name_to_find in dict_of_dfs_import[dataset].columns.tolist():
                print("Var {} is in csv with name {}"
                      .format(var_name_to_find, dataset)
                )
    else:
        print("Please import files first and create dict_of_dfs_import")
