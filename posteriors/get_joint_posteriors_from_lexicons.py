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
debug = False
debug_phon = False

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

    def __init__(self, lang, bil_lexicon_json_file, src_text_file, \
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
        self.bil_lexicon = json_to_list_of_pairs(bil_lexicon_json_file)

        self.src_vocab = self.get_vocab(src_text_file)
        tgt_vocab = defaultdict(lambda: 0)
        for (_, tgt) in self.bil_lexicon:
            tgt_vocab[tgt] += 1
        self.tgt_vocab = tgt_vocab

        self.tag2wordlist = self.get_tag2wordlist()

        # The following thresholds are trying to set a threshold for each language
        # for NED, for two words to be considered as only having a phonological change
        self.lang_specific_ned_thresholds = {
            "hin": 0.5,
            "spa": 0.4,
            "deu": 0.4
        }
        self.lang_specific_ned_thresholds = defaultdict(lambda: 0.4, self.lang_specific_ned_thresholds)

    def get_vocab(self, text_file):
        '''Initialize vocabulary from vocab file'''
        print(f"Initializing vocabulary from {text_file}...")
        vocab = defaultdict(lambda: 0)
        for line in open(text_file):
            words = line.strip().split()
            for word in words:
                # Remove punctuation
                punctuation_and_bad_chars = "»«.,!?()[]{}\"'`:;'/\\-–—~_<>|@#$%^&*+=\u200b\u200c\u200d\u200e\u200f"
                word = word.strip(punctuation_and_bad_chars)
                # If word has numeric characters, skip
                if any(char.isdigit() for char in word):
                    continue
                # All characters in word must be in character set
                # if not all(char in self.character_set for char in word):
                #     print(f"Not in character set: {word}")
                #     continue
                                
                vocab[word.lower()] += 1
        print(f"Finished initializing vocabulary from {text_file}!")
        print(f"Length of vocab: {len(vocab)}")

        return vocab

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
            if self.is_word_functional(src):
                if src != tgt:
                    count_func += 1
                    if debug:
                        print(f"Functional word: {src} -> {tgt}")
                total_func += 1
            else:
                if src != tgt and tgt not in self.src_vocab: # Try without this check
                    # We also want to check that the words don't have the same stem (because that 
                    # would be a morphological change, not a lexical change)
                    if not self.same_stem(src, tgt):
                        # We also want to check that the words don't have a high NED, because that would
                        # be a phonological change
                        ned, _ = self.min_ops(src, tgt)
                        if ned > self.lang_specific_ned_thresholds[self.lang]:
                            count_content += 1
                            if debug:
                                print(f"Content word: {src} -> {tgt}")
                total_content += 1
        
        self.theta_func = count_func/total_func
        self.theta_content = count_content/total_content

        return self.theta_func, self.theta_content
    
    def min_ops(self, src, tgt):
        '''
        Find NED and
        Find minimum list of operations to convert src to tgt in the following format
        ops (list): [(src_pos, tgt_pos, operation)]. 
        For replacements, src[src_pos] --> tgt[tgt_pos]

        Returns: 
            ned (float): normalized edit distance
            ops (list): list of operations
        '''
        n = len(src)
        m = len(tgt)
        dp = [[0 for _ in range(m+1)] for _ in range(n+1)]
        for i in range(n+1):
            dp[i][0] = i
        for j in range(m+1):
            dp[0][j] = j
        for i in range(1, n+1):
            for j in range(1, m+1):
                if src[i-1] == tgt[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        i, j = n, m
        ops = []
        while i > 0 and j > 0:
            if src[i-1] == tgt[j-1]:
                i -= 1
                j -= 1
            else:
                if dp[i][j] == 1 + dp[i-1][j-1]:
                    ops.append((i-1, j-1, "replace"))
                    i -= 1
                    j -= 1
                elif dp[i][j] == 1 + dp[i-1][j]:
                    ops.append((i-1, j, "delete"))
                    i -= 1
                else:
                    ops.append((i, j-1, "insert"))
                    j -= 1
        while i > 0:
            ops.append((i-1, j, "delete"))
            i -= 1
        while j > 0:
            ops.append((i, j-1, "insert"))
            j -= 1

        ned = dp[n][m]/max(n, m)
        return ned, ops

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
        threshold = self.lang_specific_ned_thresholds[self.lang]
        total_ngrams = defaultdict(lambda: 0)
        changed_ngrams = defaultdict(lambda: 0)
        for (src, tgt) in self.bil_lexicon:
            if src == tgt:
                continue
            if debug_phon:
                print(f"Source: {src}, Target: {tgt}")
            src = "<" + src + ">"
            tgt = "<" + tgt + ">"
            ned, ops = self.min_ops(src, tgt)
            if debug_phon:
                print(f"NED: {ned}")
                print(f"Ops: {ops}")
            if ned > threshold:
                if debug_phon:
                    print(f"Too high NED")
                continue
            for i in range(len(ops)):
                src_pos, tgt_pos, op = ops[i]
                if op == "replace":
                    if src[src_pos] == tgt[tgt_pos]:
                        continue
                    if src_pos == 0 or tgt_pos == 0 or src_pos == len(src) - 1 or tgt_pos == len(tgt) - 1:
                        continue
                    if src[src_pos - 1] == tgt[tgt_pos - 1] and src[src_pos + 1] == tgt[tgt_pos + 1]:
                        if debug_phon:
                            print(f"Changed ngram: {src[src_pos-1:src_pos+2]}-->{tgt[tgt_pos-1:tgt_pos+2]}")
                        changed_ngrams[src[src_pos-1:src_pos+2]] += 1
            for i in range(1, len(src) - 1):
                total_ngrams[src[i-1:i+2]] += 1
        
        theta_per_ngram = {ngram: changed_ngrams[ngram]/total_ngrams[ngram] for ngram in total_ngrams}
        theta_phon = sum(theta_per_ngram.values())/len(theta_per_ngram)

        if debug_phon:
            print(f"theta_phon: {theta_phon}")
        return theta_phon


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
        2. For every source word, do the following for all suffixes that lie in our suffix list
        3. Check if the target word has the same "stem". We do this by checking if the
            src and tgt have some non-trivial shared prefix (let's say length 2 or 33% of the length of the
            word). If they do, then we say that the stem is the same. We can also use NED,
            but this might be more noisy.
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
        ##### REESTIMATE THETA_MORPH BASED ON THETA_CONTENT!!! #####
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
iso3_to_iso2 = {
    "hin": "hi",
    "ind": "id",
    "spa": "es",
    "fra": "fr",
    "deu": "de",
    "arb": "ar",
}

posteriors = defaultdict(lambda: dict())

for src_lang in related_lrls:
    for tgt_lang in sorted(list(related_lrls[src_lang])):
        # if src_lang not in {"deu"}:
        #     continue
        print(f"Source language: {src_lang}, Target language: {tgt_lang}")
        bil_lexicon_json_file = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/posteriors/flores_lexicons_raw/{src_lang}_{tgt_lang}.json"
        src_text_file = f"/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/datasets/{iso3_to_iso2[src_lang]}/mmlu_{iso3_to_iso2[src_lang]}.txt"
        
        post = Posterior(src_lang, bil_lexicon_json_file, src_text_file)
        # print(f"LANGUAGES: {src_lang} -> {tgt_lang}")
        print("Lexical noiser: (functional, content)")
        theta_f, theta_c =  post.post_lexical_noiser()
        print(round(theta_c, 2))
        print(round(theta_f, 2))
        print("Morphological noiser:")
        theta_morph = post.post_morphological_noiser()
        print("Phonological noiser:")
        theta_phon = post.post_phonological_noiser()
        print(f"Theta content: {round(theta_c, 2)}")
        print(f"Theta func: {round(theta_f, 2)}")
        print(f"Theta morph: {round(theta_morph, 2)}")
        print(f"Theta phon: {round(theta_phon, 2)}")
        print("\n\n\n")
        # print(tgt_lang)
        posteriors[src_lang][tgt_lang] = (round(theta_f, 2), round(theta_c, 2), \
                                          round(theta_morph, 2), round(theta_phon, 2)) 


# Print all 
for src_lang in posteriors:
    print(f"Source language: {src_lang}")
    print(f"theta_f")
    for tgt_lang in sorted(posteriors[src_lang]):
        # print(f"Source language: {src_lang}, Target language: {tgt_lang}")
        print(posteriors[src_lang][tgt_lang][0])

    print(f"theta_c")
    for tgt_lang in sorted(posteriors[src_lang]):
        # print(f"Source language: {src_lang}, Target language: {tgt_lang}")
        print(posteriors[src_lang][tgt_lang][1])

    print(f"theta_morph")
    for tgt_lang in sorted(posteriors[src_lang]):
        # print(f"Source language: {src_lang}, Target language: {tgt_lang}")
        print(posteriors[src_lang][tgt_lang][2])
    
    print(f"theta_phon")
    for tgt_lang in sorted(posteriors[src_lang]):
        # print(f"Source language: {src_lang}, Target language: {tgt_lang}")
        print(posteriors[src_lang][tgt_lang][3])