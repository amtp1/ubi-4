import urllib.request
from json import loads

from aiogram.types import Message
from bs4 import BeautifulSoup as bs

from objects.globals import dp

@dp.message_handler(commands=["btc", "bnb", "eth"])
async def btc(message: Message):
    symbol = message.text.replace("/", "")
    response = urllib.request.urlopen(F"https://www.binance.com/en/trade/{symbol.upper()}_USDT")
    content = bs(response.read(), "html.parser").find(id="__APP_DATA")
    usd_currency = (loads(str(content)
        .replace("</script>", "")
        .replace('<script id="__APP_DATA" type="application/json">', ""))
        ["pageData"]["redux"]["products"]["currentProduct"])
    r_symbol = usd_currency["symbol"]
    r_close_price = usd_currency["close"]
    r_low_price = usd_currency["low"]
    r_high_price = usd_currency["high"]

    r_page = (
        f"<b>{r_symbol}</b>\n"
        f"<i>Now</i> {r_close_price}\n"
        f"<i>Min</i> {r_low_price}\n"
        f"<i>Max</i> {r_high_price}")
    return await message.answer(text=r_page)