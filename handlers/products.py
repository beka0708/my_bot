from aiogram import types
from config import bot

kb = types.ReplyKeyboardMarkup()
kb.add(
    types.KeyboardButton("Режим работы")
)
kb.add(
    types.KeyboardButton("Каталог книг")
)
kb.add(
    types.KeyboardButton("E-books")
)

async def show_products(call: types.CallbackQuery):
    """
    doc strings
    :param call:
    :return:
    """
    # chat_id = message.from_user.id
    await call.message.answer(
        # chat_id=chat_id,
        text="Welcome!",
        reply_markup=kb
    )


async def region(message: types.Message):
    await message.reply("Не найдено!")


async def address(call: types.CallbackQuery):
    await call.message.answer(f'Кыргызская Республика 720048\n'
                        f'г. Бишкек, ул. Анкара 20/1\n'
                        f'Тел.: +996 (551) 93-33-33\n'
                        f'email: bookaddicts@gmail.com\n')
