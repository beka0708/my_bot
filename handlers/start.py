import random

from aiogram import types

kb = types.InlineKeyboardMarkup()
kb.add(types.InlineKeyboardButton(
    text="О нас",
    callback_data="products"
))
kb.add(types.InlineKeyboardButton(
    text="Наш адрес:",
    callback_data="address"
))


# @dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user = message.from_user.full_name
    await message.answer(
        f'Приветствуем, {user}!\n')
    await message.reply(
        f'Выберите команду:',
        reply_markup=kb
    )


# @dp.message_handler(commands=["help"])
async def help(message: types.Message):
    await message.answer(
        """
        /start - Старт
/help - Список команд:
/myinfo - Данные пользователя
/gallery - random photos
/aboutus - О нас
        """
    )


# @dp.message_handler(commands=["myinfo"])
async def myinfo(message: types.Message):
    user = message.from_user.full_name
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await message.answer(
        f'Username: {user}\n'
        f'User ID: {user_id}\n'
        f'User first name: {first_name}\n'
        f'User last name: {last_name}\n'
    )
    # await message.delete()


# @dp.message_handler(commands=["picture"])
async def gallery(message: types.Message):
    photos = ['images_rnd/book1.jpeg', 'images_rnd/book2.jpeg', 'images_rnd/book3.jpeg', 'images_rnd/book4.jpeg']
    with open(random.choice(photos), 'rb') as photos:
        await message.answer_photo(
            photo=photos,
            caption='books'
        )
