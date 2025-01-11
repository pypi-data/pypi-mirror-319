# -*- coding: utf-8 -*-
import json
import re
from typing import Union, List, Optional


def generate_json_paths(data, current_path="$", paths=None):
    """Recursively generate JSON paths for a given data structure."""
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


def uniq_json_paths(paths: List[str]) -> List[str]:
    """Deduplicate array paths by replacing indices with []."""
    seen = set()
    unique_paths = []

    for path in paths:
        # Replace array indices with []
        deduped_path = re.sub(r'\[\d+\]', '[]', path)
        if deduped_path not in seen:
            seen.add(deduped_path)
            unique_paths.append(deduped_path)

    return unique_paths


def parse_json_and_get_first_path(json_content):
    """Parse JSON content and generate paths."""
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


def get_json_paths(json_content: Union[str, dict], show: bool = True, uniq_path: bool = True) -> Optional[List[str]]:
    """Get JSON paths with optional deduplication and display."""
    paths = parse_json_and_get_first_path(json_content)

    if paths is None:
        return None

    if uniq_path:
        paths = uniq_json_paths(paths)

    if show:
        for path in paths:
            print(path)

    return paths
