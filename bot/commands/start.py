from hashlib import md5

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, CallbackQuery, reply_keyboard

from models.models import *
from objects.globals import dp, bot
from decorators.decorators import *

from language_temp.language import Language

@dp.message_handler(commands="start")
@update
async def start(message: Message):
    message: Message = message[0]
    user_id: str = str(message.from_user.id)
    is_user = await AuthUser.objects.filter(username=user_id).exists()
    if not is_user:
        hash_password: str = md5(user_id.encode("utf-8")).hexdigest()[:8]

        await UserData.objects.create(username=user_id,
            auth_user_id= await AuthUser.objects.create(
                password=hash_password, username=user_id,
                last_name=message.from_user.last_name, first_name=message.from_user.first_name))

    user_data = await UserData.objects.get(username=user_id)

    if not user_data.language:
        language_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🇬🇧ENG", callback_data="language_ENG")],
                [InlineKeyboardButton(text="🇷🇺RU", callback_data="language_RU")]
            ])
        return await message.answer(text=f"👾Hey\n"f"🌐Select the language", reply_markup=language_markup)
    language = Language(user_id=user_id, symbol=user_data.language)
    return await message.answer(text=language.text(type="start"), reply_markup=language.keyboard())


@dp.callback_query_handler(lambda query: query.data.startswith(("language")))
async def set_language(query: CallbackQuery):
    """Set language
    :param: query
    :type: CallbackQuery
    :return: Bot message
    :rtype: Message
    """

    language = Language(user_id=query.from_user.id, symbol=query.data.split("_")[1])
    await language.update()

    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id,)

    return await bot.send_message(chat_id=query.from_user.id, text=language.text(type="start"),
                    reply_markup=language.keyboard())