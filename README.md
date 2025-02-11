# Evaluating LLMs along Dimensions of Language Variation: A Systematic Investigation of Cross-Lingual Generalization

This repo contains the code for this paper: https://arxiv.org/pdf/2406.13718.

* More detailed documentation coming soon *

Short version:
If you want to add your own noiser and compute trends over its parametrization, drop your noiser class in `noisers/` (it needs a function `apply_noise`), and add it to `NOISE_REGISTRY` in `noisers/main.py`. See example runs in `experiments/`.

If you are mainly interested in the noisers here, check out our [DialUp repository](https://github.com/niyatibafna/dialup) which contains documentation and run instructions for these noisers.
