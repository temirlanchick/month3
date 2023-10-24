import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
from os import getenv
from logging import basicConfig

load_dotenv()
bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    print(message.from_user)
    await message.reply(f'Привет {message.from_user.first_name}!')


@dp.message(Command('myinfo'))
async def myinfo(message: types.Message):
    print(message.from_user)
    await message.reply(f'Ваш ID {message.from_user.id}!')
    await message.reply(f'Ваш first name {message.from_user.first_name}!')
    await message.reply(f'Ваш username {message.from_user.username}!')


@dp.message(Command('picture'))
async def picture(message: types.Message):
    file = types.FSInputFile('images/EZIO.jpg')
    await message.answer_photo(photo=file, caption='Эцио Аудиторе')


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    basicConfig(level='INFO')
    asyncio.run(main())
