import string
import json
from aiogram import types, bot
from aiogram.types import CallbackQuery

from config import dp

admin_id_count = []


async def is_admin(message: types.Message):
    """
    проверка является ли автор сообщения админом данного чата
    """
    print(message.from_user)
    author = message.from_user.id
    admins = await message.chat.get_administrators()
    not_admin = False
    for admin in admins:
        if admin['user']['id'] == author:
            not_admin = True
            break
    return not_admin


async def check_bad_words(message: types.Message):
    """
    проверка содержит ли сообщение пользователя слово "мат"
    """
    abuser_id = message.from_user.id
    abuser_name_warning = message.from_user.first_name
    buttons = [
        types.InlineKeyboardButton(text='да', callback_data=f'abuser_id={abuser_id}'),
        types.InlineKeyboardButton(text='нет', callback_data=f'abuser_name_warning={abuser_name_warning}')
    ]
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(*buttons)
    admin_author = await is_admin(message)
    print(admin_id_count)
    if message.chat.type != 'private':
        if not admin_author:
            if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
                    .intersection(set(json.load(open('cenz.json')))) != set():
                await message.reply(
                    f'кикнуть пользователя {message.from_user.first_name} за иcпользование нехороших слов?',
                    reply_markup=kb
                )


async def ban_user(callback: CallbackQuery):
    """
    обработчик чтоб банить пользователя в чате через команду
    """
    await callback.answer()
    message = callback.message
    abuser_id = callback.data.replace('abuser_id=', '')
    if callback.from_user.id in admin_id_count:
        await message.bot.ban_chat_member(
            text=f'{callback.from_user.first_name} кикнул {abuser_id}',
            user_id=abuser_id
        )
    else:
        await message.bot.send_message(
            text=f'{callback.from_user.first_name} у тебя нет прав для бана!',
            chat_id=message.chat.id
        )


async def ban_user_warning(callback: CallbackQuery):
    """
    обработчик, чтоб предупредить о предстоящем бане пользователя в чате
    через команду
    """
    await callback.answer()
    message = callback.message
    abuser_name_warning = callback.data.replace('abuser_name_warning=', '')
    if callback.from_user.id in admin_id_count:
        await message.bot.send_message(
            text=f'{abuser_name_warning} не пиши плохие слова в чат иначе в следующий раз тебя забанят!',
            chat_id=message.chat.id
        )
    else:
        await message.bot.send_message(
            text=f'{callback.from_user.first_name} у тебя нет прав для бана!',
            chat_id=message.chat.id
        )

