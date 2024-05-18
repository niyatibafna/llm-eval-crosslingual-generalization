'''
What’s going on with XNLI? (xnli_mcq)

—> Let’s find the subset of questions answered wrong for 0.01 and 0.3 
- What is the intersection?
- Look at individual examples to say what’s up

'''
import json
def return_subset_wrong_answers(filename):
    wrong_docs = list()
    with open(filename) as f:
        data = json.load(f)
    # data is a list of dicts, each dict is a doc number
    for doc in data:
        if doc["acc"] == "False":
            wrong_docs.append(doc["doc_id"])
    
    return wrong_docs

wrong_docs_4  = return_subset_wrong_answers("/Users/work/Desktop/projects/llm-robustness-to-xlingual-noise/outputs/noised_data/bloomz7b/hi/morph-lang=hi,theta_morph_global=0.4~limit-300/xnli_mcq_hi_write_out_info.json")
wrong_docs_6 = return_subset_wrong_answers("/Users/work/Desktop/projects/llm-robustness-to-xlingual-noise/outputs/noised_data/bloomz7b/hi/morph-lang=hi,theta_morph_global=0.6~limit-300/xnli_mcq_hi_write_out_info.json")

print(f"#docs wrong in 0.4: {len(wrong_docs_4)}")
print(f"#docs wrong in 0.6: {len(wrong_docs_6)}")

# Intersection
print(f"Docs that are wrong in both: {set(wrong_docs_4).intersection(set(wrong_docs_6))}")
print(f"#docs wrong in both: {len(set(wrong_docs_4).intersection(set(wrong_docs_6)))}")

# Docs wrong in 4 but not in 6
wrong_in_4_but_not_6 = [doc_id for doc_id in wrong_docs_4 if doc_id not in wrong_docs_6]
print(f"Docs wrong in 0.4 but not in 0.6: {wrong_in_4_but_not_6}")
print(f"#docs wrong in 0.4 but not not 0.6: {len(wrong_in_4_but_not_6)}")

# Docs wrong in 6 but not in 4
wrong_in_6_but_not_4 = [doc_id for doc_id in wrong_docs_6 if doc_id not in wrong_docs_4]
print(f"Docs wrong in 0.6 but not in 0.4: {wrong_in_6_but_not_4}")
print(f"#docs wrong in 0.6 but not not 0.4: {len(wrong_in_6_but_not_4)}")

