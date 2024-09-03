import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

out_filename = "plots/main_results_w_arb.pdf"
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


# Now we can plot the results
## 1 plot per task per noiser
## X axis: noise_param
## Y axis: boxplot of accuracies over all languages for that task
## Total subplots: 3 tasks * 1 noiser = 3

import matplotlib.pyplot as plt
import numpy as np


def plot_results(results, tasks, curr_noisers, \
        all_noise_param_ranges, noise_type_real_points = None):

    # Use latex 
    # plt.rc('text', usetex=True)

    title_noise_type_to_idx = {
        'lexical_c0': 1,
        'lexical_f0': 2,
        'lexical_f0.5': 3,
        'lexical_f0.8': 4,
        'phonological': 5,
        'morphological': 6,
    }
    title_task_to_idx = {
        'X->eng': "a",
        'XNLI': "b",
        'XStoryCloze': "c"
    }
    
    title_noise_type = {
        'lexical_f0': r'Lexical (Content $\vert$ $\theta_f = 0$) : $\psi^{f,c}_{0,*}$',
        'lexical_f0.5': r'Lexical (Content $\vert$ $\theta_f = 0.5$) : $\psi^{f,c}_{0.5,*}$',
        'lexical_f0.8': r'Lexical (Content $\vert$ $\theta_f = 0.8$) : $\psi^{f,c}_{0.8,*}$',
        'lexical_c0': r'Lexical (Function $\vert$ $\theta_c = 0$) : $\psi^{f,c}_{*,0}$',
        'morphological': r'Morphological : $\psi^{m}_{*}$',
        'phonological': r'Phonological : $\psi^{p}_{*}$'
    }
    xlabels = {
        'lexical_f0': r'$\theta_c$',
        'lexical_f0.5': r'$\theta_c$',
        'lexical_f0.8': r'$\theta_c$',
        'lexical_c0': r'$\theta_f$',
        'morphological': r'$\theta_m$',
        'phonological': r'$\theta_p$'
    }

    # plt.rcParams.update({'font.size': 26})
    point_size = 60
    num_tasks = len(tasks)
    num_noisers = len(curr_noisers)
    fig, axs = plt.subplots(num_noisers, num_tasks, figsize=(16, 24))
    for j, noise_type in enumerate(curr_noisers):
        for i, task in enumerate(tasks):
            if num_noisers == 1:
                ax = axs[i]
            else:
                ax = axs[j, i]  # Indexing both dimensions
            
            # Lineplots with each language a different color
            # colour_scheme = plt.get_cmap('viridis', len(results.keys()))
            colors_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#ffdd57', '#17becf', '#8c564b', '#7f7f7f']

            custom_cmap = LinearSegmentedColormap.from_list('custom_cmap', colors_list, N=len(colors_list))

            # Example usage:
            colour_scheme = custom_cmap
            # print(colors)
            for lang, lang_results in results.items():
                x = list(lang_results[noise_type][task].keys())
                y = list(lang_results[noise_type][task].values())
                y = [y_val if y_val != -1 else None for y_val in y ]
                # markersize = 20
                if any(y):
                    # Plotting 0,0 for morphological noiser
                    if noise_type == "morphological":
                        x = [0] + x
                        y = [0] + y
                    ax.scatter(x, y, label=lang, marker = "x", s = point_size, linewidths = 3, \
                           color=colour_scheme(list(results.keys()).index(lang)))

            # For each noise_param, plot the mean over languages, and a regression line
            X = []
            Y = []
            for noise_param in all_noise_param_ranges[noise_type]:
                try:
                    y = [lang_results[noise_type][task][noise_param] for lang, lang_results in results.items()]
                except:
                    print(noise_type, task, noise_param)
                    print(lang_results[noise_type][task].keys())
                    raise
                y = [y_val for y_val in y if y_val != -1]
                if len(y) == 0:
                    continue
                Y.append(np.mean(y))
                X.append(noise_param)
            
            if noise_type == "morphological":
                X = [0] + X
                Y = [0] + Y

            # Plot regression line with X and Y
            m, b = np.polyfit(X, Y, 1)
            ax.plot(X, [m*x + b for x in X], color = "black", linestyle = "--", linewidth = 2)

            # Plot the mean
            ax.scatter(X, Y, label = "mean", marker = "o", s = 15, color = "black")


            ax.legend()

            ax.set_title(f"({title_noise_type_to_idx[noise_type]}{title_task_to_idx[task]}) {task} , {title_noise_type[noise_type]}")
            ax.set_xlabel(xlabels[noise_type])
            ax.set_ylabel("Performance Degradation (%)")
            xticks = list([x/10 for x in range(11)])
            yticks = list([y*10 for y in range(11)])
            ax.set_yticks(yticks)
            ax.set_yticklabels([str(y) for y in yticks])
            ax.set_xticks(xticks)
            ax.set_xticklabels(xticks)
            ax.set_xlim(-0.1, 1.1)


            # Now we plot the real language results
            if noise_type_real_points is not None and task in noise_type_real_points:
                # here, task and noise_type are fixed by the above two loops
                for lang, x, y in noise_type_real_points[task][noise_type]:
                    if x == 0 and y == 0:
                        continue
                    # The point should be annotated with the name of the language
                    ax.annotate(lang, (x, y), textcoords="offset points", xytext=(10,0), ha='center')
                    # Choose a different colour for the real language points
                    ax.scatter(x, y, color = "purple", s = point_size, marker = '^')

                # Plot a red dotted regression line for the real language points
                X = [x for lang, x, y in noise_type_real_points[task][noise_type]]
                Y = [y for lang, x, y in noise_type_real_points[task][noise_type]]
                
                if all([y == 0 for y in Y]):
                    continue

                if noise_type == 'lexical_f0.5':
                    continue

                m, b = np.polyfit(X, Y, 1)
                ax.plot(X, [m*x + b for x in X], color = "red", linestyle = "--", linewidth = 1)
                    


                    


    plt.tight_layout()  # Adjust subplots to fit into figure area.
    plt.savefig(out_filename)


