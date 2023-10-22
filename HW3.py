from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from os import getenv
from logging import basicConfig
import asyncio
from handlers import questions_router

load_dotenv()
bot = Bot(token=getenv('BOT_TOKEN'))
dp = Dispatcher()


class Questions(StatesGroup):
    name = State()
    age = State()
    gender = State()
    referral = State()


@questions_router.message(Command('stop'))
@questions_router.message(F.text.lower() == 'отмена')
async def stop_questions(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('До свидания!')


@questions_router.message(Command('polls'))
async def start_questions(message: types.Message, state: FSMContext):
    await message.answer('Для того, чтобы остановить, напишите "отмена"')
    await message.answer('Как вас зовут?')
    await state.set_state(Questions.name)


@questions_router.message(F.text, Questions.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer('Сколько вам лет?')
    await state.set_state(Questions.age)


@questions_router.message(F.text, Questions.age)
async def process_age(message: types.Message, state: FSMContext):
    age = message.text.strip()
    if not age.isdigit():
        await message.answer('Нужно ввести только цифры')
    if 12 <= int(age) <= 99:
        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Мужской"), types.KeyboardButton(text="Женский")],
            ]
        )

        await state.update_data(age=int(message.text))
        await message.answer("Какой у вас пол?", reply_markup=kb)
        await state.set_state(Questions.gender)
    else:
        await message.answer('Возраст должен быть от 12 до 99')

        kb = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="IOS"), types.KeyboardButton(text="Backend"),
                 types.KeyboardButton(text='Frontend'), types.KeyboardButton(text='Android')],
            ]
        )


@questions_router.message(F.text, Questions.gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text.strip()
    if gender.lower() == "мужской" or gender.lower() == "женский":
        kb = types.ReplyKeyboardRemove()
        await state.update_data(gender=gender)
        await state.set_state(Questions.referral)
        await message.answer('какое направление вас интересует?', reply_markup=kb)
    else:
        await message.answer('Нужно ввести "Мужской" или "Женский"')


@questions_router.message(F.text, Questions.referral)
async def process_referral(message: types.Message, state: FSMContext):
    await state.update_data(referral=message.text.strip())
    await message.answer('Спасибо за опрос!')

    data = await state.get_data()
    print(data)

    dp.include_router(questions_router)
    await dp.start_polling(bot)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    basicConfig(level='INFO')
    asyncio.run(main())
