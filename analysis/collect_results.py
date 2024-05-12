'''In this script, we'll create tables from experiment results.
Input:
param set,
folder name expression,
task name

Depending on the task name, we'll go to the correct file and get the metric of interest.
'''
'''
Example results file:
{
  "lexical-lang=hi,theta_content_global=0.05,theta_func_global=1.0,text_file=</export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/datasets/hi//flores200-hi-en.txt>,output_dir=</export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/noiser_artifacts/lexical/lexical-lang=hi,theta_content_global=0.05,theta_func_global=1.0>": {
    "results": {
      "flores200-hi-en": {
        "bleu": 48.12825830657126,
        "bleu_stderr": 1.319568969607076,
        "chrf": 0.6847904141397222,
        "chrf_stderr": 0.009365709784190806,
        "ter": 0.41640722291407223,
        "ter_stderr": 0.01329280147723964
      }
    },
    "versions": {
      "flores200-hi-en": 0
    },
    "config": {
      "model": "hf-seq2seq",
      "model_args": "pretrained=bigscience/mt0-xxl-mt",
      "batch_size": 32,
      "device": "cuda",
      "no_cache": false,
      "limit": 300.0,
      "bootstrap_iters": 100000,
      "description_dict": {
        "flores200-hi-en": "Translate from Hindi to English:\n"
      }
    }
  }
}
'''

import os
import pandas as pd
import json
from collections import defaultdict

def task_to_metric(task_name):

    if "flores200" in task_name:
        return "bleu"

    if "truthful" in task_name:
        return "mc2"
    return "acc"    
  


def get_metric_from_results_file(results, task_name):

    '''Get metric from results file
    Args:
        results: dict, results file
    Returns:
        pd.DataFrame, results
    '''

    if len(results) != 1:
      print("Results file should have only one experiment key")
      print(results.keys())
    for exp_key, exp_results in results.items():
        assert len(exp_results["results"]) == 1, "Results file should have only one task"
        for _, task_results in exp_results["results"].items():
            metric = task_to_metric(task_name)
    val = task_results[metric]
    if metric in ["acc", "mc2"] and val <= 1:
        val = val * 100

    return round(val, 2)


def get_results(param_set, folder_name_expr, task_name):
    '''Get results from experiment output files
    Args:
        param_set: str, parameter set
        folder_name_expr: str, folder name expression, with <placeholder> for param value
        task_name: str, task name
    Returns:
        pd.DataFrame, results
    '''
    all_results = dict()
    for param_value in param_set:
        folder_name = folder_name_expr.replace("<placeholder>", param_value)
        if not os.path.exists(folder_name):
            print(f"Folder {folder_name} does not exist")
            all_results[param_value] = -1
            continue
        for file in os.listdir(folder_name):
            if task_name in file:
                with open(os.path.join(folder_name, file), "r") as f:
                    results = json.load(f)
                    all_results[param_value] = get_metric_from_results_file(results, task_name)
        
        if param_value not in all_results:
            all_results[param_value] = -1

    print(all_results)
    return pd.DataFrame(all_results, index=[0])

def get_results_from_folder(folder_name, task_name):
    '''Get results from experiment output files
    Args:
        folder_name: str, folder name expression, with <placeholder> for param value
        task_name: str, task name
    Returns:
        pd.DataFrame, results
    '''
    result = -1
    for file in os.listdir(folder_name):
        if task_name in file:
            with open(os.path.join(folder_name, file), "r") as f:
                results = json.load(f)
                result = get_metric_from_results_file(results, task_name)
        

    return result



def print_in_vertical_row(param_set, results):
    '''Pretty print results so that they can be copied into Excel
    Args:
        results: pd.DataFrame, results
    Returns:
        pd.DataFrame, pretty printed results
    '''
    print(f"PARAMETERS")
    print("\n".join(param_set))
    print(f"RESULTS")
    pretty_results = results.to_string(index=False, header=False)
    pretty_results = pretty_results.replace(" ", "\n")
    print(pretty_results)

def pretty_print_baseline(results, langs, tasks):

    for task in tasks:
        print(f"TASK: {task}")
        for lang in langs:
            print(f"{results[task][lang]}")
        print("\n\n")


if __name__ == "__main__":
    param_set = ["0.01", "0.05", "0.10", "0.15", "0.3"]
    # param_set = ["0.2", "0.4", "0.6", "0.8", "1"]
    # langs = ["en", "hi", "id", "fr", "es", "de", "ar", "ru"]
    # langs = ["hi", "ru", "ar", "es", "de", "id", "en", "fr"]
    langs = ["es", "hi"]
    # tasks = ["xstory_cloze", "xnli", "arc", "hellaswag", "mmlu", "xwinograd", "xcopa", "xnli_mcq", "truthfulqa"]
    tasks = ["xnli_mcq"]

    for lang in langs:
        for task in tasks:
            # folder_name_expr = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/mt0xxlmt~0shot/{lang}/phonological-lang={lang},theta_phon=<placeholder>~limit-300"
            # folder_name_expr = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/mt0xxlmt~0shot/{lang}/lexical-lang={lang},theta_content_global=<placeholder>,theta_func_global=1.0~limit-300"
            # folder_name_expr = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/bloomz7b/{lang}/morph-lang={lang},theta_morph_global=<placeholder>~limit-300"
            # folder_name_expr = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/bloomz7b/{lang}/lexical-lang={lang},theta_content_global=<placeholder>,theta_func_global=0.8~limit-300"
            folder_name_expr = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/bloomz7b/{lang}/phonological-lang={lang},theta_phon=<placeholder>~limit-300"
            if task == "flores200":
                task = f"flores200-{lang}-en"
            else:
                task = f"{task}_{lang}"
            print(f"LANG: {lang}, TASK: {task}")
            results = get_results(param_set, folder_name_expr, task)
            print(results)
            print_in_vertical_row(param_set, results)
    

    # Baseline results:
    # lang_task = defaultdict(lambda: dict())
    # for lang in langs:
    #     for task in tasks:
    #         # folder_name_expr = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/mt0xxlmt~0shot/{lang}/phonological-lang={lang},theta_phon=<placeholder>~limit-300"
    #         # folder_name_expr = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/bloomz7b/{lang}/baselines~limit-300/"
    #         folder_name_expr = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/bloomz7b/{lang}/morph-lang={lang},theta_morph_global=<placeholder>~limit-300"
    #         if task == "flores200":
    #             task_name = f"flores200-{lang}-en"
    #         else:
    #             task_name = f"{task}_{lang}"
    #         print(f"LANG: {lang}, TASK: {task}")
    #         result = get_results_from_folder(folder_name_expr, task_name)
    #         lang_task[task][lang] = result
    
    # print(lang_task)
    # pretty_print_baseline(lang_task, langs, tasks)

    # folder_name_expr = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/results/mt0xxlmt~0shot/hi/lexical-lang=hi,theta_content_global=<placeholder>,theta_func_global=1.0~limit-300"
    # task_name = "flores200"
    # results = get_results(param_set, folder_name_expr, task_name)
    # print(results)
    # print_in_vertical_row(param_set, results)
                                    
    