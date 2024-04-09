from noise import Noise
from googletrans import Translator

class GoogleTranslateNoiser(Noise):
    def __init__(self, noise_params):
        '''Initialize noise with noise parameters
        Args:
            noise_params: dict, noise parameters, like {theta_1: 0.5}
        '''
        self.class_name = "GoogleTranslateNoiser"
        self.required_keys = {"src", "tgt"}
        self.check_noise_params(noise_params)

        for key in noise_params:
            setattr(self, key, noise_params[key])

        self.translator = Translator()

    def apply_noise(self, input):
        '''Apply noise to input
        Args:
            input: str, input text
        Returns:
            str, noised text
        '''
        # Apply noise
        return self.translator.translate(input, src=self.src, dest=self.tgt).text
    
    def find_posterior(self, text1, text2):
        '''Find the posterior MLE estimate of self.noise_params given text1 and text2
        Args:
            text1: str, text 1
            text2: str, text 2
        Returns:
            MLE estimate of self.noise_params (dict)
        '''
        raise NotImplementedError
