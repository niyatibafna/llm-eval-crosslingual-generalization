from noise import Noise
import random

class CharacterLevelNoiser(Noise):
    '''
    Noise type: switch out random characters with other characters
    Required params: script, insert_theta, delete_theta, swap_theta
    Input format: {script: latin, insert_theta: 0.1, delete_theta: 0.1, swap_theta: 0.1}
    '''
    @staticmethod
    def identify_script(text):
        '''Identify script of text
        Args:
            text: str, input text
        Returns:
            str, script of text
        '''
        # Identify script of text
        char_set = {
            "latin": set(chr(i) for i in range(65, 91)) | set(chr(i) for i in range(97, 123)),
            "devanagari": set(chr(i) for i in range(2304, 2432)),
            "arabic": set(chr(i) for i in range(1536, 1792)),
            "cyrillic": set(chr(i) for i in range(1024, 1280)),
        }
        # We'll find a majority script
        script_counts = {script: 0 for script in char_set.keys()}
        for char in text:
            for script, char_set in char_set.items():
                if char in char_set:
                    script_counts[script] += 1

        return max(script_counts, key=script_counts.get)



    def __init__(self, noise_params):
        '''Initialize noise with noise parameters
        Args:
            noise_params: dict, noise parameters, like {theta_1: 0.5}
        '''
        self.class_name = "CharacterLevelNoiser"
        self.required_keys = {"lang", "swap_theta"}
        # self.required_keys = {"lang", "insert_theta", "delete_theta", "swap_theta"}
        self.check_noise_params(noise_params)

        self.lang = noise_params['lang']
        # self.insert_theta = float(noise_params['insert_theta'])
        # self.delete_theta = float(noise_params['delete_theta'])
        self.swap_theta = float(noise_params['swap_theta'])

        # Initialize character set according to script
        self.character_set = self.get_character_set()
    
    def get_character_set(self):
        '''Get character set for script
        Returns:
            set, character set
        '''
        # Get character set for script using Unicode ranges
        lang_to_script = {
            "eng": "latin",
            "deu": "latin",
            "hin": "devanagari",
            "ara": "arabic",
            "rus": "cyrillic",
            "esp": "latin",
            "en": "latin",
            "de": "latin",
            "hi": "devanagari",
            "ar": "arabic",
            "ru": "cyrillic",
            "es": "latin",
        }
        script = lang_to_script[self.lang]

        char_set = {
            "latin": set(chr(i) for i in range(65, 91)) | set(chr(i) for i in range(97, 123)),
            "devanagari": set(chr(i) for i in range(2304, 2432)),
            "arabic": set(chr(i) for i in range(1536, 1792)),
            "cyrillic": set(chr(i) for i in range(1024, 1280)),
        }
        return char_set[script]

    def apply_noise(self, input):
        '''Apply noise to input
        Args:
            input: str, input text
        Returns:
            str, noised text
        '''
        # Apply noise
        # For each character, with probability swap_theta, 
        # swap it with another character from the same alphabet

        noised_input = ""
        for char in input:
            if char in self.character_set:
                # If the character is in the character set, apply noise
                if random.random() < self.swap_theta:
                    noised_input += random.choice(list(self.character_set - {char}))
                else:
                    noised_input += char
            else:
                # If not, leave the character alone
                noised_input += char
        return noised_input

    
    def find_posterior(text1, text2):
        '''Find the posterior MLE estimate of self.noise_params given text1 and text2
        Args:
            text1: str, text 1
            text2: str, text 2
        Returns:
            MLE estimate of self.noise_params (dict)
        '''
        raise NotImplementedError
