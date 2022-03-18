import requests
import json
from ygo_tg_bot.functions.find_ru_letters_in_string import find_ru_letters_in_string
from ygo_tg_bot.functions.get_dollar_from_cbr import get_dollar_from_cbr
from ygo_tg_bot.constants import YGO_PRO_DECK_URL, TG_URL


def get_card(update_data):
    if 'message' in update_data and 'message_id' in update_data['message'] and 'text' in update_data['message'] \
            and 'chat' in update_data['message'] and 'id' in update_data['message']['chat']:

        message_text = update_data['message']['text']

        if not('<' in message_text and '>' in message_text):
            return

        start = message_text.index('<')
        end = message_text.index('>')

        if not (end > start):
            return

        card_name = message_text[(start + 1): end]

        if not card_name:
            return

        if find_ru_letters_in_string(card_name):
            return

        message_id = update_data['message']['message_id']
        chat_id = update_data['message']['chat']['id']

        try:
            card_found = True

            url_exact = '{}cardinfo.php?name={}'.format(YGO_PRO_DECK_URL, card_name)
            card_resp = requests.get(url_exact)

            if not card_resp.status_code == 200:
                url_search = '{}cardinfo.php?fname={}'.format(YGO_PRO_DECK_URL, card_name)
                card_resp = requests.get(url_search)
                if not card_resp.status_code == 200:
                    card_found = False

            if card_found:
                card_data = json.loads(card_resp.text)['data'][0]

                card_image = card_data['card_images'][0]['image_url']

                dollar = get_dollar_from_cbr()
                card_prices = card_data['card_prices'][0]
                tcgplayer_price_usd = round(float(card_prices['tcgplayer_price']))
                tcgplayer_price_rub = int(tcgplayer_price_usd * dollar)
                cardmarket_price_usd = round(float(card_prices['cardmarket_price']))
                cardmarket_price_rub = int(cardmarket_price_usd * dollar)
                ebay_price_usd = round(float(card_prices['ebay_price']))
                ebay_price_rub = int(ebay_price_usd * dollar)

                price_message = ''
                price_message += 'tcgplayer: {}$ ({} руб.)'.format(tcgplayer_price_usd, tcgplayer_price_rub)
                price_message += '\ncardmarket: {}$ ({} руб.)'.format(cardmarket_price_usd, cardmarket_price_rub)
                price_message += '\nebay: {}$ ({} руб.)'.format(ebay_price_usd, ebay_price_rub)

                requests.post(
                    '{}sendPhoto'.format(TG_URL),
                    {
                        'chat_id': chat_id,
                        'photo': card_image,
                        'caption': price_message,
                        'reply_to_message_id': message_id
                    }
                )

            if not card_found:
                requests.post(
                    '{}sendMessage'.format(TG_URL),
                    {
                        'chat_id': chat_id,
                        'text': 'Ничего не найдено',
                        'reply_to_message_id': message_id
                    }
                )

        except Exception:
            requests.post(
                '{}sendMessage'.format(TG_URL),
                {
                    'chat_id': chat_id,
                    'text': 'ОШИБКА',
                    'reply_to_message_id': message_id
                }
            )
