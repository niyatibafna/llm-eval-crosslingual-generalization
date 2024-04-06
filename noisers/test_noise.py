'''This file is for testing out various noise classes'''
from main import parse_noise_params, get_noisers, apply_noisers

noise_specs = "phonological:theta_1=0.5,theta_2=0.2;character_level:script=devanagari,insert_theta=0.1,delete_theta=0.1,swap_theta=0.1"
all_noise_params = parse_noise_params(noise_specs)
print(f"Noise Parameters: {all_noise_params}")

noiser_classes = get_noisers(all_noise_params)
print(f"Noiser Classes: {noiser_classes}")

inputs = ["The quick brown fox jumps over the lazy dog", "जल में रहकर मगर से बैर"]

for input in inputs:
    print(f"Input: {input}")
    noised = apply_noisers(input, noiser_classes, verbose=True)
    print(f"Noised: {noised}")
    print()

# import sys
# sys.path.append("/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation/lm_eval/")
# sys.path.append("/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/mlmm-evaluation/")
# from tasks.hellaswag import HellaSwag

# task = HellaSwag()
# print(task.NUM_FEW_SHOT)