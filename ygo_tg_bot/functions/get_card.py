import requests
import time
from ygo_tg_bot.constants import TG_URL
from ygo_tg_bot.functions.get_cards_from_g_table import get_cards_from_g_table


def get_card(update_data):

    update_data_dict = {}
    for k, v in update_data.items():
        update_data_dict[k] = v

    if 'callback_query' in update_data_dict:
        update_data_dict = update_data_dict['callback_query']
        update_data_dict['message']['text'] = update_data_dict['data']

    if 'message' in update_data_dict and 'message_id' in update_data_dict['message'] and 'text' in update_data_dict['message'] \
            and 'chat' in update_data_dict['message'] and 'id' in update_data_dict['message']['chat']:

        message_text = update_data_dict['message']['text']

        is_multiple = False
        is_exact = False
        start_sub_str = '<'
        end_sub_str = '>'

        if '<|' in message_text and '|>' in message_text:
            is_exact = True
            start_sub_str = '<|'
            end_sub_str = '|>'

        if not is_exact:
            if not ('<' in message_text and '>' in message_text):
                return

        start = message_text.index(start_sub_str)
        end = message_text.index(end_sub_str)

        if not (end > start):
            return

        card_name = message_text[(start + len(start_sub_str)): end]

        if not card_name:
            return
        if len(card_name) < 3:
            return

        if message_text.startswith('/get_all_matches'):
            is_multiple = True

        card_name = card_name.lower()

        message_id = update_data_dict['message']['message_id']
        chat_id = update_data_dict['message']['chat']['id']

        cards = get_cards_from_g_table()

        fitting_cards = []

        for card in cards:
            if is_exact:
                if card_name == card[0].lower():
                    fitting_cards.append(card)
            else:
                if card_name in card[0].lower():
                    fitting_cards.append(card)

        if not is_multiple:
            fitting_cards = [fitting_cards[0]]

        for card in fitting_cards:
            time.sleep(2)

            params = {
                'chat_id': chat_id,
                'photo': card[1],
                'reply_to_message_id': message_id
            }

            if is_multiple == False and is_exact == False:
                params['reply_markup'] = '{"inline_keyboard": [[{"text": "показать еще результаты", '
                params['reply_markup'] += '"callback_data": "/get_all_matches <' + card_name + '>"}]]}'

            requests.post(
                '{}sendPhoto'.format(TG_URL),
                params
            )
