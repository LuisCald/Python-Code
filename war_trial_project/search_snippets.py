""" Extract information from snippets. We extract: name, place of birth
    or place of residence, occupation (place of crime is work in progress).

"""
from extract_snippets import extract_info
from extract_snippets import extract_info2
import regex as re

def fill_empty(trial_dict, snippet, regex):
    for i, trial in enumerate(snippet.keys()):
        if len(snippet[i])==0:        
            snippet[i] = re.findall(regex, str(trial_dict[i]))
        else:
            pass

def snippet_and_best_guess_dict(trial_dict, snippet_rules_dict, bestguess_rules_dict):
    
    # Snippets
    name_snippet = extract_info(trial_dict, snippet_rules_dict["name_snippet"])   
    place_snippet = extract_info(trial_dict, snippet_rules_dict["place_snippet"]) 
    origin_snippet = []
    occupation_snippet = extract_info(trial_dict, snippet_rules_dict["occupation_snippet"]) 
    age_snippet = extract_info(trial_dict, snippet_rules_dict["age_snippet"])
    defense_snippet = extract_info(trial_dict, snippet_rules_dict["defense_snippet"])
    
    # Applying second rules to empties if needed
    fill_empty(trial_dict, age_snippet, snippet_rules_dict["occupation_snippet"])
    
    # Best Guesses 
    name = extract_info2(name_snippet, bestguess_rules_dict["capitalized_words4"]) 
    name = extract_info2(name_snippet, bestguess_rules_dict["capitalized_words3"]) 
    name = extract_info2(name_snippet, bestguess_rules_dict["capitalized_words2"]) 
    name = extract_info2(name_snippet, bestguess_rules_dict["capitalized_words1"]) 

    place = extract_info2(place_snippet, bestguess_rules_dict["extract_places"]) 
    origin = []
    occupation = extract_info2(occupation_snippet, bestguess_rules_dict["extract_occupation"]) 
    
    age = extract_info2(age_snippet, bestguess_rules_dict["extract_age"])
    
    
    # Snippet dictionary
    snippet_dict = {"name" : name_snippet, 
                    "place" : place_snippet,
                    "origin" : origin_snippet,
                    "occupation" : occupation_snippet,
                    "age" : age_snippet,
                    "defense" : defense_snippet,
                    }
                    
    # best guess dictionary
    bestguess_dict = {"name" : name,
                      "place" : place,
                      "origin" : origin,
                      "occupation" : occupation,
                      "age" : age
                      }
    return snippet_dict, bestguess_dict

def british_snippet_and_best_guess_dict(trial_dict, snippet_rules_dict, bestguess_rules_dict):
    
    # Snippets
    age_snippet = extract_info(trial_dict, snippet_rules_dict["age_snippet"]) 
    name_snippet = extract_info(trial_dict, snippet_rules_dict["name_snippet"]) 
    occupation_snippet = extract_info(trial_dict, snippet_rules_dict["occupation_snippet"]) 
    place_snippet = extract_info(trial_dict, snippet_rules_dict["place_snippet"]) 
    guilt_snippet = extract_info(trial_dict, snippet_rules_dict["guilt_snippet"]) 
    order_snippet = extract_info(trial_dict, snippet_rules_dict["orders_snippet"]) 


    age = extract_info(age_snippet, bestguess_rules_dict["extract_age"])
    name = extract_info(name_snippet, bestguess_rules_dict["extract_name"])
    place = extract_info(place_snippet, bestguess_rules_dict["extract_place"]) 
    occupation = extract_info(occupation_snippet, bestguess_rules_dict["extract_occupation"]) 
    
    # Snippet dictionary
    snippet_dict = {"age" : age_snippet,
                    "name" : name_snippet, 
                    "place" : place_snippet,
                    "occupation" : occupation_snippet,
                    "guilt" : guilt_snippet,
                    "order" : order_snippet,
                    }
                    
    # best guess dictionary
    bestguess_dict = {"age" : age,
                      "name" : name,
                      "place" : place,
                      "occupation" : occupation,
                      }
    return snippet_dict, bestguess_dict


# count_missing(british_age_snippet)
# count_missing(british_name_snippet)
# count_missing(british_occupation_snippet)
# count_missing(british_place_snippet)

# place[58] = place_snippet[58]
# place[61] = [place_snippet[61][0]]
# place[62] = [place_snippet[62][0]]
# place[66] = place_snippet[66]
# place[68] = [place_snippet[68][0]]
# place[73] = [place_snippet[73][1]]
# place[82] = place_snippet[82]
# place[83] = place_snippet[83]
# place[88] = [place_snippet[88][0]]
# place[90] = [place_snippet[90][1]]
# place[149] = [place_snippet[149][1]]
# place[184] = place_snippet[184]
# place[185] = place_snippet[185]
# place[187] = [place_snippet[187][0]]
# place[188] = place_snippet[188]
# place[190] = [place_snippet[190][0]]
# place[207] = [place_snippet[207][0]]
# place[209] = [place_snippet[209][0]]
# place[211] = place_snippet[211]
# place[214] = [place_snippet[214][1]]
# place[236] = [place_snippet[236][0]]
# place[245] = [place_snippet[245][0]]

# defense_snippet = extract_info(trial_dict, snippet_rules_dict["defense"])
# Best guesses
# name = extract_info(name_snippet, bestguess_rules_dict["capitalized_words1"]) 
# name = extract_info(name, bestguess_rules_dict["capitalized_words2"]) 
# name = extract_info(name, bestguess_rules_dict["capitalized_words3"]) 



# To remove copy entries in the list
# for trial in name2.keys():
#     name2[trial] = list(set(name2[trial]))

# Looking at origin

# # Snippets
# name_snippet = extract_info(trial_dict, snippet_rules_dict["name_snippet"])   
# place_snippet = extract_info(trial_dict, snippet_rules_dict["place_snippet"]) 
# origin_snippet = []
# occupation_snippet = extract_info(trial_dict, snippet_rules_dict["occupation_snippet"]) 
# age_snippet = extract_info(trial_dict, snippet_rules_dict["age_snippet"])

# # Applying second rules to empties if needed
# fill_empty(trial_dict, age_snippet, snippet_rules_dict["occupation_snippet"])

# # Best Guesses 
# name = extract_info2(name_snippet, bestguess_rules_dict["capitalized_words4"]) 
# name = extract_info2(name_snippet, bestguess_rules_dict["capitalized_words3"]) 
# name = extract_info2(name_snippet, bestguess_rules_dict["capitalized_words2"]) 
# name = extract_info2(name_snippet, bestguess_rules_dict["capitalized_words1"]) 

# place = extract_info2(place_snippet, bestguess_rules_dict["extract_places"]) 
# origin = []
# occupation = extract_info2(occupation_snippet, bestguess_rules_dict["extract_occupation"]) 

# age = extract_info2(age_snippet, bestguess_rules_dict["extract_age"])


# # Snippet dictionary
# snippet_dict = {"name" : name_snippet, 
#                 "place" : place_snippet,
#                 "origin" : origin_snippet,
#                 "occupation" : occupation_snippet,
#                 "age" : age_snippet
#                 }
#      #           "defense" : defense_snippet,
                
# # best guess dictionary
# bestguess_dict = {"name" : name,
#                   "place" : place,
#                   "origin" : origin,
#                   "occupation" : occupation,
#                   "age" : age
#                   }
# return snippet_dict, bestguess_dict