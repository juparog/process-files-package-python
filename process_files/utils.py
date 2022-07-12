"""This module provides the Process Files utils methods."""
# process_files/utils.py

import json
import pandas as pd
from ast import literal_eval
from pandas import DataFrame
from process_files import SUCCESS, FILE_IS_A_DIRECTORY, FILE_NOT_FOUND, FILE_PERMISSION, VALIDATE_EXTENSION, WRONG_FORMAT, KEY_ERROR, EXTRACT_DATA_ERROR, INSERT_DATA_ERROR, TABLE_NAME_ERROR

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

def extract_data_from_columns(df: DataFrame, spec: dict) -> (DataFrame | int):
    """Organize structured data"""
    result_df = df
    columns = get_value_json(spec, "columns")
    if type(columns).__name__ != "dict":
        return columns
    for column in columns["value"]:
        isStructured = get_value_json(column, "isStructured")
        if type(isStructured).__name__ != "dict":
            continue
        if isStructured["value"] == False:
            continue
        # Convert column content from json to dataframe
        df_temp = df.iloc[:, column["columnIndex"] - 1]
        df_temp = df_temp.apply(literal_eval)
        df_temp = df_temp.tolist()
        df_temp = pd.DataFrame(df_temp)
        # Add extracted data to the resulting dataframe
        result_df = result_df.join(df_temp)
        # hide parent column
        column_name = get_value_json(column, "name")
        if type(column_name).__name__ != "dict":
            continue
        print(f'Extracted info column name: {column_name["value"]}')
        hide_parent_column = get_value_json(column, "hideParentColumn")
        if type(hide_parent_column).__name__ == "dict":
            hide_parent_column = hide_parent_column["value"]
        else:
            hide_parent_column = True
        if hide_parent_column:
            result_df.drop(column_name["value"], axis=1, inplace=True)
            print(f'Hide column name: {column_name["value"]}')
    return result_df

def upload_excel_to_db(df: DataFrame, spec: dict, engine) -> (bool | int):
    """Upload excel file to database"""
    # Arrange data
    new_df = extract_data_from_columns(df, spec)
    if type(new_df).__name__ != "DataFrame":
        return EXTRACT_DATA_ERROR
    table_name = get_value_json(spec, "table.name")
    if type(table_name).__name__ != "dict":
        return TABLE_NAME_ERROR
    if_exists = get_value_json(spec, "table.ifExists")
    if type(if_exists).__name__ != "dict":
        if_exists = "append" # option: fail, replace, append
    else:
        if_exists = if_exists["value"]
    try:
        print(f'Inserting data...')
        print(f'Options: if_exist = {if_exists}')
        new_df.to_sql(table_name["value"], if_exists = if_exists, index = False, con = engine)
    except:
        return INSERT_DATA_ERROR
    return True
