import pandas as pa
import os
from rest_framework import status

def simple_sum(df, key):
    try:
        return (df[key].apply(pa.to_numeric).sum().round(2), 'Success', status.HTTP_200_OK)
    except (ValueError, TypeError) as e:
        return (None, 'Not a numeric field', status.HTTP_400_BAD_REQUEST)

def keymap_aggregate(df, key, key_map):
    # top level keys, if it matches try to do a simple sum
    if key in df.keys():
        return simple_sum(df, key)
    for k, v in key_map.iteritems():
        if key in v:
            dataframe = pa.DataFrame(df[k])
            return find_sum(dataframe, k, key)
    return (None, 'Field not found', status.HTTP_404_NOT_FOUND)

def raw_aggregate(df, key):
    if key in df.keys():
        return simple_sum(df, key)
    key_map = {item:[] for item in df.keys()}
    for item in key_map.keys():
        if key_finder(df, item, key):
            dataframe = pa.DataFrame(df[item])
            return find_sum(dataframe, item, key)
    return (None, 'Field not found', status.HTTP_404_NOT_FOUND)

def build_key_map(df):
    key_map = {item:[] for item in df.keys()}
    for item in key_map.keys():
        list_of_keys = key_generator(df, item)
        key_map[item] = list_of_keys
    return key_map

def key_generator(df, top_level_key):
    column_keys = set()
    for obj in df[top_level_key]:
        if type(obj) in [dict, list]:
            if type(obj) == dict:
                obj = [obj]
            keys = pa.DataFrame(obj).keys()
            column_keys.update(keys)
        else:
            return []
    return list(column_keys)

def key_finder(df, top_level_key, search_key):
    for obj in df[top_level_key]:
        if type(obj) in [dict, list]:
            if type(obj) == dict:
                obj = [obj]
            keys = pa.DataFrame(obj).keys()
            if search_key in keys:
                return top_level_key
            return None

def find_sum(df, top_level_key, aggregate_column):
    """
    Given a dataframe, column key, and aggregate column it returns the aggregate/sum
    If its not a numeric field, it will return a string with an explanation
    """
    appended_data = []
    for object in df[top_level_key]:
        if type(object) == dict:
            object = [object]
        appended_data.append(pa.DataFrame(object, columns=[aggregate_column]))
    appended_data = pa.concat(appended_data, axis=0)
    appended_data[aggregate_column].dropna()
    if not appended_data[aggregate_column].count():
        return (None, 'No data to aggregate on', status.HTTP_200_OK)
    try:
        appended_data[aggregate_column] = appended_data[aggregate_column].apply(pa.to_numeric)
    except ValueError:
        return (None, 'Not a numeric field', status.HTTP_400_BAD_REQUEST)
    return (appended_data[aggregate_column].sum().round(2), 'Success', status.HTTP_200_OK)

def load_json_file(location):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    location = os.path.join(BASE_DIR, location[1:])
    df = pa.read_json(location, lines=True)
    return df
