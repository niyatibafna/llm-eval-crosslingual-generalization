from phonological import PhonologicalNoiser

NOISE_REGISTRY = {
    'phonological': PhonologicalNoiser,
}

def noiser_main(input, all_noise_params):
    '''Apply noise to input according to noise_params
    Args:
        input: str, input text
        all_noise_params: dict, noise parameters, like {phonological: {theta_1: 0.5}}
    Returns:
        str, noised text
    '''
    # Apply noise
    for noise_type, noise_params in all_noise_params.items():
        noiser = NOISE_REGISTRY[noise_type](noise_params)
        input = noiser.apply_noise(input)
    
    return input