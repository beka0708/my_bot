import logging

from aiogram import executor
from aiogram.dispatcher.filters import Text

from config import dp, scheduler
from db.base import (db_init, create_tables, populate_products, delete_tables, get_products)
from handlers.estatedb import (grafik, catalog, lot3)
from handlers.notifier import (UserText, start_reminder, process_text)
from handlers.products import (show_products, region, address)
from handlers.start import (start, help, myinfo, gallery)
from handlers.user_info_fsm import (
    UserForm,
    start_user_dialog,
    process_age,
    process_name,
    process_address,
    process_day,
    mail,
    not_mail
)


async def on_startup(_):
    db_init()
    create_tables()
    populate_products()
    get_products()


if __name__ == "__main__":
    print(__name__)
    db_init()
    create_tables()
    delete_tables()
    logging.basicConfig(level=logging.INFO)

    dp.register_message_handler(start_user_dialog, commands=["form"])
    dp.register_message_handler(process_name, state=UserForm.name)
    dp.register_message_handler(process_age, state=UserForm.age)
    dp.register_message_handler(process_address, state=UserForm.address)
    dp.register_message_handler(process_day, state=UserForm.day)
    dp.register_callback_query_handler(mail, Text(startswith="yes"))
    dp.register_callback_query_handler(not_mail, Text(startswith="no"))

    dp.register_message_handler(start_reminder, commands=["notify"])
    dp.register_message_handler(process_text, state=UserText.text)
    # dp.register_message_handler(notify_command_handler, commands=["notify"])
    # dp.register_message_handler(notify, commands=["notify"])

    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(help, commands=["help"])
    dp.register_message_handler(myinfo, commands=["myinfo"])
    dp.register_message_handler(gallery, commands=["gallery"])
    dp.register_message_handler(show_products, commands=["products"])
    dp.register_callback_query_handler(show_products, Text(equals="products"))
    dp.register_message_handler(region, Text(startswith="region"))
    dp.register_message_handler(address, Text(startswith="address"))
    dp.register_callback_query_handler(address, Text(equals='address'))
    dp.register_message_handler(grafik, Text(startswith="Режим работы"))
    dp.register_message_handler(lot3, Text(startswith="E-books"))

    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
