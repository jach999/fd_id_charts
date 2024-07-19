
import os
import pandas as pd
#from chart_config import * # Configuration variables

# Load data
HOME = os.path.dirname(__file__)

# Time
time_freq = "3 H" # The values ​​should be multiples or divisors of 24 plus a "H". Example: "12 H"
timespan = True # True to activate time_start and time_end, or False for covering the entire experiment time
time_start, time_end = ["2023-08-23",  "2023-09-13"] # Format: "YYYY-MM-DD"
hour_start, hour_end = [7, 18] # Daily start and end hours

hours = int(time_freq.split()[0])  # Extract the numeric value from time_freq
minute_start = hour_start * 60
start_datetime = pd.to_datetime(time_start) + pd.to_timedelta(hour_start, unit='h') # Add hour_start to time_start
end_datetime = pd.to_datetime(time_end) + pd.to_timedelta(hour_end, unit='h') # Add hour_end to time_end

# Read the source folders
clim_data = pd.read_excel("clim.xlsx", sheet_name="Clim", header=0, decimal=",")

# Time" columns to datetime
clim_data["DateTime"] = pd.to_datetime(clim_data["Time"], format='%d.%m.%Y %H:%M', errors="coerce")

# Convert in clim_data any non-numeric value into numeric 
cols = clim_data.columns.drop('DateTime')
clim_data[cols] = clim_data[cols].apply(pd.to_numeric, errors='coerce')
# Replace NaN values with zeros
clim_data.fillna(0, inplace=True)

# Filter by time window (timespan)
if timespan:
    clim_data_timespan = clim_data[(clim_data['DateTime'] >= start_datetime) & (clim_data['DateTime'] <= end_datetime)]
else:
    clim_data_timespan = clim_data

# Delete data between hour_start and hour_end
clim_data_timespan['Hour'] = clim_data_timespan['DateTime'].dt.hour
clim_data_timespan = clim_data_timespan[(clim_data_timespan ['Hour'] >= hour_start) & (clim_data_timespan['Hour'] <= hour_end)]
clim_data_timespan.drop('Hour', axis=1, inplace=True)

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
    dfg_clim.drop('Hour', axis=1, inplace=True)


dfg_clim.to_csv('/clim_data.csv', index=False)
