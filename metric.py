'''
Author: Qiguang Chen
LastEditors: Qiguang Chen
Date: 2023-05-22 17:58:08
LastEditTime: 2023-10-20 15:04:04
Description: 

'''
import fire
from utils.clsp_metric import compute_result as mm
from utils.choice_metric import compute_result as cm
from prettytable import PrettyTable


DATA_DICT = {
    "mgsm": {
        "LANG_DICT": {
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
        },
        "CLP": {
            "data_path": "mgsm/output/clp",
            "metric_mode": "common"
        },
        "CLSP": {
            "data_path": "mgsm/output/clsp",
            "metric_mode": "clsp"
        },
    },
    
    
}

def main(
    input_dir=None,
    metric_mode=None,
    dataset_name="mgsm",
    exp_name="CLSP",
):
    exp = DATA_DICT[dataset_name][exp_name]
    LANG_DICT = DATA_DICT[dataset_name]["LANG_DICT"]
    acc = 0
    if input_dir is None:
        input_dir = exp["data_path"]
        metric_mode = exp["metric_mode"]
    table = PrettyTable(["Language", "Acc", "Total"])
    if dataset_name == "mgsm":
        compute_fn = mm
    else:
        compute_fn = cm
    for lang in LANG_DICT.keys():
        accuracy, total = compute_fn(input_dir, lang, mode=metric_mode)
        acc += accuracy
        table.add_row([lang, round(accuracy, 1), total])
    
    table.add_row(["AVG", round(acc/len(LANG_DICT), 1), "-"])
    print(table)

if __name__ == '__main__':
    fire.Fire(main)