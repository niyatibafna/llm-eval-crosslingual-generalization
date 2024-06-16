import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

plt.figure(figsize=(4, 2))


x = ["0", "0.05", "0.1", "0.2", "0.3", "0.5", "0.8"]

# Hindi
# baselines = 56.44 51	64
hi_baseline = 51
random_baseline = 33.33

hi_y = '''44.24
43.43
41.19
40.38
40.19
37.24
36.86'''

ar_baseline = 44
random_baseline = 33.33

ar_y = '''41.81
41.0
38.7
36.97
35.6
34.97
34.3'''


def get_degradation(res, baseline):
    return (baseline - res)*100 / (baseline - random_baseline)

for lang, baseline, y in [("hi", hi_baseline, hi_y), ("ar", ar_baseline, ar_y)]:

    colour = "red" if lang == "hi" else "blue"
    degradation = [get_degradation(float(x), baseline) for x in y.split("\n")]

    # Plot :
    ## 1. horizontal line showing morph_baseline_degradation
    ## 2. points and regression line showing only lex degradation
    ## 3. points and regression line showing lex morph degradation
    ## 4. additive degradation line

    x = np.array([0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.8]).reshape(-1, 1)
    y = np.array(degradation).reshape(-1, 1)
    x = x[:-1]
    y = y[:-1]

    plt.scatter(x, y, label=lang, marker = "x", s = 4, linewidths = 8, \
                           color=colour)
    m, b = np.polyfit(x.flatten(), y.flatten(), 1)
    plt.plot(x, m*x + b, linestyle = '--', linewidth=2, color=colour)

    # reg = LinearRegression().fit(x[:-1], y[:-1])

    # plt.plot(x, y, 'o', color=colour, label=f"{lang}")
    # plt.plot(x, reg.predict(x), linestyle = '--', linewidth=2, color=colour)
    plt.ylabel("Perf. Deg. (%)")
    plt.xlabel(r"$\theta_c$")
    plt.ylim(0, 100)
    plt.legend()

plt.title(r"XNLI, Lexical (Content $\vert$ $\theta_f = 0.8$) : $\psi^{f,c}_{0.8,*}$")

plt.savefig("plots/xnli_meanoverruns.pdf", bbox_inches='tight', dpi=300)

