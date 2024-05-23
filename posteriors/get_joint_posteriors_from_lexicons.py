'''
The name of this file is a misnomer. We are not looking for joint posteriors. We are just 
looking for posteriors *taking into account* other random processes that have happened. 
It is really more of a *sequential* posterior than a joint posterior. 

Recall:

Given a bilingual lexicon between two languages, and possible monolingual data,
this script computes the posteriors of the parameters of all noisers.

We do this in different ways:
1. Compute posterior for noiser as if all change only comes from noiser
2. Try to separate out changes in languages into three types, and find posterior
    for each noiser, taking into account the other noisers.

We do the second of these. First we compute phonological change, then morphological change,
and finally lexical change. Lexical change is only counted for words that are not affected
by the other types of change.
'''
debug = True

import json
from typing import List
from collections import defaultdict

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append("../")
from noisers.utils.get_functional_words import OUTDIR, closed_class_tags
from noisers.utils.get_functional_words import output_paths as ud_wordlists_paths

from get_lexicons import json_to_list_of_pairs

class Posterior:

    def __init__(self, lang, bil_lexicon, src_vocab = None, tgt_vocab = None, \
                 noise_types: List = list()):
        '''
        Args: 
            lang (str): language code of hrl
            noise_types (list): list of noise types for which we want posterior
            bil_lexicon (list): list of pairs (hrl, lrl) - may have multiple listings for the same src word
            src_vocab (dict): frequency map of hrl vocabulary
            tgt_vocab (dict): frequency map of lrl vocabulary
        '''
        self.lang = lang
        self.bil_lexicon = bil_lexicon
        self.src_vocab = src_vocab
        self.tgt_vocab = tgt_vocab
        self.tag2wordlist = self.get_tag2wordlist()

    def get_tag2wordlist(self):
        '''Get tag2wordlist from the JSON file'''
        with open(ud_wordlists_paths[self.lang]) as f:
            tag2wordlist = json.load(f)
        return tag2wordlist

    def is_word_functional(self, word):
        '''Check if word is functional'''
        for tag in self.tag2wordlist:
            if word in self.tag2wordlist[tag]:
                return True
        return False

    def post_lexical_noiser(self):
        '''
        We want to find the number of completely new words as target.

        Returns:
            (theta_func, theta_content): proportion of functional words and content words
        '''

        count_func = 0
        count_content = 0
        total_func, total_content = 0, 0
        for (src, tgt) in self.bil_lexicon:
            if src != tgt and tgt not in self.src_vocab: # Try without this check
                if self.is_word_functional(src):
                    count_func += 1
                    if debug:
                        print(f"Functional word: {src} -> {tgt}")
                else:
                    # We also want to check that the words don't have the same stem (because that 
                    # would be a morphological change, not a lexical change)
                    if not self.same_stem(src, tgt):
                        count_content += 1
                        if debug:
                            print(f"Content word: {src} -> {tgt}")
            if self.is_word_functional(src):
                total_func += 1
            else:
                total_content += 1

        
        return count_func/total_func, count_content/total_content
    
    def post_phonological_noiser(self):
        '''
        Find theta_phon i.e. the proportion of character ngrams with a new middle character.
        We do this in the following way:
        Collect all character grams of length 3 in the source lexicon
        1. For every src-tgt pair, see whether they have "high-enough" NED
        2. If so, count insertions, deletions, and replacements in between identical characters

        There are a number of issues with the above, but there are also the same problems with the original
        noiser, so it's okay. Or at least, it's consistently bad.
        '''
        pass

    def get_suffix_frequency(self, vocab):
        '''Get suffix frequency map from vocab
        Args:
            vocab: dict, vocabulary of type {word: count}
        Returns:
            suffix_freq: dict, contains the frequency of each suffix
            most_frequent_word_per_suffix: dict, contains the most frequent word for each suffix. This is 
                used to condition the new suffix on the stem of the word if the suffix is swapped
        '''
        suffix_freq = defaultdict(lambda: 0)
        for word in vocab:
            for i in range(1, round(len(word)/2) + 1): #only allow half the word to be a suffix
                suffix_freq[word[-i:]] += vocab[word]

        return suffix_freq

    
    def filter_suffix_topk(self, suffix_freq, k = 200):
        '''
        Filter top k suffixes from suffix_freq
        '''
        suffix_freq = {suffix: freq for suffix, freq in suffix_freq.items() if len(suffix) > 1}
        sorted_suffixes = sorted(suffix_freq, key=lambda x: suffix_freq[x], reverse=True)
        suffix_freq = {suffix: suffix_freq[suffix] for suffix in sorted_suffixes[:k]}
        suffix_freq = defaultdict(lambda: 0, suffix_freq)

        return suffix_freq

    def same_stem(self, src, tgt):
        '''
        Check if src and tgt have the same stem. We do this by checking if the
            src and tgt have some non-trivial shared prefix (let's say length 2 or 33% of the length of the
            word)
        '''
        punctuation = ".,;:?!-_()[]{}\"'`~@#$%^&*+=|\\<>/"
        src = src.lower().strip(punctuation)
        tgt = tgt.lower().strip(punctuation)
        if self.lang == "hin":
            return src[0] == tgt[0]

        # longest common prefix
        lcp = 0
        for i in range(min(len(src), len(tgt))):
            if src[i] == tgt[i]:
                lcp += 1
            else:
                break
        if lcp >= 2 and lcp >= 0.33 * len(src):
            return True
    
    def post_morphological_noiser(self):
        '''
        Find theta_morph i.e. the proportion of the top k suffixes that are new.
        We do this in the following way:
        1. Find the top k suffixes in the target language (do this in the same way that we do it
            in the noiser - i.e. list the top string suffixes and then find the top k in a language specific
            way)
        2. For every source word, sample a suffix. If the suffix is not in our collected list, move on.
        3. If it is, then check if the target word has the same "stem". We do this by checking if the
            src and tgt have some non-trivial shared prefix (let's say length 2 or 33% of the length of the
            word). If they do, then we say that the stem is the same. We can also use NED,
            but this might be less noisy.
        4. In this case, check if the suffix is the same. If not, then we have a change.
        5. Note that we make this count several times per suffix, and we finally take an average for a given
            suffix to decide whether it was changed or not (i.e. we'll get something like 0.3 for a suffix)
        6. We then take the top k suffixes and find the average of the proportion of times they were changed
            to get theta_morph.
        '''

        # Collect all suffixes
        src_suffix_freq = self.get_suffix_frequency(self.src_vocab)

        # Filter top k suffixes
        src_suffix_freq = self.filter_suffix_topk(src_suffix_freq)
        if debug:
            print(f"Resulting suffix freq: ")
            print(*src_suffix_freq.items(), sep="\n")

        # Find the proportion of times the suffix was changed
        suffix_changes = defaultdict(lambda: 0)
        suffix_counts = defaultdict(lambda: 0)
        for (src, tgt) in self.bil_lexicon:
            for i in range(1, round(len(src)/2) + 1): # When we do this, we are basically saying that the word
                # exhibits *all* suffixes that it has. 
                # This is probably unlikely, but it's okay because we're checking whether the suffix belongs
                # in our collected list, which hopefully only has linguistic suffixes
                src_suffix = src[-i:]
                if src_suffix in src_suffix_freq:
                    if debug:
                        print(f"Source: {src}, Target: {tgt}, Suffix: {src_suffix}")
                    # Now we'll check whether source and target have the same stem
                    if not self.same_stem(src, tgt):
                        if debug:
                            print(f"Source and target don't have the same stem")
                        continue
                    suffix_counts[src_suffix] += 1
                    if tgt[-i:] != src[-i:]:
                        if debug:
                            print(f"Suffix changed")
                        suffix_changes[src_suffix] += 1


        # Find the proportion of times the suffix was changed
        theta_morph = 0
        for suffix in src_suffix_freq:
            if suffix_counts[suffix] == 0:
                continue
            theta_morph += suffix_changes[suffix]/suffix_counts[suffix]

        if debug:
            print(f"Suffix changes: {suffix_changes}")
            print(f"Suffix counts: {suffix_counts}")
            print(f"Theta morph: {theta_morph}")
        
        observed_suffixes = len([suffix for suffix in src_suffix_freq if suffix_counts[suffix] > 0])
        if debug:
            print(f"Observed suffixes: {observed_suffixes}")
            print(f"Total suffixes: {len(src_suffix_freq)}")
        theta_morph /= observed_suffixes

        return theta_morph
        

