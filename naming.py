def revise_naming_convention():
    name_mapping ={
        "EnvFile1" : "EnvFilePath",
        "Volume1" : "AdditionalVolumeOption",
        "External" : "ExternalVolumeNetwork",
        "External1" : "ExternalConfig",
    }

    spec_file = open("./compose_viz/spec/compose_spec.py", "r")

    for origin_name, new_name in name_mapping.items():
        spec_file.replace(origin_name, new_name)

    return


if __name__ == "__main__":
    
    revise_naming_convention()
    print("Revised naming convention successfully!")
    
    
    
    
    
    

