from noise import Noise
import random
from collections import defaultdict, Counter
import numpy as np
import json

from scipy.stats import chisquare

class GlobalLexicalNoiser(Noise):
    '''
    Noise type: switch out words from the vocabulary with non-words, and apply this change globally to every occurrence.
    Required params: text_file, theta_global
    Input format: {param: value}
    '''
    
    def __init__(self, noise_params):
        '''Initialize noise with noise parameters
        Args:
            noise_params: dict, noise parameters, like {theta_1: 0.5}
            Should contain:
                text_file: str, txt file
                theta_global: float, probability of switching out a word with a non-word
        '''
        self.class_name = "GlobalLexicalNoiser"
        self.required_keys = {"text_file", "theta_global"}
        # self.required_keys = {"lang", "insert_theta", "delete_theta", "swap_theta"}
        self.check_noise_params(noise_params)

        for key in noise_params:
            setattr(self, key, noise_params[key])

        if not hasattr(self, "chargram_length"):
            self.chargram_length = 3

        # Initialize vocabulary
        self.vocab = self.get_vocab(self.text_file)
        self.chargram_models = self.train_chargram_model(self.chargram_length)
        self.vocab_map = self.construct_new_vocab()

    @staticmethod
    def get_vocab(text_file):
        '''Initialize vocabulary from vocab file'''
        print(f"Initializing vocabulary from {text_file}...")
        vocab = defaultdict(lambda: 0)
        for line in open(text_file):
            words = line.strip().split()
            for word in words:
                # Remove punctuation
                word = word.strip(".,!?")
                # If word has non-alphabetic characters, skip
                if not word.isalpha():
                    continue
                vocab[word.lower()] += 1
        print(f"Finished initializing vocabulary from {text_file}!")

        return vocab

    def train_chargram_model(self, chargram_length=3):
        '''Train a character n-gram model on text
        Args:
            n: int, char n-gram length
        Returns:
            chargram_models: dict, contains character n-gram models for all n <= chargram_length {n: model} 
                - model: defaultdict, character n-gram model of type {prefix: {suffix: count}}
        '''
        print(f"Training chargram model with chargram length {chargram_length}...")
        chargram_models = dict() # contains chargram_models for all cgram lengths <= chargram_length
        for n in range(1, chargram_length + 1):
            chargram_model = defaultdict(lambda: defaultdict(lambda: 0)) # {prefix: {suffix: count}}

            for word in self.vocab:
                word = "!" + word # Add start token
                for i in range(len(word) - n + 1):
                    ngram = word[i:i+n]
                    # Increment count for ngram
                    chargram_model[ngram[:-1]][ngram[-1]] += 1
        
            chargram_models[n] = chargram_model

        print(f"Finished training chargram model with chargram length {chargram_length}!")
        return chargram_models

    def generate_word(self, mean_length):
        '''
        This function is for generating a non-word using the character n-gram model. We will:
        1. Sample the length of the non-word from a Poisson centered around mean_length
        2. Use self.chargram_models to generate the rest of the non-word based on the length of prefix
        Args:
            mean_length: float, mean length of non-word
        '''

        # Sample length of non-word from Poisson, must be at least 1

        length = max(1, np.random.poisson(mean_length))
        length += 1
        word = "!"

        while word == "!" or word[1:].lower() in self.vocab:
            # If generated word in vocab, generate another word
            word = "!"
            for _ in range(length):
                if len(word) < self.chargram_length-1:
                    # If the word is shorter than the length of the chargram model, 
                    # we will apply chargram model of the length of the word
                    chargram_model = self.chargram_models[len(word) + 1]
                    prefix = word
                else:
                    # If the word is longer than the prefix of the chargram model, 
                    # we will apply the chargram model of the length of the model
                    chargram_model = self.chargram_models[self.chargram_length]
                    prefix = word[-(self.chargram_length-1):]
                while len(list(chargram_model[prefix].keys())) == 0:
                    # Backing off to shorter chargram models
                    chargram_model = self.chargram_models[len(prefix)]
                    prefix = prefix[1:]
                # print(list(chargram_model[prefix].keys()))
                # print(len(list(chargram_model[prefix].keys())))

                # Sample the next character based on the prefix
                try:
                    next_char = np.random.choice(list(chargram_model[prefix].keys()), p=np.array(list(chargram_model[prefix].values())) / sum(chargram_model[prefix].values()))
                except:
                    print(f"Error: {prefix} not in chargram model")
                    # print(f"Chargram model: {chargram_model}")
                    print(f"Word: {word}")
                    print(f"Length: {length}")
                    print(f"Mean Length: {mean_length}")
                    print(f"Chargram Length: {self.chargram_length}")
                    print(f"Prefix: {prefix}")
                    print(f"{not chargram_model[prefix]}")
                    print(f"Chargram model: {chargram_model[prefix].keys()}")

                    raise
                word += next_char

        return word[1:]
    
    def construct_new_vocab(self):
        '''
        With probability theta_global, switch out a word from the vocabulary with a non-word
        Returns:
            vocab_map: dict, mapping of old word to new word
        '''
        vocab_map = dict()
        for word in self.vocab:
            if random.random() < self.theta_global:
                # print(f"Switching out {word}")
                new_word = self.generate_word(len(word))
                vocab_map[word] = new_word
            else:
                vocab_map[word] = word
        return vocab_map


    def apply_noise(self, input):
        '''Apply noise to input
        Args:
            input: str, input text
        Returns:
            str, noised text
        '''
        # Apply noise
        # For each word, map it to the corresponding word using the vocab map self.vocab_map

        noised_input = list()
        for input_word in input.split():
            word = input_word.strip(".,!?").lower()
            if word in self.vocab_map:
                mapped_word = self.vocab_map[word]
                # Capitalize first letter if original word was capitalized
                if input_word[0].isupper():
                    mapped_word = mapped_word.capitalize()
                # Add punctuation back
                if input_word[-1] in ".,!?":
                    mapped_word += input_word[-1]
                noised_input.append(mapped_word)
            else:
                noised_input.append(input_word)
        return " ".join(noised_input)

    def record_noiser_artifacts(self):
        '''Record vocab map, number of words switched out'''
        with open("vocab.txt", "w") as f:
            for word in self.vocab:
                f.write(word + "\n")
        raise NotImplementedError


    def find_posterior(self, text1, text2):
        '''Find the posterior MLE estimate of self.noise_params given text1 and text2
        Args:
            text1: str, text 1
            text2: str, text 2
        Returns:
            MLE estimate of self.theta_global
        '''
        vocab1 = self.get_vocab(text1)
        vocab2 = self.get_vocab(text2)

        # Find the number of words switched out
        switched_out = len(vocab1 - vocab2)
        mle_est_theta_global = switched_out / len(vocab1)

        # OR we can do the following:
        ## For each word, see whether its frequencies are significantly different in text1 and text2
        switched_out = 0
        for word in vocab1:
            expected = vocab1[word]
            observed = vocab2[word]

            # Chi-squared test
            res = chisquare(f_exp=[expected], f_obs=[observed])
            if res.pvalue < 0.05:
                switched_out += 1
        mle_est_theta_global = switched_out / len(vocab1)

        # OR we can use the absolute frequencies
        switched_out = total = 0
        for word in vocab1:
            if vocab1[word] <= 3:
                continue
            total += 1
            if vocab2[word] <= 3:
                switched_out += 1
        mle_est_theta_global = switched_out / total
        
        return mle_est_theta_global


