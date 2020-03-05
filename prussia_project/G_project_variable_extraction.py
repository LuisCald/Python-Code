"""
Prepare dataframes and variables.
There are two lists for each datasource. the Processing list includes all
variables we need to create the variables we want to have.
The analyze list contins all the variables including newly created
ones that we want to carry over.
Every variable that we want to inlcude in the analyze list has to be in
the process list or has to be created within this file!
"""
import os
import math

import pandas as pd
import numpy as np


# Import relevant dataframes
import_base_path = "~/Dropbox/Germany_state/"

radio_df = pd.read_stata(
        os.path.join(
                import_base_path,
                '1_Data/Radio_and_Nazis/Germany_Media_Replication_Regions.dta'
                )
        )

radio2_df = pd.read_stata(
        os.path.join(
                import_base_path,
                '1_Data/Radio_and_Nazis/Germany_Media_Replication_Towns.dta'
                )
        ).drop_duplicates(["town_id"])

persecution_df = pd.read_stata(os.path.join(import_base_path,
        "1_Data/Persecution_perpetuated/Dataset_QJE_Replicate_with_Cities.dta",
    )
)

bowling_JPE = "1_Data/Bowling_For_Fascism/Dataset_Bowling_Replication_JPE.dta"
bowling_df = (pd.read_stata(os.path.join(
        import_base_path, bowling_JPE),
        encoding="latin1")
        )

dig_weimar_df = (pd.read_csv(os.path.join(
        import_base_path,"2_Analysis/2_period_data/1_prewar/weimar_dig.csv"))
    .rename(columns = {"Unnamed: 0":"Gemeinde"})
    )
dig_nazi_df = (pd.read_csv(os.path.join(
        import_base_path,"2_Analysis/2_period_data/1_prewar/nazi_dig.csv"))
    .rename(columns = {"Unnamed: 0":"Gemeinde"})
    )


# class persecution():
#     kreis = "kreis"
#     persecution.kreis_nr = "kreis_nr"
#     persecution.tot_pop = "tot_pop"
#     persecution.stuer1 =   "stuer1"
#     persecution.stuer2="stuer2"
#     persecution.stuer3="stuer3"
#     persecution.deptotal = "deptotal"
#     persecution.jews33 ="jews33"
#     persecution.jews39 ="jews39"
#     persecution.jews25="c25juden"
#     persecution.prot25="c25prot"
#     persecution.votes33 ="n333gs"
#     persecution.nsdap33="n333nsda"
#     persecution.nsdap28 ="n285nsda"
#     persecution.votes28 = "n285gs"
#     persecution.nsdap32 ="n327nsda"
#     persecution.votes32 = "n327gs"
#     persecution.votes30 = "n309gs"
#     persecution.nsdap30 = "n309nsda"
#     persecution.pop25 = "c25pop"
#     persecution.industry_employment25 = "c25bwerk"
#     persecution.total_employment25 = "c25berwt"
#     persecution.industry_employment33 = "c33indu"
#     persecution.total_employment33 = "c33erwtt"
#     persecution.antisemitism = "antisemitic_culture_proxy"
#     persecution.dep_pc =    "deportations_per_jewish_inhabitant"
#     persecution.nazi28 = "nazi_share_28"
#     persecution.nazi30 = "nazi_share_30"
#     persecution.nazi32 = "nazi_share_32"
#     persecution.nazi33 = "nazi_share_33"
#     persecution.indu33 = "industry_share_employment_33"
#     persecution.indu25 = "industry_share_employment_25"
#     persecution.log = "logdeport"
#     persecution.deptot = "deptotal"
#     persecution.change33 = "change_jewish_inhabitants_25_33"
#     persecution.prot = "prot_share"
# =============================================================================





#######Specify variables to process
variables_to_keep_persecution_process = [
    "kreis",
    "kreis_nr",
    "totpop",
    "stuer1",
    "stuer2",
    "stuer3",
    "deptotal",
    "jews33",
    "jews39",
    "c25juden",
    "c25prot",
    "n333gs",
    "n333nsda",
    "n32nnsda",
    "n32ngs",
    "n285nsda",
    "n327gs",
    "n327nsda",
    "n309gs",
    "n309nsda",
    "n285gs",
    "c25bwerk",
    "c33erwtt",
    "c33indu",
    "c25berwt",
    "c25pop",
    "pog20s",
    "syn33",
    "pog33"
]


