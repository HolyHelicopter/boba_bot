from django.http import HttpResponse, QueryDict
import requests
import json
from django.views.decorators.csrf import csrf_exempt

from ygo_tg_bot.constants import TG_URL


@csrf_exempt
def bot_handler(request):
    message = dict(QueryDict(request.body))['update_id']

    requests.post(
        '{}sendMessage'.format(TG_URL),
        {
            'chat_id': '-601053432',
            'text': message
        }
    )

    return HttpResponse(200)
