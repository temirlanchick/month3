from aiogram import types, F, Router


echo_router = Router()


@echo_router.message(F.text == 'hi')
async def hi(message: types.Message):
    await message.answer('Hello!')


@echo_router.message()
async def echo(message: types.Message):
    await message.answer(message.text)