import pandas as pd

def insect_data_process(parent_dir, start_datetime, end_datetime, minute_start, hour_start, hour_end, taxon, taxon_level, mainVariable, subVariable, device_type, extra_filter, extra_subfilter, All, time_freq, emend_id, relative_values):
    # Read the source folders
    insect_data = pd.read_excel(parent_dir + "/source_tables/id_faird.xlsx", sheet_name="Results", header=0, decimal=",")

    # Convert "Checkin" and "Time" columns to datetime
    insect_data["DateTime"] = pd.to_datetime(insect_data["Checkin"], format='%d.%m.%Y %H:%M', errors="coerce")

    # If False, the fake ID-3 data is deleted
    if not emend_id:
        insect_data = insect_data[insect_data["Device"] != "ID3"]

    # Create the new column "CheckinDate" with combined date and time
    insect_data = insect_data.sort_values(by="DateTime")

    # Filter by time window (timespan)
    insect_data_timespan = insect_data[(insect_data['DateTime'] >= start_datetime) & (insect_data['DateTime'] <= end_datetime)]
   
    # Delete data between hour_start and hour_end
    insect_data_timespan['Hour'] = insect_data_timespan['DateTime'].dt.hour
    insect_data_timespan = insect_data_timespan[(insect_data_timespan ['Hour'] >= hour_start) & (insect_data_timespan['Hour'] <= hour_end)]
    insect_data_timespan.drop('Hour', axis=1, inplace=True)

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
    dfp_filter_factor = dfg_filter_factor.pivot_table(index="DateTime", columns=mainVariable, values=taxon_level, aggfunc='sum')
    # Calculate row sums
    dfp_filter_factor['Total'] = dfp_filter_factor.sum(axis=1)

    # Calculate mainVariable in relative values
    if relative_values:
        # Calculate relative columns for each value in mainVariable
        for col in dfp_filter_factor.columns:
            if col != 'Total':
                dfp_filter_factor[f'{col}_relative'] = dfp_filter_factor[col] / dfp_filter_factor['Total']

                # Drop the old absolute value column
                dfp_filter_factor.drop(columns=[col], inplace=True)
                # Rename the new relative column without the "_relative" suffix
                new_col_name = col.replace('_relative', '')
                dfp_filter_factor.rename(columns={f'{col}_relative': new_col_name}, inplace=True)
    
    return dfp_filter_factor, dfg_filter_factor
   