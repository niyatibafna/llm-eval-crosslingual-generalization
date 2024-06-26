def parse_excel_table_into_results(lang_results, all_noise_param_ranges, tasks = ['X->eng', 'XNLI', 'XStoryCloze']):
    results_lang_all_noisers = {}
    for noise_type, str_results in lang_results.items():
        results_lang_noise = {}
        for i, line in enumerate(str_results.split('\n')):
            if line == '':
                continue
            noise_param = all_noise_param_ranges[noise_type][i]
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



# Now we can plot the results
## 1 plot per task per noiser
## X axis: noise_param
## Y axis: boxplot of accuracies over all languages for that task
## Total subplots: 3 tasks * 1 noiser = 3

import matplotlib.pyplot as plt
import numpy as np


def plot_results(results, tasks, curr_noisers, all_noise_param_ranges):

    plt.rcParams.update({'font.size': 22})
    num_tasks = len(tasks)
    num_noisers = len(curr_noisers)
    fig, axs = plt.subplots(num_noisers, num_tasks, figsize=(50, 50))
    for j, noise_type in enumerate(curr_noisers):
        for i, task in enumerate(tasks):
            if num_noisers == 1:
                ax = axs[i]
            else:
                ax = axs[j, i]  # Indexing both dimensions
            
            for param in all_noise_param_ranges[noise_type]:
                accs = []
                for lang in results.keys():
                    if results[lang][noise_type][task][param] != -1:
                        accs.append(results[lang][noise_type][task][param])
                        print(f"Noise type: {noise_type}, Task: {task}, Lang: {lang}, Param: {param}, Acc: {results[lang][noise_type][task][param]}")
                if len(accs) > 0:
                    ax.boxplot(accs, positions=[param], widths=0.05, showmeans=True, meanline=True, meanprops=dict(color='red'))
                                    # patch_artist=True,
                                    # boxprops=dict(facecolor='blue', color='blue'),
                                    # capprops=dict(color='blue'),
                                    # whiskerprops=dict(color='blue'),
                                    # flierprops=dict(markerfacecolor='blue', marker='o', markersize=5, linestyle='none'),
                                    # medianprops=dict(color='blue')) 
            ax.set_title(task + " " + noise_type)
            ax.set_xlabel("Noise Param")
            ax.set_ylabel("% Degradation in Performance")
            xticks = list([x/10 for x in range(11)])
            yticks = list([y*10 for y in range(11)])
            ax.set_yticks(yticks)
            ax.set_yticklabels([str(y) for y in yticks])
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticks)
            ax.set_xlim(-0.1, 1.1)


    plt.tight_layout()  # Adjust subplots to fit into figure area.
    plt.savefig("boxplot_results.png")



es = {
'lexical': \
'''42.91	49.67	72.33
26.57	43	68.33
26.52	41.67	63
28.1	41.33	66.33
15.01	41.67	65
13.56	38.67	62
5.72	37.33	57.33''',
'phonological': \
'''42.91	49.67	72.33
41.92	49	67
34.74	46.67	70
30.34	37.33	66
16.02	35	63.33
10.64	35.67	59.67''',
'morphological': \
'''42.91	49.67	72.33
40.78	48	70.33
34.5	44	68.67
33.62	40	70.67
32.04	40.33	66.33
30	35.33	65.67'''
}

hi = {
'lexical': \
'''56.44	51	63.67
27.05	42.33	56.33
27.83	36	58
22.53	39	55.67
19.11	37.33	52
13.64	40	55
5.8	-1	-1''',
'phonological': \
'''56.44	51	63.67
56.13	44	59.67
45.99	47.67	59.67
36.29	45	58
16.81	35	54
7.46	38.33	48''',
'morphological': \
'''56.44	51	63.67
53.64	50.33	62
46.82	47.33	60.67
44.77	50	60.33
42.21	46.33	59.33
38.39	47.33	55.33'''
}

