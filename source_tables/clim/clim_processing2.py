import os
import pandas as pd

# Load data
HOME = os.path.dirname(__file__)

# Time
time_freq = "15 min" # The values ​​should be multiples or divisors of 24 plus a "H". Example: "12 H"
timespan = False # True to activate time_start and time_end, or False for covering the entire experiment time
time_start, time_end = ["2023-08-23",  "2023-09-13"] # Format: "YYYY-MM-DD"
hour_start, hour_end = [7, 18] # Daily start and end hours

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
# clim_data_timespan['Hour'] = clim_data_timespan['DateTime'].dt.hour
# clim_data_timespan = clim_data_timespan[(clim_data_timespan ['Hour'] >= hour_start) & (clim_data_timespan['Hour'] <= hour_end)]
# clim_data_timespan.drop('Hour', axis=1, inplace=True)

clim_data_timespan.set_index("DateTime", inplace=True)

# Resample and interpolate
clim_data_resampled = clim_data_timespan.resample(time_freq, on=None).interpolate(method='linear')
clim_data_resampled.index = clim_data_resampled.index.strftime('%Y-%m-%d %H:%M:%S')
clim_data_resampled = clim_data_resampled.drop(columns=['Tag', 'Stunde', 'Time'])
clim_data_resampled.to_excel('clim_data_resampled.xlsx', index=True)


