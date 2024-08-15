# Dictionaries for valid values

'''time_freq_options = {
    "2 H": "Every 2 hours",
    "6 H": "Every 6 hours",
    "12 H": "Every 12 hours",
    "24 H": "Every 24 hours",
    "48 H": "Every 48 hours"
}'''

time_division_options = {
    "timespan": "select time start and end period",
    "2 parts": "divide into 2 equal parts",
    "weeks": "divide into 3 weeks"
}

mainVariable_options = {
    "Ambient": {
        "All": "Maize Field and Meadow",
        "Maize": "Maize Field",
        "Meadow": "Meadow"
    },
    "Device_type": {
        "All": "FAIR-Device and Insect Detect",
        "FAIRD": "FAIR-Device",
        "ID": "Insect Detect"
    },
    "Device": {
        "All": "FAIR-Device 1, 2, 3, and 4 Insect Detect 1, 2, and 4",
        "FAIRD1": "FAIR-Device 1",
        "FAIRD2": "FAIR-Device 2",
        "FAIRD3": "FAIR-Device 3",
        "FAIRD4": "FAIR-Device 4",
        "ID1": "Insect Detect 1",
        "ID2": "Insect Detect 2",
        "ID3": "Insect Detect 3",
        "ID4": "Insect Detect 4"
    },
    "Site": {
        "All": "All Sites",
        "Site1": "Site 1",
        "Site2": "Site 2",
        "Site3": "Site 3",
        "Site4": "Site 4"
    },
    "DevicexAmbient": {
        "All": "Device Type in Ambient",
        "FAIRDxMaize": "FAIR-Device in Maize Field",
        "FAIRDxMeadow": "FAIR-Device in Meadow",
        "IDxMaize": "Insect Detect in Maize Field",
        "IDxMeadow": "Insect Detect in Meadow"
    }

}


mainVariable_description = {
    "Ambient": "Ambient",
    "Device_type": "Device Type",
    "Device": "Device",
    "Site": "Site",
    "DevicexAmbient": "Device and by Ambient"
}


device_type_options = {
    "All": "FAIR-Device and Insect Detect",
    "FAIRD": "FAIR-D",
    "ID": "Insect Detect"
}

taxon_level_options = {
    "Class": "Class level",
    "Order": "Order level",
    "Suborder": "Suborder level",
    "Superfamily": "Superfamily level",
    "Family": "Family level",
    "Subfamily": "Subfamily level",
    "Genus": "Genus level"
}

extra_filter_options = {
    "Ambient": {
        "Maize": "Maize field conditions",
        "Meadow": "Meadow conditions"
    },
    "Device_type": {
        "FAIRD": "FAIR-Device",
        "ID": "Insect Detect"
    },
    "Device": {
        "FAIRD1": "FAIR-Device 1",
        "FAIRD2": "FAIR-Device 2",
        "FAIRD3": "FAIR-Device 3",
        "FAIRD4": "FAIR-Device 4",
        "ID1": "Insect Detect 1",
        "ID2": "Insect Detect 2",
        "ID3": "Insect Detect 3",
        "ID4": "Insect Detect 4"
    },
    "Site": {
        "Site1": "Site 1",
        "Site2": "Site 2",
        "Site3": "Site 3",
        "Site4": "Site 4"
    }
}

boolean_variables = [
    "clima",
    "temperature",
    "temp_smoothing",
    "wind_speed",
    "wind_smoothing",
    "extra_clim_variable",
    "ecv_smoothing",
    "precipitation",
    "result_tables",
    "create_chart",
    "save_chart",
    "display_chart",
    "plot_title",
    "emend_id"
]


# Example usage
variable = mainVariable_options
category = "Ambient"
subkey = "Maize"
test = variable[category][subkey]
print(test)