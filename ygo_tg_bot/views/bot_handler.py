from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from ygo_tg_bot.functions.frog import frog


@csrf_exempt
def bot_handler(request):
    update_data = json.loads(request.body)

    frog(update_data)

    return HttpResponse(200)
