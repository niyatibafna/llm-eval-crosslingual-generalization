from phonological import PhonologicalNoiser

NOISE_REGISTRY = {
    'phonological': PhonologicalNoiser,
}

def get_noisers(all_noise_params):
    '''Initialize noisers with noise parameters
    Args:
        input: str, input text
        all_noise_params: dict, noise parameters, like {phonological: {theta_1: 0.5}}
    Returns:
        
    '''
    # Initialize noisers
    noise_classes = list()
    for noise_type, noise_params in all_noise_params.items():
        noiser = NOISE_REGISTRY[noise_type](noise_params)
        noise_classes.append(noiser)
    
    return noise_classes

def apply_noisers(input, noise_classes):
    '''Apply noise to input
    Args:
        input: str, input text
        noise_classes: list, list of noisers
    Returns:
        str, noised text
    '''
    for noiser in noise_classes:
        input = noiser.apply_noise(input)
    return input