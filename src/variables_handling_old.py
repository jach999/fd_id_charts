
import pandas as pd

def generate_time_variables(time_freq, time_start, time_end, hour_start, hour_end):
    hours = int(time_freq.split()[0])  # Extract the numeric value from time_freq
    minute_start = hour_start * 60
    start_datetime = pd.to_datetime(time_start) + pd.to_timedelta(hour_start, unit='h') # Add hour_start to time_start
    end_datetime = pd.to_datetime(time_end) + pd.to_timedelta(hour_end, unit='h') # Add hour_end to time_end
    return hours, minute_start, start_datetime, end_datetime


def handle_strings(clima, taxon, mainVariable, subVariable, device_type, hours, folder_sufix, file_sufix, taxon_level, extra_filter, extra_subfilter, All):

    if folder_sufix != None:
        folder_sufix = ("_" + folder_sufix)
    else:
        folder_sufix = ""


    if file_sufix != None:
        file_sufix = ("_" + file_sufix)
    else:
        file_sufix = ""    
    
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
            folder_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{subfilter_name}_Clima_{hours}H{folder_sufix}" 
            file_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{subfilter_name}_Clima_{hours}H{file_sufix}"
            plt_title = (taxon_chart_title + " " + taxon_level + " count by " + mainVariable.replace("_", " ") + " (" + subVariable + ")" + " and by " +  extra_filter + " (" + extra_subfilter + ")" + " with Climatic Conditions")
        else:
            folder_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_Clima_{hours}H{folder_sufix}"
            file_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_Clima_{hours}H{file_sufix}"
            plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable.replace("_", " ")  + " (" + subVariable + ")" + " with Climatic Conditions")
    else:
        if extra_filter != None:
            folder_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{subfilter_name}_{hours}H{folder_sufix}" 
            file_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{subfilter_name}_{hours}H{file_sufix}"
            plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable.replace("_", " ")  + " (" + subVariable + ")" + " and by " +  extra_filter + " (" + extra_subfilter + ")") 
        else:        
            # Define the folder name where the .csv tables are saved (without "_Clim")
            folder_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{hours}H{folder_sufix}"
            file_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{hours}H{file_sufix}"
            plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable.replace("_", " ")  + " (" + subVariable + ")")
    return folder_result_name, file_result_name, plt_title, taxon, folder_sufix, file_sufix
