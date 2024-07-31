import pandas as pd

def clim_data_process(parent_dir, time_freq, start_datetime, end_datetime, minute_start, hours, hour_start, hour_end):
    # Read the source folders
    clim_data = pd.read_excel(parent_dir + "/source_tables/clim_data.xlsx", sheet_name="ClimData", header=0, decimal=",")

    # Convert "Time" column to datetime
    clim_data["DateTime"] = pd.to_datetime(clim_data["Time"], format='%d.%m.%Y %H:%M', errors="coerce")

    # Convert in clim_data any non-numeric value into numeric 
    cols = clim_data.columns.drop('DateTime')
    clim_data[cols] = clim_data[cols].apply(pd.to_numeric, errors='coerce')
    # Replace NaN values with zeros
    clim_data.fillna(0, inplace=True)

    # Filter by time window
    clim_data_timespan = clim_data[(clim_data['DateTime'] >= start_datetime) & (clim_data['DateTime'] <= end_datetime)].copy()
   
    # Delete data between hour_start and hour_end
    clim_data_timespan['Hour'] = clim_data_timespan['DateTime'].dt.hour
    clim_data_timespan = clim_data_timespan[(clim_data_timespan ['Hour'] >= hour_start) & (clim_data_timespan['Hour'] <= hour_end)]
    clim_data_timespan.drop('Hour', axis=1, inplace=True)

    # Group by date (in a given time_freq) and by climatic variables
    dfg_clim = clim_data_timespan.groupby(pd.Grouper(key="DateTime", freq= time_freq, offset=f"{minute_start}T")).agg({
        "AIRTEMP": "mean",
        "WINDSPEED": "mean",
        "PRECIPITATION": "sum",
        "RAD":"mean",
        "GROUNDTEMP": "mean",
        "RH": "mean",
        "AIRP": "mean"
    }).reset_index()

    # Delete empty rows between hour_start and hour_end- if hours < 24 after clim data aggregation
    if hours < 24:
        dfg_clim['Hour'] = dfg_clim['DateTime'].dt.hour
        dfg_clim = dfg_clim[(dfg_clim ['Hour'] >= hour_start) & (dfg_clim['Hour'] <= hour_end)]
        dfg_clim.drop('Hour', axis=1, inplace=True)

    # Reorder columns to set 'DateTime' as the first column
    cols = ['DateTime'] + [col for col in dfg_clim.columns if col != 'DateTime']
    dfg_clim = dfg_clim[cols]
    
    return dfg_clim