id = {
'lexical': \
'''60	-1	69.33
34.98	-1	61.67
32.04	-1	61
34.81	-1	54.67
22.37	-1	58.67
15.91	-1	55.33
8.73	-1	-1''',
'phonological': \
'''60	-1	69.33
58.39	-1	68.67
48.58	-1	63.67
37.99	-1	65
8.81	-1	59.33
3.98	-1	54.67''',
'morphological': \
'''60	-1	69.33
49.04	-1	64
50.17	-1	58.33
42.76	-1	61
26.51	-1	56
21.81	-1	58.67'''
}

ar = {
'lexical': \
'''55.32	46	66
39.9	35	64.33
37.9	35.33	63.33
37.25	39.33	62.67
20.2	36.33	58.67
16.92	40.33	56.33
8.18	-1	-1''',
'phonological': \
'''55.32	46	66
53.48	46.67	66
41.01	43.33	60
25.91	43.33	58.67
6.66	33.33	53
3.24	33.67	53.67''',
'morphological': \
'''55.32	46	66
49.77	45.33	60.67
44.06	45	55.67
37.36	41.33	57
31.33	39	54.67
23.96	40.67	52'''
}

en = {
'lexical': \
'''99.53	60.33	77.33
65.29	34.67	72
44.22	34.33	70.67
35.78	49	69
34.36	34.33	63.67
34.79	34.33	62
17.23	-1	-1''',
'phonological': \
'''99.53	60.33	77.33
96.22	58.33	75.33
76.92	54.33	69.67
60.93	34.33	63.33
40.32	34.67	63.33
22.74	40.67	60''',
'morphological': \
'''99.53	60.33	77.33
87.66	34	72.33
84.9	57	68
69.66	52	66.67
56.96	34.33	61.67
51.1	33.67	59.67'''
}

de = {
'lexical': \
'''-1	-1	-1
-1	-1	-1
-1	-1	-1
-1	-1	-1
-1	-1	-1
-1	-1	-1
-1	-1	-1''',
'phonological': \
'''-1	47.33	-1
-1	46	-1
-1	45	-1
-1	42.33	-1
-1	33.33	-1
-1	34.67	-1''',
'morphological': \
'''-1	47.33	-1
-1	47.33	-1
-1	45.67	-1
-1	34	-1
-1	44.67	-1
-1	43.33	-1'''
}


all_lang_results = {"es": es, "hi": hi, "id": id, "de": de, "ar": ar}

# We'll build a results dictionary with the following structure:
# results = {lang: noise_type: {task: {noise_param: acc}}
noise_types = ["lexical", "morphological", "phonological"]
all_noise_param_ranges = {
    'lexical': [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5],
    'morphological': [0, 0.2, 0.4, 0.6, 0.8, 1],
    'phonological': [0, 0.01, 0.05, 0.1, 0.2, 0.3],
}
tasks = ['X->eng', 'XNLI', 'XStoryCloze']

results = {}
for lang, lang_results in all_lang_results.items():
    results[lang] = parse_excel_table_into_results(lang_results, all_noise_param_ranges, tasks = tasks)

print(results)

curr_noisers = results[list(results.keys())[0]].keys()
baselines = {
    lang : { 
        noise_type: {
            task: results[lang][noise_type][task][0] for task in tasks
        } for noise_type in curr_noisers
    } for lang in results.keys()
}

print("\n\n\n\n BASELINES")
print(baselines)



results = normalize_and_transform_scores(results, baselines, tasks = tasks)
# Pretty print
for lang, lang_results in results.items():
    print(lang.upper())

    for noise_type, noise_results in lang_results.items():
        print(noise_type)
        for task in tasks:
            print(task)
            for noise_param, acc in noise_results[task].items():
                print(noise_param, acc)
            print()
    
    print("\n\n\n")

plot_results(results, tasks, curr_noisers, all_noise_param_ranges)