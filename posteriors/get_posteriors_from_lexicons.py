'''
Given a bilingual lexicon between two languages, and possible monolingual data,
this script computes the posteriors of the parameters of all noisers.

We do this in different ways:
1. Compute posterior for noiser as if all change only comes from noiser
2. Try to separate out changes in languages into three types, and find posterior
    for each noiser, taking into account the other noisers.

'''

import json
from typing import List

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append("../")
from noisers.utils.get_functional_words import OUTDIR, closed_class_tags
from noisers.utils.get_functional_words import output_paths_local as ud_wordlists_paths

from get_lexicons import json_to_list_of_pairs

class Posterior:

    def __init__(self, lang, bil_lexicon, src_vocab = None, tgt_vocab = None, \
                 noise_types: List = list()):
        '''
        Args: 
            lang (str): language code of hrl
            noise_types (list): list of noise types for which we want posterior
            bil_lexicon (list): list of pairs (hrl, lrl) - may have multiple listings for the same src word
            src_vocab (set): set of hrl vocabulary
            tgt_vocab (set): set of lrl vocabulary
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
                    # print(f"Functional word: {src} -> {tgt}")
                else:
                    count_content += 1
                    # print(f"Content word: {src} -> {tgt}")
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

        pass

hin_langs = ["bho", "mag", "mai", "hne", "awa"]

for lang in hin_langs:
    bil_lexicon_json_file = f"/Users/work/Desktop/projects/llm-robustness-to-xlingual-noise/posteriors/lexicons/hin-{lang}.json"
    bil_lexicon = json_to_list_of_pairs(bil_lexicon_json_file)
    src_vocab = set()
    tgt_vocab = set()
    for (src, tgt) in bil_lexicon:
        src_vocab.add(src)
        tgt_vocab.add(tgt)

    post = Posterior("hin", bil_lexicon, src_vocab, tgt_vocab)
    print(f"LANGUAGE: {lang}")
    print(post.post_lexical_noiser())
    print("\n\n\n")