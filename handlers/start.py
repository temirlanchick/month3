from aiogram import types, Router, F
from aiogram.filters import Command


start_router = Router()


@start_router.message(Command("start"))
async def start(message: types.Message):
    # print(message.from_user)
    # await message.answer(f'Привет {message.from_user.first_name}!')
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Наш сайт", url="https://python.org")],
            [
                types.InlineKeyboardButton(
                    text="Наш инстаграм", url="https://instagram.com"
                )
            ],
            [types.InlineKeyboardButton(text="О нас", callback_data="about_us")],
            [types.InlineKeyboardButton(text="Отправить номер", request_contact=True)],
            [types.InlineKeyboardButton(text="Отправить геолокацию", request_location=True)]
        ]
    )
    await message.reply(f"Привет {message.from_user.first_name}!", reply_markup=kb)


# 'about_us'.startswith('about')
# 'about_us'.endswith('us')
# 'about_us'.contains('t_us')
@start_router.callback_query(F.data.startswith("about"))
async def show_about_us(call: types.CallbackQuery):
    await call.answer()

    await call.message.answer("О нас")