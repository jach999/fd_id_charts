All = "All"


#-------------------------#
#      Data settings      #
#-------------------------#

# Modify these factors to display different info in the charts
mainVariable = "Device x Ambient" # "Device_type", "Device", "Ambient", "Site", and "Devixe x Ambient"
subVariable = All #  Set to All to show all. In "Device_type": FAIR-D or "ID"; in "Device": FAIR-D1 -D2, -D3, or -D4, ID1, ID2, ID4; in "Ambient": "Maize Field" or "Meadow"; in "Site": "Site 1", "Site 2", "Site 3", "Site 4"; in "Device x Ambient": “FAIR-D - Maize Field”, “FAIR-D - Meadow”, “ID - Maize Field”, “ID - Meadow”
device_type = "FAIR-D" # Set to All to show all devices, or choose between "FAIR-D" or "ID"
taxon_level = "Class" # "Class", "Order", "Suborder", "Family", "Subfamily", "Genus"
taxon = "Insecta" # Acording the selected taxon_level, the desired taxon. If more than one is wanted:["taxon1","taxon2", ...] - Example for taxon_level = "Order": ["Diptera", "Coleoptera", "Hymenoptera"] 

# Additional filter
extra_filter = None # None for not adding an additional filter. Same settings as in "mainVariable"
extra_subfilter = "Site 1" # Same settings as in "subvariable". If extra_filter = None, extra_subfilter does nothing.


#-------------------------#
#      Time settings      #
#-------------------------#

time_freq = "3 H" # The values ​​should be multiples or divisors of 24 hours or 60 min and have time units. Example: "12 H" or "15 min"
time_division = "weeks" # Select the time division mode. "timespan": to activate time_start and time_end; "2 parts": to activate part_nr; "weeks": to activate week_nr. None to cover the entire time of the data.
time_start, time_end = ["2023-08-23",  "2023-09-12"] # When time_division = "timespan" - Format: "YYYY-MM-DD"
part_nr = 2 # When: time_division = "2 parts" - 1 or 2, 11 days each part
week_nr = 2 # When time_division = "weeks" - 1, 2 or 3
hour_start, hour_end = [7, 18] # Daily start and end hours


#-------------------------------#
#     Chart display options     #
#-------------------------------#

plot_title = True # Plot automatic generated plot title

# # Insect count Y-axis scaling options
log_scale = False # Activate Y-axis logarithmic scale
fix_count_ylim = False # True activates min and max Y-axis values
min_count_ylim, max_count_ylim = [0, 300]
num_ticks = 7 # Num of Y-axis ticks if 

# Climatic variables
clima = True # Activate temperature, windspeed, precipitation and solar radiaion for adding to the chart (True/False)

temperature, temp_smoothing, fix_temp_ylim = [True, True, True] # First option from the list: True to display the climatic variable on the chart. Second option: True to smooth the displayed line. Third option: activates the Y-axis limits min_temp_ylim and max_temp_ylim
min_temp_ylim, max_temp_ylim = [0, 40] # Defines the lower and upper limit of the Y-axis

wind_speed, wind_smoothing, fix_wind_ylim = [True, True, True] 
min_wind_ylim, max_wind_ylim = [0, 14]

precipitation, fix_pp_ylim = [True, True] 
min_pp_ylim, max_pp_ylim = [0, 15]

extra_clim_variable, ecv_value, ecv_smoothing, fix_ecv_ylim = [False, "RAD", True, True] # extra_clim_variable,: True for activating an extra climatic variable. ecv_value: "RAD" for displaying "Solar Radiation", "RH" for "Relative Humidity","GROUNDTEMP" for "Ground Temperature", and "AIRP" for "Air Pressure"
min_ecv_ylim, max_ecv_ylim = [900, 1050]

# Smoothing settings
x_points = 200 # New curve points
k = 2 # Smoothing factor


#--------------------------#
#     Results managing     #
#--------------------------#

result_tables = False # Saves the interim result tables in the result/ folder
create_chart = True # Activates the save_chart and display_chart options
save_chart = True # Save chart .png file in the result/ folder
display_chart = False # Display the generated chart in a new window
folder_sufix = None # Add an extra folder sufix to the results data folder and chart name. None to deactivate
file_sufix = None # Add an extra file sufix to the results data folder and chart name. None to deactivate

#---------------------#

# Set to true for rectifying the data due to the ID-3 failure, creating a FAKE ID-3 by multiplying data of ID-4 *2
emend_id = False

# Experimental
relative_values = False