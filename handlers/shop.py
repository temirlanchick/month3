from pathlib import Path
from pprint import pprint
from aiogram import types, Router, F
from aiogram.filters import Command
import sqlite3

shop_router = Router()


def init_db():
    global db, cursor
    db = sqlite3.connect(Path(__file__).parent.parent / "db.sqlite3")
    cursor = db.cursor()


def create_tables():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            productsId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            image TEXT)
            """)

    cursor.execute(
        """
        INSERT INTO products (name)
        VALUES ('Игры'),
               ('Скины'),
               ('Оружие')
        """
    )

    cursor.execute(
        """
        INSERT INTO products (name, price, image, productsId)
        VALUES ('Игры 1', 100.0, 'images/Altair.jpg', 1),
               ('Игры 2', 200.0, 'images/EZIO.jpg', 1),
               ('Игры 3', 300.0, 'images/Radunhageydu.jpg', 1)
               ('Оружие', 3000.0, 'images/clinoc.jpg' 3)
    """
    )


def get_all_products():
    cursor.execute(
        "SELECT * FROM products ORDER BY productsId "
        "DESC LIMIT 10"
    )
    return cursor.fetchall()


@shop_router.message(Command("shop"))
async def shop(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Игры")],
            [
                types.KeyboardButton(text="Скины"),
                types.KeyboardButton(text="Оружие"),
            ],
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите категорию товаров ниже:", reply_markup=kb)


@shop_router.message(F.text.lower() == "игры")
async def show_games(message: types.Message):
    kb = types.ReplyKeyboardRemove()
    await message.answer("Игры в нашем магазине", reply_markup=kb)
    games = get_all_products()
    for game in games:
        await message.answer(game[1])
    db.commit()


if __name__ == "__main__":
    init_db()

    pprint(get_all_products())
