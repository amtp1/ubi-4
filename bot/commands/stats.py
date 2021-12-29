from datetime import timedelta

from aiogram.types import Message

from objects.globals import dp
from models.models import *

@dp.message_handler(commands="stat")
async def stat(message: Message):
    all_users = await AuthUser.objects.all()
    last_day = await AuthUser.objects.filter(last_login__gt = (dt.now() - timedelta(days=1))).count()
    is_bomber = await UserData.objects.filter(is_bomber=True).count()
    prioritety_status = await BomberData.objects.filter(circles="∞").count()
    blocked_users = await UserData.objects.filter(is_blocked=True).count()
    stat_page: str = (f"<b>Статистика</b>\n"
            f"<code>|--</code><i>Общее количество</i>: {all_users.__len__()}\n"
            f"<code>|--</code><i>Активные за день</i>: {last_day}\n"
            f"<code>|--</code><i>Активировали бомбер</i>: {is_bomber}\n"
            f"<code>|--</code><i>С приоритетным статусом</i>: {prioritety_status}\n"
            f"<code>|--</code><i>Заблокировали</i>: {blocked_users}")
    return await message.answer(text=stat_page)