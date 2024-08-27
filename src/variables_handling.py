
import pandas as pd
from datetime import datetime

def generate_time_variables(time_division, time_freq, hour_start, hour_end, timespan_start, timespan_end, division_nr):
   
    if time_division == False:
        timespan_start = "2023-08-23"
        timespan_end = "2023-09-13"
    elif time_division== "2 parts":
        if division_nr == 1:
            timespan_start = "2023-08-23"
            timespan_end = "2023-09-02"
        elif division_nr == 2:
            timespan_start = "2023-09-03"
            timespan_end = "2023-09-13"
    elif time_division== "weeks":
        if division_nr == 1:
            timespan_start = "2023-08-23"
            timespan_end = "2023-08-29"
        elif division_nr == 2:
            timespan_start = "2023-08-30"
            timespan_end = "2023-09-05"
        elif division_nr == 3:
            timespan_start = "2023-09-06"
            timespan_end = "2023-09-12"

    
    freq, unit = time_freq.split()

    if unit == 'H':
        hours = int(freq)
    elif unit == 'min':
        hours = int(freq) / 60
        
    minute_start = hour_start * 60
    start_datetime = pd.to_datetime(timespan_start) + pd.to_timedelta(hour_start, unit='h') # Add hour_start to timespan_start
    end_datetime = pd.to_datetime(timespan_end) + pd.to_timedelta(hour_end, unit='h') # Add hour_end to timespan_end
    timedelta = datetime.strptime(timespan_end, "%Y-%m-%d") - datetime.strptime(timespan_start, "%Y-%m-%d")
    timedelta = timedelta.days + 1
    return hours, minute_start, start_datetime, end_datetime, timedelta


def handle_strings(clima, taxon, device_type, time_freq, folder_sufix, file_sufix, taxon_level, extra_filter, extra_subfilter, All, emend_id, time_division, timedelta, division_nr, device_type_options, mainVariable=None, subVariable=None, mainVariable_options=None, mainVariable_description=None):

    mainVariable = mainVariable if mainVariable else ""
    subVariable = subVariable if subVariable else ""
    mainVariable_options = mainVariable_options if mainVariable_options else ""
    mainVariable_description = mainVariable_description if mainVariable_description else ""

    if mainVariable != "":
        if mainVariable == "DevicexAmbient":
            if subVariable != All:
                mainVariable_string = mainVariable_description[mainVariable]
                subVariable_string = " (" + mainVariable_options[mainVariable][subVariable] + ") "
            else:
                mainVariable_string =  mainVariable_description[mainVariable]
                subVariable_string = " (" + device_type_options[device_type] + " in Maize Field and Meadow" + ") " 
        else:
            mainVariable_string = mainVariable_description[mainVariable]
            subVariable_string = " (" + mainVariable_options[mainVariable][subVariable] + ") "
    else:
        mainVariable_string = ""
        subVariable_string = ""  


    if folder_sufix != None:
        folder_sufix = ("_" + folder_sufix)
    else:
        folder_sufix = ""

    time_freq_sufix = time_freq.replace(' ', '') 
    
    if time_division != None:
        if time_division == "timespan":
            time_sufix = "_" + str(timedelta) + "_days"
        if time_division == "2 parts":
            time_sufix = "_part_" + str(division_nr)
        elif time_division == "weeks":
            time_sufix = "_week_" + str(division_nr)    

            
    if time_division != None:
        if time_division == "timespan":
            time_chart_title = ""
            title_pad = 35
        if time_division == "2 parts":
            time_chart_title = "\n - Part " + str(division_nr) + " -"
            title_pad = 45
        elif time_division == "weeks":
            time_chart_title = "\n - Week " + str(division_nr) + " -"   
            title_pad = 45

    if file_sufix != None:
        file_sufix = ("_" + file_sufix)
        if time_division != None:
            file_sufix = time_sufix + "_" + file_sufix
            if emend_id:
                file_sufix = "_emend_" + file_sufix
    else:
        if time_division != None:
            file_sufix = time_sufix 
            if emend_id:
                file_sufix = "_emend_" + file_sufix
        else:
            if emend_id:
                file_sufix= "emend"
            else:
                file_sufix = ""    
    
    # Handle cases when taxon = list
    if not isinstance(taxon, list):
        taxon = [taxon]
    if len(taxon) > 1:
        taxon_chart_title = ', '.join(taxon[:-1]) + f", and {taxon[-1]}"
    else:
        taxon_chart_title = taxon[0]

         
    if clima == True:
        # Define the folder name where the .csv tables are saved
        if extra_filter != None:
            folder_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{extra_subfilter.replace(' ', '_')}_Clima_{time_freq.replace(' ', '')}{folder_sufix}" 
            file_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{extra_subfilter.replace(' ', '_')}_Clima_{time_freq.replace(' ', '')}{file_sufix}"
            plt_title = (taxon_chart_title + " " + taxon_level + " count by " + mainVariable_string + subVariable_string + "and by " +  extra_filter + " (" + extra_subfilter + ")" + " with Climatic Conditions" + time_chart_title)
        else:
            folder_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_Clima_{time_freq.replace(' ', '')}{folder_sufix}"
            file_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_Clima_{time_freq.replace(' ', '')}{file_sufix}"
            plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable_string + subVariable_string + "with Climatic Conditions"  + time_chart_title)
    else:
        if extra_filter != None:
            folder_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{extra_subfilter.replace(' ', '_')}_{time_freq.replace(' ', '')}{folder_sufix}" 
            file_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{extra_subfilter.replace(' ', '_')}_{time_freq.replace(' ', '')}{file_sufix}"
            plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable_string + subVariable_string + "and by " +  extra_filter + " (" + extra_subfilter + ")"  + time_chart_title) 
        else:        
            # Define the folder name where the .csv tables are saved (without "_Clim")
            folder_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{time_freq.replace(' ', '')}{folder_sufix}"
            file_result_name = f"{'_'.join(taxon)}_{mainVariable.replace(' ', '_')}{'_' + subVariable if subVariable != All else ''}{'_' + device_type if device_type != All else ''}_{time_freq.replace(' ', '')}{file_sufix}"
            plt_title = (taxon_chart_title + " " + taxon_level + " count by " +  mainVariable_string  + subVariable_string  + time_chart_title)
   
    return folder_result_name, file_result_name, plt_title, taxon, folder_sufix, file_sufix, time_sufix, time_freq_sufix, title_pad