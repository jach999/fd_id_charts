import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(parent_dir)
sys.path.append(parent_dir)
# Get the parent directory of parent_dir
grandparent_dir = os.path.abspath(os.path.join(parent_dir, ".."))
print("Grandparent Directory:", grandparent_dir)

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from tools.grouped_tables_config import * # Configuration variables
from src.dictionaries_control import *
from src.variables_handling import generate_time_variables, handle_strings
from src.insect_data_processing_tables import insect_data_process_tables
from src.clim_data_processing import clim_data_process

# Load data
HOME = parent_dir

print(HOME)


print()
print("##### Data settings #####")
print("-------------------------")
def main():
    # Call the variables_checker function
    # Validate each variable
    if not validate_time_division(time_division):
        return
    if not validate_device_type(device_type):
        return
    if not validate_taxon_level(taxon_level):
        return
    if not validate_extra_filter(extra_filter):
        return
    if not validate_extra_subfilter(extra_filter, extra_subfilter):
        return
 
    print("\033[92m" + "All variables are valid." + "\033[0m")

if __name__ == "__main__":
    main()

# Generate time variables
hours, minute_start, start_datetime, end_datetime, timedelta = generate_time_variables(time_division, time_freq, hour_start, hour_end, timespan_start, timespan_end, division_nr)
# Generate strings
folder_result_name, file_result_name, _, taxon, folder_sufix, file_sufix, time_sufix, time_freq_sufix, _ = handle_strings(clima, taxon, device_type, time_freq, folder_sufix, file_sufix, taxon_level, extra_filter, extra_subfilter, All, emend_id, time_division, timedelta, division_nr, device_type_options)

grouped_table_name = str('fd_id_' + time_freq_sufix + file_sufix + '.csv')

print()
print("##### Time settings #####")
print("-------------------------")
print(time_sufix.replace("_", " ").strip() + ":")
print("Time start: "+ str(start_datetime))
print("Time end: "+ str(end_datetime))
print("Timedelta: " + str(timedelta))
print()
print("Data saved as: " + "\033[94m" + HOME + "\\results\\grouped_tables\\" + folder_result_name + "\\" + grouped_table_name + "\033[0m")
print()

# Create the folder if it doesn't exist
if not os.path.exists("results/grouped_tables/" + folder_result_name):
    os.makedirs("results/grouped_tables/" + folder_result_name, 0o777)

# Process insect data and clima data functions
dfg_insect = insect_data_process_tables(parent_dir, time_freq, start_datetime, end_datetime, hour_start, hour_end, taxon, taxon_level, device_type, extra_filter, extra_subfilter, All, emend_id)
dfg_clim = clim_data_process(parent_dir, time_freq, start_datetime, end_datetime, minute_start, hours, hour_start, hour_end)
   
# merge_filter_factor and climatic tables
merged_df =  pd.merge(dfg_insect, dfg_clim, on="DateTime", how="outer")

# Set missing values to zero
merged_df.fillna(0, inplace=True)

# Delete rows where ID = 0
#merged_df = merged_df[merged_df["ID"] != 0]

# Sort merged_df by date
merged_df.sort_values(by="DateTime", inplace=True)

# Set the index to the "DateTime" column
merged_df.set_index("DateTime", inplace=True)


if day_column:
    merged_df['Day'] = (merged_df.index - merged_df.index[0]).days + 1
    
if week_column:
    # Create the 'Week' column
    merged_df['Week'] = ((merged_df.index - merged_df.index[0]).days // 7) + 1


merged_df.to_csv(HOME + "\\results\\grouped_tables\\" + folder_result_name + "\\" + grouped_table_name, index=True)  # Set index=True to include row labels (index) in the CSV

if stat_save == True:
    merged_df.to_csv(grandparent_dir + "/stat/source_tables/" + grouped_table_name, index=True) 

if interim_result_tables:
    dfg_insect.to_csv("results/grouped_tables/" + folder_result_name + "/" + file_result_name + '_dfg_insect.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    dfg_clim.to_csv("results/grouped_tables/" + folder_result_name + "/" + file_result_name + '_dfg_clim.csv', index=True) 
    
 
