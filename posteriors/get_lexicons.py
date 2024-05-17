import json

def json_to_list_of_pairs(bil_lexicon_json_file):
    '''
    Assuming that the structure of the original is 
    src: {tgt1: freq1, tgt2: freq2, ...}
    '''
    with open(bil_lexicon_json_file) as f:
        bil_lexicon_dict = json.load(f)
    
    bil_lexicon = list()
    for src in bil_lexicon_dict:
        # Pick best target
        if src in bil_lexicon_dict[src]:
            bil_lexicon.append((src, src))
            continue
        tgt = max(bil_lexicon_dict[src], key=bil_lexicon_dict[src].get)
        bil_lexicon.append((src, tgt))

    return bil_lexicon
    