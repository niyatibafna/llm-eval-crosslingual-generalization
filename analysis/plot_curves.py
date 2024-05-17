import matplotlib.pyplot as plt

# Increase fontsize for all labels, legends, and titles
plt.rcParams.update({'font.size': 20})


########## HINDI ######################

## LEXICAL NOISE
# Data
x_axis = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
tasks = {
    "X->eng": [56.44, 27.05, 27.83, 22.53, 19.11, 13.64, 5.8],
    "XNLI": [51, 42.33, 36, 39, 37.33, 40, None],  # None added for missing value
    "XStoryCloze": [63.67, 56.33, 58, 55.67, 52, 55, None]

}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)


# Labels and title
plt.xlabel('Theta_content')
plt.ylabel('Scores')
# plt.title('XNLI, XStoryCloze, X->eng scores with lexical noise for Hindi')
plt.legend()
plt.grid(True)

# Show plot
plt.savefig("curves/hin_lex_xnli_xstorycloze_flores200.png")

## PHONOLOGICAL NOISE

# Data
x_axis = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
tasks = {
    "X->eng": [56.44, 56.13, 45.99, 36.29, 16.81, 7.46, None],
    "XNLI": [51, 44, 47.67, 45, 35, 38.33, None],  # None added for missing value
    "XStoryCloze": [63.67, 59.67, 59.67, 58, 54, 48, None]

}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)

# Labels and title
plt.xlabel('Theta_phon')
plt.ylabel('Scores')
# plt.title('XNLI, XStoryCloze, X->eng scores with phonological noise for Hindi')
plt.legend()
plt.grid(True)

# Show plot
plt.savefig("curves/hin_phon_xnli_xstorycloze_flores200.png")

## MORPHOLOGICAL NOISE

# Data
x_axis = [0, 0.2, 0.4, 0.6, 0.8, 1]
tasks = {
    "X->eng": [56.44, 53.64, 46.82, 44.77, 42.21, 38.39],
    "XNLI": [51, 50.33, 47.33, 50, 46.33, 47.33],
    "XStoryCloze": [63.67, 62, 60.67, 60.33, 59.33, 55.33]

}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)

# Labels and title
plt.xlabel('Theta_morph')
plt.ylabel('Scores')
# plt.title('XNLI, XStoryCloze, X->eng scores with morphological noise for Hindi')
plt.legend()
plt.grid(True)

# Show plot
plt.savefig("curves/hin_morph_xnli_xstorycloze_flores200.png")


############ SPANISH #################

# LEXICAL NOISE
'''
X->eng XNLI XStoryCloze 
42.91	49.67	72.33
26.57	43	68.33
26.52	41.67	63
28.1	41.33	66.33
15.01	41.67	65
13.56	38.67	62
5.72	37.33	57.33'''

# Data
x_axis = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
tasks = {
    "X->eng": [42.91, 26.57, 26.52, 28.1, 15.01, 13.56, 5.72],
    "XNLI": [49.67, 43, 41.67, 41.33, 41.67, 38.67, 37.33],
    "XStoryCloze": [72.33, 68.33, 63, 66.33, 65, 62, 57.33]

}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)

# Labels and title
plt.xlabel('Theta_content')
plt.ylabel('Scores')
# plt.title('XNLI, XStoryCloze, X->eng scores with lexical noise for Spanish')
plt.legend()
plt.grid(True)

# Show plot
plt.savefig("curves/spa_lex_xnli_xstorycloze_flores200.png")

## PHONOLOGICAL NOISE
'''
X->eng XNLI XStoryCloze 
42.91	49.67	72.33
41.92	49	67
34.74	46.67	70
30.34	37.33	66
16.02	35	63.33
10.64	35.67	59.67
'''

# Data
x_axis = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
tasks = {
    "X->eng": [42.91, 41.92, 34.74, 30.34, 16.02, 10.64, None],
    "XNLI": [49.67, 49, 46.67, 37.33, 35, 35.67, None],
    "XStoryCloze": [72.33, 67, 70, 66, 63.33, 59.67, None]

}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)

