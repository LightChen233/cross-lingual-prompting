'''
Author: Qiguang Chen
LastEditors: Qiguang Chen
Date: 2023-10-13 14:34:55
LastEdiosime: 2023-10-13 14:35:00
Description: 

'''

import os
import re

import numpy as np

from utils.tools import read_jsonl

def get_pred_max(data_list):
    pred_max = {}
    for j, data in enumerate(data_list):
        # extract answer
        mes = data["message"][-1]["content"].split("Answer:")[-1].replace(",", "")
        pred_list = [s for s in re.findall(r'-?\d+\.?\d*', mes)]
        if len(pred_list)==0:
            continue
        pred = str(float(pred_list[-1]))
        # get all predicted answer
        if pred not in pred_max:
            pred_max[pred] = []
        pred_max[pred].append({"source": j, "value": pred})
    return pred_max

def extract_max(pred_max):
    max_data = 0
    max_index = 0
    # get the most frequently predicted answer
    for x in pred_max:
        if len(pred_max[x])>max_data:
            max_data = len(pred_max[x])
            max_index = x
    return max_index, max_data

def judge_equal(pred, answer):
    # judgment of equality, precision to two decimal places
    flag = (np.array([int(float(pred)*100)]) == np.array([int(float(answer)*100)])).sum().item()
    return flag == 1

def compute_result(input_dir, lang, mode="clsp"):
    data_all = []
    if mode in ["origin", "clp", "clsp"]:
        if mode == "clp":
            lang_list = ["en"]
        elif mode == "clsp":
            lang_list = ["en", "de", "es", "fr", "ja", "ru", "zh"]
        else:
            lang_list = [lang]
        for lang2 in lang_list:
            for idx, x in enumerate(read_jsonl(os.path.join(input_dir, f"{lang}/{lang2}.jsonl"))):
                if len(data_all) <= idx:
                    data_all.append([x])
                else:
                    data_all[idx].append(x)
    else:
        for idx, x in enumerate(read_jsonl(os.path.join(input_dir, f"{lang}.jsonl"))):
            if len(data_all) <= idx:
                data_all.append([x])
            else:
                data_all[idx].append(x)
    total = 0
    correct = 0
    for data_list in data_all:
        total += 1
        pred_max = get_pred_max(data_list)
        pred, _ = extract_max(pred_max)
        answer = data_list[0]["origin"]["answer"].replace(",", "")
        if judge_equal(pred, answer):
            correct += 1
        
    if total == 0:
        return 0, 0
    return correct*100.0/total, total