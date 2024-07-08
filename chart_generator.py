import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from chart_config import * # Configuration variables
from src.dictionaries_control import *
from matplotlib.ticker import ScalarFormatter

# Load data
HOME = os.path.dirname(__file__)

if folder_sufix != None:
    folder_sufix = ("_" + folder_sufix)
else:
    folder_sufix = ""


if file_sufix != None:
    file_sufix = ("_" + file_sufix)
else:
    file_sufix = ""

hours = int(time_freq.split()[0])  # Extract the numeric value from time_freq
minute_start = hour_start * 60

# Handle cases when taxon = list
if not isinstance(taxon, list):
    taxon = [taxon]
if len(taxon) > 1:
    taxon_chart_title = ', '.join(taxon[:-1]) + f", and {taxon[-1]}"
else:
    taxon_chart_title = taxon[0]

if extra_subfilter != None:
    subfilter_name = extra_subfilter.replace(" ", "_")

if clima == True:
    # Define the folder name where the .csv tables are saved
    if extra_filter != None:
        folder_result_name = f"{'_'.join(taxon)}_{mainVariable}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{subfilter_name}_Clima_{hours}H{folder_sufix}" 
        file_result_name = f"{'_'.join(taxon)}_{mainVariable}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{subfilter_name}_Clima_{hours}H{file_sufix}"
        plt_title = (taxon_chart_title + " " + taxon_level + " count by " + mainVariable.replace("_", " ") + " (" + subVariable + ")" + " and by " +  extra_filter + " (" + extra_subfilter + ")" + " with Climatic Conditions")
    else:
        folder_result_name = f"{'_'.join(taxon)}_{mainVariable}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_Clima_{hours}H{folder_sufix}"
        file_result_name = f"{'_'.join(taxon)}_{mainVariable}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_Clima_{hours}H{file_sufix}"
        plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable.replace("_", " ")  + " (" + subVariable + ")" + " with Climatic Conditions")
else:
    if extra_filter != None:
       folder_result_name = f"{'_'.join(taxon)}_{mainVariable}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{subfilter_name}_{hours}H{folder_sufix}" 
       file_result_name = f"{'_'.join(taxon)}_{mainVariable}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{subfilter_name}_{hours}H{file_sufix}"
       plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable.replace("_", " ")  + " (" + subVariable + ")" + " and by " +  extra_filter + " (" + extra_subfilter + ")") 
    else:        
       # Define the folder name where the .csv tables are saved (without "_Clim")
       folder_result_name = f"{'_'.join(taxon)}_{mainVariable}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{hours}H{folder_sufix}"
       file_result_name = f"{'_'.join(taxon)}_{mainVariable}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{hours}H{file_sufix}"
       plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable.replace("_", " ")  + " (" + subVariable + ")")

# Create the folder if it doesn't exist
if not os.path.exists("results/" + folder_result_name):
    os.makedirs("results/" + folder_result_name, 0o777)

print("Data saved in: /results/"+ folder_result_name)

# Read the source folders
insect_data = pd.read_excel("source_tables/id_faird.xlsx", sheet_name="Results", header=0, decimal=",")
clim_data = pd.read_excel("source_tables/clim_data.xlsx", sheet_name="ClimData", header=0, decimal=",")

# Convert "Checkin" and "Time" columns to datetime
insect_data["DateTime"] = pd.to_datetime(insect_data["Checkin"], format='%d.%m.%Y %H:%M', errors="coerce")
clim_data["DateTime"] = pd.to_datetime(clim_data["Time"], format='%d.%m.%Y %H:%M', errors="coerce")

# If False, the fake ID-3 data is deleted
if emend_id != True:
    insect_data = insect_data[insect_data["Device"] != "ID-3"]

# Convert in clim_data any non-numeric value into numeric 
cols = clim_data.columns.drop('DateTime')
clim_data[cols] = clim_data[cols].apply(pd.to_numeric, errors='coerce')
# Replace NaN values with zeros
clim_data.fillna(0, inplace=True)

# Create the new column "CheckinDate" with combined date and time
insect_data = insect_data.sort_values(by="DateTime")

