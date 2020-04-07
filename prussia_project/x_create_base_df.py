"""Create base map."""
import os
import math
import pandas as pd
import numpy as np

from Desktop.pre_war_copy.all_var_lists import weimar_variables 
from Desktop.pre_war_copy.all_var_lists import nazi_variables 
from Desktop.pre_war_copy.all_var_lists import clean_base_map

def create_base_map():
    # Import relevant dataframes
    import_base_path = r"~\Dropbox\Germany_state\2_Analysis\2_period_data\1_prewar"
    
    source_data_dict = {}
    for source_data in ['persecution', 'bowling', 'radio', 'weimar', 'nazi']:
        source_data_dict["{}".format(source_data)] = (
            pd.read_csv(os.path.join(
                                        import_base_path,
                                        '{}_mapped.csv'.format(source_data)
                                        )
                )
            )
    variables_to_remove, main_map_variables = clean_base_map()
    
    # Remove some variables we never use.  
    for source_data in source_data_dict.keys():
        source_data_dict[source_data] = (
            source_data_dict[source_data].drop(
                                                variables_to_remove, 
                                                axis=1,
                                                errors='ignore'
                                                )
            )
    
    # One of them is left out so that we don't have "NEAR_DIST" repeating for each source
    for source_data in source_data_dict.keys():
        if source_data in ["radio", "bowling", "nazi", "weimar"]:
            source_data_dict[source_data] = (
                source_data_dict[source_data].drop(main_map_variables, axis=1)
                )
        else:
            print("Like Magic")
            
    
    # Create objects of the 5 datasets
    radio_df = source_data_dict["radio"]
    bowling_df = source_data_dict["bowling"]
    persecution_df = source_data_dict["persecution"]
    weimar_df = source_data_dict["weimar"]
    nazi_df = source_data_dict["nazi"]
    
    # Rename some columns to avoid merge conflicts
    weimar_df = weimar_df.rename(columns={
                                            "business_tax": "business_tax_weimar",
                                            "infrastructure_exp_pc": "infrastructure_exp_pc_weimar",
                                            }
        )
    
    radio_with_bowling = radio_df.merge(
                                            bowling_df,
                                            how="inner",
                                            on="map_kreisnr"
                                            )
    persecution_radio_bowling = radio_with_bowling.merge(
                                                            persecution_df,
                                                            how="inner",
                                                            on="map_kreisnr"
                                                            )
    nazi_full_df = persecution_radio_bowling.merge(
                                                    nazi_df,
                                                    how="inner",
                                                    on="map_kreisnr"
                                                    )
    base_df = nazi_full_df.merge(
                                    weimar_df,
                                    how="inner",
                                    on="map_kreisnr"
                                    )
    
    # To remove duplicate columns with _y
    base_df.drop(list(base_df.filter(regex='_y$')), axis=1, inplace=True)
    
    # To remove the _x from the column names
    for column in base_df.columns:
       if "_x" in column:
           base_df = base_df.rename(columns={column: column[:-2]})
       else:
           pass  
         
    # Creating new variables
    
    base_df["sum_stuermer"] = base_df[[
                                        "stuer1", 
                                        "stuer2", 
                                        "stuer3"
                                        ]].sum(axis=1)
    
    base_df["antisemitic_culture_proxy"] = (
            base_df[
                    "sum_stuermer"
                    ].divide(
                    base_df["pop33"]).replace({np.inf:np.nan})
            )
    
    base_df["nazi_share_28"] = base_df["n285nsda"].divide(base_df["n285gs"])
            
            
    base_df["nazi_share_30"] = base_df["n309nsda"].divide(base_df["n309gs"])
    
            
    base_df["nazi_share_32"] = base_df["n327nsda"].divide(base_df["n327gs"])
    
    
    base_df["nazi_share_33"] = base_df["n333nsda"].divide(base_df["n333gs"])
    
    
    base_df["deportations_per_jewish_inhabitant"] = base_df["deptotal"].divide(base_df["jews33"])
            
    
    base_df["deportations_per_jewish_inhabitant39"] = base_df["deptotal"].divide(base_df["jews39"])
    
            
    base_df["prot_share"] = base_df["c25prot"].divide(base_df["c25pop"])
    
    
    base_df["prot_share"][np.isinf(base_df["prot_share"])] = np.nan 
    
    
    dep = "deportations_per_jewish_inhabitant"
    
    
    base_df[dep][np.isinf(base_df[dep])] = np.nan 
    
    
    dep39 = "deportations_per_jewish_inhabitant39"
    
    
    base_df[dep39][np.isinf( base_df[dep39])] = np.nan 
            
    
    base_df["industry_share_employment_25"] = base_df["c25bwerk"].divide(base_df["c25berwt"])
            
    
    base_df["industry_share_employment_33"] = base_df["c33indu"].divide(base_df["c33erwtt"])
            
    
    base_df["logdeport"] = base_df["deptotal"].map(lambda x: math.log(1+x))
            
    
    change_jewish33_39 = "change_jewish_inhabitants_33_39"
    
    
    base_df[change_jewish33_39] = (base_df["jews39"] - base_df["jews33"]).divide(base_df["jews33"])
    
    
    base_df[change_jewish33_39][np.isinf(base_df[change_jewish33_39])] = np.nan 
           
    
    change_jewish25_33 = "change_jewish_inhabitants_25_33"
    
    
    base_df[change_jewish25_33] = (base_df["jews33"] - base_df["c25juden"]).divide(base_df["c25juden"])
    
    
    change_jewish25_39 = "change_jewish_inhabitants_25_39"
    
    
    base_df[change_jewish25_39] =(base_df["jews39"] - base_df["c25juden"]).divide(base_df["c25juden"])
    
    
    base_df[change_jewish25_33][np.isinf(base_df[change_jewish25_33])] = np.nan 
    
    
    base_df[change_jewish25_39][np.isinf( base_df[change_jewish25_39])] = np.nan 
                    
    
    base_df["income_tax_per_capita"] = base_df["logtaxpers"].map(lambda x: math.exp(x))
    
    
    base_df["property_tax_per_capita"] = base_df["logtaxprop"].map(lambda x: math.exp(x))
    
    
    base_df["total_tax_per_capita"] = base_df["property_tax_per_capita"] + base_df["income_tax_per_capita"]
    
    
    base_df["clubs_per_capita"] = base_df["clubs_all"].divide(base_df["pop25"])
            
    
    #Change zeros to missing values for one column. We have some sv import issues 
    #there 
    base_df["wealth_transfer_tax_nominal"] = (
        base_df["wealth_transfer_tax_nominal"].copy().replace(0, np.nan)
        )
    
    
    to_make_pc = [ 
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
    
    pc = [ 
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
    
    # Divide each nominal value with pop_residential_june_1933
    for column, column1 in zip(to_make_pc, pc):
        base_df[column1] = (
                base_df[column]
                .divide(base_df["pop_residential_june_1933"])
                )
    
    # Create Weimar df
    variables_to_keep_weimar_dig_analyse = weimar_variables()
    weimar_full_df = base_df.copy()[variables_to_keep_weimar_dig_analyse]
    
    # Create Nazi df
    final_variable_collection = nazi_variables()
    nazi_full_df = base_df[final_variable_collection]
    
    # Export df 
    output_base_path = "~/Dropbox/Germany_state"
    
    weimar_full_df.to_csv(os.path.join(
        output_base_path, "2_Analysis/2_period_data/1_prewar/final_weimar_df.csv")
        )
    
    nazi_full_df.to_csv(os.path.join(
        output_base_path, "2_Analysis/2_period_data/1_prewar/final_nazi_df.csv")
        )
    
    final_dfs = {}
    final_dfs["base"] = base_df
    final_dfs["weimar"] = weimar_full_df
    final_dfs["nazi"] = nazi_full_df
    
    return final_dfs