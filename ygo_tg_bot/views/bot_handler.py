from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from ygo_tg_bot.functions.frog import frog
from ygo_tg_bot.functions.get_card_inline import get_card_inline


@csrf_exempt
def bot_handler(request):
    update_data = json.loads(request.body)

    frog(update_data)

    get_card_inline(update_data)

    return HttpResponse(200)
