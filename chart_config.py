All = "All"

#---------------------#

# Time
time_freq = "24 H" # The values ​​should be multiples or divisors of 24 plus a "H". Example: "12 H"
timespan = True # True to activate time_start and time_end, or False for covering the entire experiment time
#time_start, time_end = ["2023-08-23",  "2023-09-01"] # Format: "YYYY-MM-DD"
hour_start, hour_end = [6, 19] # Daily start and end hours

#---------------------#

# Modify these factors to display different info in the charts
mainVariable = "Device" # "Device_type", "Device", "Ambient", "Site"
subVariable = All #  Set to All to show all. In "Device_type": FAIR-D or "ID"; in "Device": FAIR-D1 -D2, -D3, or -D4, ID1, ID2, ID4; in "AmbienT": "Maize Field" or "Meadow"; in "Site": "Site 1", "Site 2", "Site 3", "Site 4" 
device_type = All # Set to All to show all devices, or choose between "FAIR-D" or "ID"
taxon_level = "Class" # "Class", "Order", "Suborder", "Family", "Subfamily", "Genus"
taxon = "Insecta" # Acording the selected taxon_level, the desired taxon. If more than one is wanted:["taxon1","taxon2", ...] - Example for taxon_level = "Order": ["Diptera", "Coleoptera", "Hymenoptera"] 

# Additional filter
extra_filter = "Site" # None for not adding an additional filter. Same settings as in "mainVariable"
extra_subfilter = "Site 1" # Same settings as in "subvariable". If extra_filter = None, extra_subfilter does nothing.

#---------------------#

# # Y-axis scaling options
log_scale = True # Activate Y-axis logarithmic scale
fix_count_ylim = True # True activates min and max Y-axis values
min_count_ylim, max_count_ylim = [0, 200]
num_ticks = 7 # Num of Y-axis ticks if 

# Climatic variables
clima = True # Activate temperature, windspeed, precipitation and solar radiaion for adding to the chart (True/False)

temperature, temp_smoothing, fix_temp_ylim = [True, True, True] # First option from the list: True to display the climatic variable on the chart. Second option: True to smooth the displayed line. Third option: activates the Y-axis limits min_temp_ylim and max_temp_ylim
min_temp_ylim, max_temp_ylim = [0, 40] # Defines the lower and upper limit of the Y-axis

wind_speed, wind_smoothing, fix_wind_ylim = [True, True, True] 
min_wind_ylim, max_wind_ylim = [0, 14]

radiation, rad_smoothing, fix_rad_ylim = [False, True, True] 
min_rad_ylim, max_rad_ylim = [0, 600]

precipitation, fix_pp_ylim = [True, True] 
min_pp_ylim, max_pp_ylim = [0, 10]

# Smoothing settings
x_points = 200 # New curve points
k = 2 # Smoothing factor

#---------------------#

# Results managing
result_tables = True # Saves the interim result tables in the result/ folder
create_chart = True # Activates the save_chart and display_chart options
save_chart = True # Save chart .png file in the result/ folder
display_chart = False # Display the generated chart in a new window
folder_sufix = None # Add an extra folder sufix to the results data folder and chart name. None to deactivate
#file_sufix = None # Add an extra file sufix to the results data folder and chart name. None to deactivate
#plot_title = True # Plot automatic generated plot title

#---------------------#

# Quick options for generating Part 1 and Part 2 charts. Please before using this outcomment time_start, time_end, file_sufix, and plot_title from the upper configurations
time_start, time_end, file_sufix, plot_title = ["2023-08-23",  "2023-09-01", "Part_1", True] 
#time_start, time_end, file_sufix, plot_title = ["2023-09-02", "2023-09-13", "Part_2", False]

#---------------------#

# Set to true for rectifying the data due to the ID-3 failure, creating a FAKE ID-3 by multiplying data of ID-4 *2
emend_id = True

# Experimental
relative_values = False