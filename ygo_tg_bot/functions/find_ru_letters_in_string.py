from ygo_tg_bot.constants import RUSSIAN_ALPHABET


def find_ru_letters_in_string(string):
    ru_letter_found = False
    for letter in string:
        if letter in RUSSIAN_ALPHABET:
            ru_letter_found = True
    return ru_letter_found