# Add hour_start, hour_end to time_start, time_end,
start_datetime = pd.to_datetime(time_start) + pd.to_timedelta(hour_start, unit='h')
end_datetime = pd.to_datetime(time_end) + pd.to_timedelta(hour_end, unit='h')

# Filter by time window (timespan)
if timespan == True:
    insect_data_timespan = insect_data[(insect_data['DateTime'] >= start_datetime) & (insect_data['DateTime'] <= end_datetime)]
    clim_data_timespan = clim_data[(clim_data['DateTime'] >= start_datetime) & (clim_data['DateTime'] <= end_datetime)]
else:
    insect_data_timespan = insect_data
    clim_data_timespan = clim_data

# Delete data between hour_start and hour_end
clim_data_timespan['Hour'] = clim_data_timespan['DateTime'].dt.hour
clim_data_timespan = clim_data_timespan[(clim_data_timespan ['Hour'] >= hour_start) & (clim_data_timespan['Hour'] <= hour_end)]
insect_data_timespan['Hour'] = insect_data_timespan['DateTime'].dt.hour
insect_data_timespan = insect_data_timespan[(insect_data_timespan ['Hour'] >= hour_start) & (insect_data_timespan['Hour'] <= hour_end)]

# Filter by taxon in the selected taxon level
insect_data_filtered = insect_data_timespan[insect_data_timespan[taxon_level].isin(taxon)]

# Filter by subvariable in the selected filter factor
if subVariable != All:
    insect_data_filtered = insect_data_filtered[insect_data_filtered[mainVariable] == subVariable]

# Filter by subfilter in the selected filter factor
if extra_filter != None:
   insect_data_filtered = insect_data_filtered[insect_data_filtered[extra_filter] == extra_subfilter]

# If device_type is set to All, all device_type are displayed
if device_type != All:
    insect_data_filtered = insect_data_filtered[insect_data_filtered["Device_type"] == device_type]


# Group by date (in a given time_freq) and by mainVariable
dfg_filter_factor = insect_data_filtered.groupby([pd.Grouper(key="DateTime", freq= time_freq, offset=f"{minute_start}T"), mainVariable])[taxon_level].count().reset_index()

# Make a pivot table with a column for each_filter_factor and insect count per day
#fp_filter_factor = dfg_filter_factor.pivot(index="DateTime", columns=mainVariable, values=taxon_level)
dfp_filter_factor = dfg_filter_factor.pivot_table(index="DateTime", columns=mainVariable, values=taxon_level, aggfunc='sum')
# Calculate row sums
dfp_filter_factor['Total'] = dfp_filter_factor.sum(axis=1)

# Calculate mainVariable in relative values
if relative_values == True:
# Calculate relative columns for each value in mainVariable
    for col in dfp_filter_factor.columns:
        if col != 'Total':
            dfp_filter_factor[f'{col}_relative'] = dfp_filter_factor[col] / dfp_filter_factor['Total']

            # Drop the old absolute value column
            dfp_filter_factor.drop(columns=[col], inplace=True)
                    # Rename the new relative column without the "_relative" suffix
            new_col_name = col.replace('_relative', '')
            dfp_filter_factor.rename(columns={f'{col}_relative': new_col_name}, inplace=True)

   
# Group by date (in a given time_freq) and by climatic variables
dfg_clim = clim_data_timespan.groupby(pd.Grouper(key="DateTime", freq= time_freq, offset=f"{minute_start}T")).agg({
    "AIRTEMP": "mean",
    "WINDSPEED": "mean",
    "PRECIPITATION": "sum",
    "RAD":"mean"
}).reset_index()

# Delete empty rows between hour_start and hour_end- if hours < 24 after clim data aggregation
if hours < 24:
    dfg_clim['Hour'] = dfg_clim['DateTime'].dt.hour
    dfg_clim = dfg_clim[(dfg_clim ['Hour'] >= hour_start) & (dfg_clim['Hour'] <= hour_end)]

# merge_filter_factor and climatic tables
merged_df =  pd.merge(dfp_filter_factor, dfg_clim, on="DateTime", how="outer")