variables_to_keep_bowling_process = [
        "logtaxprop",
        "logtaxpers",
        "share_prot25",
        "cityid",
        "landweimar",
        "pop25",
        "clubs_all"
        ]

variables_to_keep_radio_process = [
        "id",
        "share_listeners31"
        ]


#Maybe get population out of here
variables_to_keep_radio2_process = [
        "town_id",
        "c25kath_share",
        "c25juden_share"
        ]

variables_to_keep_weimar_dig_process = [
    "beamte_1910",
    "pop_residential_june_1933",
    "tot_empl",

    "property_taxes_weimar_nominal",
    "business_tax",
    "wealth_transfer_tax_nominal_weimar",
    "tot_local_tax_weimar_nominal",
    "tot_qualified_to_pay_taxes",
    "tot_female_tax_payers",
    "tot_taxed",
    "tot_tax_exempt",
    "tot_untaxed",
    "percent_tot_taxed",
    "percent_tot_tax_exempt",
    "percent_tot_untaxed",
    'taxable_income_thousands_weimar',
    'taxable_income_thousands_weimar_pc',
    'income_taxes_collected_thousands_weimar',
    'income_taxes_collected_thousands_weimar_pc',
    'exp_unemployment_1000RM',
    'exp_museums_arts_1000RM',
    'exp_teacher_trainings_1000RM',
    'exp_libraries_pc',
    'exp_trade_schols_pc',
    'exp_primary_education_pc',
    'exp_theatre_concerts_pc',
    'exp_museums_arts_pc',
    'exp_associations_1000RM',
    'exp_secondary_education_pc',
    'exp_youth_wellbeing_pc',
    'exp_post_secondary_education_pc',
    'exp_associations_pc',
    'exp_libraries_1000RM',
    'exp_post_secondary_education_1000RM',
    'exp_unemployment_pc',
    'exp_teacher_trainings_pc',
    'exp_secondary_education_1000RM',
    'exp_welfare_including_youth_pc',
    'exp_theatre_concerts_1000RM',
    'tot_exp_police_pc',
    'exp_health_pc',
    'exp_welfare_pc',

    'nominal_general_admin_exp',
    'nominal_infra_exp',
    'exp_healthcare_1000RM',
    'exp_welfare_1000RM',
    'tot_exp_general_tax_finance_ market ',
    'tot_exp_police',
    'Education_nominal',



    'General_admin_exp_pc',
    'infrastructure_exp_pc',
    'Education_exp_pc',
    'Land_management_other_exp_pc',
    'Police_admin',
    'School_admin',
    'other_education_officials',
    'civil_engineering_man',
    "fleet_management",
    "park_garden_man",
    "fire_management",
    'Health_care_workers',
    'tax_financial_admin',
    'all_gemeinde_admin',

    'tot_employees_building_construction_management',
    'tot_empl_sewage',
    'tot_empl_fleet_and_road_cleaning',
    'tot_empl_garden_park_management',
    'tot_empl_fire_dep',
    'tot_empl_healthcare',
    'tot_empl_welfare_system',
    'tot_empl_edu_system',
    'tot_empl_police_tax_financial',
       # 'tot_empl',

    'Lifetime_Beamte_a',
    'Part_time_Beamte_a',
    'scientific_beamte_a',
    'trainee_beamte_a',
    'Fireable_Beamte_a',
    'Total_beamte_a',
    'angestellte_pension_a',
    'angestellte_Nopension_a',
    'tot_empl_a',

       'Lifetime_Beamte_b',
    'Part_time_Beamte_b',
    'scientific_beamte_b',
    'trainee_beamte_b',
    'Fireable_Beamte_b',
    'Total_beamte_b',
     'angestellte_pension_b',
    'angestellte_Nopension_b',
    'tot_empl_b',
    'General_management',
    'welfare_empl_nom',

    'tot_localdeaths_1year',
    'local_deaths_1yearp100',
    'tot_nonlocaldeaths_1year',
    'nonlocal_deaths_1yearp100',
    'tot_deaths_local',
    'tot_deaths_foreign',
    'tot_births_residents',
    'tot_births_nonlocal',
    "tot_immigrants",
    "tot_emigrants",
    "net_migration",
    "value_added_tax_1000RM",
    "population1930",
    "Gemeinde"
    ]

