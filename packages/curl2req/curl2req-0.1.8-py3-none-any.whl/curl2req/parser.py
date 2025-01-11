# -*- coding: utf-8 -*-
from jsonpath_ng import parse


def json_get_data(json_data, path):
    expr = parse(path)
    return [match.value for match in expr.find(json_data)]


def to_kv(json_data, key_path):
    try:
        items = {}
        keys = json_get_data(json_data, key_path)
        if keys == "" or len(keys) == 0:
            return {}

        if isinstance(keys, list):
            for key in keys:
                items[key] = json_data
        elif isinstance(keys, str):
            items[keys] = json_data
        return items
    except Exception as e:
        print("args: ", key_path, json_data)
        print("keys: ", keys)
        print("items: ", items)
        raise e

