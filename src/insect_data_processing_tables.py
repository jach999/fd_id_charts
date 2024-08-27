import pandas as pd

def insect_data_process_tables(parent_dir, time_freq, start_datetime, end_datetime, hour_start, hour_end, taxon, taxon_level, device_type, extra_filter, extra_subfilter, All, emend_id):
    # Read the source folders
    insect_data = pd.read_excel(parent_dir + "/source_tables/id_faird.xlsx", sheet_name="Results", header=0, decimal=",")

    # Convert "Checkin" column to datetime
    insect_data["DateTime"] = pd.to_datetime(insect_data["Checkin"], format='%d.%m.%Y %H:%M', errors="coerce")

    # If False, the fake ID-3 data is deleted
    if emend_id == False:
        insect_data = insect_data[insect_data["Device"] != "ID3"]

    # Create the new column "CheckinDate" with combined date and time
    insect_data = insect_data.sort_values(by="DateTime")

    # Filter by time window
    insect_data_timespan = insect_data[(insect_data['DateTime'] >= start_datetime) & (insect_data['DateTime'] <= end_datetime)].copy()

    # Delete data between hour_start and hour_end
    insect_data_timespan['Hour'] = insect_data_timespan['DateTime'].dt.hour
    insect_data_timespan = insect_data_timespan[(insect_data_timespan ['Hour'] >= hour_start) & (insect_data_timespan['Hour'] <= hour_end)]
    insect_data_timespan.drop('Hour', axis=1, inplace=True)

    # Filter by taxon in the selected taxon level
    insect_data_filtered = insect_data_timespan[insect_data_timespan[taxon_level].isin(taxon)]

      # Filter by subfilter in the selected filter factor
    if extra_filter != None:
       insect_data_filtered = insect_data_filtered[insect_data_filtered[extra_filter] == extra_subfilter]

    # If device_type is set to All, all device_type are displayed
    if device_type != All:
        insect_data_filtered = insect_data_filtered[insect_data_filtered["Device_type"] == device_type]

    # Create DataFrame
    insect_data_filtered = pd.DataFrame(insect_data_filtered)
    insect_data_filtered['DateTime'] = pd.to_datetime(insect_data_filtered['DateTime'])

    # Define a function to adjust the DateTime based on the given time frequency
    def adjust_datetime(dt, freq):
        base_time = pd.Timestamp(dt.date()) + pd.Timedelta(hours=hour_start)
        freq_timedelta = pd.Timedelta(freq)
        while base_time <= dt:
            base_time += freq_timedelta
        return base_time - freq_timedelta

    # Apply the function to adjust the DateTime
    insect_data_filtered['AdjustedDateTime'] = insect_data_filtered['DateTime'].apply(adjust_datetime, freq=time_freq)

    # Drop the original 'DateTime' column
    insect_data_filtered = insect_data_filtered.drop(columns=['DateTime'])

    # Rename the 'AdjustedDateTime' column to 'DateTime'
    insect_data_filtered = insect_data_filtered.rename(columns={'AdjustedDateTime': 'DateTime'})

    # Group by the adjusted DateTime and keep all rows
    dfg_insect = insect_data_filtered.groupby('DateTime').apply(lambda x: x).reset_index(drop=True)

    # Reorder columns to set 'DateTime' as the first column
    cols = ['DateTime'] + [col for col in dfg_insect.columns if col != 'DateTime']
    dfg_insect = dfg_insect[cols]
    
    return dfg_insect


   