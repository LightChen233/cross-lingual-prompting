# Cross-lingual Prompting: Improving Zero-shot Chain-of-Thought Reasoning across Languages

<div align="center">
<a href="https://github.com/LightChen233/cross-lingual-prompting/pulls">
<image src="https://img.shields.io/badge/PRs-welcome-brightgreen">
</a>
<a>
    <img alt="stars" src="https://img.shields.io/github/stars/LightChen233/cross-lingual-prompting" />
</a>
<a href="https://github.com/LightChen233/cross-lingual-prompting/network/members">
    <img alt="FORK" src="https://img.shields.io/github/forks/LightChen233/cross-lingual-prompting?color=FF8000" />
</a>
<a href="https://github.com/LightChen233/cross-lingual-prompting/issues">
    <img alt="Issues" src="https://img.shields.io/github/issues/LightChen233/cross-lingual-prompting?color=0088ff"/>
</a>
</div>
<div>
<img src="./img/csu_logo.png" width="48%">
<img src="./img/SCIR_logo.png" width="48%">
</div>
This repository contains the implementation and the data of the paper: Cross-lingual Prompting: Improving Zero-shot Chain-of-Thought Reasoning across Languages. Libo Qin*, Qiguang Chen*, Fuxuan Wei, Shijue Huang, Wanxiang Che. EMNLP 2023.[PDF] .

## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/motivation.png" width="25" />  Motivation
There are over 200 countries and 7,000 languages worldwide. With the acceleration of globalization, there is an urgent need for generalizing the current CoT across different languages. 
Despite the remarkable success of zero-shot CoT, its reasoning abilities still struggle to generalize to different languages. Unfortunately, little attention has been paid to zero-shot cross-lingual CoT.
<div align="center">
<img src="./img/intro.png" width="240" />
</div>
To generalize the current CoT across languages, we propose a novel cross-lingual prompting (CLP), which aims to effectively bridge the gap across different languages.
It consists of two components: (1) *Cross-lingual Alignment Prompting* and (2) *Task-specific Solver Prompting*.

Specifically, the **cross-lingual alignment prompting** is used to align representations between different languages. In our experiments, instead of the traditional `Let's think step by step`, we use `Let's understand the task in English step-by-step.`. 
The inherent intuition is that as model gradually understands the task in English, it inherently captures the relationship between the source language and English.
After aligning the representations between different languages, we further utilize a *task-specific solve prompting* to complete the final task by setting `Let's resolve the task you understand above step-by-step!`. Such simple yet effective CLP can greatly enhance the reasoning ability of cross-lingual scenarios. Furthermore, inspired by the self-consistency work, we propose cross-lingual self-consistent prompting (CLSP), which enables the model to ensemble different views of reasoning paths across languages.
## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/notes.png" width="25" /> Reference

If you find this project useful for your research, please consider citing the following paper:

```
@misc{qin2023clp,
      title={Cross-lingual Prompting: Improving Zero-shot Chain-of-Thought Reasoning across Languages}, 
      author={Libo Qin and Qiguang Chen and Fuxuan Wei and Shijue Huang and Wanxiang Che},
      year={2023},
      eprint={xxx},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/folders.png" width="25" /> Framework
![](./img/framework.png)

## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/resource.png" width="25" /> Quick Start

### Install from git
```shell
git clone https://github.com/LightChen233/cross-lingual-prompting.git && cd cross-lingual-prompting/
pip install -r requirements.txt
```

### Reproduction
```shell
python metric.py --dataset-name mgsm \
                 --exp-name CLSP
```
**Parameters:**
- `dataset-name`: dataset name.
- `exp-name`: experiment names, which are selected from `['CLP', 'CLSP']`, .

### 1. Request from ChatGPT
```shell
python request.py --api-key sk-xxx \
                  --input-dir mgsm/input \
                  --output-dir mgsm/output \
                  --parallel-num 10
```
**Parameters:**
- `api-key`: OpenAI API-KEY
- `input-dir`: original data dir path
- `output-dir`: generated data dir path to save
- `parallel-num`: the parallel thread number of request

### 2. Merge Output Files
```shell
python request.py --input-dir mgsm/output \
                  --output-dir mgsm/output \
                  --parallel-num 10
```
**Parameters:**
- `input-dir`: generated data dir path to merge, which equals to `output-dir` in step 1.
- `output-dir`: generated data dir path to save.
- `parallel-num`: the parallel thread number of request, which equals to `parallel-num` in step 1.
### 3. Metric Outputs
```shell
python metric.py --input-dir mgsm/output \
                  --metric-mode common
```
**Parameters:**
- `input-dir`: generated data dir path to save, which equals to `output-dir` in step 2.
- `metric-mode`: selected from `['common', 'clsp']`, `common` denotes the regular CoT metrics and `clsp` denotes the vote mechanism for CLSP.
**Parameters:**
- `api-key`: OpenAI API-KEY
- `input-dir`: original data dir path
- `output-dir`: generated data dir path to save
- `parallel-num`: the parallel thread number of request

## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/organizer.png" width="25" /> Model Performance
![](./img/result.png)


## <img src="https://cdn.jsdelivr.net/gh/LightChen233/blog-img/intro.png" width="25" /> Contact

Please create Github issues here or email [Libo Qin](mailto:lbqin@ir.hit.edu.cn) or [Qiguang Chen](mailto:charleschen2333@gmail.com) if you have any questions or suggestions.