from phonological import PhonologicalNoiser
from character_level import CharacterLevelNoiser

from collections import defaultdict

NOISE_REGISTRY = {
    'phonological': PhonologicalNoiser,
    'character_level': CharacterLevelNoiser
}

def parse_noise_params(noise_params_str):
    '''
    Parse noise parameters e.g. phonological:theta_1=0.5,theta_2=0.2;syntax:theta_2=0.5
    Args:
        noise_params_str: str, noise parameters
    Returns:
        dict, noise parameters, like {phonological: {theta_1: 0.5}}
    
    '''
    all_noise_params = defaultdict(dict)
    
    all_noise_type_params = noise_params_str.split(";")
    for noise_type_params in all_noise_type_params: # phonological:theta_1=0.5,theta_2=0.2
        noise_type = noise_type_params.split(":")[0] # phonological
        noise_type_params = noise_type_params.split(":")[1] # theta_1=0.5,theta_2=0.2
        noise_type_params = noise_type_params.split(",") # [theta_1=0.5,theta_2=0.2]
        for noise_param in noise_type_params:
            param_name = noise_param.split("=")[0]
            param_value = noise_param.split("=")[1]
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