from os import path as PATH

# Declare the constant path for icon images
_PATH: str = PATH.join(PATH.dirname(__file__), "icons")


# Define the function to get the icon path
def get_icon_path(name: str) -> str:
    """
    Returns the file path for the given icon name.

    Parameters:
    name (str): The name of the icon.

    Returns:
    str: The full file path to the icon.
    """
    return PATH.join(_PATH, f"{name}.svg")
