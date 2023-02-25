from aiogram import types
import db
from config import bot,dp
from db import base
from db.base import get_products


async def grafik(message: types.Message):
    await message.reply("""
График работы: 
Понедельник - Пятница с 09:00 до 18:00 
Суббота с 10:00 до 17:00
Воскресенье - выходной
    
с 13:00 до 14:00 обеденный перерыв 
    """)


async def catalog(message: types.Message):
    for product in get_products():
        print(product)
        with open(product[3], 'rb') as image:
            await message.answer_photo(
                photo=image,
                caption=f'{product[1]}\n Цена:{product[2]}'
            )