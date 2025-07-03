import os
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from chart_config import * # Configuration variables
from src.dictionaries import *
from src.dictionaries_control import *
from src.variables_handling import generate_time_variables, handle_strings
from src.insect_data_processing import insect_data_process
from src.clim_data_processing import clim_data_process
from src.labels import ecv_value_label, ecv_value_label_color, custom_colors
#from src.var_checker import variables_checker
from matplotlib.ticker import ScalarFormatter
import helpers

# Load data
HOME = os.path.dirname(__file__)
parent_dir= HOME

#print(extra_filter)
#print(mainVariable)

print()
print("##### Data settings #####")
print("-------------------------")
def main():
    # Call the variables_checker function
    # Validate each variable
    if not validate_time_division(time_division):
        return
    if not validate_mainVariable(mainVariable):
        return
    if not validate_subVariable(mainVariable, subVariable):
        return
    if not validate_device_type(device_type):
        return
    if not validate_taxon_level(taxon_level):
        return
    if not validate_extra_filter(extra_filter):
        return
    if not validate_extra_subfilter(extra_filter, extra_subfilter):
        return
    
    # Validate boolean variables
    if not validate_boolean_variables(boolean_variables):
        return
 
    print("\033[92m" + "All variables are valid." + "\033[0m")

if __name__ == "__main__":
    main()


# Generate time variables
hours, minute_start, start_datetime, end_datetime, timedelta = generate_time_variables(time_division, time_freq, hour_start, hour_end, timespan_start, timespan_end, division_nr)
# Generate strings
folder_result_name, file_result_name, plt_title, taxon, folder_suffix_string, file_suffix_string, time_suffix, time_freq_suffix, title_pad = handle_strings(clima, taxon, device_type, time_freq, folder_suffix, file_suffix, taxon_level, extra_filter, extra_subfilter, All, emend_id, time_division, timedelta, division_nr, device_type_options, mainVariable, subVariable, mainVariable_options, mainVariable_description)

print()
print("##### Time settings #####")
print("-------------------------")
print(time_suffix.replace("_", " ").strip() + ":")
print("Time start: "+ str(start_datetime))
print("Time end: "+ str(end_datetime))
print("Timedelta: " + str(timedelta))
print()
print("Data saved in: " + "\033[94m" + "/results/charts/"+ folder_result_name + "\033[0m")
print()

# Create the folder if it doesn't exist
if not os.path.exists("results/charts/" + folder_result_name):
    os.makedirs("results/charts/" + folder_result_name, 0o777)

# Process insect data and clima data functions
dfp_filter_factor, dfg_filter_factor = insect_data_process(parent_dir, start_datetime, end_datetime, minute_start, hour_start, hour_end, taxon, taxon_level, mainVariable, subVariable, device_type, extra_filter, extra_subfilter, All, time_freq, emend_id, relative_values)
dfg_clim = clim_data_process(parent_dir, time_freq, start_datetime, end_datetime, minute_start, hours, hour_start, hour_end)
   
# merge_filter_factor and climatic tables
merged_df =  pd.merge(dfp_filter_factor, dfg_clim, on="DateTime", how="outer")

# Set missing values to zero
merged_df.fillna(0, inplace=True)

# Sort merged_df by date
merged_df.sort_values(by="DateTime", inplace=True)

# Set the index to the "DateTime" column
merged_df.set_index("DateTime", inplace=True)

# Get unique main variables and sort them so that label colors are assigned consistently
unique_main_variables = sorted(dfg_filter_factor[mainVariable].unique())

# Create an empty DataFrame for the ax1 table
ax1_merged_df = pd.DataFrame()

# Create a dictionary for renaming columns
rename_dict = {}

# Loop through each unique main variable
for var in unique_main_variables:
    # Extract the variables descriptions
    description = mainVariable_options[mainVariable][var]
    # Extract the corresponding column from merged_df
    column_data = merged_df[var]
    # Assign it to the new DataFrame with the desired column name
    ax1_merged_df[var] = column_data
    # Add to rename dictionary
    rename_dict[var] = description

# Rename the columns using the description mapping
ax1_merged_df.rename(columns=rename_dict, inplace=True)


# Sort the column names alphabetically so that label colors are assigned consistently
ax1_merged_df = ax1_merged_df.sort_index(axis=1)

