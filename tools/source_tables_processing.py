import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(parent_dir)
sys.path.append(parent_dir)
import pandas as pd
import glob


# This script is used to generate the "id_faird.xlsx" table from the original tables of each of the devices located in /Original_Tables. 
# "id_faird.xlsx" provides the data necessary to generate the desired charts by running "chart_taxon_ambient_clim.py"

# Specify the path where your Excel files are located
HOME = os.path.dirname(os.path.abspath(__file__))

print(HOME)

path = "/original_tables"

# Get a list of all Excel files in the specified path
file_list = glob.glob(parent_dir + path + "/*.xlsx")

# Initialize an empty list to store DataFrames
dfs = []

# Read each Excel file and append its "For_Statistics" worksheet to the list
for file in file_list:
    df = pd.read_excel(file, sheet_name="For_Statistics")
    dfs.append(df)

# Concatenate all DataFrames along rows
merged_df = pd.concat(dfs, ignore_index=True)

# filter out other detections different than Insecta Class
merged_df = merged_df[merged_df["Class"] == "Insecta"]

# Add an "ID" column starting from 1
merged_df["ID"] = range(1, len(merged_df) + 1)

# Save the merged DataFrame to a new Excel file
merged_df.to_excel(parent_dir + "/source_tables/id_faird2.xlsx",  sheet_name="Results", index=False)

print(f"Merged data saved to {parent_dir}\source_tables\id_faird.xlsx")
