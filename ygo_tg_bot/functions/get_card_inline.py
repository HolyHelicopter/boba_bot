import requests
from ygo_tg_bot.constants import TG_URL
from ygo_tg_bot.functions.get_cards_from_g_table import get_cards_from_g_table


def get_card_inline(update_data):
    if 'inline_query' in update_data and isinstance(update_data['inline_query'], dict) \
            and 'query' in update_data['inline_query'] and update_data['inline_query']['query']:

        inline_query = update_data['inline_query']['query'].lower()

        if len(inline_query) < 3:
            return

        cards = get_cards_from_g_table()

        fitting_cards = []
        for card in cards:
            if inline_query in card[0].lower():
                fitting_cards.append(card)

        results = '['
        i = 1
        for fitting_card in fitting_cards:
            results += '{"id": "' + str(i) + '", "type": "article",'
            results += '"title": "' + fitting_card[0] + '", "input_message_content": {"message_text": "<|'
            results += fitting_card[0] + '|>"}}'

            if i != len(fitting_cards):
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