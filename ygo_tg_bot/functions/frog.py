import requests
import random

from ygo_tg_bot.constants import TG_URL
from ygo_tg_bot.functions.find_ru_letters_in_string import find_ru_letters_in_string

BING_URL = "https://bing-image-search1.p.rapidapi.com/images/search?q="
BING_HEADERS = {
    "x-rapidapi-host": "bing-image-search1.p.rapidapi.com",
    "x-rapidapi-key": "fb3dd38f00msh738d9f9b25b29acp13d692jsn8859445253e3",
    "useQueryString": 'true'
}
BACKUP_QUERIES = [
    'лягушка мем',
    'лягушка косплей',
    'лягушка сказка',
    'лягушка нарисованная',
    'лягушка смешная',
    'лягушка кермит'
]


def frog(update_data):
    if 'message' in update_data and 'message_id' in update_data['message'] and 'text' in update_data['message'] \
            and 'chat' in update_data['message'] and 'id' in update_data['message']['chat']:

        try:
            message_text = update_data['message']['text']

            lowercase_text = message_text.replace('К', 'к').replace('В', 'в').replace('А', 'а')

            if 'квак' in lowercase_text:
                words = message_text.split()

                kvak_found = False
                words_temp = []
                for word in words:
                    word_formatted = word.replace('К', 'к').replace('В', 'в').replace('А', 'а')
                    if word_formatted == 'квак':
                        kvak_found = True
                    else:
                        words_temp.append(word)
                words = words_temp

                if kvak_found:
                    if find_ru_letters_in_string(lowercase_text.replace('квак', '')):
                        query = 'лягушка'
                    else:
                        query = 'frog'
                    for word in words:
                        query += ' ' + word

                    found_images = requests.get(
                        BING_URL + query,
                        headers=BING_HEADERS
                    ).json()['value']

                    if not len(found_images):
                        backup_index = random.randint(0, len(BACKUP_QUERIES) - 1)
                        backup_query = BACKUP_QUERIES[backup_index]
                        found_images = requests.get(
                            BING_URL + backup_query,
                            headers=BING_HEADERS
                        ).json()['value']

                    if len(found_images):
                        found_images = found_images[:20]

                        image_index = random.randint(0, len(found_images) - 1)
                        image_url = found_images[image_index]['contentUrl']

                        message_id = update_data['message']['message_id']
                        chat_id = update_data['message']['chat']['id']

                        try:
                            requests.post(
                                '{}sendPhoto'.format(TG_URL),
                                {
                                    'chat_id': chat_id,
                                    'photo': image_url,
                                    'reply_to_message_id': message_id
                                }
                            )
                        except Exception as e:
                            image_index = random.randint(0, len(found_images) - 1)
                            image_url = found_images[image_index]['contentUrl']
                            try:
                                requests.post(
                                    '{}sendPhoto'.format(TG_URL),
                                    {
                                        'chat_id': chat_id,
                                        'photo': image_url,
                                        'reply_to_message_id': message_id
                                    }
                                )
                            except Exception as e:
                                pass
        except Exception:
            pass
