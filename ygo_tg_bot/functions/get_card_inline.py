import requests
from ygo_tg_bot.constants import TG_URL
from ygo_tg_bot.constants import GET_CARDS_URL


def get_card_inline(update_data):
    if 'inline_query' in update_data and isinstance(update_data['inline_query'], dict) \
            and 'query' in update_data['inline_query'] and update_data['inline_query']['query']:

        inline_query = update_data['inline_query']['query'].lower()

        resp = requests.get(GET_CARDS_URL)
        cards = resp.json()['values']

        fitting_cards_images = []
        for card in cards:
            if inline_query in card[0].lower():
                fitting_cards_images.append(card[1])

        results = '['
        i = 1
        for fitting_card_image in fitting_cards_images:
            results += '{"id": "' + str(i) + '", "type": "photo",'
            results += '"photo_url": "' + fitting_card_image + '", "thumbnail_url": "' + fitting_card_image + '"}'
            if i != len(fitting_cards_images):
                results += ','
            i += 1
        results += ']'

        requests.post(
            '{}answerInlineQuery'.format(TG_URL),
            {
                'inline_query_id': update_data['inline_query']['id'],
                'results': results
            }
        )