es = { \
'lexical_c0': \
'''42.85	49.33	72.33
-1	-1	-1
39.82	49.67	69
39.12	48.67	71
40.25	46.67	72.67
28.45	47.33	67
23.27	44	67.33''',
'lexical_f0': \
'''42.85	49.33	72.33
40.9	47	70.67
36.42	45.67	68.67
30.77	41.67	65.67
26.37	37	65
15.42	34.33	57.33
4.88	33.33	57.67''',
'lexical_f0.5': \
'''32.59	43.67	66.67
30.52	43	69.33
27.13	42.67	67
22.7	39.67	63.33
19.97	39	64
9.21	35.67	60.33
1.95	33.67	55''',
'lexical_f0.8': \
'''28.81	43.33	63.33
27.47	43	68.33
21.07	41.67	63
28.1	41.33	66.33
15.01	41.67	65
14.15	38.67	62
5.72	37.33	57.33
1.33	34.67	53''',
'phonological': \
'''42.91	49.67	72.33
41.92	49	67
34.74	46.67	70
30.34	37.33	66
16.02	35	63.33
10.64	35.67	59.67''',
'morphological': \
'''38.63	45.33	70.67
36.19	44.67	68.33
33.34	44	70
30.12	40	66
23.74	39.67	59.67'''
}

hi = {
'lexical_c0': \
'''56.51	51	64
-1	-1	-1
53.69	51.33	65.67
49.77	52	63.67
49.77	42.33	61.33
29.09	49.67	58.67
28.1	47.67	60.67''',
'lexical_f0': \
'''56.51	51	64
52.77	48.33	65
47.05	49.33	65
40.78	47	61.67
32.22	44	55.33
16.94	41.67	54.33
6.16	38	49.67''',
'lexical_f0.5': \
'''44.86	48.67	61.67
33.92	47.67	61
30.15	38	52.33
19.71	37.67	60.67
21.79	43.67	56.33
11.03	42	56.33
2.23	36	51''',
'lexical_f0.8': \
'''25.75	39.67	60.67
27.05	42.33	56.33
27.83	36	58
22.53	39	55.67
19.11	37.33	52
13.64	40	55
5.8	37	55.67
1.74	35.67	47''',
'phonological': \
'''56.44	51	63.67
56.13	44	59.67
45.99	47.67	59.67
36.29	45	58
16.81	35	54
7.46	38.33	48''',
'morphological': \
'''51.95	47.67	66
49.16	46.67	61.67
44.88	50.67	62
43.89	46	61
38.66	43.33	57'''
}

