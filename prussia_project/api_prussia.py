"""To run the Prussia pipeline."""

from Desktop.pre_war_copy.clean_digitization import clean_digitization  
from Desktop.pre_war_copy.bowling_mapped import map_bowling  
from Desktop.pre_war_copy.digitization_mapped import map_digitization  
from Desktop.pre_war_copy.persecution_mapped import map_persecution  
from Desktop.pre_war_copy.radio_mapped import map_radio  
from Desktop.pre_war_copy.x_create_base_df import create_base_map

# To see all variables of nazi and weimar, see here
cleaned_nazi_weimar_dict = clean_digitization()

# Mapped Datasets
bowling = map_bowling()
nazi, weimar = map_digitization()
persecution = map_persecution()
radio = map_radio()

# Return base map and dataframes exported for analysis
final_dfs = create_base_map()