# Labels and title
plt.xlabel('Theta_phon')
plt.ylabel('Scores')
# plt.title('XNLI, XStoryCloze, X->eng scores with phonological noise for Spanish')

plt.legend()
plt.grid(True)

# Show plot
plt.savefig("curves/spa_phon_xnli_xstorycloze_flores200.png")

## MORPHOLOGICAL NOISE

theta_morph = [0, 0.2, 0.4, 0.6, 0.8, 1]
'''
56.44	51	63.67
53.64	50.33	62
46.82	47.33	60.67
44.77	50	60.33
42.21	46.33	59.33
38.39	47.33	55.33'''

# Data
x_axis = [0, 0.2, 0.4, 0.6, 0.8, 1]
tasks = {
    "X->eng": [56.44, 53.64, 46.82, 44.77, 42.21, 38.39],
    "XNLI": [51, 50.33, 47.33, 50, 46.33, 47.33],
    "XStoryCloze": [63.67, 62, 60.67, 60.33, 59.33, 55.33]

}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)

# Labels and title
plt.xlabel('Theta_morph')
plt.ylabel('Scores')
# plt.title('XNLI, XStoryCloze, X->eng scores with morphological noise for Spanish')
plt.legend()
plt.grid(True)

# Show plot
plt.savefig("curves/spa_morph_xnli_xstorycloze_flores200.png")

########### Indonesian ################

# LEXICAL NOISE
'''
60	69.33
34.98		61.67
32.04		61
34.81		54.67
22.37		58.67
15.91		55.33
8.73		'''

# Data
x_axis = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
tasks = {
    "X->eng": [60, 34.98, 32.04, 34.81, 22.37, 15.91, 8.73],
    "XStoryCloze": [69.33, 61.67, 61, 54.67, 58.67, 55.33, None],
}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)

# Labels and title
plt.xlabel('Theta_content')
plt.ylabel('Scores')
# plt.title('XStoryCloze, X->eng scores with lexical noise for Indonesian')
plt.legend()

plt.grid(True)

# Show plot
plt.savefig("curves/ind_lex_xstorycloze_xeng_flores200.png")

## PHONOLOGICAL NOISE
'''
60		69.33
58.39	68.67
48.58	63.67
37.99	65
8.81	59.33
3.98	54.67
'''

# Data
x_axis = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.5]
tasks = {
    "X->eng": [60, 58.39, 48.58, 37.99, 8.81, 3.98, None],
    "XStoryCloze": [69.33, 68.67, 63.67, 65, 59.33, 54.67, None],
}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)

# Labels and title
plt.xlabel('Theta_phon')
plt.ylabel('Scores')
# plt.title('XStoryCloze, X->eng scores with phonological noise for Indonesian')
plt.legend()
plt.grid(True)

# Show plot
plt.savefig("curves/ind_phon_xstorycloze_xeng_flores200.png")

## MORPHOLOGICAL NOISE
'''
60		69.33
49.04		64
50.17		58.33
42.76		61
26.51		56
21.81		58.67
'''

# Data
x_axis = [0, 0.2, 0.4, 0.6, 0.8, 1]
tasks = {
    "X->eng": [60, 49.04, 50.17, 42.76, 26.51, 21.81],
    "XStoryCloze": [69.33, 64, 58.33, 61, 56, 58.67],
}

# Plotting
plt.figure(figsize=(10, 6))

# Plotting for each task
for task, values in tasks.items():
    plt.plot(x_axis, values, marker='o', label=task)

# Labels and title
plt.xlabel('Theta_morph')
plt.ylabel('Scores')
# plt.title('XStoryCloze, X->eng scores with morphological noise for Indonesian')
plt.legend()
plt.grid(True)

# Show plot
plt.savefig("curves/ind_morph_xstorycloze_xeng_flores200.png")