variables_to_keep_nazi_dig_process = [
    "taxable_income_thousands",
    "tot_income_tax_thousands",
    "tot_income_tax_pt",
    "income_tax_pc",
     "land_and_building_taxes_nominal",
    "business_tax_nominal",
    "wealth_transfer_tax_nominal",
    "local_tax_tot_nominal",
    "local_tax_pc",
    "land_and_building_tax",
    "business_tax",
    "wealth_transfer_tax",
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
    "Gemeinde"
                                      ]


######Specify varaibles to analyse
variables_to_keep_persecution_analyse = [
        "kreis_nr",
        "kreis",
        "antisemitic_culture_proxy",
        "deportations_per_jewish_inhabitant",
        "deportations_per_jewish_inhabitant39",
        "nazi_share_28",
        "nazi_share_30",
        "nazi_share_32",
        "nazi_share_33",
        "industry_share_employment_25",
        "industry_share_employment_33",
        "logdeport",
        "deptotal",
        "change_jewish_inhabitants_33_39",
        "change_jewish_inhabitants_25_33",
        "change_jewish_inhabitants_25_39",
        "prot_share",
        "pog20s",
        "syn33",
        "jews33",
        "c25juden",
        "pog33"
        ]

variables_to_keep_bowling_analyse = [
        "income_tax_per_capita",
        "property_tax_per_capita",
        "total_tax_per_capita",
        "cityid",
        "landweimar",
        "share_prot25",
        "clubs_per_capita"
        ]

variables_to_keep_radio_analyse = [
        "id",
        "share_listeners31"
        ]

variables_to_keep_radio2_analyse = [
        "town_id",
        "c25kath_share",
        "c25juden_share"
        ]

