# -*- coding: utf-8 -*-
import json


def generate_json_paths(data, current_path="$", paths=None):
    if paths is None:
        paths = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{current_path}.{key}" if current_path != "$" else f"$.{key}"
            paths.append(new_path)
            generate_json_paths(value, new_path, paths)
    elif isinstance(data, list):
        for index, value in enumerate(data):
            new_path = f"{current_path}[{index}]"
            paths.append(new_path)
            generate_json_paths(value, new_path, paths)

    return paths


def parse_json_and_get_first_path(json_content):
    try:
        if isinstance(json_content, str):
            data = json.loads(json_content)
        else:
            data = json_content

        paths = generate_json_paths(data)

        if paths:
            return paths
        else:
            return None
    except json.JSONDecodeError:
        return "Invalid JSON content"


def get_json_paths(json_content, show=True):
    paths = parse_json_and_get_first_path(json_content)
    if show:
        for path in paths:
            print(path)
    return paths