id = {
'lexical_f0.8': \
'''36.87	-1	62
34.98	-1	61.67
32.04	-1	61
34.81	-1	54.67
22.37	-1	58.67
15.91	-1	55.33
8.73	-1	52.67
3.02	-1	49.33''',
'lexical_f0': \
'''59.12	-1	70
55.55	-1	68.67
53.49	-1	67.33
44	-1	66.33
36.19	-1	63.67
20.75	-1	55.33
7.45	-1	52.67''',
'lexical_f0.5': \
'''49.97	-1	67.67
43.61	-1	66.33
33.59	-1	67
30.94	-1	57.33
24.1	-1	57.67
11.99	-1	58.67
4.82	-1	47''',
'lexical_c0': \
'''59.12	-1	70
-1	-1	-1
55.84	-1	69.67
54.92	-1	70.67
51.74	-1	67
46.47	-1	66
36.82	-1	64.67''',
'phonological': \
'''60	-1	69.33
58.39	-1	68.67
48.58	-1	63.67
37.99	-1	65
8.81	-1	59.33
3.98	-1	54.67''',
'morphological': \
'''46.91	-1	70.33
39.17	-1	62.67
29.25	-1	61.33
23.01	-1	58.67
15.8	-1	55.67'''
}

ar = {
'lexical_f0.8': \
'''43.56	44	64.33
39.9	35	64.33
37.9	35.33	63.33
37.25	39.33	62.67
20.2	36.33	58.67
16.92	40.33	56.33
8.18	37	56.33
1.17	34.67	50.67''',
'lexical_f0': \
'''56.68	46.33	66
51.62	45.67	61.67
44.72	41.33	62
33.02	39	54
22.15	38	56.67
9.51	35.33	54.33
1.86	34.33	48.33''',
'lexical_f0.5': \
'''47.06	44	65
41.21	41	63.33
34.92	41.33	60.33
24.81	39	58
17.52	38	59.33
5.18	37	50.33
1.53	34	49.33''',
'lexical_c0': \
'''56.68	46.33	66
-1	-1	-1
55.41	45.33	64.33
54.76	44	65
52.56	42.33	63.33
53.32	45.67	64.33
48.44	40.33	63.33''',
'phonological': \
'''55.32	46	66
53.48	46.67	66
41.01	43.33	60
25.91	43.33	58.67
6.66	33.33	53
3.24	33.67	53.67''',
'morphological': \
'''52.99	44	63.33
41.25	41.33	60
31.07	39	58.33
25.29	40	55.33
19.45	37.67	51'''
}

en = {
'lexical_f0.8': \
'''60.09	51	69.67
65.29	51.67	72
44.22	51.33	70.67
35.78	49	69
34.36	34.33	63.67
34.79	47.33	62
17.23	43.33	60
9.54	38.67	53.33''',
'lexical_f0': \
'''98.94	59.67	77.33
94.97	56.33	74.33
88.14	55.67	73.67
77.72	53.67	65.33
65.6	50	62.67
48.22	47.67	60.67
24.55	42	51.67''',
'lexical_f0.5': \
'''63.88	52	74
70.86	49.67	73.67
64.82	48.67	69.33
58.78	44.33	60.33
45.01	46	64.67
23.85	43	56.33
14.67	38	53.33''',
'lexical_c0': \
'''98.94	59.67	77.33
-1	-1	-1
96.4	58.33	77.67
88.82	56.33	78
81.89	51.67	78
83.22	55.67	71.33
54.81	53	70''',
'phonological': \
'''99.53	60.33	77.33
96.22	58.33	75.33
76.92	54.33	69.67
60.93	34.33	63.33
40.32	34.67	63.33
22.74	40.67	60''',
'morphological': \
'''86.26	59.33	73
79.79	50	68.33
67.69	50.67	59
51.88	48.33	65.33
42.48	46.33	54.33'''
}

