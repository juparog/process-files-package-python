"""This module provides the Process Files utils methods."""
# process_files/utils.py

import json
import pandas as pd
from pandas import DataFrame
from process_files import SUCCESS, FILE_IS_A_DIRECTORY, FILE_NOT_FOUND, FILE_PERMISSION, VALIDATE_EXTENSION, WRONG_FORMAT, KEY_ERROR

def validate_extension(file_path: str, expected_extension: str) -> int:
    """Validate spec file extension"""
    if file_path.endswith(f'{expected_extension}'):
        return SUCCESS
    return VALIDATE_EXTENSION

def read_json_file(file_path: str) -> (dict | int):
    """Read json file"""
    try:
        f = open(file_path)
        data = json.load(f)
        return data
    except FileNotFoundError:
        return FILE_NOT_FOUND
    except PermissionError:
        return FILE_PERMISSION
    except IsADirectoryError:
        return FILE_IS_A_DIRECTORY
    except:
        return WRONG_FORMAT

def read_excel_file(file_path: str, sheet_name: str = "Sheet1") -> (DataFrame | int):
    """Read excel file"""
    try:
        df = pd.read_excel (file_path, sheet_name = sheet_name)
        return df
    except FileNotFoundError:
        return FILE_NOT_FOUND
    except PermissionError:
        return FILE_PERMISSION
    except IsADirectoryError:
        return FILE_IS_A_DIRECTORY
    except:
        return WRONG_FORMAT

def get_value_json(data: dict, key_path: str) -> (dict | int):
    """Get valor de un json"""
    arr_keys = key_path.split(".")
    result = data
    try:
        for key in arr_keys:
            result = result[key]
    except:
        return KEY_ERROR
    return {
        "value": result
    }