# Set missing values to zero
merged_df.fillna(0, inplace=True)

# Sort merged_df by date
merged_df.sort_values(by="DateTime", inplace=True)

# Set the index to the "DateTime" column
merged_df.set_index("DateTime", inplace=True)

unique_main_variables = dfg_filter_factor[mainVariable].unique()

# Create an empty DataFrame for the ax1 table
ax1_merged_df = pd.DataFrame()

# Loop through each unique main variable
for var in unique_main_variables:
    # Extract the corresponding column from merged_df
    column_data = merged_df[var]
    # Assign it to the new DataFrame with the desired column name
    ax1_merged_df[var] = column_data


if result_tables == True:
    #insect_data.to_csv("results/" + folder_result_name + '/insect_data.csv', index=False)
    #clim_data.to_csv("results/" + folder_result_name + '/clim_data.csv', index=False)
    # Save the date and filter_factor group table to a CSV file
    dfg_filter_factor.to_csv("results/" + folder_result_name + "/" + file_result_name + '_filter_factors_group_table.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    # Save the filter_factor pivot table to a CSV file
    #dfp_filter_factor.to_csv("results/" + folder_result_name + "/" + folder_result_name +  '_filter_factor_count_table.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    # Save merged_data to a CSV file (adjust the file path as needed)
    #insect_data_filtered.to_csv("results/" + folder_result_name +  "/" + folder_result_name + '_insect_data_filtered.csv', index=False)
    # Save the date and cimatic group table to a CSV file
    #dfg_clim.to_csv("results/" + folder_result_name + "/" + file_result_name +  '_dfg_clim_table.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    # Save the merged table to a CSV file
    merged_df.to_csv("results/" + folder_result_name + "/" + file_result_name +  '_result_table.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    # Save the ax1_merged table to a CSV file
    #ax1_merged_df.to_csv("results/" + folder_result_name + "/" + folder_result_name +  '_ax1_merged_df_table.csv', index=True)
    

if create_chart == True:
    # Define colors based on conditions
    if mainVariable == "Ambient":
        colors = ["gold", "olivedrab"]
    elif device_type != All:
        colors = ["gold", "orange", "olivedrab", "yellowgreen"]
    elif device_type == All and mainVariable == "Site":
        colors = ["gold", "olivedrab", "orange", "yellowgreen"]
    elif extra_filter == "Site":
        if extra_subfilter == "Site 1" or extra_subfilter == "Site 2":
            colors = ["gold", "goldenrod"]
        elif extra_subfilter == "Site 3" or extra_subfilter == "Site 4":
            colors = ["yellowgreen", "olivedrab"]
    elif extra_filter == "Ambient":
        if extra_subfilter == "Maize Field":
            colors = ["gold", "goldenrod", "yellow", "orange"]
        elif extra_subfilter == "Meadow":
            colors = ["olivedrab","yellowgreen", "forestgreen", "lime"]        
    else:
        colors = None

    # Calculate the number of data points within the specified time_freq
    data_points = len(ax1_merged_df)


    # Set the bars width and the font based on the number of data points
    if data_points < 90:
        figwidth = 18
        fontsize = 8
    elif data_points > 130:
        figwidth = 26
        fontsize = 6
    else:
        figwidth = data_points/5
        fontsize = (720/data_points)

    #print("Data points:" + str(data_points))
    #print("Figure widht: " + str(figwidth))
    #print("Font size: " + str(fontsize))

    # Set the interval for the x-axis based on time_freq
    if hours >= 24:
        ax1 = ax1_merged_df.plot.bar(figsize=(figwidth, 8), legend=False, color=colors, alpha=0.7, fontsize=fontsize)
        ax1.set_xticklabels(ax1_merged_df.index.strftime("%Y-%m-%d"), rotation=45, ha="right")
    else:
        ax1 = ax1_merged_df.plot.bar(figsize=(figwidth, 8), legend=False, color=colors, alpha=0.7, fontsize=fontsize)
        ax1.set_xticklabels(ax1_merged_df.index.strftime("%Y-%m-%d %H:%M"), rotation=45, ha="right")


    # Y axis scaling options
    if fix_count_ylim == True:

        if log_scale == True:
            ax1.set_yscale("log")
            # Customize y-axis tick labels
            ax1.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
            # Calculate logarithmic values
            min_count_ylim = min_count_ylim + 1
            log_step = np.log10(max_count_ylim / min_count_ylim) / (num_ticks - 1)
            log_values = [min_count_ylim * 10**(i * log_step) for i in range(num_ticks)]
            # Round the logarithmic values to the nearest integer
            rounded_values = [int(round(val)) for val in log_values]
            # Set custom y-axis ticks
            ax1.set_yticks(rounded_values)
        else:
            ax1.set_ylim(min_count_ylim, max_count_ylim)
            tick_values = np.linspace(min_count_ylim, max_count_ylim, num_ticks)
            ax1.set_yticks(tick_values)
    else:
        if log_scale == True:
            ax1.set_yscale("log")
            ax1.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
            # Set the desired number of ticks (e.g., six ticks)
            tick_values = [10**i for i in range(num_ticks)]
            ax1.set_yticks(tick_values)
        else:
            y_values = ax1.get_yticks()
            tick_values = np.linspace(min(y_values), max(y_values), num_ticks).astype(int)
            ax1.set_yticks(tick_values)


                
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Insect Count", color="black") 
    ax1.tick_params(axis="y", labelcolor="black")
    ax1.set_facecolor("None") # Background of the axis transparent
    ax1.set_zorder(3) # Set the plotting order explicitly

        # Set y-axis scale to logarithmic
   
    if clima == True:
    
        # Create a single legend for all axes
        combined_handles, combined_labels = ax1.get_legend_handles_labels()
    

        if temperature == True:
            # Create a secondary y-axis for temperature
            ax2 = ax1.twinx()
            ax2.spines["right"].set_position(("outward", 60))  # Adjust the position of the third y-axis
                        
            if temp_smoothing == True:
                # Smooth the temperature data
                temp_x_values = np.arange(len(merged_df))
                temp_y_values = merged_df["AIRTEMP"]
                temp_xnew = np.linspace(temp_x_values.min(), temp_x_values.max(), x_points)  # Create a smoother x-axis
                temp_spl = make_interp_spline(temp_x_values, temp_y_values, k=k)  # Use cubic spline (adjust k as needed)
                temp_ynew = temp_spl(temp_xnew)
                # Plot the smoothed temperature curve
                ax2.plot(temp_xnew, temp_ynew, color="r", label="Temperature")
            else:
                # We use range(len(merged_df)) as the x-values to ensure alignment between the two DataFrames
                ax2.plot(range(len(merged_df)), merged_df["AIRTEMP"], color="r", label="Temperature") # Plotting without smooting
            
            if fix_temp_ylim == True:
                ax2.set_ylim(min_temp_ylim, max_temp_ylim)
            else:
                 ax2.set_ylim(0, max(merged_df["AIRTEMP"]) + 2)  # Adjust the utemper limit as needed

            ax2.set_ylabel("Temperature (°C)", color="r")
            ax2.tick_params(axis="y", labelcolor="r")
            ax2.set_facecolor("None")
            ax2.set_zorder(2)
            combined_handles.extend(ax2.get_legend_handles_labels()[0])
            combined_labels.extend(ax2.get_legend_handles_labels()[1])

        if wind_speed == True:        
            # Create a tertiary y-axis for wind speed
            ax3 = ax1.twinx()
            ax3.spines["right"].set_position(("outward", 120))  # Adjust the position of the third y-axis
                        
            if wind_smoothing == True:
                # Smooth the wind speed data
                wind_x_values = np.arange(len(merged_df))
                wind_y_values = merged_df["WINDSPEED"]
                wind_xnew = np.linspace(wind_x_values.min(), wind_x_values.max(), x_points)  # Create a smoother x-axis
                wind_spl = make_interp_spline(wind_x_values, wind_y_values, k=k)  # Use cubic spline (adjust k as needed)
                wind_ynew = wind_spl(wind_xnew)
                # Plot the smoothed wind curve
                ax3.plot(wind_xnew, wind_ynew, color="c", label="Wind Speed")
            else:
                ax3.plot(range(len(merged_df)), merged_df["WINDSPEED"], color="c", label="Wind Speed") # Plotting without smooting
            
            if fix_wind_ylim == True:
                ax3.set_ylim(min_wind_ylim, max_wind_ylim)
            else:
                 ax3.set_ylim(0, max(merged_df["WINDSPEED"]) + 2)  # Adjust the uwinder limit as needed

            ax3.set_ylabel("Wind Speed (m/s)", color="c")
            ax3.tick_params(axis="y", labelcolor="c")
            ax3.set_facecolor("None")
            ax3.set_zorder(1)
            combined_handles.extend(ax3.get_legend_handles_labels()[0])
            combined_labels.extend(ax3.get_legend_handles_labels()[1])

        if radiation == True:
            # Create a tertiary y-axis for radiation
            ax4 = ax1.twinx()
            ax4.spines["right"].set_position(("outward", 180))  # Adjust the position of the third y-axis
            
            if rad_smoothing == True:   
               # Smooth the solar radiation data
                rad_x_values = np.arange(len(merged_df))
                rad_y_values = merged_df["RAD"]
                rad_xnew = np.linspace(rad_x_values.min(), rad_x_values.max(), x_points)  # Create a smoother x-axis
                rad_spl = make_interp_spline(rad_x_values, rad_y_values, k=k)  # Use cubic spline (adjust k as needed)
                rad_ynew = rad_spl(rad_xnew)
                # Plot the smoothed raderature curve
                ax4.plot(rad_xnew, rad_ynew, color="darkorange", label="Solar radiation") 
            else:    
                ax4.plot(range(len(merged_df)), merged_df["RAD"], color="darkorange", label="Radiation")

            if fix_rad_ylim == True:
                ax4.set_ylim(min_rad_ylim, max_rad_ylim)
            else:
                 ax4.set_ylim(0, max(merged_df["RAD"]) + 20)  # Adjust the urader limit as needed
            
            ax4.set_ylabel("Radiation", color="darkorange")
            ax4.tick_params(axis="y", labelcolor="darkorange")
            ax4.set_facecolor("None")
            ax4.set_zorder(0)
            combined_handles.extend(ax4.get_legend_handles_labels()[0])
            combined_labels.extend(ax4.get_legend_handles_labels()[1])

        if precipitation == True:
                    # Plot the precipitation line and shaded area
                    ax5 = ax1.twinx()
                    ax5.fill_between(range(len(merged_df)), merged_df["PRECIPITATION"], color="lightskyblue", alpha=0.3, label="Precipitation")
                    ax5.set_ylabel("Precipitation", color="lightskyblue")
                    ax5.tick_params(axis="y", labelcolor="lightskyblue")
                    ax5.set_facecolor("None")
                    ax5.set_zorder(0)  # ax5 is plotted first
                    # Set the same y-axis limits for ax5
                    if fix_pp_ylim == True:
                        ax5.set_ylim(min_pp_ylim, max_pp_ylim)  # Adjust the upper limit as neede
                    else:
                        ax5.set_ylim(0, max(merged_df["PRECIPITATION"]) + 10)  # Adjust the upper limit as needed

                    combined_handles.append(ax5.fill_between(range(len(merged_df)), merged_df["PRECIPITATION"], color="lightskyblue", alpha=0.3))
                    combined_labels.append("Precipitation")
            
        # Create the main axis in the updated legend
        ax1.legend(combined_handles, combined_labels, loc="upper left", bbox_to_anchor=((-0.15, 1)))
        
    else:
        ax1.legend(loc="upper left", bbox_to_anchor=((-0.15, 1)))

    if plot_title == True:
        plt.title(plt_title)

    #plt.tight_layout()
    if save_chart == True:
        plt.savefig("results/" + folder_result_name + "/" + file_result_name + ".png", bbox_inches="tight")
    if display_chart == True:
        plt.show()