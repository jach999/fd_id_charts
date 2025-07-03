import sys
import os
import pandas as pd
import glob

# Get the parent directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(parent_dir)
sys.path.append(parent_dir)

# Specify the path where your Excel files are located
path = os.path.join(parent_dir, "original_tables")

# Get a list of all Excel files in the specified path
file_list = glob.glob(os.path.join(path, "*.xlsx"))

# Initialize an empty list to store DataFrames
dfs = []

# Read each Excel file and append its "For_Statistics" worksheet to the list
for file in file_list:
    df = pd.read_excel(file, sheet_name="For_Statistics")
    dfs.append(df)

# Check if there are any DataFrames to concatenate
if dfs:
    # Concatenate all DataFrames along rows
    merged_df = pd.concat(dfs, ignore_index=True)

    # Filter out other detections different than Insecta Class
    merged_df = merged_df[merged_df["Class"] == "Insecta"]

    # Add an "ID" column starting from 1
    merged_df["ID"] = range(1, len(merged_df) + 1)

    # Save the merged DataFrame to a new Excel file
    merged_df.to_excel(os.path.join(parent_dir, "source_tables", "id_faird.xlsx"), sheet_name="Results", index=False)

    print("Merged data saved to: " + "\033[94m" + os.path.join(parent_dir, "source_tables", "id_faird.xlsx") + "\033[0m")
else:
    print("No Excel files found in the specified path.")

