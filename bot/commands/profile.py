from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from objects.globals import dp, bot
from models.models import *
from language_temp.language import Language
from decorators.decorators import *

@dp.message_handler(lambda message: message.text=="ð¤My profile")
@update
async def profile_eng(message: Message):
    message: Message = message[0]
    user_id: int = message.from_user.id
    auth_user = await AuthUser.objects.get(username=user_id)
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
            f"\t\t\t\t<code>|--</code>Circles â {bomber_data.circles}\n"
            f"\t\t\t\t<code>|--</code>Phone number â {bomber_data.last_phone if bomber_data.last_phone else 'Unknow'}\n"
            f"\t\t\t\t<code>|--</code>Date â {date_format}\n"
        )
    else:
        bomber_page: str = ("Is not found bomber data")
    profile_page: str = (
        f"<b>Profile info</b>\n"
        f"<code>|-</code>User\n"
        f"\t\t\t\t<code>|--</code>User ID â <code>{user_id}</code>\n"
        f"\t\t\t\t<code>|--</code>Password â <code>{auth_user.password}</code>\n"
        f"\t\t\t\t<code>|--</code>Language â {user_data.language}\n"
        f"\t\t\t\t<code>|--</code>Balance â {float(user_data.balance)}\n"
        f"{bomber_page}"
    )
    return await message.answer(text=profile_page, reply_markup=inline_keybaord)

@dp.message_handler(lambda message: message.text=="ð¤ÐÐ¾Ð¹ Ð¿ÑÐ¾ÑÐ¸Ð»Ñ")
async def profile_ru(message: Message):
    user_id: int = message.from_user.id
    auth_user = await AuthUser.objects.get(username=user_id)
    user_data = await UserData.objects.get(username=user_id)
    inline_keybaord = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="ÐÐ·Ð¼ÐµÐ½Ð¸ÑÑ ÑÐ·ÑÐº", callback_data="select_language")]
        ])
    if user_data.is_bomber:
        bomber_data = await BomberData.objects.get(username=user_id)
        if bomber_data.last_launch:
            date_format = dt.strftime(bomber_data.last_launch, "%Y/%m/%d %H:%M:%S")
        else:
            date_format = "Unknow"
        bomber_page: str = (
            f"<code>|-</code>Bomber\n"
            f"\t\t\t\t<code>|--</code>ÐÑÑÐ³Ð¸ â {bomber_data.circles}\n"
            f"\t\t\t\t<code>|--</code>ÐÐ¾Ð¼ÐµÑ ÑÐµÐ»ÐµÑÐ¾Ð½Ð° â {bomber_data.last_phone if bomber_data.last_phone else 'Unknow'}\n"
            f"\t\t\t\t<code>|--</code>ÐÐ°ÑÐ° â {date_format}\n"
        )
    else:
        bomber_page: str = ("ÐÐµÑ Ð´Ð°Ð½Ð½ÑÑ Ð¿Ð¾ Ð±Ð¾Ð¼Ð±ÐµÑÑ!")
    profile_page: str = (
        f"<b>ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ Ð¿ÑÐ¾ÑÐ¸Ð»Ñ</b>\n"
        f"<code>|-</code>User\n"
        f"\t\t\t\t<code>|--</code>ID Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ â <code>{user_id}</code>\n"
        f"\t\t\t\t<code>|--</code>ÐÐ°ÑÐ¾Ð»Ñ â <code>{auth_user.password}</code>\n"
        f"\t\t\t\t<code>|--</code>Ð¯Ð·ÑÐº â {user_data.language}\n"
        f"\t\t\t\t<code>|--</code>ÐÐ°Ð»Ð°Ð½Ñ â {float(user_data.balance)}\n"
        f"{bomber_page}"
    )
    return await message.answer(text=profile_page, reply_markup=inline_keybaord)

@dp.callback_query_handler(lambda query: query.data.startswith(("select_language")))
async def set_language(query: CallbackQuery):
    user_data = await UserData.objects.get(username=str(query.from_user.id))
    language = Language(user_id=query.from_user.id, symbol=user_data.language)
    language_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="ð¬ð§ENG", callback_data="language_ENG")],
                [InlineKeyboardButton(text="ð·ðºRU", callback_data="language_RU")]
            ])
    return await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                       text=language.text(type="change_language"), reply_markup=language_markup)