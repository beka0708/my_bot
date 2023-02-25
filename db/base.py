import sqlite3
from pathlib import Path

from aiogram.types import message
from config import bot
import random


def db_init():
    DB_PATH = Path(__file__).parent.parent
    DB_FILE = 'db.sqlite'
    global db, cur  # orm
    db = sqlite3.connect(DB_PATH / DB_FILE)
    cur = db.cursor()
    print(DB_PATH)


def create_tables():
    cur.execute("""CREATE TABLE IF NOT EXISTS products(
    product_id INTEGER PRIMARY KEY,
    name TEXT ,
    price REAL,
    photo TEXT
    ) """)

    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER 
    user_name TEXT,
    address TEXT,
    product_id INTEGER,
    PRIMARY KEY (order_id),
    FOREIGN KEY (product_id) REFERENCES products(products_id)
    ON DELETE CASCADE
    )""")

    db.commit()


def delete_tables():
    cur.execute("""DROP TABLE IF EXISTS products""")
    db.commit()


def populate_products():
    cur.execute("""INSERT INTO products (name, price, photo) VALUES
                            ('The tehno 1', 500, 'imagess/divan.jpg'),
                            ('The tehno 2', 600, 'imagess/razmer.jpg'),
                            ('The tehno 3', 700, 'imagess/shkaf.jpg') 
                            """)
    db.commit()


def get_products():
    cur.execute("""SELECT * from products""")
    all_products = cur.fetchall()
    print(all_products)
    return all_products


if __name__ == "__main__":
    print(__name__)
    db_init()
    delete_tables()
    create_tables()
    populate_products()
    get_products()
