import re


def revise_naming_convention():
    name_mapping = {
        "EnvFile1": "EnvFilePath",
        "Volume1": "AdditionalVolumeOption",
        "External": "ExternalVolumeNetwork",
        "External2": "ExternalConfig",
    }

    spec_content: str
    with open("./compose_viz/spec/compose_spec.py", "r+") as spec_file:
        spec_content: str = spec_file.read()

        for origin_name, new_name in name_mapping.items():
            spec_content = re.sub(rf"\b{origin_name}\b", new_name, spec_content)

        spec_file.seek(0)
        spec_file.write(spec_content)

    print("Revised naming convention successfully!")


def update_version_number():
    new_version_number: str
    with open("./compose_viz/__init__.py", "r+") as init_file:
        init_content: str = init_file.read()

        version_number = init_content.split(" ")[-1].replace('"', "").strip()
        major, minor, patch = version_number.split(".")
        new_version_number = f"{major}.{minor}.{int(patch) + 1}"

        init_file.seek(0)
        init_file.write(
            f"""__app_name__ = "compose_viz"
__version__ = "{new_version_number}"
"""
        )

    with open("./pyproject.toml", "r+") as pyproject_file:
        pyproject_content: str = pyproject_file.read()

        pyproject_content = pyproject_content.replace(version_number, new_version_number)

        pyproject_file.seek(0)
        pyproject_file.write(pyproject_content)

    print(f"Version number updated to {new_version_number} successfully!")


if __name__ == "__main__":
    revise_naming_convention()
    update_version_number()