de = {
'lexical_f0.8': \
'''13.11	38	-1
17.35	39	-1
12.46	40	-1
9.58	38	-1
7.09	38.67	-1
7.43	35.67	-1
2.8	37.33	-1
1.6	34.67	-1''',
'lexical_f0': \
'''40.63	47.67	-1
36.87	48.33	-1
34.31	48.67	-1
29.16	45.33	-1
20.53	44.33	-1
11.92	38	-1
5.15	36.33	-1''',
'lexical_f0.5': \
'''24.64	42.67	-1
22.31	43	-1
17.93	42.33	-1
11.73	38.67	-1
10.43	39	-1
5.2	37	-1
2.03	35.67	-1''',
'lexical_c0': \
'''40.63	47.67	-1
-1	-1	-1
37.95	46.33	-1
33.86	44.33	-1
32.38	42.67	-1
25.5	40.33	-1
15.63	38.67	-1''',
'phonological': \
'''40.63	47.33	-1
24.68	46	-1
19.54	45	-1
5.71	42.33	-1
3.25	33.33	-1
1.65	34.67	-1''',
'morphological': \
'''32.12	46.67	-1
28.42	44	-1
25.63	44.67	-1
18.99	43	-1
18.79	41	-1'''
}

fr = {
'lexical_f0.8': \
'''44.5	44	-1
40.48	43	-1
37.25	44.67	-1
34.87	42	-1
36.67	39.67	-1
26.08	42.33	-1
12.45	40.67	-1
3.03	37	-1''',
'lexical_f0': \
'''56.2	54.67	-1
53.48	53	-1
49.71	51	-1
43.04	48	-1
36.91	42.33	-1
25.32	44.33	-1
8.48	38.33	-1''',
'lexical_f0.5': \
'''48.08	47	-1
40.8	46	-1
40.21	46.67	-1
36.52	41.67	-1
28.45	41.67	-1
20.29	41	-1
3.88	38	-1''',
'lexical_c0': \
'''56.2	54.67	-1
-1	-1	-1
54.52	53.67	-1
53.09	50	-1
53.87	49.33	-1
45.22	47	-1
46.29	44.67	-1''',
'phonological': \
'''57.34	54.67	-1
55.08	51	-1
50.76	43.33	-1
47.95	37.67	-1
37.53	37	-1
19.45	34.67	-1''',
'morphological': \
'''53.95	49	-1
50.15	47	-1
45.85	43.33	-1
42.02	39	-1
40.45	40.33	-1'''
}




all_lang_results = {"es": es, "hi": hi, "id": id, "de": de, "ar": ar, "fr": fr, "en": en}

# We'll build a results dictionary with the following structure:
# results = {lang: noise_type: {task: {noise_param: acc}}
noise_types = ["lexical_f0", "lexical_f0.5", "lexical_f0.8", "lexical_c0", "morphological", "phonological"]
all_noise_param_ranges = {
    'lexical_f0': [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8],
    'lexical_f0.5': [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8],
    'lexical_f0.8': [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8],
    'lexical_c0': [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8],
    'morphological': [0.2, 0.4, 0.6, 0.8, 1],
    'phonological': [0, 0.01, 0.05, 0.1, 0.2, 0.3],
}
tasks = ['X->eng', 'XNLI', 'XStoryCloze']

results = {}
for lang, lang_results in all_lang_results.items():
    print(lang)
    results[lang] = parse_excel_table_into_results(lang_results, all_noise_param_ranges, tasks = tasks)

print(results)

curr_noisers = results[list(results.keys())[0]].keys()
baselines = {
    lang : { 
        noise_type: {
            task: results[lang]['lexical_f0'][task][0] for task in tasks
        } for noise_type in curr_noisers
    } for lang in results.keys()
}


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

### Points on plots obtained from noise parameter posteriors on real language eval data
posteriors_str = '''0	0	0	0
0.15	0.67	0.26	0.05
0.24	0.79	0.32	0.07
0.18	0.67	0.24	0.05
0.14	0.7	0.26	0.05
0.2	0.81	0.34	0.04
0	0	0	0
0.19	0.46	0.13	0.06
0	0	0	0
0.22	0.71	0.2	0.11
0	0	0	0
0.47	0.88	0.73	0.09
0	0	0	0
0.5	0.98	0.71	0.1
0.75	0.99	0.68	0.15
0.56	0.99	0.7	0.1
0	0	0	0
0.09	0.32	0.08	0.03
0.06	0.25	0.04	0.04
0.2	0.43	0.11	0.05
0.21	0.55	0.15	0.04
0.21	0.64	0.18	0.04
0.02	0.02	0.01	0.05
0.32	0.6	0.12	0.03
0.19	0.5	0.1	0.04'''

degradations = '''0
34.39
42.63
41.11
26.52
49.68
0
11.65
0
-9.55
0
33.03
0.00
60.32
90.04
59.52
0
56.31
15.47
21.28
30.86
19.72
12.58
9.33
40.26'''

