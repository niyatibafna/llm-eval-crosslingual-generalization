from collections import defaultdict
import numpy as np
import pandas as pd

hi = { 
"lexical": '''20.55	37	55
18.11	43	52.67
22.07	39	58
19.13	44.67	53.67
21.47	42	52.67
22.58	33	53
19.64	38.33	54.33
17.34	41.33	55
22.5	40.33	59.33
14.35	42	58''',
"morphological": '''45.53	48	60.33
45.81	48.67	61
46.98	49	61.67
47.97	49	59.67
46.84	50	64.33
48.4	47	61.67
47.77	48.67	61
47.48	51.33	59.67
44.26	44.67	59.67
49.44	47.33	63.33''',
"phonological": '''32.72	49.67	58.67
35.4	42.33	59.33
34.68	41.33	60
34.62	39	58
34.65	47	61.67
38.02	44	58.33
36.32	45.67	62.33
28.7	47.67	58.67
37.17	43.67	61.33
37.43	44.67	62'''
}

ar = {
"lexical": '''16.1	36.33	56
19.77	36.33	59.67
20.36	38	54.33
18.81	37	53.33
17.84	35.67	57.33
16.35	35.67	52.33
19.56	35.33	54.33
17.86	34	58.33
19.61	35	57.67
15.95	38	57.67''',
"morphological": '''38.4	38.67	58.33
37.64	42.67	57.33
36.64	42.33	58
35.82	43.33	58.33
35.53	40	56.33
38.91	41	61.67
35.21	40.67	54.33
37.16	41	61.67
37.37	42	56
36.52	39.33	60.67''',
"phonological": '''28.44	39.67	52.67
27.24	40.33	53.67
25.11	40.67	60.33
33.63	41	58.67
17.58	40.33	53.33
28.96	39.67	60
25.72	41.33	61.33
28.15	41	54.67
25.93	41.33	57
29.46	42.67	61'''
}

def parse_excel_table_into_results(lang_results, all_noise_param_ranges, tasks = ['X->eng', 'XNLI', 'XStoryCloze']):
    results_lang_all_noisers = {}
    for noise_type, str_results in lang_results.items():
        results_lang_noise = {}
        for i, line in enumerate(str_results.split('\n')):
            if line == '':
                continue
            try:
                noise_param = all_noise_param_ranges[noise_type][i]
            except:
                print(noise_type, i, line), all_noise_param_ranges[noise_type], len(str_results.split('\n'))
                raise
            for task in tasks:
                if task not in results_lang_noise:
                    results_lang_noise[task] = {}

            for j in range(len(line.split('\t'))):
                results_lang_noise[tasks[j]][noise_param] = float(line.split('\t')[j])

        results_lang_all_noisers[noise_type] = results_lang_noise
    
    return results_lang_all_noisers
            

# Transform the results based on task
## This is because we want to measure degradation of performance in a way that is comparable across tasks

def normalize_and_transform_scores(results, baselines, tasks = ['X->eng', 'XNLI', 'XStoryCloze']):
    '''
    We transform the scores to make degradation comparable across tasks
    '''

    zero_perfs = {
    "X->eng": 0,
    "XNLI": 33.33,
    "XStoryCloze": 50
    }

    transformed_results = {}
    for lang, lang_results in results.items():
        transformed_results[lang] = {}
        for noise_type, noise_results in lang_results.items():
            transformed_results[lang][noise_type] = {}
            for task in tasks:
                zero_perf = zero_perfs[task]
                transformed_results[lang][noise_type][task] = {}
                for noise_param, acc in noise_results[task].items():
                    if acc == -1:
                        transformed_results[lang][noise_type][task][noise_param] = -1
                    else:    
                        transformed_results[lang][noise_type][task][noise_param] = \
                            ((baselines[lang][noise_type][task] - zero_perf) - (acc - zero_perf)) / (baselines[lang][noise_type][task] - zero_perf)
                        # We multiply by 100 to get percentage
                        transformed_results[lang][noise_type][task][noise_param] *= 100
    return transformed_results


all_lang_results = {"hi": hi, "ar": ar}
noise_types = ["lexical", "morphological", "phonological"]
all_noise_param_ranges = defaultdict(lambda: list(range(0,10)))

tasks = ['X->eng', 'XNLI', 'XStoryCloze']

results = {}
for lang, lang_results in all_lang_results.items():
    print(lang)
    results[lang] = parse_excel_table_into_results(lang_results, all_noise_param_ranges, tasks = tasks)

print(results)

baselines = {"hi": defaultdict(lambda: {'X->eng': 56.51, 'XNLI': 51.0, 'XStoryCloze': 64.0}), 
             "ar": defaultdict(lambda: {'X->eng': 56.68, 'XNLI': 46.33, 'XStoryCloze': 66.0})}

transformed_results = normalize_and_transform_scores(results, baselines, tasks = tasks)

print(transformed_results)

# Make table of std dev for each noise type and task


for lang in baselines:
    df = pd.DataFrame(columns = ["lexical", "morphological", "phonological", "task_avg"], index = ["X->eng", "XNLI", "XStoryCloze", "noise_avg"])
    print(f"LANG: {lang}")
    for task in tasks:
        for noise_type in noise_types:
            std_dev = np.std([transformed_results[lang][noise_type][task][noise_param] for noise_param in all_noise_param_ranges[noise_type]])
            df.loc[task, noise_type] = std_dev
    
    for noise_type in noise_types:
        df.loc["noise_avg", noise_type] = np.mean([df.loc[task, noise_type] for task in tasks])

    for task in tasks:
        df.loc[task, "task_avg"] = np.mean([df.loc[task, noise_type] for noise_type in noise_types])
    
    # Round each cell to 1 decimal place
    
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            df.iloc[i,j] = round(df.iloc[i,j], 1)
    

    print(df)