from noise import Noise
import random

class PhonologicalNoiser(Noise):
    def __init__(self, noise_params):
        '''Initialize phonological noiser with noise parameters
        Args:
            noise_params: dict, noise parameters, like {theta_1: 0.5}
        '''
        self.class_name = "PhonologicalNoiser"
        self.required_keys = {"theta_1"}
        self.check_noise_params(noise_params)
        
        self.theta_1 = float(noise_params['theta_1'])

    
    def apply_noise(self, input):
        '''Apply phonological noise to input
        Args:
            input: str, input text
        Returns:
            str, noised text
        '''
        # Apply noise
        # With probability theta_1, delete the first character
        # if random.random() < self.theta_1:
        #     return input[1:]

        # TODO: Function should not affect certain things, like the tokens "Question:", "Choices:", "Answer:
        # input = "NOISE MARK " + input
        return input

    
    def find_posterior(self, text1, text2):
        '''Find the posterior MLE estimate of self.noise_params given text1 and text2
        Args:
            text1: str, text 1
            text2: str, text 2
        Returns:
            MLE estimate of self.noise_params (dict)
        '''
        raise NotImplementedError