import sqlite3
from pathlib import Path
from pprint import pprint
from main import shop_router
from aiogram import types, F
from aiogram.filters import Command


def init_db():
    global db, cursor
    db = sqlite3.connect(Path(__file__).parent.parent / "db.sqlite3")
    cursor = db.cursor()


def create_tables():
    cursor.execute(
        """ 
        DROP TABLE IF EXISTS game
        """
    )
    cursor.execute(
        """ 
        DROP TABLE IF EXISTS categories 
        """
    )
    cursor.execute(
        """ 
        CREATE TABLE IF NOT EXISTS categories ( 
            categoryId INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT 
        ) 
        """
    )
    cursor.execute(
        """ 
        CREATE TABLE IF NOT EXISTS game ( 
            gameId INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT, 
            price REAL, 
            image TEXT, 
            categoryId INTEGER, 
            FOREIGN KEY (categoryId) REFERENCES categories(categoryId) 
        ) 
        """
    )
    db.commit()


def populate_tables():
    cursor.execute(
        """ 
        INSERT INTO categories (name) 
        VALUES ('Игры'),
               ('Скины'),
               ('Оружие')
        """
    )
    cursor.execute(
        """ 
        INSERT INTO game (name, price, image, categoryId) 
        VALUES ('Assasins Creed 3', 100.0, 'images/Radunhageydu.jpg', 1),
               ('Far Cry 5', 200.0, 'images/far cry 5.jpg', 1),
               ('Наряд Эцио', 300.0, 'images/EZIO.jpg', 2),
               ('Наряд Альтаира', 400.0, 'images/Altair.jpg', 2),
               ('Клинок', 1000.0, 'images/clinoc.jpg', 3),
               ('Арбалет', 2000.0, 'images/arbalet.jpg', 3) 
    """
    )
    db.commit()


def get_all_game():
    cursor.execute("SELECT * FROM game ORDER BY gameId DESC LIMIT 10")
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
    games = get_all_game()
    for game in games:
        await message.answer(game[1])
    db.commit()


if __name__ == "__main__":
    init_db()
    create_tables()
    populate_tables()
    pprint(get_all_game())
