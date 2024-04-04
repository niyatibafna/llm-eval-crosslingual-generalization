from noise import Noise
import random

class CharacterSwap(Noise):
    '''
    Noise type: switch out random characters with other characters
    '''

    def __init__(self, noise_params):
        '''Initialize noise with noise parameters
        Args:
            noise_params: dict, noise parameters, like {theta_1: 0.5}
        '''
        pass
    
    def check_noise_params(self):
        '''Check if noise parameters are valid for noise class
        Returns:
            bool, True if noise parameters are valid
        '''
        raise NotImplementedError

    def apply_noise(self, input):
        '''Apply noise to input
        Args:
            input: str, input text
        Returns:
            str, noised text
        '''
        raise NotImplementedError
    
    def find_posterior(text1, text2):
        '''Find the posterior MLE estimate of self.noise_params given text1 and text2
        Args:
            text1: str, text 1
            text2: str, text 2
        Returns:
            MLE estimate of self.noise_params (dict)
        '''
        raise NotImplementedError