langs_real_points = '''hin
awa
bho
hne
mag
mai
ind
zsm
spa
glg
fra
oci
deu
dan
isl
swe
arb
acm
acq
aeb
ajp
apc
ars
ary
arz'''

posteriors = [(float(x), float(y), float(z), float(w)) \
              for x, y, z, w in [line.split() for line in posteriors_str.split("\n")]]
# post_df = pd.DataFrame(posteriors, columns = ["theta_content", "theta_functional", "theta_morph"])
degradations = [float(x) for x in degradations.split("\n")]

langs_real_points = [lang for lang in langs_real_points.split("\n")]

noise_type_real_points_xeng = {noise_type: list() for noise_type in curr_noisers}
for lang, post, deg in zip(langs_real_points, posteriors, degradations):
    theta_c, theta_f, theta_m, theta_p = post
    if theta_f > 0.7:
        noise_type_real_points_xeng["lexical_f0.8"].append((lang, theta_c, deg))
    elif theta_f >= 0.3:
        noise_type_real_points_xeng["lexical_f0.5"].append((lang, theta_c, deg))
    else:
        noise_type_real_points_xeng["lexical_f0"].append((lang, theta_c, deg))
    
    noise_type_real_points_xeng["lexical_c0"].append((lang, theta_f, deg))
    noise_type_real_points_xeng["morphological"].append((lang, theta_m, deg))
    noise_type_real_points_xeng["phonological"].append((lang, theta_p, deg))

noise_type_real_points = dict()
noise_type_real_points["X->eng"] = noise_type_real_points_xeng

plot_results(results, tasks, curr_noisers, all_noise_param_ranges, noise_type_real_points = noise_type_real_points)

print("\n\n\n\n BASELINES")
print(baselines)

# Archive:
## This has the old morph results: without language specific thresholds, and not noising aux 
## XNLI noises the label words for all EXCEPT lexical_f0.5 (which has new XNLI results)
# es = { \
# 'lexical_f0.5': \
# '''32.59	43.67	66.67
# 30.52	43	69.33
# 27.13	42.67	67
# 22.7	39.67	63.33
# 19.97	39	64
# 9.21	35.67	60.33
# 1.95	33.67	55''',
# 'lexical': \
# '''42.91	49.67	72.33
# 26.57	43	68.33
# 26.52	41.67	63
# 28.1	41.33	66.33
# 15.01	41.67	65
# 13.56	38.67	62
# 5.72	37.33	57.33''',
# 'phonological': \
# '''42.91	49.67	72.33
# 41.92	49	67
# 34.74	46.67	70
# 30.34	37.33	66
# 16.02	35	63.33
# 10.64	35.67	59.67''',
# 'morphological': \
# '''42.91	49.67	72.33
# 40.78	48	70.33
# 34.5	44	68.67
# 33.62	40	70.67
# 32.04	40.33	66.33
# 30	35.33	65.67'''
# }

# hi = {
# 'lexical_f0.5': \
# '''44.86	48.67	61.67
# 33.92	47.67	61
# 30.15	38	52.33
# 19.71	37.67	60.67
# 21.79	43.67	56.33
# 11.03	42	56.33
# 2.23	36	51''',
# 'lexical': \
# '''56.44	51	63.67
# 27.05	42.33	56.33
# 27.83	36	58
# 22.53	39	55.67
# 19.11	37.33	52
# 13.64	40	55
# 5.8	-1	-1''',
# 'phonological': \
# '''56.44	51	63.67
# 56.13	44	59.67
# 45.99	47.67	59.67
# 36.29	45	58
# 16.81	35	54
# 7.46	38.33	48''',
# 'morphological': \
# '''56.44	51	63.67
# 53.64	50.33	62
# 46.82	47.33	60.67
# 44.77	50	60.33
# 42.21	46.33	59.33
# 38.39	47.33	55.33'''
# }

