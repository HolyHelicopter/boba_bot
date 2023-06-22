import requests
from ygo_tg_bot.constants import GET_CARDS_URL


def get_cards_from_g_table():
    resp = requests.get(GET_CARDS_URL)
    cards = resp.json()['values']
    return cards