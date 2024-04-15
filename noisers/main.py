from phonological import PhonologicalNoiser
from character_level import CharacterLevelNoiser
from lexical import GlobalLexicalNoiser

from collections import defaultdict
import regex

NOISE_REGISTRY = {
    'phonological': PhonologicalNoiser,
    'character_level': CharacterLevelNoiser,
    'lexical': GlobalLexicalNoiser,
}

def parse_noise_params(noise_params_str):
    '''
    Parse noise parameters e.g. phonological:theta_1=0.5,theta_2=0.2;syntax:theta_2=0.5
    Args:
        noise_params_str: str, noise parameters
    Returns:
        dict, noise parameters, like {phonological: {theta_1: 0.5}}
    
    '''
    if noise_params_str == "":
        return defaultdict(dict)

    all_noise_params = defaultdict(dict)

    # We will ignore anything enclosed in <>
    ## Extract text enclosed in <>
    text_files = regex.findall(r'<(.*?)>', noise_params_str)
    ## Replace text enclosed in <> with a placeholder
    noise_params_str = regex.sub(r'<(.*?)>', "<placeholder>", noise_params_str)

    print(noise_params_str)

    all_noise_type_params = noise_params_str.split(";")
    for noise_type_params in all_noise_type_params: # phonological:theta_1=0.5,theta_2=0.2
        noise_type = noise_type_params.split("-")[0] # phonological
        noise_type_params = noise_type_params.split("-")[1] # theta_1=0.5,theta_2=0.2
        noise_type_params = noise_type_params.split(",") # [theta_1=0.5,theta_2=0.2]
        for noise_param in noise_type_params:
            param_name = noise_param.split("=")[0]
            param_value = noise_param.split("=")[1]
            print(param_name, param_value)
            # If param_value is a placeholder, replace it with the actual text_file
            if param_value == "<placeholder>":
                all_noise_params[noise_type][param_name] = text_files.pop(0)
            else:
                try:
                    all_noise_params[noise_type][param_name] = float(param_value)
                except:
                    all_noise_params[noise_type][param_name] = param_value

    return all_noise_params
    

def get_noisers(all_noise_params):
    '''Initialize noisers with noise parameters
    Args:
        input: str, input text
        all_noise_params: dict, noise parameters, like {phonological: {theta_1: 0.5}}
    Returns:
        noise_classes: list, list of noiser class objects
    '''
    if not all_noise_params:
        return list()

    # Initialize noiser objects from noise type classes
    noise_classes = list()
    for noise_type, noise_params in all_noise_params.items():
        noiser = NOISE_REGISTRY[noise_type](noise_params)
        noise_classes.append(noiser)
    
    return noise_classes

def apply_noisers(input, noise_classes, verbose = False):
    '''Apply noise to input
    Args:
        input: str, input text
        noise_classes: list, list of noisers
    Returns:
        str, noised text
    '''
    for noiser in noise_classes:
        if verbose:
            print(f"Applying noise: {noiser}")
        input = noiser.apply_noise(input)
    return input

def record_noiser_artifacts(noise_classes):
    '''Save noiser artifacts to output file
    Args:
        noise_classes: list, list of noisers
    '''
    for noiser in noise_classes:
        noiser.record_noiser_artifacts()