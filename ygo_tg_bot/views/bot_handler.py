from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from ygo_tg_bot.functions.frog import frog


@csrf_exempt
def bot_handler(request):
    update_data = json.loads(request.body)

    frog(update_data)

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
