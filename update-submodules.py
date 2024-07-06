import re


def revise_naming_convention():
    name_mapping = {
        "EnvFile1": "EnvFilePath",
        "Volume1": "AdditionalVolumeOption",
        "External": "ExternalVolumeNetwork",
        "External2": "ExternalConfig",
    }

    with open("./compose_viz/spec/compose_spec.py", "r") as spec_file:
        spec_content = spec_file.read()

    for origin_name, new_name in name_mapping.items():
        spec_content = re.sub(rf"\b{origin_name}\b", new_name, spec_content)

    with open("./compose_viz/spec/compose_spec.py", "w") as spec_file:
        spec_file.write(spec_content)

    print("Revised naming convention successfully!")


def update_version_number():
    with open("./compose_viz/__init__.py", "r") as init_file:
        init_content = init_file.read()

    version_number = init_content.split(" ")[-1].replace('"', "").strip()
    major, minor, patch = version_number.split(".")
    new_version_number = f"{major}.{minor}.{int(patch) + 1}"

    new_init_content = f"""__app_name__ = "compose_viz"
__version__ = "{new_version_number}"
"""

    with open("./compose_viz/__init__.py", "w") as init_file:
        init_file.write(new_init_content)

    with open("./pyproject.toml", "r") as pyproject_file:
        pyproject_content = pyproject_file.read()

    pyproject_content = pyproject_content.replace(version_number, new_version_number)

    with open("./pyproject.toml", "w") as pyproject_file:
        pyproject_file.write(pyproject_content)

    print(f"Version number updated to {new_version_number} successfully!")


if __name__ == "__main__":
    revise_naming_convention()
    update_version_number()
