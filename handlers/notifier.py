from aiogram import types, bot
from config import scheduler, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import string


class UserText(StatesGroup):
    text = State()


async def start_reminder(message: types.Message):
    """
    Запрашиваем текст напоминалки у пользователя
    """
    await UserText.text.set()
    await message.answer("Input your reminder:")


async def process_text(message: types.Message, state: FSMContext):
    """
    Сохраняем текст напоминалки без слова <напомнить> и показываем текст напоминалки
    в конце вызываем напоминалку с заданным интервалом
    """
    async with state.proxy() as data:
        text = message.text
        key_word = "напомнить"
        await message.answer("Принято!")
        if key_word in text:
            text_res = text.split(' ', 1)[1]
            data['text']=text_res

            await message.answer(f"your reminder text is: <<{data['text']}>>")
        else:
            data['text'] = text
            await message.answer(f"your reminder text is: <<{data['text']}>>")

    await state.finish()

    async def notify(user_id: int):
        await bot.send_message(
            text=f"{data['text']}",
            chat_id=user_id
        )

    scheduler.add_job(notify, 'interval', seconds=2, args=(message.from_user.id,))



# async def notify_command_handler(message: types.Message):
#     scheduler.add_job(notify, 'interval', seconds=2, args=(message.from_user.id,))


# async def notify(user_id: int):
#     await bot.send_message(
#             text=f'Hello world',
#             chat_id=user_id
#         )
