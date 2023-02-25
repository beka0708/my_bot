from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery


class UserForm(StatesGroup):
    name = State()
    age = State()
    address = State()
    day = State()


async def start_user_dialog(message: types.Message):
    """
    Обработчик чтоб принять двнные о пользователе
    """
    await UserForm.name.set()
    await message.answer("Please input your name and last name:")

async def process_name(message: types.Message, state: FSMContext):
    """
    сохраняем данные об имени
    """
    async with state.proxy() as data:
        data['name'] = message.text
    await UserForm.next()
    await message.answer("How old are you?")


async def process_age(message: types.Message, state: FSMContext):
    """
    обработчик для проверки возраста на цифры
    """
    age = message.text
    if not age.isnumeric():
        await message.reply("Wrong data! Input only numbers!")
        await message.answer("How old are you?")
    else:
        async with state.proxy() as data:
            """
            сохраняем данные о возрасте
            """
            data['age'] = age
        await UserForm.next()
        await message.answer("Input your address: ")


async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        """
        сохраняем данные об адресе
        """
        data['address'] = message.text
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        kb.add(*buttons)

    await UserForm.next()
    await message.answer("What day of the week do you want to deliver your order?\n"
                         "Our schedule: Mon - Sat, Sunday - day-off", reply_markup=kb)


async def process_day(message: types.Message, state: FSMContext):
    """
    сохраяем данные о дне недели для получения товара
    """
    async with state.proxy() as data:
        data['day'] = message.text
        buttons = [
            types.InlineKeyboardButton(text='Yes', callback_data='yes'),
            types.InlineKeyboardButton(text='No', callback_data='no')
        ]
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb.add(*buttons)
        print(data)

    await state.finish()
    await message.answer(f"Thank you for your order! Do you want leave a review {data['name']} ?",
                         reply_markup=kb)

async def mail(callback: CallbackQuery):
    """
    обработчик чтоб принять сообщение
    """
    await callback.answer()
    message = callback.message
    user = message.from_user.full_name
    # user = UserForm.name
    await message.answer(f"Review from {user}:")
    await message.bot.send_message(
        text=f'{callback.from_user.first_name} Thank you for your review!',
        chat_id=message.chat.id
    )


async def not_mail(callback: CallbackQuery):
    """
    обработчик чтоб попращаться
    """
    await callback.answer()
    message = callback.message
    await message.bot.send_message(
        text=f'{callback.from_user.first_name} Bye! See you soon!',
        chat_id=message.chat.id
    )