import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv
from os import getenv
from logging import basicConfig
from handlers.shop import shop_router

load_dotenv()
bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    # print(message.from_user)
    # await message.reply(f'Привет {message.from_user.first_name}!')
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Наш адрес', url='https://2gis.kg/bishkek/geo/15763234351098492')], [
                types.InlineKeyboardButton(text='Наши соц.сети', url='https://instagram.com'),
            ]
        ]
    )

    await message.reply(f"Привет {message.from_user.first_name}!", reply_markup=kb)


@dp.message(Command('myinfo'))
async def myinfo(message: types.Message):
    print(message.from_user)
    await message.reply(f'Ваш ID {message.from_user.id}!')
    await message.reply(f'Ваш first name {message.from_user.first_name}!')
    await message.reply(f'Ваш username {message.from_user.username}!')


@dp.message(Command('picture'))
async def picture(message: types.Message):
    file = types.FSInputFile('images/EZIO.jpg')
    await message.answer_photo(file)


@shop_router.message(Command("shop"))
async def shop(message: types.Message):
    kb = (types.InlineKeyboardMarkup(
        inline_keyboard=[types.InlineKeyboardButton(text='в начало', url='/start)')]))
    kb1 = (types.ReplyKeyboardMarkup(

        keyboard=[
            [types.KeyboardButton(text="Игры")],
            [
                types.KeyboardButton(text="Скины"),
                types.KeyboardButton(text="Оружие"),
            ],
        ],
        resize_keyboard=True,
    ))
    await message.answer("Выберите категорию товаров ниже:", reply_markup=kb)


@shop_router.message(F.text.lower() == 'игры')
async def show_books(message: types.Message):
    kb = types.ReplyKeyboardRemove()
    await message.answer("Игры в нашем магазине", reply_markup=kb)

    dp.include_router(shop_router)
    await dp.start_polling(bot)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    basicConfig(level='INFO')
    asyncio.run(main())
