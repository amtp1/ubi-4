from datetime import datetime as dt

from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import ChatNotFound, UserDeactivated, BotBlocked

from objects import globals
from objects.globals import dp, bot
from states.states import Mailing
from models.models import UserData


@dp.message_handler(commands="mail")
async def mailing(message: Message):
    if message.from_user.id == globals.config["bot"]["MAIN_ADMIN"]:
        if globals.is_mailing:
            return await message.answer(text="Рассылка проводится!")
        await message.answer(text="/cancel - Отменить\nВведите текст для рассылки:")
        await Mailing.set_mailing_text_call.set()

@dp.message_handler(state=Mailing.set_mailing_text_call)
async def set_mailing_text(message: Message, state: FSMContext):
    await state.finish()
    if message.text == "/cancel":
        return await message.answer(text="Рассылка отменена")
    globals.is_mailing = True
    users = await UserData.objects.all()
    start_time = dt.now()
    for user in users:
        try:
            await bot.send_message(chat_id=user.username, text=message.text)
        except (UserDeactivated, BotBlocked,):
            blocked_user = await UserData.objects.get(username=user.username)
            await blocked_user.update(is_blocked=True)
        except ChatNotFound:pass
    globals.is_mailing = False
    end_time = int((dt.now() - start_time).total_seconds())
    return await message.answer(text="Рассылка завершена!\n"f"⏱Минут: {end_time // 60} Секунд: {end_time % 60}")