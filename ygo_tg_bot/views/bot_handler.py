from django.http import HttpResponse
import requests
import json

from ygo_tg_bot.constants import TG_URL


def bot_handler(request):
    message = json.dumps(request.POST)

    requests.post(
        '{}sendMessage'.format(TG_URL),
        {
            'chat_id': '-601053432',
            'text': message
        }
    )

    return HttpResponse(200)
