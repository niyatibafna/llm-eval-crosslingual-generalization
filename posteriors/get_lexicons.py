import json

def json_to_list_of_pairs(bil_lexicon_json_file):
    '''
    Assuming that the structure of the original is 
    src: {tgt1: freq1, tgt2: freq2, ...}
    '''
    with open(bil_lexicon_json_file) as f:
        bil_lexicon_dict = json.load(f)
    
    punctuation = ".,;:?!-_()[]{}\"'`~@#$%^&*+=|\\<>/"
    
    bil_lexicon = list()
    for src in bil_lexicon_dict:
        # Pick best target
        if src in bil_lexicon_dict[src]:
            src = src.lower().strip(punctuation)
            if src:
                bil_lexicon.append((src, src))
            continue
        if isinstance(bil_lexicon_dict[src], str):
            tgt = bil_lexicon_dict[src]
        else:
            tgt = max(bil_lexicon_dict[src], key=bil_lexicon_dict[src].get)
            src = src.lower().strip(punctuation)
            tgt = tgt.lower().strip(punctuation)
        if src and tgt:
            bil_lexicon.append((src, tgt))

    return bil_lexicon

def google_translate_lexicon(bil_lexicon, src_lang, tgt_lang, outpath = None):
    '''
    Assuming that the structure of the original is 
    src: {tgt1: freq1, tgt2: freq2, ...}
    '''
    import googletrans
    print(f"Processing {src_lang} to {tgt_lang}...")
    google_lexicon = dict()
    for src, tgt in bil_lexicon:
        tgt = googletrans.Translator().translate(src, src=src_lang, dest=tgt_lang).text
        google_lexicon[src] = tgt
        if len(google_lexicon) == 500:
            break

    if outpath:
        with open(outpath, "w") as f:
            json.dump(google_lexicon, f, indent=2, ensure_ascii=False)
    
    return google_lexicon

# bil_lexicon = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/flores_lexicons_raw/deu_swe.json"
# src_lang = "de"
# tgt_lang = "sv"
# outpath = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/google_translate_lexicons/deu_swe.json"

# google_translate_lexicon(json_to_list_of_pairs(bil_lexicon), src_lang, tgt_lang, outpath)

# bil_lexicon = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/flores_lexicons_raw/deu_dan.json"
# src_lang = "de"
# tgt_lang = "da"
# outpath = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/google_translate_lexicons/deu_dan.json"

# google_translate_lexicon(json_to_list_of_pairs(bil_lexicon), src_lang, tgt_lang, outpath)

# bil_lexicon = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/flores_lexicons_raw/deu_isl.json"
# src_lang = "de"
# tgt_lang = "is"
# outpath = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/google_translate_lexicons/deu_isl.json"

# google_translate_lexicon(json_to_list_of_pairs(bil_lexicon), src_lang, tgt_lang, outpath)

# bil_lexicon = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/flores_lexicons_raw/ind_zsm.json"
# src_lang = "id"
# tgt_lang = "ms"
# outpath = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/google_translate_lexicons/ind_zsm.json"

# google_translate_lexicon(json_to_list_of_pairs(bil_lexicon), src_lang, tgt_lang, outpath)