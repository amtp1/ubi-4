from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from objects.globals import dp, bot
from models.models import *
from language_temp.language import Language
from decorators.decorators import *

@dp.message_handler(lambda message: message.text=="👤My profile")
@update
async def profile_eng(message: Message):
    message: Message = message[0]
    user_id: int = message.from_user.id
    user_data = await UserData.objects.get(username=user_id)
    inline_keybaord = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Change language", callback_data="select_language")]
        ])
    if user_data.is_bomber:
        bomber_data = await BomberData.objects.get(username=user_id)
        if bomber_data.last_launch:
            date_format = dt.strftime(bomber_data.last_launch, "%Y/%m/%d %H:%M:%S")
        else:
            date_format = "Unknow"
        bomber_page: str = (
            f"<code>|-</code>Bomber\n"
            f"\t\t\t\t<code>|--</code>Circles ➜ {bomber_data.circles}\n"
            f"\t\t\t\t<code>|--</code>Phone number ➜ {bomber_data.last_phone if bomber_data.last_phone else 'Unknow'}\n"
            f"\t\t\t\t<code>|--</code>Date ➜ {date_format}\n"
        )
    else:
        bomber_page: str = ("Is not found bomber data")
    profile_page: str = (
        f"<b>Profile info</b>\n"
        f"<code>|-</code>User\n"
        f"\t\t\t\t<code>|--</code>User ID ➜ {user_id}\n"
        f"\t\t\t\t<code>|--</code>Language ➜ {user_data.language}\n"
        f"\t\t\t\t<code>|--</code>Balance ➜ {float(user_data.balance)}\n"
        f"{bomber_page}"
    )
    return await message.answer(text=profile_page, reply_markup=inline_keybaord)

@dp.message_handler(lambda message: message.text=="👤Мой профиль")
async def profile_ru(message: Message):
    user_id: int = message.from_user.id
    user_data = await UserData.objects.get(username=user_id)
    inline_keybaord = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Изменить язык", callback_data="select_language")]
        ])
    if user_data.is_bomber:
        bomber_data = await BomberData.objects.get(username=user_id)
        if bomber_data.last_launch:
            date_format = dt.strftime(bomber_data.last_launch, "%Y/%m/%d %H:%M:%S")
        else:
            date_format = "Unknow"
        bomber_page: str = (
            f"<code>|-</code>Bomber\n"
            f"\t\t\t\t<code>|--</code>Круги ➜ {bomber_data.circles}\n"
            f"\t\t\t\t<code>|--</code>Номер телефона ➜ {bomber_data.last_phone if bomber_data.last_phone else 'Unknow'}\n"
            f"\t\t\t\t<code>|--</code>Дата ➜ {date_format}\n"
        )
    else:
        bomber_page: str = ("Нет данных по бомберу!")
    profile_page: str = (
        f"<b>Информация профиля</b>\n"
        f"<code>|-</code>User\n"
        f"\t\t\t\t<code>|--</code>User ID ➜ {user_id}\n"
        f"\t\t\t\t<code>|--</code>Язык ➜ {user_data.language}\n"
        f"\t\t\t\t<code>|--</code>Баланс ➜ {float(user_data.balance)}\n"
        f"{bomber_page}"
    )
    return await message.answer(text=profile_page, reply_markup=inline_keybaord)

@dp.callback_query_handler(lambda query: query.data.startswith(("select_language")))
async def set_language(query: CallbackQuery):
    user_data = await UserData.objects.get(username=str(query.from_user.id))
    language = Language(user_id=query.from_user.id, symbol=user_data.language)
    language_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🇬🇧ENG", callback_data="language_ENG")],
                [InlineKeyboardButton(text="🇷🇺RU", callback_data="language_RU")]
            ])
    return await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                       text=language.text(type="change_language"), reply_markup=language_markup)