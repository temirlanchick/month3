from aiogram import types, Router
from aiogram.filters import Command


pic_router = Router()

@pic_router.message(Command('pic'))
async def pic(message: types.Message):
    file = types.FSInputFile('images/EZIO.jpg')
    await message.answer_photo(photo=file, caption='Эцио Аудиторе')