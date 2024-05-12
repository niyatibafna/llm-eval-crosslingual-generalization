import sys
import json

baseline_translation_file = sys.argv[1]
output_translation_file = sys.argv[2]

# def merge_translation_log_files(baseline_translation_file, output_translation_file):

with open(baseline_translation_file, 'r') as f:
    baseline_translation = json.load(f)

with open(output_translation_file, 'r') as f:
    output_translation = json.load(f)

for doc_idx, doc in enumerate(output_translation):
    assert output_translation[doc_idx]['src'] == baseline_translation[doc_idx]['src']
    doc = {}
    doc['doc_id'] = output_translation[doc_idx]['doc_id']
    doc['prompt'] = output_translation[doc_idx]['prompt']
    doc['src'] = output_translation[doc_idx]['src']
    doc['src_noised'] = output_translation[doc_idx]['noised_src']
    predicted_noised = output_translation[doc_idx]['predicted']
    doc['predicted'] = baseline_translation[doc_idx]['predicted']
    doc['predicted_noised'] = predicted_noised
    doc['truth'] = output_translation[doc_idx]['truth']
    
    output_translation[doc_idx] = doc
    
with open(output_translation_file, 'w') as f:
    json.dump(output_translation, f, indent=2, ensure_ascii=False)

