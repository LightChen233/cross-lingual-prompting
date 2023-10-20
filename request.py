'''
Author: Qiguang Chen
LastEditors: Qiguang Chen
Date: 2023-05-22 11:07:11
LastEditTime: 2023-10-20 14:51:51
Description: 

'''
import json
import os
import threading
import time
import fire

import openai
from tqdm import tqdm

def get_data(input_path, split_num=4):
    input_data = []
    with open(input_path, "r", encoding="utf8") as f:
        for line in f:
            data = line.strip().split("\t")
            input_data.append({"text": data[0], "answer": data[1]})

    splits = []
    for _ in range(split_num):
        splits.append([])
    for i, data in enumerate(input_data):
        splits[i % split_num].append(data)
    return splits

# 定义一个函数，用于调用API并处理数据
def process_table(input_list,
                  idx,
                  output_path,
                  source_language,
                  target_language):
    idx = str(idx)
    print(f"Processing split {idx}.")
    max_id = -1
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if os.path.exists(output_path+f"/{idx}.jsonl"):
        with open(output_path+f"/{idx}.jsonl", "r", encoding="utf8") as f:
            for line in f:
                obj = json.loads(line.strip())
                if max_id < obj["id"]:
                    max_id = obj["id"]
    else:
        with open(output_path+f"/{idx}.jsonl", 'w', encoding="utf8") as file:
            print("Writing")
    input_list = input_list[max_id+1:]
    
    
    j = max_id+1
    for data in tqdm(input_list, desc=f"{source_language}-{idx}"):
        instruction = f"Please act as an expert in multi-lingual understanding in {source_language}.\n\n"
        instruction += "Request:\n" + data["text"] + "\n\n"
        instruction += f"Let's understand the task in {target_language} step-by-step!"
        messages = [{"role": "user", "content": instruction}]
        while True:
            try:
                completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", 
                            messages=messages,
                            temperature=1,
                            top_p=1)
                break
            except Exception as e:
                print(e)
                time.sleep(1)
        messages += [{"role": "assistant", "content":  completion["choices"][0]["message"]["content"]}]
        instruction = f"After understanding, you should act as an expert in arithmetic reasoning in {target_language}.\n"
        instruction += "Let's resolve the task you understand above step-by-step!\n"
        instruction += "Finally, you should format your answer as 'Answer: [num]'."
        messages += [{"role": "user", "content":  instruction}]
        while True:
            try:
                completion = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", 
                            messages=messages,
                            temperature=0.2,
                            top_p=1)
                break
            except Exception as e:
                print(e)
                time.sleep(1)
        
        res_list = [x["message"]["content"] for x in completion["choices"]]
        messages = messages + [{"role": "assistant", "content":  res_list[0]}]
        print({"id": j, "message": messages, "origin": data})
        with open(output_path+f"/{idx}.jsonl", 'a', encoding="utf8") as file:
            file.write(json.dumps({"id": j, "message": messages, "origin": data}, ensure_ascii=False)+"\n")
        j += 1



def parallel_run(input_path,
                 data_fn,
                 output_path,
                 process_fn,
                 source_language,
                 target_language,
                 parallel_num=10,):
    threads = []
    for i, input_list in enumerate(data_fn(input_path, split_num=parallel_num)):
        thread = threading.Thread(target=process_fn, args=(input_list, i, output_path, source_language, target_language))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("All API calls and data processing completed.")

LANG_DICT = {
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

def main(
    api_key,
    input_dir="mgsm/input",
    output_dir="mgsm/output",
    parallel_num=1,
):
    openai.api_key = api_key
    for lang in list(LANG_DICT.keys()):
        parallel_run(input_path=f"{input_dir}/mgsm_{lang}.tsv",
                    data_fn=get_data,
                    output_path=f"{output_dir}/{lang}",
                    source_language=LANG_DICT[lang],
                    target_language="English",
                    process_fn=process_table,
                    parallel_num=parallel_num)

if __name__ == '__main__':
    fire.Fire(main)
