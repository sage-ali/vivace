from typing import List, Dict, Any


def extract_settings(settings_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract settings from a list of dictionaries.

    Given a list of dictionaries, each containing a "label" and a "default" value,
    return a dictionary with the labels as keys and the default values as values.

    Args:
        settings_list (List[Dict[str, Any]]): A list of dictionaries, each with a "label" and a "default" value.

    Returns:
        Dict[str, Any]: A dictionary with the labels as keys and the default values as values.
    """
    extracted_settings = {}
    for setting in settings_list:
        extracted_settings[setting["label"]] = setting["default"]
    return extracted_settings


def get_dynamic_settings(
    count: int,
    types: List[str],
    labels: List[str],
    descriptions: List[str],
    defaults: List[Any],
    required: List[bool],
    options: List[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate a list of setting dictionaries with specified attributes.

    This function constructs a list of dictionaries, where each dictionary represents a setting
    with various attributes such as label, type, description, default value, and requirements.
    It supports additional options for dropdown settings.

    Args:
        count (int): The number of settings to generate.
        types (List[str]): A list indicating the type of each setting (e.g., "text", "dropdown").
        labels (List[str]): A list of labels for each setting.
        descriptions (List[str]): A list of descriptions for each setting.
        defaults (List[Any]): A list of default values for each setting.
        required (List[bool]): A list indicating whether each setting is required.
        options (List[List[str]], optional): A list of options for dropdown settings. Defaults to None.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the attributes of a setting.
    """

    options = (
        options or [None] * count
    )  # Ensure options is a list of None if not provided
    return [
        {
            "label": labels[i],
            "type": types[i],
            "description": descriptions[i],
            "default": defaults[i],
            "required": required[i],
            **({"options": options[i]} if types[i] == "dropdown" else {}),
        }
        for i in range(count)
    ]
