from typing import List, Dict, Any

def extract_settings(settings_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    extracted_settings = {}
    for setting in settings_list:
        extracted_settings[setting["label"]] = setting["default"]
    return extracted_settings

def get_dynamic_settings(count: int, types: List[str], labels: List[str], descriptions: List[str], defaults: List[Any], required: List[bool], options: List[List[str]] = None) -> List[Dict[str, Any]]:
    options = options or [None] * count  # Ensure options is a list of None if not provided
    return [
        {
            "label": labels[i],
            "type": types[i],
            "description": descriptions[i],
            "default": defaults[i],
            "required": required[i],
            **({"options": options[i]} if types[i] == "dropdown" else {})
        }
        for i in range(count)
    ]
