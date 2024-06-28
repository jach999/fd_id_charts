'''from dictionaries import *

# Determine valid subVariables based on the selected mainVariable
def get_valid_subVariables(mainVariable):
    if mainVariable in mainVariable_options:
        return list(mainVariable_options[mainVariable].keys())
    else:
        return []


# Determine valid subVariables based on the selected mainVariable
def get_valid_extra_subfilters(extra_filter):
    if extra_filter in extra_filter_options:
        return list(extra_filter_options[extra_filter].keys())
    else:
        return []


# Prompt user for input
def get_valid_input(prompt, options_list):
    while True:
        print(f"Valid options for {prompt}: {', '.join(options_list)}")
        user_input = input(f"Enter {prompt}: ").strip()
        if user_input in options_list:
            return user_input
        else:
            print("Invalid input. Please choose a valid option.")

# Validate boolean input
def get_valid_boolean_input(prompt):
    while True:
        user_input = input(f"Enter {prompt} (True/False): ").strip().lower()
        if user_input in ["true", "false"]:
            return user_input == "true"
        else:
            print("Invalid input. Please enter True or False.")


# Get user input for subVariable
mainVariable = input("Enter mainVariable: ")
valid_subVariables = get_valid_subVariables(mainVariable)
subVariable = get_valid_input("subVariable", valid_subVariables)
extra_filter = input("Enter extra_filter: ")
valid_extra_subfilters = get_valid_extra_subfilters(extra_filter)
extra_subfilter = get_valid_input("extra_subfilter", valid_extra_subfilters)
device_type = get_valid_input("device_type", device_type_options)
taxon_level = get_valid_input("taxon_level", taxon_level_options)

# Get user input for boolean variables
clima = get_valid_boolean_input("clima")
temperature = get_valid_boolean_input("temperature")
temp_smoothing = get_valid_boolean_input("temp_smoothing")
wind_speed = get_valid_boolean_input("wind_speed")
wind_smoothing = get_valid_boolean_input("wind_smoothing")
radiation = get_valid_boolean_input("radiation")
rad_smoothing = get_valid_boolean_input("rad_smoothing")
precipitation = get_valid_boolean_input("precipitation")'''

from chart_config import *
from src.dictionaries import *

# Validate mainVariable
def is_valid_mainVariable(mainVariable):
    return mainVariable in mainVariable_options

# Validate subVariable
def is_valid_subVariable(mainVariable, subVariable):
    return subVariable in mainVariable_options.get(mainVariable, {})

# Validate device_type
def is_valid_device_type(device_type):
    return device_type in device_type_options

# Validate taxon_level
def is_valid_taxon_level(taxon_level):
    return taxon_level in taxon_level_options

# Validate extra_filter
def is_valid_extra_filter(extra_filter):
    return extra_filter in extra_filter_options or extra_filter is None

# Validate extra_subfilter
def is_valid_extra_subfilter(extra_filter, extra_subfilter):
    if extra_filter is None:
        return True  # Any value is valid when extra_filter is None
    return extra_subfilter in extra_filter_options.get(extra_filter, {})

def validate_boolean_variables():
    boolean_variables = [
        "clima",
        "temperature",
        "temp_smoothing",
        "wind_speed",
        "wind_smoothing",
        "radiation",
        "rad_smoothing",
        "precipitation",
        "result_tables",
        "create_chart",
        "save_chart",
        "display_chart",
        "plot_title",
        "emend_id"
    ]

    for var_name in boolean_variables:
        var_value = globals().get(var_name)
        if not isinstance(var_value, bool):
            print(f"Error: {var_name} is not a boolean variable.")
            return False

    print("All boolean variables are valid.")
    return True

# Control the variables

validate_boolean_variables()

if is_valid_mainVariable(mainVariable):
    print(f"Selected mainVariable: {mainVariable}")
else:
    print("Invalid mainVariable. Please choose a valid option.")

if is_valid_subVariable(mainVariable, subVariable):
    print(f"Selected subVariable: {subVariable}")
else:
    print("Invalid subVariable. Please choose a valid option.")

if is_valid_device_type(device_type):
    print(f"Selected device type: {device_type}")
else:
    print("Invalid device type. Please choose a valid option.")

if is_valid_taxon_level(taxon_level):
    print(f"Selected taxon level: {taxon_level}")
else:
    print("Invalid taxon level. Please choose a valid option.")

    print((f"Selected taxon: {taxon}"))

if is_valid_extra_filter(extra_filter):
    print(f"Selected extra filter: {extra_filter}")
else:
    print("Invalid extra filter. Please choose a valid option.")

if is_valid_extra_subfilter(extra_filter, extra_subfilter):
    if extra_filter == None:
        print("Selected extra subfilter: None")
    else:
        print(f"Selected extra subfilter: {extra_subfilter}")
else:
    if extra_subfilter == All:
        print ("Invalid extra subfilter: All is not acceped, you must specify a valid option")
    else:
        print("Invalid extra subfilter: Please choose a valid option.")


