# -*- coding: utf-8 -*-
import os
import json
import datetime
import curl2req.req as req
from curl2req.parser import json_get_data


def datetime_str():
    now = datetime.datetime.now()
    formatted_string = now.strftime('%Y%m%d-%H%M%S.%f')
    return formatted_string[:-3]


def save_json(data, file):
    print("save: ", file)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_txt(items, file):
    print("save: ", file)
    with open(file, 'a', encoding='utf-8') as f:
        for event in items:
            for key, value in event.items():
                f.write(f"{key}: {value}\n")
            f.write('\n' + '-'*50 + '\n\n')


def mkdirp(path):
    path = os.path.dirname(path)
    if not os.path.exists(path):
        os.makedirs(path)


def curl_to_req(
        url_file,
        xpath: str = "",
        dir_name: str = ".res",
        output_file_prefix: str = None,
        repl_kv: dict = {},
):
    curl_context = open(url_file).read()
    for k, v in repl_kv.items():
        curl_context = curl_context.replace(k, v)
    resp = req.convert_and_execute(curl_context)

    timestamp_str = datetime_str()
    if not output_file_prefix:
        output_file_prefix = 'temp'
    mkdirp(f'./{dir_name}/{output_file_prefix}')
    save_json(
        resp.json(),
        f'./{dir_name}/{output_file_prefix}-res-{timestamp_str}.json',
    )
    if not xpath == "":
        save_txt(
            json_get_data(resp.json(), xpath),
            f'./{dir_name}/{output_file_prefix}-txt-{timestamp_str}.txt',
        )
    return resp
