from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from objects import globals
from objects.globals import dp, bot
from models.models import *
from language_temp.language import Language
from states.states import Attack
from utils.attack import Phone

language = Language()

@dp.message_handler(lambda message: message.text=="💣Attack number")
async def attack_ru(message: Message):
    user_id: int = message.from_user.id
    user_data = await UserData.objects.get(username=user_id)
    language = Language(user_id=user_id, symbol=user_data.language)
    if not user_data.is_bomber:
        count_circles: str = "30"
        await BomberData.objects.create(
            username=str(user_id), circles=count_circles)
        bomber_status = await UserData.objects.get(username=str(user_id))
        await bomber_status.update(is_bomber=True)
        await message.answer(text=language.set_circles_text())
    await message.answer(text=language.set_phone_text())
    await Attack.set_phone_call.set()

@dp.message_handler(lambda message: message.text=="💣Атаковать номер")
async def attack_ru(message: Message):
    user_id: int = message.from_user.id
    user_data = await UserData.objects.get(username=user_id)
    language = Language(user_id=user_id, symbol=user_data.language)
    if not user_data.is_bomber:
        count_circles: str = "30"
        await BomberData.objects.create(
            username=str(user_id), circles=count_circles)
        bomber_status = await UserData.objects.get(username=str(user_id))
        await bomber_status.update(is_bomber=True)
        await message.answer(text=language.set_circles_text())
    await message.answer(text=language.set_phone_text())
    await Attack.set_phone_call.set()

@dp.message_handler(lambda message: message.text not in [k[0] for k in language.extend_keyboards()],
    state=Attack.set_phone_call)
async def get_phone_targ(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    user_data = await UserData.objects.get(username=user_id)
    language = Language(user_id=user_id, symbol=user_data.language)
    if message.text=="/cancel":
        await state.finish()
        return await message.answer(text=language.text(type="cancel"))
    else:
        if not message.text.isdigit():
            return await message.answer(text=language.text(type="correct_phone"))
        else:
            await state.finish()
            bomber_data = await BomberData.objects.get(username=user_id)
            if bomber_data.circles == 0:
                return await message.answer(text="🗑Количество кругов израсходовано!")
            markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="⏹", callback_data="stop_attack")]
                ])
            await message.answer(text=language.text(type="stop_attack"), reply_markup=markup)
            await bomber_data.update(last_launch=dt.now(), last_phone=message.text)
            globals.phone = Phone(user_id=message.from_user.id, phone=message.text)
            await globals.phone.start(message=message)

@dp.callback_query_handler(lambda query: query.data=="stop_attack")
async def stop_attack(query: CallbackQuery, state: FSMContext):
    await globals.phone.stop()
    return await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id, text="✅")