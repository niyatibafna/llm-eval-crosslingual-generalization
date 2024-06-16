
def degradation(res, baseline, random_baseline):
    return (baseline - res)*100 / (baseline - random_baseline)


def plot_composite(only_lex, lex_morph, morph_baseline, baseline, random_baseline, task, filename):
    
    only_lex = [float(x) for x in only_lex.split("\n")]
    lex_morph = [float(x) for x in lex_morph.split("\n")]

    only_lex_degradation = [degradation(x, baseline, random_baseline) for x in only_lex]
    lex_morph_degradation = [degradation(x, baseline, random_baseline) for x in lex_morph]
    morph_baseline_degradation = degradation(morph_baseline, baseline, random_baseline)
    additive_degradation = [x + morph_baseline_degradation for x in only_lex_degradation]

    # Plot :
    ## 1. horizontal line showing morph_baseline_degradation
    ## 2. points and regression line showing only lex degradation
    ## 3. points and regression line showing lex morph degradation
    ## 4. additive degradation line

    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.linear_model import LinearRegression
    plt.figure(figsize=(4, 2))

    x = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8]).reshape(-1, 1)
    y = np.array(only_lex_degradation).reshape(-1, 1)
    reg = LinearRegression().fit(x, y)
    plt.scatter(x, y)

    # plt.axhline(y=morph_baseline_degradation, color='r', linestyle='--', label=r"Only morph: $\psi^m_{0.5}$", linewidth=2)
    plt.axhline(y=morph_baseline_degradation, color='r', linestyle='--', label=r"$\psi^m_{0.5}$", linewidth=2)

    # plt.plot(x, reg.predict(x), label=r'$\psi^{f,c}_{0.5,*}$:cont $\vert$ $\theta_f = 0.5$', linestyle='--', linewidth=2)
    plt.plot(x, reg.predict(x), label=r'$\psi^{f,c}_{0.5,*}$', linestyle='--', linewidth=2)

    
    x = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8]).reshape(-1, 1)
    y = np.array(additive_degradation).reshape(-1, 1)
    reg = LinearRegression().fit(x, y)
    plt.scatter(x, y)
    # plt.plot(x, reg.predict(x), label=r"Theoretical:$\psi^{f,c}_{0.5,*}+\psi^m_{0.5}$", linestyle='--', linewidth=2)
    plt.plot(x, reg.predict(x), label=r"$\psi^{f,c}_{0.5,*}+\psi^m_{0.5}$", linestyle='--', linewidth=2)

    x = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8]).reshape(-1, 1)
    y = np.array(lex_morph_degradation).reshape(-1, 1)
    reg = LinearRegression().fit(x, y)
    plt.scatter(x, y)
    # plt.plot(x, reg.predict(x), label=r'$\psi^{f,c,m}_{0.5,*,0.5}$:cont $\vert$ $\theta_f = 0.5$,$\theta_m = 0.5$', linestyle='--', linewidth=2)
    plt.plot(x, reg.predict(x), label=r'$\psi^{f,c,m}_{0.5,*,0.5}$', linestyle='--', linewidth=2)



    # plt.axhline(y=0, color='g', linestyle='--', label="Baseline Degradation")
    plt.xlabel(r"$\theta_c$")
    plt.ylim(0, 100)
    # plt.title(f"Hindi, {task}:" + r"$\psi^{f,c,m}_{0.5,*,0.5}$")
    # Make legend next to plot
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # Make legend smaller
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 6})
    plt.savefig(f"plots/{filename}", bbox_inches='tight')


# X->eng
random_baseline = 0
baseline = 56.44

morph_baseline = 47.02

only_lex = '''33.92
30.15
19.71
21.79
11.03
2.23'''

lex_morph = '''33.47
27.28
24.26
13.04
10.87
4.32'''

plot_composite(only_lex, lex_morph, morph_baseline, baseline, random_baseline, "X->eng", "composite_lex_morph_flores.pdf")

# XNLI
baseline = 51
morph_baseline = 48.67
random_baseline = 33.33

only_lex = '''47.67
38
37.67
43.67
42
36'''

lex_morph = '''43.33
43.33
42.67
44
38
36.33'''

plot_composite(only_lex, lex_morph, morph_baseline, baseline, random_baseline, "XNLI", "composite_lex_morph_xnli.pdf")

baseline = 64
morph_baseline = 61.8
random_baseline = 50

only_lex = '''61
52.33
60.67
56.33
56.33
51'''

lex_morph = '''58.67
56.33
53
53.33
51.33
49'''

plot_composite(only_lex, lex_morph, morph_baseline, baseline, random_baseline,"XSC", "composite_lex_morph_xsc.pdf")