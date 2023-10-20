'''
Author: Qiguang Chen
LastEditors: Qiguang Chen
Date: 2023-10-20 13:32:04
LastEditTime: 2023-10-20 15:03:17
Description: 

'''
import json
import os

import fire

from utils.tools import write_jsonl


def get_table_data(dir_path, split_num=10, lang="te"):
    input_data = []
    
    for idx in range(split_num):
        path = f"{dir_path}/{lang}/{idx}.jsonl"
        if os.path.exists(path):
            with open(path, "r", encoding="utf8") as f:
                for line in f:
                    input_data.append(json.loads(line.strip()))
    
    return input_data

def main(input_dir="mgsm/output",
         output_dir=None,
         parallel_num=2):
    if output_dir is None:
        output_dir = input_dir
    for lang in LANG_DICT.keys():
        data_list = get_table_data(input_dir, parallel_num, lang=lang)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        write_jsonl(f"{output_dir}/{lang}.jsonl", data_list, "w")

LANG_DICT= {
    "bn": "Bengali", 
    "de": "German",
    "es": "Spanish",
    "fr": "French",
    "ja": "Japanese",
    "ru": "Russian",
    "sw": "Swahili",
    "te": "Telugu",
    "th": "Thai",
    "zh": "Chinese"
}
if __name__ == '__main__':
    fire.Fire(main)
