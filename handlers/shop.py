from aiogram import types, Router, F
from aiogram.filters import Command


shop_router = Router()


@shop_router.message(Command("shop"))
async def shop(message: types.Message):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Книги")],
            [
                types.KeyboardButton(text="Сувениры"),
                types.KeyboardButton(text="Манга"),
            ],
        ],
        resize_keyboard=True,
    )
    await message.answer("Выберите категорию товаров ниже:", reply_markup=kb)

@shop_router.message(F.text.lower() == "книги")
async def show_books(message: types.Message):
    kb = types.ReplyKeyboardRemove()
    await message.answer("Книги в нашем магазине", reply_markup=kb)