variables_to_keep_weimar_dig_analyse = [
    "Gemeinde",
    "beamte_1910",
    "pop_residential_june_1933",
    "property_taxes_weimar_pc",
    "business_tax_weimar_pc",
    "wealth_transfer_tax_weimar_pc",
    "local_tax_weimar_pc",
    "property_taxes_weimar_nominal",
    "business_tax",
    "wealth_transfer_tax_nominal_weimar",
    "tot_local_tax_weimar_nominal",
    "tot_qualified_to_pay_taxes",
    "tot_female_tax_payers",
    "tot_taxed",
    "tot_tax_exempt",
    "tot_untaxed",
    "percent_tot_taxed",
    "percent_tot_tax_exempt",
    "percent_tot_untaxed",
    'taxable_income_thousands_weimar',
    'taxable_income_thousands_weimar_pc',
    'income_taxes_collected_thousands_weimar',
    'income_taxes_collected_thousands_weimar_pc',
    'exp_unemployment_1000RM',
    'exp_museums_arts_1000RM',
    'exp_teacher_trainings_1000RM',
    'exp_libraries_pc',
    'exp_trade_schols_pc',
    'exp_primary_education_pc',
    'exp_theatre_concerts_pc',
    'exp_museums_arts_pc',
    'exp_associations_1000RM',
    'exp_secondary_education_pc',
    'exp_youth_wellbeing_pc',
    'exp_post_secondary_education_pc',
    'exp_associations_pc',
    'exp_libraries_1000RM',
    'exp_post_secondary_education_1000RM',
    'exp_unemployment_pc',
    'exp_teacher_trainings_pc',
    'exp_secondary_education_1000RM',
    'exp_welfare_including_youth_pc',
    'exp_theatre_concerts_1000RM',
    'tot_exp_police_pc',
    'exp_health_pc',
    'exp_welfare_pc',
    'General_admin_exp_pc',
    'infrastructure_exp_pc',
    'Education_exp_pc',
    'Land_management_other_exp_pc',

    'nominal_general_admin_exp',
    'nominal_infra_exp',
    'exp_healthcare_1000RM',
    'exp_welfare_1000RM',
    'tot_exp_general_tax_finance_ market ',
    'tot_exp_police',
    'Education_nominal',

    'Police_admin_pc',
    'School_admin_pc',
    'other_education_officials_pc',
    "civil_engineering_man_pc",
    "fleet_management_pc",
    "park_garden_man_pc",
    "fire_management_pc",
    'Health_care_workers_pc',
    'tax_financial_admin_pc',
    'all_gemeinde_admin_pc',
    'Police_admin',
    'School_admin',
    'other_education_officials',
    'civil_engineering_man',
    "fleet_management",
    "park_garden_man",
    "fire_management",
    'Health_care_workers',
    'tax_financial_admin',
    'all_gemeinde_admin',
    'tot_employees_building_construction_management_pc',
    'tot_empl_sewage_pc',
    'tot_empl_fleet_and_road_cleaning_pc',
    'tot_empl_garden_park_management_pc',
    'tot_empl_fire_dep_pc',
    'tot_empl_healthcare_pc',
    'tot_empl_welfare_system_pc',
    'tot_empl_edu_system_pc',
    'tot_empl_police_tax_financial_pc',
    'tot_empl_pc',

    'tot_employees_building_construction_management',
    'tot_empl_sewage',
    'tot_empl_fleet_and_road_cleaning',
    'tot_empl_garden_park_management',
    'tot_empl_fire_dep',
    'tot_empl_healthcare',
    'tot_empl_welfare_system',
    'tot_empl_edu_system',
    'tot_empl_police_tax_financial',
    'tot_empl',


    'Lifetime_Beamte_a',
    'Part_time_Beamte_a',
    'scientific_beamte_a',
    'trainee_beamte_a',
    'Fireable_Beamte_a',
    'angestellte_pension_a',
    'angestellte_Nopension_a',
    'Total_beamte_a',
    'tot_empl_a',

    'Lifetime_Beamte_b',
    'Part_time_Beamte_b',
    'scientific_beamte_b',
    'trainee_beamte_b',
    'Fireable_Beamte_b',
    'angestellte_pension_b',
    'angestellte_Nopension_b',
    'Total_beamte_b',
    'tot_empl_b',

    'Lifetime_Beamte_pc_a',
    'Part_time_Beamte_pc_a',
    'scientific_beamte_pc_a',
    'trainee_beamte_pc_a',
    'Fireable_Beamte_pc_a',
    'angestellte_pension_pc_a',
    'angestellte_Nopension_pc_a',
    'Total_beamte_pc_a',
    'tot_empl_pc_a',

    'Lifetime_Beamte_pc_b',
    'Part_time_Beamte_pc_b',
    'scientific_beamte_pc_b',
    'trainee_beamte_pc_b',
    'Fireable_Beamte_pc_b',
    'angestellte_pension_pc_b',
    'angestellte_Nopension_pc_b',
    'Total_beamte_pc_b',
    'tot_empl_pc_b',

    'welfare_empl_nom',
    'welfare_empl_pc',

    'General_management',
    'General_management_pc',
    'tot_localdeaths_1year',
    'local_deaths_1yearp100',
    'tot_nonlocaldeaths_1year',
    'nonlocal_deaths_1yearp100',
    'tot_deaths_local',
    'tot_deaths_foreign',
    'tot_births_residents',
    'tot_births_nonlocal',
    "tot_immigrants",
    "tot_emigrants",
    "net_migration",
    "value_added_tax_1000RM",
    "population1930",
    ]

