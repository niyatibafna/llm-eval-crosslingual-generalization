from noise import Noise
import random
import os
from collections import defaultdict
import json
from utils.misc import get_character_set

class GlobalPhonologicalNoiser(Noise):
    def __init__(self, noise_params):
        '''Initialize phonological noiser with noise parameters
        Args:
            noise_params: dict, noise parameters, like {theta_1: 0.5}
            Should contain:
                lang: str, language code
                text_file: str, path to text file
                theta_phon: float, probability of phonological noise
            Also accepts:
                output_dir: str, path to output directory

        '''
        self.class_name = "GlobalPhonologicalNoiser"
        self.required_keys = {"lang", "text_file", "theta_phon"}
        self.allowed_keys = {"output_dir"}
        self.check_noise_params(noise_params)

        for key in noise_params:
            setattr(self, key, noise_params[key])

        script, self.character_set = get_character_set(self.lang)
        self.chargram_map = self.construct_charmap_with_context()

        if hasattr(self, "output_dir"):
            os.makedirs(self.output_dir, exist_ok=True)

    def is_valid_word(self, word):
        '''Check if word is valid
        Args:
            word: str, word to check
        Returns:
            bool, whether word is valid
        '''
        return all(char in self.character_set for char in word)

    def get_ngrams_from_text(self):
        '''Get words from text file
        Returns:
            list, list of words
        '''
        words = set()
        with open(self.text_file, "r") as f:
            for line in f:
                line_words = line.strip().split()
                words.update({"<"+word+">" for word in line_words if self.is_valid_word(word)}) # Add < and > to denote start and end of word
        
        ngrams = defaultdict(lambda: 0)
        n = 3
        for word in words:
            for i in range(len(word) - n + 1):
                ngram = word[i:i+n]
                ngrams[ngram] += 1
        return ngrams
    
    def sample_new_char(self, char):
        '''Sample a new character
        Args:
            char: str, character to sample new character for
        Returns:
            str, new character, maintain casing
        '''

        new_char = random.choice(list(self.character_set - {char}))
        if char.isupper():
            new_char = new_char.upper()
        if char.islower():
            new_char = new_char.lower()
        return new_char
                
    def construct_charmap_with_context(self):
        '''
        Samples source characters given context to swap out globally, and creates a map.
        '''
        chargram_map = {}
        ngrams = self.get_ngrams_from_text()
        for ngram in ngrams:
            if random.random() < self.theta_phon:
                # We'll swap out the middle character
                new_char = self.sample_new_char(ngram[1])
                chargram_map[ngram] = ngram[0] + new_char + ngram[2]
        
        return chargram_map


    def construct_charmap(self):
        '''
        Samples source characters to swap out globally, and creates a map.
        Initializes self.charmap: dict, {source_char: target_char}
        '''
        charmap = {}
        for char in self.character_set:
            if random.random() < self.theta_phon:
                charmap[char] = random.choice(list(self.character_set - {char}))
            else:
                charmap[char] = char
        return charmap

    
    def apply_noise(self, input):
        '''Apply phonological noise to input
        Args:
            input: str, input text
        Returns:
            str, noised text
        '''
        # Apply noise
        words = input.split()
        noised_words = list()
        for word in words:
            noised_word = ""
            if not self.is_valid_word(word):
                noised_words.append(word)
                continue
            word = "<" + word + ">" # Add < and > to denote start and end of word
            for i in range(len(word)):
                if i == 0 or i == len(word) - 1:
                    pass # Don't add EOS and BOS chars
                else:
                    ngram = word[i-1:i+2]
                    if ngram in self.chargram_map:
                        noised_word += self.chargram_map[ngram][1]
                    else:
                        noised_word += word[i]
        
            noised_words.append(noised_word)
        return " ".join(noised_words)
    
    def record_noiser_artifacts(self):
        '''Record vocab map, number of words switched out'''

        if hasattr(self, "output_dir"):
            with open(f"{self.output_dir}/chargram_map.json", "w") as f:
                json.dump(self.chargram_map, f, indent=2, ensure_ascii=False)
            # stats = self.get_vocab_map_stats()
            # with open(f"{self.output_dir}/stats.json", "w") as f:
            #     json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def find_posterior(self, text1, text2):
        '''Find the posterior MLE estimate of self.noise_params given text1 and text2
        Args:
            text1: str, text 1
            text2: str, text 2
        Returns:
            MLE estimate of self.noise_params (dict)
        '''
        raise NotImplementedError