import json

lexicon_path = "/Users/work/Desktop/projects/llm-robustness-to-xlingual-noise/posteriors/flores_lexicons_raw/hin_mai.json"
with open(lexicon_path, "r") as f:
    lexicon = json.load(f)

# For every source, pick the topmost frequent target
source_targets = dict()
for src in lexicon:
    target = max(list(lexicon[src].items()), key = lambda x:x[1])[0]
    source_targets[src] = {target:1}

new_path = "/Users/work/Desktop/projects/llm-robustness-to-xlingual-noise/posteriors/flores_lexicons/hin_mai.json"
with open(new_path, "w")  as f:
    json.dump(source_targets, f, indent = 2, ensure_ascii=False)
