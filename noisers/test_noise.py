'''This file is for testing out various noise classes'''
from main import parse_noise_params, get_noisers, apply_noisers

# noise_specs = "phonological-theta_1=0.5,theta_2=0.2;character_level:script=devanagari,insert_theta=0.1,delete_theta=0.1,swap_theta=0.1"
# all_noise_params = parse_noise_params(noise_specs)
# print(f"Noise Parameters: {all_noise_params}")

# noiser_classes = get_noisers(all_noise_params)
# print(f"Noiser Classes: {noiser_classes}")

# inputs = ["The quick brown fox jumps over the lazy dog", "जल में रहकर मगर से बैर"]

# for input in inputs:
#     print(f"Input: {input}")
#     noised = apply_noisers(input, noiser_classes, verbose=True)
#     print(f"Noised: {noised}")
#     print()

# Testing out lexical noiser with GlobalLexicalNoise

read_file = "/export/b08/nbafna1/projects/llm-robustness-to-xlingual-noise/outputs/noised_data/de/character_level-lang=de,swap_theta=0.0/arc_de_write_out_info.json"
noise_specs = f"lexical-theta_global=0.5,text_file=<{read_file}>"
all_noise_params = parse_noise_params(noise_specs)
print(f"Noise Parameters: {all_noise_params}")

noiser_classes = get_noisers(all_noise_params)
print(f"Noiser Classes: {noiser_classes}")

inputs = ["The quick brown fox jumps over the lazy dog"]

# Some common German sentences:
inputs = [
    "Wie geht es dir?",  # How are you?
    "Guten Morgen!",  # Good morning!
    "Ich heiße Anna.",  # My name is Anna.
    "Wo ist die Toilette?",  # Where is the toilet?
    "Es tut mir leid.",  # I'm sorry.
    "Was kostet das?",  # How much does it cost?
    "Ich spreche ein wenig Deutsch.",  # I speak a little German.
    "Danke schön!",  # Thank you very much!
    "Woher kommst du?",  # Where are you from?
    "Wie spät ist es?",  # What time is it?
    "Auf Wiedersehen!",  # Goodbye!
    "Ich verstehe nicht.",  # I don't understand.
    "Wie heißt das auf Deutsch?",  # What is that called in German?
    "Kann ich Ihnen helfen?",  # Can I help you?
    "Ich liebe dich.",  # I love you.
    "Wo wohnst du?",  # Where do you live?
    "Bitte schön.",  # You're welcome.
    "Wie alt bist du?",  # How old are you?
    "Was machst du gerne?",  # What do you like to do?
    "Entschuldigen Sie bitte.",  # Excuse me, please.
    "Ich bin müde.",  # I'm tired.
    "Gute Nacht!",  # Good night!
    "Bis später!",  # See you later!
    "Prost!",  # Cheers!
    "Alles Gute zum Geburtstag!",  # Happy Birthday!
    "Wie ist dein Name?",  # What is your name?
    "Das ist lecker.",  # That is delicious.
    "Ich komme aus Deutschland.",  # I am from Germany.
    "Ich bin ein Tourist.",  # I am a tourist.
    "Wo ist der Bahnhof?",  # Where is the train station?
    "Ich habe mich verlaufen.",  # I am lost.
    "Können Sie das bitte wiederholen?",  # Can you please repeat that?
    "Wie viel Uhr ist es?",  # What time is it?
    "Ich brauche Hilfe.",  # I need help.
    "Wo ist das Hotel?",  # Where is the hotel?
    "Es freut mich, Sie kennenzulernen.",  # Nice to meet you.
    "Ich bin hier für eine Woche.",  # I am here for a week.
    "Was ist das?",  # What is that?
    "Wie war deine Reise?",  # How was your trip?
    "Haben Sie Wasser?",  # Do you have water?
]

for input in inputs:
    print(f"Input: {input}")
    noised = apply_noisers(input, noiser_classes, verbose=True)
    print(f"Noised: {noised}")
    print()

