from noise import Noise
import random

class PhonologicalNoiser(Noise):
    def __init__(self, noise_params):
        '''Initialize phonological noiser with noise parameters
        Args:
            noise_params: dict, noise parameters, like {theta_1: 0.5}
        '''
        # super().__init__(noise_params)
        self.check_noise_params(noise_params)

        if 'theta_1' in noise_params:
            self.theta_1 = noise_params['theta_1']
            noise_params.pop('theta_1')

        for key in noise_params:
            print(f"WARNING: Invalid parameter for PhonologicalNoiser: {key}")
    
    def check_noise_params(self, noise_params):
        '''Check if noise parameters are valid for phonological noiser
        Returns:
            bool, True if noise parameters are valid
        '''
        if 'theta_1' not in noise_params:
            raise ValueError("Missing noise parameter for PhonologicalNoiser: theta_1")
        return True

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
        input = "NOISE MARK " + input
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