from phonological import GlobalPhonologicalNoiser
from character_level import CharacterLevelNoiser
from lexical import GlobalLexicalNoiser
from morphological import GlobalMorphologicalNoiser
# from google_translate import GoogleTranslateNoiser

from collections import defaultdict
import regex

NOISE_REGISTRY = {
    'phonological': GlobalPhonologicalNoiser,
    'character_level': CharacterLevelNoiser,
    'lexical': GlobalLexicalNoiser,
    'morph': GlobalMorphologicalNoiser,
    # 'gtrans': GoogleTranslateNoiser,
}

def parse_noise_params(noise_params_str):
    '''
    Parse noise parameters e.g. phonological-theta_1=0.5,theta_2=0.2;syntax-theta_2=0.5
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
    if len(noise_classes) > 1:
        return apply_noisers_compose(input, noise_classes, verbose)

    for noiser in noise_classes:
        if verbose:
            print(f"Applying noise: {noiser}")
        input = noiser.apply_noise(input)
    return input

def apply_noisers_compose(input, noise_classes, verbose = False):
    '''Apply noise to input, compose all noisers
    Args:
        input: str, input text
        noise_classes: list, list of noisers
    Returns:
        str, noised text
    '''
    noise_type_output = dict()
    for noiser in noise_classes:
        if verbose:
            print(f"Applying noise: {noiser}")
        noise_type_output[noiser.class_name] = noiser.apply_noise(input).split()

        assert len(input.split()) == len(noise_type_output[noiser.class_name])

    print(noise_type_output)
    
    # If some kind of noise is not applied, we will add it as the original input
    for noiser in {"GlobalPhonologicalNoiser", "GlobalLexicalNoiser", "GlobalMorphologicalNoiser"}:
        if noiser not in noise_type_output:
            noise_type_output[noiser] = input.split()

    # Now we will compose these outputs
    ## We assume that the order is phonological, morphological, lexical
    final_output = list()

    for i, word in enumerate(input.split()):
        noised_word = word
        if noise_type_output['GlobalLexicalNoiser'][i] != word:
            # If lexical noiser has changed the word, we will use that
            noised_word = noise_type_output['GlobalLexicalNoiser'][i]
            final_output.append(noised_word)
            continue
        # Else we take the phonological noised word
        noised_word = noise_type_output['GlobalPhonologicalNoiser'][i]

        # If morphological change changed the suffix, we'll apply the new suffix
        if noise_type_output['GlobalMorphologicalNoiser'][i] != word:
            morph_noised_word = noise_type_output['GlobalMorphologicalNoiser'][i]
            ## First let's find the suffix
            ## The stem is simply the longest shared prefix
            stem = ""
            for j in range(min(len(word), len(morph_noised_word))):
                if word[j] == morph_noised_word[j]:
                    stem += word[j]
                else:
                    break
            ## The suffix is the remaining part
            morph_noised_suffix = morph_noised_word[len(stem):]

            phon_noised_stem = noised_word[:len(stem)]
            noised_word = phon_noised_stem + morph_noised_suffix

            ## All of the above assumes that phon noise preserves the length of the word
            ## which thankfully it does
        final_output.append(noised_word)

    return " ".join(final_output)

def record_noiser_artifacts(noise_classes):
    '''Save noiser artifacts to output file
    Args:
        noise_classes: list, list of noisers
    '''
    for noiser in noise_classes:
        noiser.record_noiser_artifacts()