variables_to_keep_nazi_dig_analyse =[
    "Gemeinde",
    "taxable_income_thousands",
    "tot_income_tax_thousands",
    "tot_income_tax_pt",
    "local_tax_pc",
    "income_tax_pc",
    "land_and_building_taxes_nominal",
    "business_tax_nominal",
    "wealth_transfer_tax_nominal",
    "local_tax_tot_nominal",
    "land_and_building_tax",
    "business_tax",
    "wealth_transfer_tax",
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


###############################################################################
############################Process persecution################################
###############################################################################

#Aggregate on the county level. Sum everything since all absolute quantities
pers_processed_df = (persecution_df
                            .copy()[variables_to_keep_persecution_process]
                            .groupby(["kreis_nr","kreis"]).sum().reset_index()
                            )


pers_processed_df["sum_stuermer"] = (
    pers_processed_df["stuer1"]
    + pers_processed_df["stuer2"]
    + pers_processed_df["stuer3"]
)

persecution_divide = {"antisemitic_culture_proxy":{"numerator":"sum_stuermer",
                                                   "denominator":"totpop"
                                                   },
                      "nazi_share_28":{"numerator":"n285nsda",
                                       "denominator":"n285gs"
                                                   },
                      "nazi_share_30":{"numerator":"n309nsda",
                                       "denominator":"n309gs"
                                                   },

                      "nazi_share_32":{"numerator":"n327nsda",
                                       "denominator":"n327gs"
                                                   },
                      "nazi_share_30":{"numerator":"n333nsda",
                                       "denominator":"n333gs"
                                                   },
                      "nazi_share_30":{"numerator":"n333nsda",
                                       "denominator":"n333gs"
                                                   }




                      }

pers_processed_df["antisemitic_culture_proxy"] = (
        pers_processed_df[
                "sum_stuermer"
                ].divide(
                pers_processed_df["totpop"]).replace({np.inf:np.nan})
        )

pers_processed_df["nazi_share_28"] = (
        pers_processed_df["n285nsda"].divide(
    pers_processed_df["n285gs"]
)
        )

pers_processed_df["nazi_share_30"] = (
        pers_processed_df["n309nsda"].divide(
    pers_processed_df["n309gs"]
)
        )

pers_processed_df["nazi_share_32"] = (
        pers_processed_df["n327nsda"].divide(
    pers_processed_df["n327gs"]
)
        )
pers_processed_df["nazi_share_33"] = pers_processed_df["n333nsda"].divide(
    pers_processed_df["n333gs"]
)

pers_processed_df["deportations_per_jewish_inhabitant"] =(
        pers_processed_df["deptotal"]
        .divide(pers_processed_df["jews33"]
        )
        )
pers_processed_df["deportations_per_jewish_inhabitant39"] =(
        pers_processed_df["deptotal"]
        .divide(pers_processed_df["jews39"]
        )
        )

#Run subsetted
pers_processed_df["prot_share"] =(
        pers_processed_df["c25prot"]
        .divide(pers_processed_df["c25pop"]
        )
        )

pers_processed_df["prot_share"][
        np.isinf( pers_processed_df["prot_share"])] = np.nan

dep = "deportations_per_jewish_inhabitant"
pers_processed_df[dep][
        np.isinf(pers_processed_df[dep])] = np.nan

dep39 = "deportations_per_jewish_inhabitant39"
pers_processed_df[dep39][
        np.isinf( pers_processed_df[dep39])] = np.nan

pers_processed_df["industry_share_employment_25"] = (
        pers_processed_df[
    "c25bwerk"
].divide(pers_processed_df["c25berwt"])
        )

pers_processed_df["industry_share_employment_33"] = (
        pers_processed_df[
    "c33indu"
].divide(pers_processed_df["c33erwtt"])
        )

pers_processed_df["logdeport"] = (
        pers_processed_df["deptotal"].map(lambda x: math.log(1+x))
        )
change_jewish33_39 = "change_jewish_inhabitants_33_39"
pers_processed_df[change_jewish33_39] =(
        pers_processed_df["jews39"] - pers_processed_df["jews33"]
        ).divide(pers_processed_df["jews33"])


pers_processed_df[change_jewish33_39][
        np.isinf( pers_processed_df[change_jewish33_39])] = np.nan

change_jewish25_33 = "change_jewish_inhabitants_25_33"
pers_processed_df[change_jewish25_33] =(
        pers_processed_df["jews33"] - pers_processed_df["c25juden"]
        ).divide(pers_processed_df["c25juden"])

change_jewish25_39 = "change_jewish_inhabitants_25_39"
pers_processed_df[change_jewish25_39] =(
        pers_processed_df["jews39"] - pers_processed_df["c25juden"]
        ).divide(pers_processed_df["c25juden"])


pers_processed_df[change_jewish25_33][
        np.isinf(pers_processed_df[change_jewish25_33])] = np.nan

pers_processed_df[change_jewish25_39][
        np.isinf( pers_processed_df[change_jewish25_39])] = np.nan

persecution_final_df = pers_processed_df[

     variables_to_keep_persecution_analyse

]



###############################################################################
############################Process Bowling####################################
###############################################################################
bowling_processed_df = bowling_df.copy()[variables_to_keep_bowling_process]

bowling_processed_df["income_tax_per_capita"] = (
        bowling_processed_df["logtaxpers"].map(
    lambda x: math.exp(x)
)
        )

bowling_processed_df["property_tax_per_capita"] = bowling_processed_df[
    "logtaxprop"
].map(lambda x: math.exp(x))

bowling_processed_df["total_tax_per_capita"] = (
    bowling_processed_df["property_tax_per_capita"]
    + bowling_processed_df["income_tax_per_capita"]
)

bowling_processed_df["clubs_per_capita"] = (
        bowling_processed_df["clubs_all"].divide(
                bowling_processed_df["pop25"]
                )
        )

bowling_final_df = bowling_processed_df.copy()[

     variables_to_keep_bowling_analyse

]

nazi_dig_processed_df = dig_nazi_df[variables_to_keep_nazi_dig_analyse].copy()
#Change zeros to missing values for one column. We have some sv import issues
#there
nazi_dig_processed_df["wealth_transfer_tax_nominal"] = (
        nazi_dig_processed_df["wealth_transfer_tax_nominal"]
        .copy()
        .replace(0,np.nan)
        )

nazi_dig_final_df = nazi_dig_processed_df.copy()

weimar_processed_df = dig_weimar_df[variables_to_keep_weimar_dig_process]


to_make_pc = [ 'tot_employees_building_construction_management',
                                        'tot_empl_sewage',
                                        'tot_empl_fleet_and_road_cleaning',
                                        'tot_empl_garden_park_management',
                                        'tot_empl_fire_dep',
                                        'tot_empl_healthcare',
                                        'tot_empl_welfare_system',
                                        'tot_empl_edu_system',
                                        'tot_empl_police_tax_financial',
                                        'tot_empl',


                                        'General_management',
                                          'Lifetime_Beamte_a',
                                        'Part_time_Beamte_a',
                                        'scientific_beamte_a',
                                        'Fireable_Beamte_a',
                                        'trainee_beamte_a',
                                         'angestellte_pension_a',
                                        'angestellte_Nopension_a',
                                        'Total_beamte_a',
                                        'tot_empl_a',

                                       'Lifetime_Beamte_b',
                                        'Part_time_Beamte_b',
                                        'scientific_beamte_b',
                                        'trainee_beamte_b',
                                        'Fireable_Beamte_b',
                                        'angestellte_pension_b',
                                        'angestellte_Nopension_b',
                                        'Total_beamte_b',
                                        'tot_empl_b',
                                        'welfare_empl_nom',

                                        "property_taxes_weimar_nominal",
                                        "business_tax",
                                        "wealth_transfer_tax_nominal_weimar",
                                        "tot_local_tax_weimar_nominal",
                                        "Police_admin",
                                        "School_admin",
                                        "other_education_officials",
                                        "Health_care_workers",
                                        "tax_financial_admin",
                                        "all_gemeinde_admin",
                                        "civil_engineering_man",
                                        "fleet_management",
                                        "park_garden_man",
                                        "fire_management"
        ]

pc = [ 'tot_employees_building_construction_management_pc',
                                        'tot_empl_sewage_pc',
                                        'tot_empl_fleet_and_road_cleaning_pc',
                                        'tot_empl_garden_park_management_pc',
                                        'tot_empl_fire_dep_pc',
                                        'tot_empl_healthcare_pc',
                                        'tot_empl_welfare_system_pc',
                                        'tot_empl_edu_system_pc',
                                        'tot_empl_police_tax_financial_pc',
                                        'tot_empl_pc',


                                        'General_management_pc',
                                        'Lifetime_Beamte_pc_a',
                                        'Part_time_Beamte_pc_a',
                                        'scientific_beamte_pc_a',
                                        'trainee_beamte_pc_a',
                                        'Fireable_Beamte_pc_a',
                                        'angestellte_pension_pc_a',
                                        'angestellte_Nopension_pc_a',
                                        'Total_beamte_pc_a',
                                        'tot_empl_pc_a',

                                        'Lifetime_Beamte_pc_b',
                                        'Part_time_Beamte_pc_b',
                                        'scientific_beamte_pc_b',
                                        'trainee_beamte_pc_b',
                                        'Fireable_Beamte_pc_b',
                                        'angestellte_pension_pc_b',
                                        'angestellte_Nopension_pc_b',
                                        'Total_beamte_pc_b',
                                        'tot_empl_pc_b',
                                        'welfare_empl_pc',

                                        "property_taxes_weimar_pc",
                                        "business_tax_weimar_pc",
                                        "wealth_transfer_tax_weimar_pc",
                                        "local_tax_weimar_pc",
                                        "Police_admin_pc",
                                        "School_admin_pc",
                                        "other_education_officials_pc",
                                        "Health_care_workers_pc",
                                        "tax_financial_admin_pc",
                                        "all_gemeinde_admin_pc",
                                        "civil_engineering_man_pc",
                                        "fleet_management_pc",
                                        "park_garden_man_pc",
                                        "fire_management_pc"
                                        ]
for column, column1 in zip(to_make_pc, pc):
    weimar_processed_df[column1] = (
            weimar_processed_df[column]
            .divide(weimar_processed_df["pop_residential_june_1933"])
            )



#weimar_processed_df["tot_employees_building_construction_management_pc"] = weimar_processed_df["tot_employees_building_construction_management"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["tot_empl_sewage_pc"] = weimar_processed_df["tot_empl_sewage"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["tot_empl_fleet_and_road_cleaning_pc"] = weimar_processed_df["tot_empl_fleet_and_road_cleaning"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["tot_empl_garden_park_management_pc"] = weimar_processed_df["tot_empl_garden_park_management"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["tot_empl_fire_dep_pc"] = weimar_processed_df["tot_empl_fire_dep"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["tot_empl_healthcare_pc"] = weimar_processed_df["tot_empl_healthcare"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["tot_empl_welfare_system_pc"] = weimar_processed_df["tot_empl_welfare_system"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["tot_empl_edu_system_pc"] = weimar_processed_df["tot_empl_edu_system"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["tot_empl_police_tax_financial_pc"] = weimar_processed_df["tot_empl_police_tax_financial"].divide(weimar_processed_df["pop_apr_1928"])
###weimar_processed_df["tot_empl_pc"] = weimar_processed_df["tot_empl"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["Waterworks_pc"] = weimar_processed_df["Waterworks"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["Gas_pc"] = weimar_processed_df["Gas"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["Electric_pc"] = weimar_processed_df["Electric"].divide(weimar_processed_df["pop_apr_1928"])
#weimar_processed_df["Transport_pc"] = weimar_processed_df["Transport"].divide(weimar_processed_df["pop_apr_1928"])

#weimar_processed_df["property_taxes_weimar_pc"] = weimar_processed_df["property_taxes_weimar_nominal"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["business_tax_weimar_pc"] = weimar_processed_df["business_tax"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["wealth_transfer_tax_weimar_pc"] = weimar_processed_df["wealth_transfer_tax_nominal_weimar"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["local_tax_weimar_pc"] = weimar_processed_df["tot_local_tax_weimar_nominal"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["Police_admin_pc"] = weimar_processed_df["Police_admin"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["School_admin_pc"] = weimar_processed_df["School_admin"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["other_education_officials_pc"] = weimar_processed_df["other_education_officials"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["Health_care_workers_pc"] = weimar_processed_df["Health_care_workers"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["tax_financial_admin_pc"] = weimar_processed_df["tax_financial_admin"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["all_gemeinde_admin_pc"] = weimar_processed_df["all_gemeinde_admin"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["civil_engineering_man_pc"] = weimar_processed_df["civil_engineering_man"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["fleet_management_pc"] = weimar_processed_df["fleet_management"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["park_garden_man_pc"] = weimar_processed_df["park_garden_man"].divide(weimar_processed_df["pop_residential_june_1933"])
#weimar_processed_df["fire_management_pc"] = weimar_processed_df["fire_management"].divide(weimar_processed_df["pop_residential_june_1933"])


weimar_final_df = (weimar_processed_df
                   .copy()[variables_to_keep_weimar_dig_analyse]
                   )

###############################################################################
############################Process Radio######################################
###############################################################################

radio_final_df = radio_df.copy()[variables_to_keep_radio_analyse]

radio2_final_df = radio2_df.copy()[variables_to_keep_radio2_analyse]

###export data
output_base_path = "~/Dropbox/Germany_state/2_Analysis"

persecution_final_df.to_csv(
    os.path.join(
        output_base_path, "2_period_data/1_prewar/persecution_processed.csv"
    )
)

bowling_processed = "2_period_data/1_prewar/bowling_processed.csv"
bowling_final_df.to_csv(os.path.join(output_base_path, bowling_processed))

radio_processed = "2_period_data/1_prewar/radio_processed.csv"
radio_final_df.to_csv(os.path.join(output_base_path, radio_processed))

radio2_processed = "2_period_data/1_prewar/radio2_processed.csv"
radio2_final_df.to_csv(os.path.join(output_base_path, radio2_processed))

weimar_dig = "2_period_data/1_prewar/weimar_dig_processed.csv"
weimar_final_df.to_csv(os.path.join(output_base_path, weimar_dig))

nazi_dig = "2_period_data/1_prewar/nazi_dig_processed.csv"
nazi_dig_final_df.to_csv(os.path.join(output_base_path, nazi_dig))