if result_tables == True:
    #insect_data.to_csv("results/charts/" + folder_result_name + '/insect_data.csv', index=False)
    dfg_clim.to_csv("results/charts/" + folder_result_name + '/clim_data.csv', index=False)
    # Save the date and filter_factor group table to a CSV file
    dfg_filter_factor.to_csv("results/charts/" + folder_result_name + "/" + file_result_name + '_filter_factors_group_table.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    # Save the filter_factor pivot table to a CSV file
    #dfp_filter_factor.to_csv("results/charts/" + folder_result_name + "/" + file_result_name +  '_filter_factor_count_table.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    # Save merged_data to a CSV file (adjust the file path as needed)
    #insect_data_filtered.to_csv("results/charts/" + folder_result_name +  "/" + file_result_name + '_insect_data_filtered.csv', index=False)
    # Save the date and cimatic group table to a CSV file
    #dfg_clim.to_csv("results/charts/" + folder_result_name + "/" + file_result_name +  '_dfg_clim_table.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    # Save the merged table to a CSV file
    merged_df.to_csv("results/charts/" + folder_result_name + "/" + file_result_name +  '_result_table.csv', index=True)  # Set index=True to include row labels (index) in the CSV
    # Save the ax1_merged table to a CSV file
    ax1_merged_df.to_csv("results/charts/" + folder_result_name + "/" + file_result_name +  '_ax1_merged_df_table.csv', index=True)
    
if create_chart == True:
    colors = [custom_colors.get(var, 'magenta') for var in unique_main_variables]
  
     # Calculate the number of data points within the specified time_freq
    data_points = len(ax1_merged_df)

    # Set the bars width and the font based on the number of data points
    figwidth,fontsize = SetBarsWithAndSize(data_points)

    #print("Data points:" + str(data_points))
    #print("Figure widht: " + str(figwidth))
    #print("Font size: " + str(fontsize))

    # Set the interval for the x-axis based on time_freq
    if hours >= 24:
        ax1 = ax1_merged_df.plot.bar(figsize=(figwidth, 8), legend=False, color=colors, alpha=0.7, fontsize=fontsize)
        ax1.set_xticklabels(ax1_merged_df.index.strftime("%Y-%m-%d"), rotation=45, ha="right")
        ax1.set_xlabel("Date")
    else:
        ax1 = ax1_merged_df.plot.bar(figsize=(figwidth, 10), legend=False, color=colors, alpha=0.7, fontsize=fontsize, width=0.8)
        ax1.set_xticklabels(ax1_merged_df.index.strftime("%H:%M"), rotation=45)
        x_axis = ax1.xaxis
        x_axis.label.set_visible(False) # Remove x-axis labels
        
        # Create secondary x-axis below the primary x-axis
        sec = ax1.secondary_xaxis('bottom')

        # Calculate the positions for the secondary ticks
        unique_days = ax1_merged_df.index.normalize().unique()
        day_positions = [(ax1_merged_df.index.get_indexer([day], method='nearest')[0] + ax1_merged_df.index.get_indexer([day + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)], method='nearest')[0]) / 2 for day in unique_days]
        
        # Set the secondary ticks and labels
        sec.set_xticks(day_positions)
        sec.set_xticklabels(unique_days.strftime("%d %b"), ha="center")

        # Adjust the position of the secondary x-axis
        sec.spines['bottom'].set_position(('outward', 50))
        sec.set_xlabel("Date", labelpad=8, fontsize=fontsize*1.4)

        # Remove the tick markers and horizontal lines from the secondary x-axis
        sec.tick_params(which='both', length=0)  # Set tick length to 0 to remove markers
        sec.spines['bottom'].set_visible(False)  # Hide the horizontal line (spine)

        # Set the fontsize of the secondary x-axis tick labels
        sec.tick_params(axis='x', labelsize=fontsize*1.2)


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
            rounded_values = [int(round(val)) for val in tick_values]
            # Set custom y-axis ticks
            ax1.set_yticks(rounded_values)
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


                
    
    ax1.set_ylabel("Insect Count", color="black", fontsize=fontsize*1.4) 
    ax1.tick_params(axis="y", labelcolor="black", labelsize=fontsize)
    ax1.set_facecolor("None") # Background of the axis transparent
    ax1.set_zorder(3) # Set the plotting order explicitly

        # Set y-axis scale to logarithmic
   
    if clima == True:
    
        # Create a single legend for all axes
        combined_handles, combined_labels = ax1.get_legend_handles_labels()
    

        if temperature == True:
            # Create a secondary y-axis for temperature
            ax2 = ax1.twinx()
                                    
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

            ax2.set_ylabel("Temperature (°C)", color="r", fontsize=fontsize*1.4)
            ax2.tick_params(axis="y", labelcolor="r", labelsize=fontsize)
            ax2.set_facecolor("None")
            ax2.set_zorder(2)
            combined_handles.extend(ax2.get_legend_handles_labels()[0])
            combined_labels.extend(ax2.get_legend_handles_labels()[1])

        if wind_speed == True:        
            # Create a tertiary y-axis for wind speed
            ax3 = ax1.twinx()
            ax3.spines["right"].set_position(("outward", 60))  # Adjust the position of the third y-axis
                        
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

            ax3.set_ylabel("Wind Speed (m/s)", color="c",fontsize=fontsize*1.4)
            ax3.tick_params(axis="y", labelcolor="c", labelsize=fontsize)
            ax3.set_facecolor("None")
            ax3.set_zorder(1)
            combined_handles.extend(ax3.get_legend_handles_labels()[0])
            combined_labels.extend(ax3.get_legend_handles_labels()[1])

        if extra_clim_variable == True:
            # Use ecv_value to look up the label in the dictionary
            ecv_label = ecv_value_label[ecv_value]
             # Use ecv_value to look up the label color in the dictionary
            ecv_label_color = ecv_value_label_color[ecv_value]
            # Create a tertiary y-axis for the extra climatic variable
            ax4 = ax1.twinx()
            ax4.spines["right"].set_position(("outward", 180))  # Adjust the position of the third y-axis
            
            if ecv_smoothing == True:   
               # Smooth the extra climatic variable data
                ecv_x_values = np.arange(len(merged_df))
                ecv_y_values = merged_df[ecv_value]
                ecv_xnew = np.linspace(ecv_x_values.min(), ecv_x_values.max(), x_points)  # Create a smoother x-axis
                ecv_spl = make_interp_spline(ecv_x_values, ecv_y_values, k=k)  # Use cubic spline (adjust k as needed)
                ecv_ynew = ecv_spl(ecv_xnew)
                # Plot the smoothed ecv curve
                ax4.plot(ecv_xnew, ecv_ynew, color=ecv_label_color, label=ecv_label) 
            else:    
                ax4.plot(range(len(merged_df)), merged_df[ecv_value], color=ecv_label_color, label=ecv_label)

            if fix_ecv_ylim == True:
                ax4.set_ylim(min_ecv_ylim, max_ecv_ylim)
            else:
                 ax4.set_ylim(0, max(merged_df[ecv_value]) + 20)  # Adjust the urader limit as needed
            
            ax4.set_ylabel(ecv_label, color=ecv_label_color,fontsize=fontsize*1.4)
            ax4.tick_params(axis="y", labelcolor=ecv_label_color, labelsize=fontsize)
            ax4.set_facecolor("None")
            ax4.set_zorder(0)
            combined_handles.extend(ax4.get_legend_handles_labels()[0])
            combined_labels.extend(ax4.get_legend_handles_labels()[1])

        if precipitation == True:
                    # Plot the precipitation line and shaded area
                    ax5 = ax1.twinx()
                    ax5.spines["right"].set_position(("outward", 120)) 
                    ax5.fill_between(range(len(merged_df)), merged_df["PRECIPITATION"], color="lightskyblue", alpha=0.3, label="Precipitation")
                    ax5.set_ylabel("Precipitation", color="lightskyblue", fontsize=fontsize*1.4)
                    ax5.tick_params(axis="y", labelcolor="lightskyblue", labelsize=fontsize)
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
        #ax1.legend(combined_handles, combined_labels, loc="upper left", bbox_to_anchor=((-0.18, 1)))
        ax1.legend(combined_handles, combined_labels, loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=8, fontsize=fontsize) 

    else:
        ax1.legend(loc="upper left", bbox_to_anchor=((-0.18, 1)))

    if plot_title == True:
        plt.title(plt_title, fontsize=20, linespacing=2, pad=title_pad)

    #plt.tight_layout()
    if save_chart == True:
        plt.savefig("results/charts/" + folder_result_name + "/" + file_result_name + ".png", bbox_inches="tight")
    if display_chart == True:
        plt.show()