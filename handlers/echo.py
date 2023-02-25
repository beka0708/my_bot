from aiogram import types
from config import dp

@dp.message_handler()
async def echo(message: types.Message):
    text = len(message.text)
    if text > 3:
        await message.answer(
            f'{message.text.upper()}'
        )
    else:
        pass