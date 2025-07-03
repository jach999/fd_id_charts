All = "All"


#-------------------------#
#      Data settings      #
#-------------------------#

# Modify these factors to display different info in the tables
device_type = All # Set to All to show all devices, or choose between "FAIRD" or "ID"
taxon_level = "Class" # "Class", "Order", "Suborder", "Family", "Subfamily", "Genus"
taxon = "Insecta" # Acording the selected taxon_level, the desired taxon. If more than one is wanted:["taxon1","taxon2", ...] - Example for taxon_level = "Order": ["Diptera", "Coleoptera", "Hymenoptera"] 

# Additional filter
extra_filter = None # None for not adding an additional filter. Otherwise use Device_type", "Device", "Ambient", "Site", and "DevixexAmbient"
extra_subfilter = None # If extra_filter = None, extra_subfilter does nothing. Otherwise: in "Device_type": FAIR-D or "ID"; in "Device": FAIRD1, -D2, -D3, or -D4, ID1, -2, or -4; in "Ambient": "Maize" or "Meadow"; in "Site": "Site1", "Site2", "Site3", "Site4"; in "DevicexAmbient": “FAIRDxMaize”, “FAIRDxMeadow”, “IDxMaize”, “IDxMeadow”

# Climatic variables
clima = True # Activate temperature, windspeed, precipitation and solar radiaion for adding to the chart (True/False)


#-------------------------#
#      Time settings      #
#-------------------------#

time_freq = "1 min" # The values ​​should be multiples or divisors of 24 hours or 60 min and have time units. Example: "12 h" or "15 min"
time_division = "timespan" # Select the time division mode. "timespan": to activate time_start and time_end; "2 parts": to activate part_nr; "weeks": to activate week_nr. None to cover the entire time of the data.
timespan_start, timespan_end = ["2023-08-23",  "2023-09-12"] # When time_division = "timespan" - Format: "YYYY-MM-DD"
division_nr= 1 # When: time_division = "2 parts" - 1 or 2, 11 days each part. When time_division = "weeks" - 1, 2 or 3
hour_start, hour_end = [7, 18] # Daily start and end hours
day_column, week_column = [True, True]


#--------------------------#
#     Results managing     #
#--------------------------#

interim_result_tables = False # Saves the interim result tables in the result/ folder
folder_suffix = None # Add an extra folder suffix to the results data folder and chart name. None to deactivate
file_suffix = None # Add an extra file suffix to the results data folder and chart name. None to deactivate
stat_save = True # Save a copy of the result grouped table in the stat folder 

#---------------------#

# Set to true for rectifying the data due to the ID-3 failure, creating a FAKE ID-3 by multiplying data of ID-4 *2
emend_id = False