# id = {
# 'lexical_f0.5': \
# '''49.97	-1	67.67
# 43.61	-1	66.33
# 33.59	-1	67
# 30.94	-1	57.33
# 24.1	-1	57.67
# 11.99	-1	58.67
# 4.82	-1	47''',
# 'lexical': \
# '''60	-1	69.33
# 34.98	-1	61.67
# 32.04	-1	61
# 34.81	-1	54.67
# 22.37	-1	58.67
# 15.91	-1	55.33
# 8.73	-1	-1''',
# 'phonological': \
# '''60	-1	69.33
# 58.39	-1	68.67
# 48.58	-1	63.67
# 37.99	-1	65
# 8.81	-1	59.33
# 3.98	-1	54.67''',
# 'morphological': \
# '''60	-1	69.33
# 49.04	-1	64
# 50.17	-1	58.33
# 42.76	-1	61
# 26.51	-1	56
# 21.81	-1	58.67'''
# }

# ar = {
# 'lexical_f0.5': \
# '''-1	-1	-1
# -1	-1	-1
# -1	-1	-1
# -1	-1	-1
# -1	-1	-1
# -1	-1	-1
# -1	-1	-1''',
# 'lexical': \
# '''55.32	46	66
# 39.9	35	64.33
# 37.9	35.33	63.33
# 37.25	39.33	62.67
# 20.2	36.33	58.67
# 16.92	40.33	56.33
# 8.18	-1	-1''',
# 'phonological': \
# '''55.32	46	66
# 53.48	46.67	66
# 41.01	43.33	60
# 25.91	43.33	58.67
# 6.66	33.33	53
# 3.24	33.67	53.67''',
# 'morphological': \
# '''55.32	46	66
# 49.77	45.33	60.67
# 44.06	45	55.67
# 37.36	41.33	57
# 31.33	39	54.67
# 23.96	40.67	52'''
# }

# en = {
# 'lexical_f0.5': \
# '''63.88	52	74
# 70.86	49.67	73.67
# 64.82	48.67	69.33
# 58.78	44.33	60.33
# 45.01	46	64.67
# 23.85	43	56.33
# 14.67	38	53.33''',
# 'lexical': \
# '''99.53	60.33	77.33
# 65.29	34.67	72
# 44.22	34.33	70.67
# 35.78	49	69
# 34.36	34.33	63.67
# 34.79	34.33	62
# 17.23	-1	-1''',
# 'phonological': \
# '''99.53	60.33	77.33
# 96.22	58.33	75.33
# 76.92	54.33	69.67
# 60.93	34.33	63.33
# 40.32	34.67	63.33
# 22.74	40.67	60''',
# 'morphological': \
# '''99.53	60.33	77.33
# 87.66	34	72.33
# 84.9	57	68
# 69.66	52	66.67
# 56.96	34.33	61.67
# 51.1	33.67	59.67'''
# }

# de = {
# 'lexical_f0.5': \
# '''24.64	42.67	-1
# 22.31	43	-1
# 17.93	42.33	-1
# 11.73	38.67	-1
# 10.43	39	-1
# 5.2	37	-1
# 2.03	35.67	-1''',
# 'lexical': \
# '''-1	-1	-1
# -1	-1	-1
# -1	-1	-1
# -1	-1	-1
# -1	-1	-1
# -1	-1	-1
# -1	-1	-1''',
# 'phonological': \
# '''-1	47.33	-1
# -1	46	-1
# -1	45	-1
# -1	42.33	-1
# -1	33.33	-1
# -1	34.67	-1''',
# 'morphological': \
# '''-1	47.33	-1
# -1	47.33	-1
# -1	45.67	-1
# -1	34	-1
# -1	44.67	-1
# -1	43.33	-1'''
# }

# fr = {
# 'lexical_f0.5': \
# '''48.08	47	-1
# 40.8	46	-1
# 40.21	46.67	-1
# 36.52	41.67	-1
# 28.45	41.67	-1
# 20.29	41	-1
# 3.88	38	-1''',
# 'lexical_f0.8': \
# '''57.34	-1	-1
# 40.48	-1	-1
# 37.25	-1	-1
# 34.87	-1	-1
# 36.67	-1	-1
# 26.08	-1	-1
# 12.45	-1	-1''',
# 'phonological': \
# '''57.34	-1	-1
# 55.08	-1	-1
# 50.76	-1	-1
# 47.95	-1	-1
# 37.53	-1	-1
# 19.45	-1	-1''',
# 'morphological': \
# '''57.34	-1	-1
# 53.9	-1	-1
# 52.65	-1	-1
# 48.81	-1	-1
# 44.92	-1	-1
# 45.27	-1	-1'''
# }
