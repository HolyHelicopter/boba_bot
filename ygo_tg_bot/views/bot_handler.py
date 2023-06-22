from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from ygo_tg_bot.functions.frog import frog
from ygo_tg_bot.functions.get_card_inline import get_card_inline
from ygo_tg_bot.functions.get_card import get_card


@csrf_exempt
def bot_handler(request):
    update_data = json.loads(request.body)

    frog(update_data)

    get_card(update_data)

    get_card_inline(update_data)

    from ygo_tg_bot.constants import TG_URL
    import requests
    requests.post(
        '{}sendMessage'.format(TG_URL),
        {
            'chat_id': '-807618183',
            'text': str(update_data)
        }
    )

    return HttpResponse(200)
