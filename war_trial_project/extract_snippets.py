""" Extract snippets from each trial. We extract: snippet containing name, 
    snippet containing information on the accused (such as place of 
    birth or residence, occupation, age) and snippet containing information 
    on presumably residence of the accused.

"""
import regex as re
import pandas as pd


def extract_info(trial_item, regex):
    """Runs regex rule over list of trials. Returns matches in a dictionary
    
    Args:
        trial_item (dict): a dictionary created with **file_writer**
        regex (string): a rule to search the trialdict values
    
    Returns:
        results_dict (list): a dict of all matches with respect to the trials
    
    """
    results= []
    for trial in trial_item:      
            regex = regex
            out = re.findall(regex, str(trial_item[trial]))
            results.append(out)

    results_dict = {}
    for i in range(len(results)):
        results_dict[i] = results[i]
    
    return results_dict

def extract_info2(trial_item, regex):
    """Runs regex rule over list of trials. Returns matches.
    
    Args:
        trial_item (dict): a dictionary created with **file_writer**
        regex (string): a rule to search the trialdict values
    
    Returns:
        results_dict (list): a dict of all matches with respect to the trials
    
    """
    all_trial_results= []
    for trial in trial_item.keys():
        trial_result = []
        if len(trial_item[trial])==0:
            out = []
            trial_result.append(out)
        else:
            for i, values in enumerate(trial_item[trial]):
                regex = regex
                out = re.findall(regex, trial_item[trial][i])
                trial_result.append(out)
        all_trial_results.append(trial_result)        

    results_dict = {}
    for i in range(len(all_trial_results)):
        results_dict[i] = all_trial_results[i]
        results_dict[i] = sum(all_trial_results[i], [])
    
    return results_dict

def analysis(extract_info_dict):
    """Reports how many missing/unmatched from a dictionary of trials.
    
    Args:
        extract_info_dict (dict): dictionary of trials
    
    Returns:
        missing (non-negative integer): the number of missing/unmatched cases
    
    """
    for meta_info in extract_info_dict.keys():
        if extract_info_dict[meta_info]==[]:
            pass
        else:
            missing = sum(1 for trial in extract_info_dict[meta_info].values() if len(trial)==0)
            print("We are still missing {} from {}".format(missing, meta_info))



# results_occupation = extract_info2(occupation_snippet, bestguess_rules_dict["extract_occupation"]) 
# for keys in results_occupation.keys():
#     results_occupation[key]