hin_langs = ["bho", "mag", "mai", "hne", "awa"]
spa_langs = ["glg"]
fra_langs = ["oci"]
ind_langs = ["zsm"]
arb_langs = ["acm", "acq", "aeb", "ajp", "apc", "ars", "ary", "arz"]

related_lrls = {
        "hin": {"bho", "awa", "mag", "mai", "hne"},
        "ind": {"zsm"},
        "spa": {"glg"},
        "fra": {"oci"},
        "deu": {"dan", "isl", "swe"},
        "arb": {"acm", "acq", "aeb", "ajp", "apc", "ars", "ary", "arz"},
    }

for src_lang in related_lrls:
    for tgt_lang in sorted(list(related_lrls[src_lang])):
        if src_lang != "hin" or tgt_lang != "mai":
            continue
        bil_lexicon_json_file = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/flores_lexicons/{src_lang}_{tgt_lang}.json"
        bil_lexicon = json_to_list_of_pairs(bil_lexicon_json_file)
        src_vocab = defaultdict(lambda: 0)
        tgt_vocab = defaultdict(lambda: 0)
        for (src, tgt) in bil_lexicon:
            src_vocab[src] += 1
            tgt_vocab[tgt] += 1

        post = Posterior(src_lang, bil_lexicon, src_vocab, tgt_vocab)
        # print(f"LANGUAGES: {src_lang} -> {tgt_lang}")
        print("Lexical noiser: (content, functional)")
        theta_c, theta_f =  post.post_lexical_noiser()
        print(round(theta_c, 2))
        print(round(theta_f, 2))
        print("Morphological noiser:")
        theta_morph = post.post_morphological_noiser()
        print(round(theta_morph, 2))
        print("\n\n\n")
        # print(tgt_lang)

# # Print all related langs in vertical line
# for src_lang in related_lrls:
#     for tgt_lang in related_lrls[src_lang]:
#         print(f"{tgt_lang}")