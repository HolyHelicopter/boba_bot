import requests
import xmltodict

from ygo_tg_bot.constants import CBR_URL


def get_dollar_from_cbr():
    cbr_resp = requests.get(CBR_URL)

    cbr_dict = xmltodict.parse(cbr_resp.text)

    dollar = float({currency['@ID']: currency['Value'] for currency in cbr_dict["ValCurs"]["Valute"]}['R01235'].replace(',', '.'))

    return dollar
